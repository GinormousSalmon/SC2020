import InetConnection
import socket
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
result = socket.connect("tcp://45.143.136.117:9000")
print(result)
socket.send_string("212")
message = str(socket.recv_string())
print(message)
# print("connect OK!")




# ic_v = InetConnection.InetConnect(socket.gethostname() + "_v", "client")
# ic_v.connect()
# pass_hash = "csssscc"
# ic_v.send_and_wait_answer("12.13.14.15", "p|" + pass_hash)
# print("sent")
# j_mesg, jpg_bytes = ic_v.take_answer_bytes()
# print(j_mesg, jpg_bytes)
