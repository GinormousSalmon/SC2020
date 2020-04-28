import zmq
import time
import json
import threading
import datetime

context2 = zmq.Context()

socket2 = context2.socket(zmq.REP)
socket2.bind("tcp://*:9000")


def __del__():
    # def cleanup():
    global socket2
    print("close socket")
    socket2.close()


# atexit.register(cleanup)

message_list = []  # id_from, text, id_to, type, data


def take_message(id, type):
    # find message for client  id_from, text, id_to
    # print("take_message", id)
    # print(message_list)
    for i in range(len(message_list)):
        if message_list[i][1] == id and type == message_list[i][3]:
            mes = message_list.pop(i)
            return mes
    return []


def clear_packet(id):
    global message_list
    id = int(id)
    count = 0
    new_list = []
    for i in range(len(message_list)):
        if message_list[i][0] == id or message_list[i][2] == id:
            count += 1
            pass
        else:
            new_list.append(message_list[i])

    message_list = new_list.copy()
    return count


def find_duplication(mes):
    for i in range(len(message_list)):
        # print( message_list[i], mes)
        if message_list[i][0] == int(mes[1]) and message_list[i][1] == int(mes[2]) and message_list[i][2] == mes[3]:
            # message_list.pop(i)
            # print("duble", mes)
            return True
    return False
    pass


# my_thread = threading.Thread(target=test_client)
# my_thread.daemon = True
# my_thread.start()


print("start")
while 1:
    message = socket2.recv_string()
    message = message.split("~")
    print(message)
    if message[0] == "nice cock":
        socket2.send_string("awesome balls")
    continue
    # sending info
    if message[0] == "s":
        # deleting requests
        # while 1:
        #     mes = take_message(int(message[1]), "s")
        #     if len(mes) == 0:
        #         break
        # print(message)
        if not find_duplication(message):
            try:
                message_list.append([int(message[1]), int(message[2]), message[3], "s"])
            except:
                pass
        # print(message_list)
        socket2.send_string("1~")
        continue

    # request for answer
    if message[0] == "t":
        # deleting requests
        # while 1:
        #     mes = take_message(int(message[1]), "t")
        #     if len(mes) == 0:
        #         break
        mes = take_message(int(message[1]), "s")

        flag_reg = False
        # print(clients_list, message)

        # print(message)
        resp = "0~"
        if not flag_reg:
            print("nedd reg", message)
            resp = "-1~"

        if len(mes) > 0:
            if mes[3] == "s":
                resp = str(mes[0]) + "~" + (mes[2]) + "~"
            # print(resp)
        # print(resp)
        socket2.send_string(resp)
        continue

    # sending bytes
    if message[0] == "b":
        # print(message)
        message_byte = socket2.recv(0)
        # print("take bytes", len(message_byte))

        # deleting byte messages
        while 1:
            mes = take_message(int(message[1]), "b")
            if len(mes) == 0:
                break
        message_list.append([int(message[1]), int(message[2]), message[3], "b", message_byte])
        # print(message_list)
        socket2.send_string("1~")
        continue

    # request for byte answer
    if message[0] == "bt":
        # print(message)
        mes = take_message(int(message[1]), "b")
        # print("bt_mes", mes)
        frame_json = "-1"
        frame_bytes = b''
        resp = "-1~"
        if len(mes) > 0:
            if mes[3] == "b":
                # resp = str(mes[0]) + "~" + (mes[2]) + "~"
                # socket2.send_string(resp)
                # print("send,",mes[1] )
                frame_json = json.loads(mes[2])
                frame_bytes = mes[4]

            # print(resp)
        # socket2.send_string(frame_json, zmq.SNDMORE)

        socket2.send_json(frame_json, zmq.SNDMORE)
        socket2.send(frame_bytes)
        continue

    if message[0] == "clear":
        # print("take num ", num_client)
        # print("clear", message)
        count = clear_packet(message[1])
        socket2.send_string(str(count))
        continue

    # print(message)
    socket2.send_string("error")

    # socket2.send_string(message)
