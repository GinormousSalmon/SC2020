import traceback

from PyQt5 import uic, QtCore, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import zmq
import os
from datetime import datetime
import time


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# connecting to server
context = zmq.Context()
socket = context.socket(zmq.REQ)
result = socket.connect("tcp://45.143.136.117:9000")

messages = ""  # local chat history
update = False

# loading ui's
form_main, base_main = uic.loadUiType(resource_path('mainForm.ui'))
form_chat, base_chat = uic.loadUiType(resource_path('chat.ui'))


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    # import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    Qt.QMessageBox.critical(None, 'Error', text)
    quit()


sys.excepthook = log_uncaught_exceptions


class AThread(QThread):
    threadSignalAThread = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        global messages, update
        while update:
            socket.send_string("history")
            print("waiting answer from server", datetime.now())
            messages = str(socket.recv_string())  # download chat history
            print(messages)
            self.threadSignalAThread.emit(messages)
            QThread.msleep(1000)


class MainUI(base_main, form_main):
    def __init__(self):
        super(base_main, self).__init__()
        self.setupUi(self)
        self.main = None

        # buttons binding
        self.crm_button = self.findChild(QPushButton, 'crmButton')
        self.crm_button.clicked.connect(self.crm_button_click)

        self.hr_button = self.findChild(QPushButton, 'hrHelperButton')
        self.hr_button.clicked.connect(self.hr_button_click)

        self.equipment_button = self.findChild(QPushButton, 'equipmentStateButton')
        self.equipment_button.clicked.connect(self.equipment_button_click)

        self.staff_button = self.findChild(QPushButton, 'staffButton')
        self.staff_button.clicked.connect(self.staff_button_click)

        self.store_button = self.findChild(QPushButton, 'storeButton')
        self.store_button.clicked.connect(self.store_button_click)

        self.chat_button = self.findChild(QPushButton, 'chatButton')
        self.chat_button.clicked.connect(self.chat_button_click)

    def crm_button_click(self):
        # This is executed when the button is pressed
        print('crm_button_click')

    def hr_button_click(self):
        # This is executed when the button is pressed
        print('hr_button_click')

    def equipment_button_click(self):
        # This is executed when the button is pressed
        print('equipment_button_click')

    def staff_button_click(self):
        # This is executed when the button is pressed
        print('staff_button_click')

    def store_button_click(self):
        # This is executed when the button is pressed
        print('store_button_click')

    def chat_button_click(self):
        # close current window and open chat window
        self.main = ChatUI()
        self.main.show()
        self.close()


class ChatUI(base_chat, form_chat):
    def __init__(self):
        global update, messages
        super(base_chat, self).__init__()
        self.setupUi(self)
        self.main = None
        self.thread = None

        # widgets binding
        self.back_button = self.findChild(QPushButton, 'backFromChatButton')
        self.back_button.clicked.connect(self.back_from_chat_click)

        self.send_button = self.findChild(QPushButton, 'sendButton')
        self.send_button.clicked.connect(self.send_button_click)

        self.message_field = self.findChild(QLineEdit, 'inputMessage')
        self.message_field.returnPressed.connect(self.send_button_click)

        self.chat_field = self.findChild(QTextEdit, 'chatField')
        self.chat_field.setHtml(messages)  # first updating chat field
        self.chat_field.verticalScrollBar().setValue(self.chat_field.verticalScrollBar().maximum())  # scroll to end

        update = True

        # ----------------------------------------------------------------------------------------------------
        # my_thread = threading.Thread(target=self.chat_updater)
        # my_thread.daemon = True
        # my_thread.start()
        self.using_q_thread()

    def using_q_thread(self):
        if self.thread is None:
            self.thread = AThread()
            self.thread.threadSignalAThread.connect(self.on_threadSignalAThread)
            self.thread.finished.connect(self.finishedAThread)
            self.thread.start()
            # self.btnA.setText("Stop AThread(QThread)")
        else:
            self.thread.terminate()
            self.thread = None
            # self.btnA.setText("Start AThread(QThread)")

    def finishedAThread(self):
        self.thread = None
        # self.btnA.setText("Start AThread(QThread)")

    def on_threadSignalAThread(self, value):
        # self.msg.label.setText(str(value))
        # print(value)
        self.chat_field.setHtml(str(value))  # updating chat field
        self.chat_field.verticalScrollBar().setValue(self.chat_field.verticalScrollBar().maximum())  # scroll to end
        # Восстанавливаем визуализацию потокового окна, если его закрыли. Поток работает.
        # .setVisible(true) или .show() устанавливает виджет в видимое состояние,
        # если видны все его родительские виджеты до окна.
        # if not self.msg.isVisible():
        #     self.msg.show()

    print("started")

    # ----------------------------------------------------------------------------------------------------

    def chat_updater(self):
        global messages, update
        while update:
            socket.send_string("history")
            print("waiting answer from server")
            messages = str(socket.recv_string())  # download chat history
            print(messages)
            self.chat_field.setHtml("messages")  # updating chat field
            self.chat_field.verticalScrollBar().setValue(self.chat_field.verticalScrollBar().maximum())  # scroll to end
            time.sleep(1)

    def back_from_chat_click(self):
        # go back to main window
        self.thread.terminate()
        self.thread = None

        self.main = MainUI()
        self.main.show()
        self.close()

    def send_button_click(self):
        # send message button clicked
        global messages
        text = self.message_field.text().strip(" ")
        if len(text) > 0:  # if message is not empty
            messages += text + '<br/>'  # appending message to local history
            socket.send_string("in_mes|" + text)
            print(str(socket.recv_string()))
        self.chat_field.setHtml(messages)  # updating chat field
        self.chat_field.verticalScrollBar().setValue(self.chat_field.verticalScrollBar().maximum())  # scroll to end
        self.message_field.clear()


app = QApplication(sys.argv)
window = MainUI()
window.show()
sys.exit(app.exec())
