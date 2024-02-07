import matplotlib.pyplot as plt
import numpy as np

def create_plot(file_path: str):
    data_dict = {}
    days=7

    with open(file_path, 'r') as file:
        for line in file:
            series_name, series_data = line.split(':')
            series_data = series_data.split(' ')
            series_data = [float(data_point) for data_point in series_data]
            data_dict[series_name.strip()] = series_data

    plt.figure(figsize=(10, 6))

    for series_name, series_data in data_dict.items():
        plt.plot(series_data, '.-', label=series_name)

    plt.axvline(x=days-1, color='red')

    plt.xlabel('Dzień')
    plt.ylabel('Cena zamknięcia')
    plt.title('EUR / PLN')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid()
    plt.show()