import numpy as np
import pandas as pd
import pandas_ta as ta
from statistics import mode

def get_decision_RSI(df: pd.DataFrame, days: int = 14):
    rsi = ta.rsi(close=df["Close"], length=days).values[-1]
    print(rsi)
    if rsi > 80: return 0
    elif rsi > 60 and rsi <= 80: return 1
    elif rsi >= 40 and rsi <= 60: return 2
    elif rsi >= 30 and rsi < 40: return 3
    elif rsi < 30: return 4

def get_decision_MA(df: pd.DataFrame, MA_type: str = "SMA", days: int = 50):
    ma = None
    if MA_type.upper() == "SMA": ma = ta.sma(close=df["Close"], length=days)
    elif MA_type.upper() == "WMA": ma = ta.wma(close=df["Close"], length=days)
    else: ma = ta.ema(close=df["Close"], length=days)

    ma.dropna(inplace=True)
    ma = ma.values

    last_ma = ma[-1]
    last_close = df["Close"].values[-1] 

    perc = ((last_close - last_ma) / last_ma) * 100
    print(perc)
    if perc > 2: return 0
    elif perc > 1 and perc <= 2: return 1
    elif perc >= -1 and perc <= 1: return 2
    elif perc >= -2 and perc < -1: return 3
    elif perc < -2: return 4
