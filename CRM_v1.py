import traceback

from PyQt5 import uic, QtCore, Qt, QtGui
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

# 1-сотрудник, 2-руководитель отдела, 3-руководитель подразделения, 4-руководитель предприятия
current_user = "none", 0  # ФИ, должность

# loading ui's
form_main, base_main = uic.loadUiType(resource_path('mainForm.ui'))
form_chat, base_chat = uic.loadUiType(resource_path('chat.ui'))
form_login, base_login = uic.loadUiType(resource_path('login.ui'))
form_reg, base_reg = uic.loadUiType(resource_path('registration.ui'))


def send(message):
    return 1


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


class LoginUI(base_login, form_login):
    def __init__(self):
        super(base_login, self).__init__()
        self.setupUi(self)
        self.main = None

        self.signin_button = self.findChild(QPushButton, 'signin_button')
        self.signin_button.clicked.connect(self.signin_button_click)

        self.signup_button = self.findChild(QPushButton, 'signup_button')
        self.signup_button.clicked.connect(self.signup_button_click)

        self.email_input = self.findChild(QLineEdit, 'mail_login_input')

        self.password_input = self.findChild(QLineEdit, 'pw_login_input')

        self.info_label = self.findChild(QLabel, 'info')
        pal = self.info_label.palette()
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
        self.info_label.setPalette(pal)

    def signin_button_click(self):
        email = self.email_input.text().strip(" ")
        password = self.password_input.text().strip(" ")
        if len(email) == 0:
            self.info_label.setText("email is empty")
        elif len(password) == 0:
            self.info_label.setText("password is empty")
        else:
            result = send("usercheck|" + email + "|" + password)
            if result is None:
                self.info_label.setText("connection error. try again")
            elif result == "exist":
                self.main = MainUI()
                self.main.show()
                self.close()
            else:
                self.info_label.setText("login or password incorrect")

    def signup_button_click(self):
        self.main = RegUI()
        self.main.show()
        self.close()


class RegUI(base_reg, form_reg):
    def __init__(self):
        super(base_reg, self).__init__()
        self.setupUi(self)
        self.main = None

        self.signup_button = self.findChild(QPushButton, 'reg_button')
        self.signup_button.clicked.connect(self.signup_button_click)

        self.cancel_button = self.findChild(QPushButton, 'cancel_reg_button')
        self.cancel_button.clicked.connect(self.cancel_button_click)

        self.name_input = self.findChild(QLineEdit, 'name_reg_input')

        self.email_input = self.findChild(QLineEdit, 'email_reg_input')

        self.password_input = self.findChild(QLineEdit, 'pw_reg_input')

        self.position_input = self.findChild(QComboBox, 'position_box_input')
        self.position_input.addItem("Сотрудник")
        self.position_input.addItem("Руководитель отдела")
        self.position_input.addItem("Руководитель подразделения")
        self.position_input.addItem("Руководитель предприятия")

        self.info_label = self.findChild(QLabel, 'info')
        pal = self.info_label.palette()
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
        self.info_label.setPalette(pal)

    def signup_button_click(self):
        name = self.name_input.text().strip(" ")
        email = self.email_input.text().strip(" ")
        position = self.position_input.currentText().strip(" ")
        password = self.password_input.text().strip(" ")

        if len(name) == 0:
            self.info_label.setText("name is empty")
        elif len(email) == 0:
            self.info_label.setText("email is empty")
        elif len(password) == 0:
            self.info_label.setText("password is empty")
        else:
            result = send("reg|" + email + "|" + password + "|" + name + "|" + position)
            if result is None:
                self.info_label.setText("connection error. try again")
            elif result == "reg_ok":
                self.main = MainUI()
                self.main.show()
                self.close()
            else:
                self.info_label.setText("this email already registered")

    def cancel_button_click(self):
        self.main = LoginUI()
        self.main.show()
        self.close()


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

        self.logout_button = self.findChild(QPushButton, 'log_out_button')
        self.logout_button.clicked.connect(self.logout_button_click)

        self.username = self.findChild(QLabel, 'current_user_label')

        self.user_position = self.findChild(QLabel, 'user_position_label')

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

    def logout_button_click(self):
        pass


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

        # starting new thread
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

    print("thread started")

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
window = LoginUI()
window.show()
sys.exit(app.exec())
