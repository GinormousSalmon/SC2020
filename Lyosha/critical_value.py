from lyosha.read_data import Data
import sqlite3
import pandas as pd
import sys
import os


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


conn = sqlite3.connect(resource_path("mydatabase.db"))  #
cursor = conn.cursor()

data = pd.read_sql_query(f"select * from critical ", conn, index_col="index")

cols = ["GG", "Warning", "Type"]
index = False
del cursor
conn.close()


def get_value(key, param):
    mask = data['Type'] == param
    return float(data[mask][key].values[0])


def warning(x, p):
    print(f"До опасного: {x} {p}")


def dangerous(x, p):
    print(f"До критического значения: {x} {p}")


def critical(x, p):
    print(f"ВНИМАНИЕ, ДО ПРЕВЫШЕНИЯ КРИТИЧЕСКОГО ЗНАЧЕНИЯ: {x} {p}")
    print(f"Вам необходимо {recommendation_critical[p]}")


def death(x, p):
    print(f"Оборудование сломано: предел {p} превышен на {x} ")
    print(f"Вам необходимо {recommendation_death[p]}")


err = {
    0: warning,
    1: dangerous,
    2: critical,
    3: death
}
recommendation_death = {
    "С": "выключить и охладить установку",
    "ву/вс": "охладить установку",
    "загрузка": "уменьшить нагрузку на установку",
    "кВт": "уменьшить нагрузку на установку",
    "часов": "остановить процесс и выключить оборудование",
}
recommendation_critical = {
    "С": "охладить установку",
    "ву/вс": "охладить установку",
    "загрузка": "уменьшить нагрузку на установку",
    "кВт": "уменьшить нагрузку на установку",
    "часов": "в скором времени потребуется отключить установку"
}
