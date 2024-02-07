import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import pandas_ta as ta
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard
import time
import tensorflow as tf

from model_utils import *


def model_test(
        data_path: str = '',
        model_path: str = '',
        move: int = 0,
        seq_len: int = 30
    ):

    df = pd.read_csv(data_path)
    df.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1, inplace=True)
    df.dropna(inplace=True)

    N = 7

    base_dataset = df[['Close']].values
    base_dates= df[['Date']].values

    scaler = MinMaxScaler(feature_range=(0,1))
    base_scaled_data = scaler.fit_transform(base_dataset)

    split = int(len(base_scaled_data) * 0.9) + move
    scaled_data = base_scaled_data[:split]

    print(f"DATE --------------------------> {base_dates[split]}")

    x_train, y_train = create_sequences(scaled_data, seq_len)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = tf.keras.models.load_model(model_path)

    dates_df = pd.DataFrame(columns=['t0', 't1', 't2', 't3', 't4', 't5', 't6'])
    real_df = pd.DataFrame(columns=['d0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6'])
    predicted_df = pd.DataFrame(columns=['d0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6'])

    ttt = time.strftime("%Y%m%d-%H%M%S")
    loop_end = len(base_scaled_data[split:]) - seq_len - N + 1
    for i in range(loop_end):   
        seq = np.reshape(base_scaled_data[(split + i):(split + seq_len + i)], (1, seq_len, 1))
        real_seq = np.reshape(base_scaled_data[(split + seq_len + i):(split + seq_len + i + N)], (1, N, 1))
        dates_seq = np.reshape(base_dates[(split + seq_len + i):(split + seq_len + i + N)], (1, N, 1))
        next_days = []
        for _ in range(N):
            seq = np.reshape(seq, (1, seq_len, 1))
            preds = model.predict(seq)
            next_days.append(preds)
            seq = np.append(seq, np.reshape(preds, (1,1,1)), axis=1)
            seq = seq[0][-seq_len:]
        print(next_days)

        dates_df.loc[len(dates_df)] = list(list(np.reshape(dates_seq, (1, N)))[0])
        real_df.loc[len(real_df)] = list(list(scaler.inverse_transform(np.reshape(real_seq, (1, N))))[0])
        predicted_df.loc[len(predicted_df)] = list(list(scaler.inverse_transform(np.reshape(next_days, (1, N))))[0])

        print(f"{i}/{loop_end}")

    print("end")
    #print(dates_df)
    #print(real_df)
    #print(predicted_df)

    mse_df = (real_df - predicted_df) ** 2

    #print(mse_df)

    concated_df = pd.concat([mse_df, dates_df], axis=1)
    #print(concated_df)

    concated_df.to_csv(f"dfs/{ttt}_{model_path.split('/')[-1]}.csv", index=False)

    print(mse_df.mean())

        

if __name__ == "__main__":
    model = model_test(data_path='data/eur_pln.csv', move=50, seq_len=7, 
    model_path="models/<enter_model_name>")
