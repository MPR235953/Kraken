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

from plot_create import create_plot

def model_create(
        data_path: str = '',
        log_path: str = '',
        new_model=True,
        move: int = 0,
        years: int = 2,
        seq_len: int = 30,
        batch: int = 1,
        epoch: int = 20,
        LSTM_layers=[128, 64],
        Dense_layers=[16, 1],
        Dropouts=[0.05, 0.1, 0.1, 0.05]
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

    print(f"DATE --------------------------> {base_dates[split + move]}")

    x_train, y_train = create_sequences(scaled_data, seq_len)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    ttt = time.strftime("%Y%m%d-%H%M%S")
    case_name = f"{ttt}_LSTM_{data_path.split('/')[-1].split('.')[0]}_sl{seq_len}_b{batch}_e{epoch}_L{'-'.join(map(str, LSTM_layers))}_D{'-'.join(map(str, Dense_layers))}_d{'-'.join(map(str, Dropouts))}"

    if new_model:
        model = Sequential()
        i = 0
        for _ in range(len(LSTM_layers)):
            if i != len(LSTM_layers) - 1:
                model.add(LSTM(LSTM_layers[i], return_sequences=True, input_shape= (x_train.shape[1], 1)))
            else:
                model.add(LSTM(LSTM_layers[i], return_sequences=False))
            model.add(Dropout(Dropouts[i]))
            i += 1
        
        for j in range(len(LSTM_layers)):
            model.add(Dense(Dense_layers[j]))
            model.add(Dropout(Dropouts[i]))
            i += 1

        model.compile(optimizer=Adam(lr=0.01), loss="mse", metrics=["mae", "mse", "mape"])

        log_directory = f'{log_path}{case_name}/{ttt}'
        tensorboard_callback = TensorBoard(log_dir=log_directory)
        
        model.fit(x_train, y_train, batch_size=batch, epochs=epoch, callbacks=[tensorboard_callback])
        model.save(f"models/{case_name}")
    else:
        model = tf.keras.models.load_model("models/<enter_model_name>")
        
    #ttt = time.strftime("%Y%m%d-%H%M%S")
    #case_name = f"{ttt}_LSTM_{data_path.split('/')[-1].split('.')[0]}_sl{seq_len}_b{batch}_e{epoch}_L{'-'.join(map(str, LSTM_layers))}_D{'-'.join(map(str, Dense_layers))}_d{'-'.join(map(str, Dropouts))}"
    
    seq = np.reshape(base_scaled_data[split:(split + seq_len)], (1, seq_len, 1))
    next_days = []
    for _ in range(N):
        seq = np.reshape(seq, (1, seq_len, 1))
        preds = model.predict(seq)
        next_days.append(preds)
        seq = np.append(seq, np.reshape(preds, (1,1,1)), axis=1)
        seq = seq[0][-seq_len:]
    print(next_days)


    #real = base_dataset[(split + seq_len):(split + seq_len + N)]
    real = base_dataset[(split):(split + seq_len + N)]
    #predicted = scaler.inverse_transform(np.reshape(next_days, (N, 1)))
    predicted = np.append(base_dataset[(split):(split + seq_len)], scaler.inverse_transform(np.reshape(next_days, (N, 1))))


    with open(f"predictions/{ttt}.txt", "a") as f:
        #f.write(f"expected:{' '.join(map(str, np.reshape(expected, (expected.shape[0]))))}\n")
        f.write(f"real:{' '.join(map(str, np.reshape(real, (real.shape[0]))))}\n")
        f.write(f"{case_name}:{' '.join(map(str, np.reshape(predicted, (predicted.shape[0]))))}\n")

    create_plot(f"predictions/{ttt}.txt")

    print("finished")

if __name__ == "__main__":
    #LSTM_y5_ts0.9_sl120_b128_e10_L256-128_D16-1_d0-0-0-0
    #move=246 # max
    model = model_create(data_path='data/pln_usd.csv', log_path='logs/', 
                         new_model=False, move=7, years=-1, seq_len=7, batch=256, epoch=10, LSTM_layers=[512, 256, 128, 64], Dense_layers=[64, 32, 16, 1], Dropouts=[0, 0, 0, 0, 0, 0, 0, 0])
