import sys
import os

import lyosha.critical_value as cv
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from lyosha.Plotter import *
from math import ceil
import numpy as np


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


conn = sqlite3.connect(resource_path("mydatabase.db"))  #
cursor = conn.cursor()


def create_telemetry_mask(crkey, crparam, k1, k2=None):
    if not k2 is None:
        arr = [f"{crkey} > {cv.get_value(crparam, crkey) * k1} AND "
               f"{crkey} < {cv.get_value(crparam, crkey) * k2}", 2, crkey]
        mask = arr[0]
        code = arr[1]
        key = arr[2]
    else:
        arr = [f"{crkey} > {cv.get_value(crparam, crkey) * k1}", 3, crkey]
        mask = arr[0]
        code = arr[1]
        key = arr[2]
    return [mask, code, key]


def create_date_mask(date1, date2):
    mask = f"datetime(date) >'{date1}' AND datetime(date) < '{date2}'"
    return mask


def update_plot(date1, date2):
    interval = (date2 - date1).days / 10
    if interval == 0:
        interval = (date2 - date1).seconds / (3600 * 12)
        date_limit([date1, date2], days=0, hours=2)
        _format = "%H"
        update_hour_formatter(format=_format, interval=ceil(interval))
    else:
        _format = "%d.%m %H"
        date_limit([date1, date2])
        update_day_formatter(format=_format, interval=ceil(interval))


def sum_mask(masks):
    out = "WHERE "
    for mask in masks:
        # print(mask)
        out += mask + " AND "
    return out[:len(out) - 5]


masks = [
    create_telemetry_mask('oC', 'GG', 0.95, 1),  # temperature
    create_telemetry_mask('oC', 'GG', 1),

    create_telemetry_mask('vsu', 'GG', 0.95, 1),  # vibrations
    create_telemetry_mask('vsu', 'GG', 1),

    create_telemetry_mask('congestion', 'GG', 0.8, 0.95),  # загруженность
    create_telemetry_mask('congestion', 'GG', 0.95),

    create_telemetry_mask('W', 'GG', 0.95, 1),  # power
    create_telemetry_mask('W', 'GG', 1),

    create_telemetry_mask('Hours', 'GG', 0.85, 1),  # time
    create_telemetry_mask('Hours', 'GG', 1)
]


def fig2rgb_array(fig):
    fig.canvas.draw()

    buf = fig.canvas.tostring_rgb()
    ncols, nrows = fig.canvas.get_width_height()
    return np.fromstring(buf, dtype=np.uint8).reshape(nrows, ncols, 3)


# num of vehicle, from date1 to date2, tasks mask
def create_graphic(num, date1, date2, key, mask="True", out=0):
    fig, ax = plt.subplots(1, sharex=True, sharey=False)
    # ax.set_facecolor('seashell')
    fig.set_facecolor('floralwhite')
    plt.grid()

    date_mask = create_date_mask(date1, date2)
    num_mask = f"num == {num}" if num > 0 else f"num > 0"
    final_mask = sum_mask([date_mask, num_mask, mask])

    new_data = pd.read_sql_query(f"select * from telemetry "
                                 f"{final_mask}", conn, index_col="index")

    new_data['date'] = [datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in new_data['date'].values]
    update_plot(date1, date2)
    ax.set_ylabel(key)
    ax.set_xlabel("Date")

    if out == 0:  # table
        print(new_data)
        return new_data
    elif out == 1:  # graphic
        if len(new_data) > 0:
            y_limit([min(new_data[key]), max(new_data[key])], new_data[key].std())
            plt.scatter(new_data['date'].values, new_data[key].values)
            fig.canvas.draw()
            data = fig2rgb_array(fig)
            plt.close()
            return data
    elif out == 2:  # bar
        if len(new_data) > 0:
            y_limit([min(new_data[key]), max(new_data[key])], new_data[key].std())
            plt.bar(new_data['date'].values, new_data[key].values)
            fig.canvas.draw()
            data = fig2rgb_array(fig)
            plt.close()
            return data

# date1 = datetime(2020, 3, 1, 11)
# date2 = datetime(2020, 3, 10, 11)
# # create_graphic(0, date1, date2, "oC", mask="True", out=1)
# create_graphic(0, date1, date2, "oC", masks[3][0], 1)
