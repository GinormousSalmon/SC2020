import numpy as np
from datetime import datetime
import pandas as pd


def mean(data):
    return data.rolling(window=2).mean()


def averge(data, step, cols):
    new_data = []
    for i in range(0, len(data) - step, step):
        k = []
        for x in cols:
            if x == 'date':
                date = []
                for j, jd in enumerate(data[i:step + i].values):
                    date.append(datetime.strptime(jd[1], '%d.%m.%Y;%H:%M:%S').timestamp())
                k.append(np.mean(date))
            else:
                k.append(data[x][i:step + i].mean())
        new_data.append(k)
    return pd.DataFrame(new_data, columns=cols)


def approx(x: list, y: list, epsilon):
    ox = []
    oy = []
    for i in range(len(x) - 1):
        distanse = np.sqrt((x[i + 1] - x[i]) ** 2 + (y[i + 1] - y[i]) ** 2)
        print(distanse)
        if distanse > epsilon:
            ox.append(x[i])
            oy.append(y[i])
    return ox, oy
