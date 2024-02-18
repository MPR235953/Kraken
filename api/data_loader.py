import yfinance as yf
import datetime
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import random

engine = create_engine("mysql+mysqlconnector://root:root@kraken-mysql-container-1:3306/currencies")

def add_log(is_success: bool, msg: str = ""):
    with open("loader_log.txt", "w") as f:
        if is_success:
            f.write(f"SUCCESS - {msg}")
        else:
            f.write(f"ERROR - {msg}")

if __name__ == '__main__':
    try:
        currency_mapper = {
            "pln_usd": "PLNUSD=x",
            "usd_pln": "PLN=x",
            "eur_pln": "EURPLN=x",
            "pln_eur": "PLNEUR=x",
            "eur_usd": "EURUSD=x",
            "usd_eur": "EUR=x"
        }

        msg = ""

        for table_name, yf_symbol in currency_mapper.items():

            query = f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1"
            df = pd.read_sql(query, engine)

            if not df.empty:
                start_date = str(df["Date"].values[-1])
                current_date = datetime.date.today()  # yahoo finance will deliver date - 1 (because curr date not yet finished)
                end_date = current_date.strftime("%Y-%m-%d")

                stock_data = yf.download(yf_symbol, start=start_date, end=end_date, interval="1d").reset_index()
                if not stock_data.empty:  # in case of lack of internet conn
                    last_date_yf = str(stock_data["Date"].values[-1]).split('T')[0]
                    if last_date_yf != start_date:  # do not duplicate data if last date in mysql is the same as last date in yf
                        stock_data.to_sql(name=table_name, con=engine, if_exists='append', index=False)
                    else: msg += "|No update due to duplication.|"
                else: msg += "|No intenren connection.|"
                
            else:
                msg += "|Empty table download whole data.|"
                current_date = datetime.date.today()  # yahoo finance will deliver date - 1 (because curr date not yet finished)
                end_date = current_date.strftime("%Y-%m-%d")
                stock_data = yf.download(yf_symbol, start=f"2004-11-01", end=end_date, interval="1d").reset_index()
                if not stock_data.empty:  # in case of lack of internet conn
                    stock_data.to_sql(name=table_name, con=engine, if_exists='append', index=False)
                else: 
                    msg += "|No intenren connection (Empty table).|"
                    add_log(is_success=False, msg=msg)
                    exit(1)

        add_log(is_success=True, msg=msg)
    except Exception as e:
        add_log(is_success=False, msg=str(f"|{e}|"))

    