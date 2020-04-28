import zmq
import time
import json
import threading
import datetime
from peewee import *

context = zmq.Context()

socket = context.socket(zmq.REP)
socket.bind("tcp://*:9000")

db = SqliteDatabase('messages.db')
db.connect()


class Message(Model):
    username = CharField()
    text = CharField()
    time = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db


def __del__():
    # def cleanup():
    global socket
    print("close socket")
    socket.close()


# my_thread = threading.Thread(target=test_client)
# my_thread.daemon = True
# my_thread.start()

Message.create_table()

print("start")
while True:
    data = socket.recv_string()
    data = data.split("|")
    print(data)
    if data[0] == "in_mes":
        message = Message(username="anonymous", text=data[1])
        message.save()
    elif data[0] == "history":
        history = ""
        for mes in Message.select():
            history += mes.tex
        socket.send_string(history)
