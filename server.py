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


def send(mes):
    try:
        print("sending " + mes)
    except UnicodeEncodeError:
        print("UnicodeEncodeError")
    socket.send_string(mes)


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
            print("UnicodeEncodeError")
        if data[0] == "in_mes":
            message = Message(username=data[1], text=data[2])
            message.save()
            send("ok")
        elif data[0] == "history":
            history = ""
            for mes in Message.select():
                history += mes.text + '<br/>'
            send(history)
            # result = send("usercheck|" + email + "|" + password)
        elif data[0] == "usercheck":
            if len(User.select().where(User.email == data[1], User.password == data[2])) > 0:
                user = User.get(User.email == data[1])
                send("exist$#$" + user.name + "$#$" + str(user.position))
            else:
                send("wrong user")
                #            result = send("reg|" + email + "|" + password + "|" + name + "|" + position)
        elif data[0] == "reg":
            if len(User.select().where(User.email == data[1], User.password == data[2])) > 0:
                send("exist")
            else:
                user = User(email=data[1], name=data[3], position=int(data[4]), password=data[2])
                user.save()
                send("reg_ok")
        else:
            send("error")
    except Exception as ex:
        try:
            send("error")
        except:
            pass
        print(ex)
        time.sleep(0.5)
