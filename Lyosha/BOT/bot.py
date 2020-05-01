import critical_value as cv
import read_data
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from Plotter import *
from math import ceil

cv.create_table()

direct = "E:\\DRIVE\\Projects\\Ending\\NTI2020\\SS\\task2\\Data\\dataframes"
cols = ['#', 'date', "oC", 'vsu', 'W', '%', 'Hours']
cr2cols = {
    "С": "oC",
    "ву/вс": 'vsu',
    "загрузка": '%',
    "кВт": 'W',
    "часов": 'Hours'
}
index = ['date']
key = "oC"

dataset = read_data.Data()
dataset.read_from_dir(direct)
dataset.read(cols, index, ["#", "date"])


def echo(message):
    print(message.text)


def telemetry_analize(message):
    pass


command = {
    "/echo": echo,
    "/telemetry_analize": echo,
}
