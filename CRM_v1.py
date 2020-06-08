import shutil
import subprocess
import traceback

import qimage2ndarray as qimage2ndarray
from PyQt5 import uic, QtCore, Qt, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import zmq
import os
import lyosha.first_task as graphics
from datetime import datetime
import time


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# try:
#     print(resource_path('_cnames.json'))
#     os.mkdir(resource_path('branca'))
#     shutil.copy(resource_path('_cnames.json'),
#                 resource_path('_cnames.json').strip('_cnames.json') + 'branca\\_cnames.json')
#
#     shutil.copy(resource_path('_schemes.json'),
#                 resource_path('_schemes.json').strip('_schemes.json') + 'branca\\_schemes.json')
#
#     shutil.copy(resource_path('scheme_base_codes.json'),
#                 resource_path('scheme_base_codes.json').strip(
#                     'scheme_base_codes.json') + 'branca\\scheme_base_codes.json')
#
#     shutil.copy(resource_path('scheme_info.json'),
#                 resource_path('scheme_info.json').strip('scheme_info.json') + 'branca\\scheme_info.json')
#
#     shutil.copy(resource_path('__init__.py'),
#                 resource_path('__init__.py').strip('__init__.py') + 'branca\\__init__.py')
# except Exception as ex:
#     print(ex)

try:
    import main
except Exception as ex:
    print(ex)

# connecting to server
context = zmq.Context()
socket = context.socket(zmq.REQ)
result = socket.connect("tcp://46.173.215.129:9000")

messages = ""  # local chat history
update = False

# 1-сотрудник, 2-руководитель отдела, 3-руководитель подразделения, 4-руководитель предприятия
current_user = "none", "none", 0  # email, ФИ, должность
positions = ["Сотрудник", "Руководитель отдела", "Руководитель подразделения", "Руководитель предприятия"]

# loading ui's
form_main, base_main = uic.loadUiType(resource_path('mainForm.ui'))
form_chat, base_chat = uic.loadUiType(resource_path('chat.ui'))
form_login, base_login = uic.loadUiType(resource_path('login.ui'))
form_reg, base_reg = uic.loadUiType(resource_path('registration.ui'))
form_tele, base_tele = uic.loadUiType(resource_path('telemetry.ui'))


def send(message):
    global socket
    # thread = threading.Thread(target=test_client)
    # thread.daemon = True
    # thread.start()
    socket.send_string(message)
    print(message + " waiting answer from server")
    for i in range(10):
        try:
            answer = socket.recv_string(zmq.NOBLOCK)
        except zmq.ZMQError:
            pass
        else:
            print("got answer")
            return answer
        finally:
            time.sleep(0.1)
    print("no answer")
    return None


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
            # socket.send_string("history")
            messages = send("history")
            # print("waiting answer from server", datetime.now())
            # messages = str(socket.recv_string())  # download chat history
            # print(messages)
            self.threadSignalAThread.emit(messages)
            QThread.msleep(1000)


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.values[index.row()][index.column()]))
        return QtCore.QVariant()


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
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.signin_button_click)

        self.info_label = self.findChild(QLabel, 'info')
        pal = self.info_label.palette()
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
        self.info_label.setPalette(pal)

    def signin_button_click(self):
        global current_user
        email = self.email_input.text().strip(" ")
        password = self.password_input.text().strip(" ")
        # email = "terleckii"
        # password = "1234"  # #######################################################################
        if len(email) == 0:
            self.info_label.setText("email is empty")
        elif len(password) == 0:
            self.info_label.setText("password is empty")
        else:
            result = send("usercheck|" + email + "|" + password)
            if result is None:
                self.info_label.setText("connection error. try again")
                return 0
            result = result.split("$#$")
            print(result)
            if result[0] == "exist":
                name = result[1]
                position = int(result[2])
                current_user = email, name, position
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

        self.age_input = self.findChild(QLineEdit, 'age_reg_input')

        self.password_input = self.findChild(QLineEdit, 'pw_reg_input')
        self.password_input.setEchoMode(QLineEdit.Password)

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
        global current_user, positions
        name = self.name_input.text().strip(" ")
        email = self.email_input.text().strip(" ")
        position = positions.index(self.position_input.currentText()) + 1
        password = self.password_input.text().strip(" ")

        if len(name) == 0:
            self.info_label.setText("name is empty")
        elif len(email) == 0:
            self.info_label.setText("email is empty")
        elif len(password) == 0:
            self.info_label.setText("password is empty")
        else:
            result = send("reg|" + email + "|" + password + "|" + name + "|" + str(position))
            if result is None:
                self.info_label.setText("connection error. try again")
            elif result == "reg_ok":
                current_user = email, name, int(position)
                print(current_user)
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
        global current_user, positions
        super(base_main, self).__init__()
        self.setupUi(self)
        self.main = None

        # buttons binding
        self.crm_button = self.findChild(QPushButton, 'crmButton')
        self.crm_button.clicked.connect(self.crm_button_click)

        self.map_button = self.findChild(QPushButton, 'mapsButton')
        self.map_button.clicked.connect(self.map_button_click)

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
        self.username.setText(current_user[1])

        self.user_position = self.findChild(QLabel, 'user_position_label')
        self.user_position.setText(positions[current_user[2] - 1])

    def crm_button_click(self):
        # This is executed when the button is pressed
        print('crm_button_click')

    def map_button_click(self):
        # This is executed when the button is pressed
        print('map_button_click')
        try:
            main.work()
        except Exception as ex:
            print(ex)
        # subprocess.call("python " + resource_path("main.py"), shell=True)

    def equipment_button_click(self):
        # This is executed when the button is pressed
        print('equipment_button_click')
        self.main = TelemetryUI()
        self.main.show()
        self.close()

    def staff_button_click(self):
        # This is executed when the button is pressed
        print('staff_button_click')

    def store_button_click(self):
        # This is executed when the button is pressed
        print('store_button_click')

    def chat_button_click(self):
        # close current window and open chat window
        print('chat_button_click')
        self.main = ChatUI()
        self.main.show()
        self.close()

    def logout_button_click(self):
        print('logout_button_click')
        self.main = LoginUI()
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

        self.info_label = self.findChild(QLabel, 'info')
        pal = self.info_label.palette()
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
        self.info_label.setPalette(pal)

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
        if value is None:
            self.info_label.setText("connection error. try again")
        else:
            self.info_label.setText("")
            self.chat_field.setHtml(str(value))  # updating chat field
            self.chat_field.verticalScrollBar().setValue(self.chat_field.verticalScrollBar().maximum())  # scroll to end

    # print("thread started")

    def back_from_chat_click(self):
        global update
        # go back to main window
        update = False
        # self.thread.terminate()
        self.thread = None

        self.main = MainUI()
        self.main.show()
        self.close()

    def send_button_click(self):
        # send message button clicked
        global messages, current_user
        text = self.message_field.text().strip(" ")
        if len(text) > 0:  # if message is not empty
            messages += text + '<br/>'  # appending message to local history
            answer = send("in_mes|" + current_user[0] + "|" + text)
            # socket.send_string("in_mes|" + text)
            # print(str(socket.recv_string()))
            print(answer)
        self.chat_field.setHtml(messages)  # updating chat field
        self.chat_field.verticalScrollBar().setValue(self.chat_field.verticalScrollBar().maximum())  # scroll to end
        self.message_field.clear()


class TelemetryUI(base_tele, form_tele):
    def __init__(self):
        super(base_tele, self).__init__()
        self.setupUi(self)
        self.main = None

        self.back_button = self.findChild(QPushButton, 'back_tele_button')
        self.back_button.clicked.connect(self.back_click)

        self.all_data_button = self.findChild(QPushButton, 'all_devices_data')
        self.all_data_button.clicked.connect(self.all_data_click)

        self.warning_button = self.findChild(QPushButton, 'warning_tele_button')
        self.warning_button.clicked.connect(self.warning_click)

        self.critical_button = self.findChild(QPushButton, 'critical_tele_button')
        self.critical_button.clicked.connect(self.critical_click)

        self.graphic_radiobutton = self.findChild(QRadioButton, 'graphic_rbutton')
        self.table_radiobutton = self.findChild(QRadioButton, 'table_rbutton')
        self.diagram_radiobutton = self.findChild(QRadioButton, 'diagram_rbutton')

        self.date_begin = self.findChild(QDateTimeEdit, 'dateBegin')
        self.date_end = self.findChild(QDateTimeEdit, 'dateEnd')

        self.equipment_input = self.findChild(QComboBox, 'equipment_box')
        self.equipment_input.addItem("Все")
        self.box_dict = {"Номер": 'num', "Дата": 'date', "Температура": "oC", "Уровень вибраций": 'vsu',
                         "Загруженность": 'congestion', "Мощность": 'W', "Время": 'Hours'}
        for i in range(1, 13):
            self.equipment_input.addItem(str(i))

        self.telemetry_input = self.findChild(QComboBox, 'telemetry_type')
        self.telemetry_input.addItem("Номер")
        self.telemetry_input.addItem("Температура")
        self.telemetry_input.addItem("Уровень вибраций")
        self.telemetry_input.addItem("Загруженность")
        self.telemetry_input.addItem("Мощность")
        self.telemetry_input.addItem("Время")

        self.table = self.findChild(QTableView, 'tableView')
        self.image_view = self.findChild(QGraphicsView, 'graphicsView')

    def back_click(self):
        self.main = MainUI()
        self.main.show()
        self.close()

    # mask = masks[0][0] | masks[2][0] | masks[4][0] | masks[6][0] | masks[8][0]
    def all_data_click(self):
        if self.table_radiobutton.isChecked():
            style = 0
        elif self.graphic_radiobutton.isChecked():
            style = 1
        elif self.diagram_radiobutton.isChecked():
            style = 2
        else:
            return 0
        telemetry_type = self.box_dict.get(self.telemetry_input.currentText())
        number = self.equipment_input.currentText()
        if number == "Все":
            number = 0

        begin_date = self.date_begin.dateTime()
        year_1 = begin_date.date().year()
        month_1 = begin_date.date().month()
        day_1 = begin_date.date().day()
        hour_1 = begin_date.time().hour()

        end_date = self.date_end.dateTime()
        year_2 = end_date.date().year()
        month_2 = end_date.date().month()
        day_2 = end_date.date().day()
        hour_2 = end_date.time().hour()

        date1 = datetime(year_1, month_1, day_1, hour_1)
        date2 = datetime(year_2, month_2, day_2, hour_2)
        print("mask", graphics.masks[3][0])
        result = graphics.create_graphic(int(number), date1, date2, telemetry_type, out=style)
        if style == 0:
            model = PandasModel(result)
            self.table.setModel(model)
            # self.image_view.hide()
            self.table.show()
        else:
            # self.image_view.setBackgroundBrush(result)
            scene = QGraphicsScene(self)
            scene.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(result)))
            self.image_view.setScene(scene)
            self.table.hide()
            self.image_view.show()

    def warning_click(self):
        if self.table_radiobutton.isChecked():
            style = 0
        elif self.graphic_radiobutton.isChecked():
            style = 1
        elif self.diagram_radiobutton.isChecked():
            style = 2
        else:
            return 0
        telemetry_type = self.box_dict.get(self.telemetry_input.currentText())
        number = self.equipment_input.currentText()
        if number == "Все":
            number = 0

        begin_date = self.date_begin.dateTime()
        year_1 = begin_date.date().year()
        month_1 = begin_date.date().month()
        day_1 = begin_date.date().day()
        hour_1 = begin_date.time().hour()

        end_date = self.date_end.dateTime()
        year_2 = end_date.date().year()
        month_2 = end_date.date().month()
        day_2 = end_date.date().day()
        hour_2 = end_date.time().hour()

        date1 = datetime(year_1, month_1, day_1, hour_1)
        date2 = datetime(year_2, month_2, day_2, hour_2)
        print("mask", graphics.masks[3][0])
        mask = graphics.masks[0][0] + ' OR ' + graphics.masks[2][0] + ' OR ' + graphics.masks[4][0] + ' OR ' + \
               graphics.masks[6][0] + ' OR ' + graphics.masks[8][0]
        result = graphics.create_graphic(int(number), date1, date2, telemetry_type, mask=mask, out=style)
        if style == 0:
            model = PandasModel(result)
            self.table.setModel(model)
            # self.image_view.hide()
            self.table.show()
        else:
            # self.image_view.setBackgroundBrush(result)
            scene = QGraphicsScene(self)
            scene.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(result)))
            self.image_view.setScene(scene)
            self.table.hide()
            self.image_view.show()

    def critical_click(self):
        if self.table_radiobutton.isChecked():
            style = 0
        elif self.graphic_radiobutton.isChecked():
            style = 1
        elif self.diagram_radiobutton.isChecked():
            style = 2
        else:
            return 0
        telemetry_type = self.box_dict.get(self.telemetry_input.currentText())
        number = self.equipment_input.currentText()
        if number == "Все":
            number = 0

        begin_date = self.date_begin.dateTime()
        year_1 = begin_date.date().year()
        month_1 = begin_date.date().month()
        day_1 = begin_date.date().day()
        hour_1 = begin_date.time().hour()

        end_date = self.date_end.dateTime()
        year_2 = end_date.date().year()
        month_2 = end_date.date().month()
        day_2 = end_date.date().day()
        hour_2 = end_date.time().hour()

        date1 = datetime(year_1, month_1, day_1, hour_1)
        date2 = datetime(year_2, month_2, day_2, hour_2)
        print("mask", graphics.masks[3][0])
        mask = graphics.masks[1][0] + ' OR ' + graphics.masks[3][0] + ' OR ' + graphics.masks[5][0] + ' OR ' + \
               graphics.masks[7][0] + ' OR ' + graphics.masks[9][0]
        result = graphics.create_graphic(int(number), date1, date2, telemetry_type, mask=mask, out=style)
        if style == 0:
            model = PandasModel(result)
            self.table.setModel(model)
            # self.image_view.hide()
            self.table.show()
        else:
            # self.image_view.setBackgroundBrush(result)
            scene = QGraphicsScene(self)
            scene.addPixmap(QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(result)))
            self.image_view.setScene(scene)
            self.table.hide()
            self.image_view.show()


app = QApplication(sys.argv)
window = LoginUI()
window.show()
sys.exit(app.exec())
