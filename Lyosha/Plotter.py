import matplotlib.pyplot as plt
from matplotlib import dates
import matplotlib.ticker as ticker
from matplotlib import dates as dts
from datetime import datetime, timedelta


def scatter_plot(x, y, step_x=15, step_y=100, scatter_size=2,
                 color_plot='r', date=False, grid=False):
    fig, ax = plt.subplots()
    ax.grid(grid)
    if date:
        formatter = dates.DateFormatter("%m-%d")
        ax.xaxis.set_major_formatter(formatter)
        plt.xticks(rotation=45)
    else:
        ax.xaxis.set_major_locator(ticker.MultipleLocator(step_x))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(step_y))
    ax.scatter(x, y, s=[scatter_size for _ in range(len(x))])
    # ax.plot(x[::], y[::], c=color_plot)
    plt.show()


def update_day_formatter(format='%d/%m', interval=1):
    plt.gcf().autofmt_xdate()
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(dts.DateFormatter(format))
    plt.gca().xaxis.set_major_locator(dts.DayLocator(interval=interval))


def update_hour_formatter(format='%d/%m', interval=1):
    plt.gcf().autofmt_xdate()
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(dts.DateFormatter(format))
    plt.gca().xaxis.set_major_locator(dts.HourLocator(interval=interval))


def date_limit(limit, ax=None, days=1, hours=0):
    if ax is None:
        plt.xlim([limit[0] - timedelta(days=days, hours=hours), limit[1] + timedelta(days=days, hours=hours)])
    else:
        for i, j in enumerate(ax):
            j.set_xlim(
                [limit[i][0] - timedelta(days=days, hours=hours), limit[i][1] + timedelta(days=days, hours=hours)])


def y_limit(limit, deviation=0, ax=None):
    if ax is None:
        plt.ylim([limit[0] - deviation, limit[1] + deviation])
    else:
        for i, j in enumerate(ax):
            j.set_ylim(
                [limit[i][0] - deviation, limit[i][1] + deviation])
