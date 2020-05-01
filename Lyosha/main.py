# Import necessary packages
import os
import folium
from folium import plugins
import lyosha.read_data as read_data
import sqlite3
import pandas as pd
import numpy as np
import sys


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# import rasterio as rio
# from rasterio.warp import calculate_default_transform, reproject, Resampling

def get_distanse(lat1, lat2, lon1, lon2):
    R = 6371
    sin1 = np.sin((lat1 - lat2) / 2)
    sin2 = np.sin((lon1 - lon2) / 2)
    return 2 * R * np.arcsin(np.sqrt(sin1 * sin1 + sin2 * sin2 * np.cos(lat1) * np.cos(lat2)))


# Create map
folium_map = folium.Map(tiles="CartoDB dark_matter", location=[52.2167, 21.0],
                        zoom_start=2.5, min_zoom=3)

fg = folium.FeatureGroup(name='Грузы', show=False)
tasks_cluster = plugins.MarkerCluster().add_to(fg)
folium_map.add_child(fg)

fg2 = folium.FeatureGroup(name='Филиалы', show=True)
build_cluster = plugins.MarkerCluster().add_to(fg2)
folium_map.add_child(fg2)
folium.LayerControl().add_to(folium_map)

dataset = read_data.Data()

conn = sqlite3.connect(resource_path("mydatabase.db"))  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
GPS = pd.read_sql_query("select * from GPS", conn)
points = []
flag = "автомобиль"
dots = ["Филиал компании в Нью-Йорке", ""]
for _, name, _, transport, la, lo in GPS.values:
    if flag == transport:
        points.append([la, lo])
    else:
        dots[1] = name
        points.append([la, lo])
        folium.PolyLine(points, color="blue", weight=2.5, opacity=1,
                        popup=f"{dots[0]}-{dots[1]}, {flag}").add_to(tasks_cluster)
        dots[0] = name
        points = [[la, lo]]
        marker = folium.CircleMarker(location=[la, lo], radius=1, color='orange')
        marker.add_to(tasks_cluster)
        flag = transport
folium.PolyLine(points, color="blue", weight=2.5, opacity=1,
                popup=f"{GPS['name'][len(GPS) - 2]}-{GPS['name'][len(GPS) - 1]},"
                      f"{GPS['transport'][len(GPS) - 1]}").add_to(tasks_cluster)

otdeli = [[55.716304, 37.730819, "Россия", "Центральное отделение компании ", "Москва, Люблинская ул., Д 5, КОРП 4",
           "Сафронова Евгения Анатольевна", 1000, 1],
          [59.939, 30.315, "Россия", "Филиал компании в Санкт-Петербурге", "Санкт-Петербург, Искровский пр., дом 22 А",
           "Яманаев Андрей Викторович", 250, 0],
          [56.316667, 44, "Россия", "Филиал компании в Нижнем Новгороде", "Нижний Новгород, пр. Ленина, 100",
           "Зиновьев Василий Валентинович", 400, 0],
          [40.923084, -73.839054, "США", "Американский филиал компании", "NY 10552, Mt Vernon, 33 William St",
           "Эбигейл Гибсон", 25, 1],
          [39.908288, 116.427688, "Китай", "Китайский филиал компании", "", "Тедань Хуан", 43, 0],
          [52.502044, 13.413828, "Германия", "Немецкий филиал компании", "10969 Berlin, Prinzessinnenstraße 29",
           "Алекс Гросс", 43, 1]]

for tip in otdeli:
    i = ""
    if tip[3] in GPS['name'].values:
        val = GPS[GPS['name'].values == tip[3]]
        i = f"<hr>" \
            f"<div>В {tip[3]} прийдет груз на {val['transport'].values[0]}е</div>" \
            f"<hr>" \
            f"<div>Время принятия груза: {val['date'].values[0]}</div>" \
            f"<hr>"

        i += f"<div>Время отправки:{val['date'].values[0]}</div>" \
            if not val.index == len(GPS) - 1 else "Конечная остановка"

    marker = folium.Marker(location=[tip[0], tip[1]],
                           popup=f"<div><b>{tip[2]}</b></div>"
                                 f"<div>{tip[3]}</div>"
                                 f"<hr size='#'>"
                                 f"<div>{tip[4]}</div>"
                                 f"<hr size='#'>"
                                 f"<div>Руководитель: <i>{tip[5]}</i></div>"
                                 f"<hr size='#'>"
                                 f"<div>Сотрудников: {tip[6]}</div>"
                                 f"<hr size='#'>"
                                 f"<div>Филиал {'функционирует' if tip[7] == 1 else 'не функционирует'}</div>"
                                 f"{i}",
                           # pop-up label for the marker
                           icon=folium.Icon(icon='building', prefix='fa'), name='Филиалы')
    marker.add_to(build_cluster)

places = [
    "ekb.dat", "msk.dat", "nvs.dat", "china.dat", "ger.dat", "ny.dat",
]
for x in places:
    dataset = read_data.Data()
    lines = dataset.lines_read(f"{x}", 1)
    if x == 'ekb.dat':
        new_linse = []
        for x in lines:
            if not x == '\x00\n':
                new_linse.append(x.replace('\x00', ''))
        dataset.str_read(new_linse)
    else:
        dataset.str_read(lines)
    dataset.read(["La", "Lo", "E"], sep=',')
    points = []
    for la, lo, e in dataset.data.values:
        points.append([la, lo])
        # marker = folium.CircleMarker(location=[la, lo], radius=1)
        # marker.add_to(folium_map)
    folium.PolyLine(points, color="blue", weight=2.5, opacity=1, popup="123", name='Грузы').add_to(tasks_cluster)

folium_map.save(resource_path("my_map.html"))

import os

os.system("start " + resource_path("my_map.html"))
