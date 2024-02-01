import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def get_forecast(df, days: int, time_step: int = 7):
    data = df[['Close']].values[-30:]

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    model = tf.keras.models.load_model("src/models/20240120-181519_LSTM_y15_sl7_b256_e10_L512-256-128-64_D64-32-16-1_d0-0-0-0-0-0-0-0")

    seq = np.reshape(scaled_data[-time_step:], (1, time_step, 1))
    next_days = []
    for _ in range(days):
        seq = np.reshape(seq, (1, time_step, 1))
        preds = model.predict(seq)
        next_days.append(preds)
        seq = np.append(seq, np.reshape(preds, (1,1,1)), axis=1)
        seq = seq[0][-time_step:]
    print(next_days)

    rescaled_next_days = scaler.inverse_transform(np.reshape(next_days, (days, 1)))
    print(rescaled_next_days)

    return rescaled_next_days