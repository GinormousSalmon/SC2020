import InetConnection
import socket

ic_v = InetConnection.InetConnect(socket.gethostname() + "_v", "client")
ic_v.connect()
pass_hash = "csssscc"
ic_v.send_and_wait_answer("12.13.14.15", "p|" + pass_hash)
j_mesg, jpg_bytes = ic_v.take_answer_bytes()
