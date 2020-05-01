import zmq
import time
import json
import threading
import datetime
from peewee import *

context = zmq.Context()

socket = context.socket(zmq.REP)
socket.bind("tcp://*:9000")

db_mes = SqliteDatabase('messages.db')
db_mes.connect()

db_users = SqliteDatabase('users.db')
db_users.connect()

positions = "Сотрудник", "Руководитель отдела", "Руководитель подразделения", "Руководитель предприятия"


class Message(Model):
    username = CharField()
    text = CharField()
    time = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db_mes


class User(Model):
    email = CharField()
    name = CharField()
    position = IntegerField()
    password = CharField()

    class Meta:
        database = db_users


def __del__():
    # def cleanup():
    global socket
    print("close socket")
    socket.close()


# my_thread = threading.Thread(target=test_client)
# my_thread.daemon = True
# my_thread.start()

Message.create_table()
User.create_table()

print("start")
while True:
    try:
        data = socket.recv_string()
        data = data.split("|")
        try:
            print(data)
        except UnicodeEncodeError:
            print("encode error")
        if data[0] == "in_mes":
            message = Message(username=data[1], text=data[2])
            message.save()
            socket.send_string("ok")
        elif data[0] == "history":
            history = ""
            for mes in Message.select():
                history += mes.text + '<br/>'
            socket.send_string(history)
            # result = send("usercheck|" + email + "|" + password)
        elif data[0] == "usercheck":
            if len(User.select().where(User.email == data[1], User.password == data[2])) > 0:
                user = User.get(User.email == data[1])
                socket.send_string("exist$#$" + user.name + "$#$" + user.position)
            else:
                socket.send_string("error")
                #            result = send("reg|" + email + "|" + password + "|" + name + "|" + position)
        elif data[0] == "reg":
            if len(User.select().where(User.email == data[1], User.password == data[2])) > 0:
                socket.send_string("exist")
            else:
                user = User(email=data[1], name=data[3], position=int(data[4]), password=data[2])
                user.save()
                socket.send_string("reg_ok")
    except:
        pass
