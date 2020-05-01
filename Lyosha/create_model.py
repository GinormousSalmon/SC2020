import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import keras
from keras.layers import Dense


def norm(x, mean, std):
    return (x - mean) / std


def build_model(input_len):
    model = keras.Sequential([Dense(64, activation='elu', input_shape=[input_len]),
                              Dense(64, activation='elu'),
                              Dense(32, activation='elu'),
                              Dense(1)
                              ])

    optimizer = keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae', 'mse'])
    return model


def get_stats(dataset):
    stats = dataset.describe()
    stats = stats.transpose()
    return stats


def load_model(direct):
    return keras.models.load_model(direct)


def plot_history(history):
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [MPG]')
    plt.plot(hist['epoch'], hist['mean_absolute_error'],
             label='Train Error')
    plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
             label='Val Error')
    plt.ylim([0, 5])
    plt.legend()

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Square Error [$MPG^2$]')
    plt.plot(hist['epoch'], hist['mean_squared_error'],
             label='Train Error')
    plt.plot(hist['epoch'], hist['val_mean_squared_error'],
             label='Val Error')
    plt.ylim([0, 20])
    plt.legend()
    plt.show()
