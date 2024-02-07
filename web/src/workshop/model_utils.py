import numpy as np

def create_sequences(data, seq_len):
    seq_x, seq_y = [], []
    for i in range(len(data) - seq_len):
        x = data[i:(i + seq_len), :]
        y = data[i + seq_len, -1]
        seq_x.append(x)
        seq_y.append(y)
    return np.array(seq_x), np.array(seq_y)
