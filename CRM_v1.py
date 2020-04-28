from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys

form_main, base_main = uic.loadUiType('mainForm.ui')
form_chat, base_chat = uic.loadUiType('chat.ui')
messages = ""


class MainUI(base_main, form_main):
    def __init__(self):
        super(base_main, self).__init__()
        self.setupUi(self)
        self.main = None

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
        self.main = ChatUI()
        self.main.show()
        self.close()


class ChatUI(base_chat, form_chat):
    def __init__(self):
        super(base_chat, self).__init__()
        self.setupUi(self)
        self.main = None

        self.back_button = self.findChild(QPushButton, 'backFromChatButton')
        self.back_button.clicked.connect(self.back_from_chat_click)

        self.send_button = self.findChild(QPushButton, 'sendButton')
        self.send_button.clicked.connect(self.send_button_click)

        self.message_field = self.findChild(QLineEdit, 'inputMessage')
        self.message_field.returnPressed.connect(self.send_button_click)

        self.chat_field = self.findChild(QTextEdit, 'chatField')

    def back_from_chat_click(self):
        self.main = MainUI()
        self.main.show()
        self.close()

    def send_button_click(self):
        global messages
        text = self.message_field.text().strip(" ")
        if len(text) > 0:
            messages += text + '<br/>'
            self.chat_field.setHtml(messages)
            self.chat_field.verticalScrollBar().setValue(self.chat_field.verticalScrollBar().maximum())
        self.message_field.clear()


app = QApplication(sys.argv)
window = MainUI()
window.show()
sys.exit(app.exec())

# class ChatUI(QWidget):
#     def __init__(self, parent=None):
#         super(ChatUI, self).__init__()
#         uic.loadUi('chat.ui', self)
#         # mainwindow.setWindowIcon(QtGui.QIcon('PhotoIcon.png'))
#         # self.ToolsBTN = QPushButton('text', self)
#         # self.ToolsBTN.move(50, 350)
#
#
# class Ui(QMainWindow):
#     def __init__(self):
#         super(Ui, self).__init__()
#         uic.loadUi('mainForm.ui', self)
#
#         self.crm_button = self.findChild(QPushButton, 'crmButton')
#         self.crm_button.clicked.connect(self.crm_button_click)
#
#         self.hr_button = self.findChild(QPushButton, 'hrHelperButton')
#         self.hr_button.clicked.connect(self.hr_button_click)
#
#         self.equipment_button = self.findChild(QPushButton, 'equipmentStateButton')
#         self.equipment_button.clicked.connect(self.equipment_button_click)
#
#         self.staff_button = self.findChild(QPushButton, 'staffButton')
#         self.staff_button.clicked.connect(self.staff_button_click)
#
#         self.store_button = self.findChild(QPushButton, 'storeButton')
#         self.store_button.clicked.connect(self.store_button_click)
#
#         self.chat_button = self.findChild(QPushButton, 'chatButton')
#         self.chat_button.clicked.connect(self.chat_button_click)
#
#         self.main_layout = self.findChild(QLayout, 'mainLayout')
#         self.chat_layout = self.findChild(QLayout, 'chatLayout')
#
#         self.main_widget = self.findChild(QWidget, 'widget1')
#         self.chat_widget = self.findChild(QWidget, 'widget2')
#
#         print(self.chat_layout)
#
#         # self.chat_field = self.findChild(QTextEdit, 'chatField')
#         # self.chat_field.setVisible(False)
#         #
#         # self.input_message = self.findChild(QLineEdit, 'inputMessage')
#         # self.input_message.hide()
#         self.show()
#
#     def start_chat_ui(self):
#         # self.setLayout(self.main_layout)
#         stack = QStackedLayout()
#         # stack.addWidget(self.chat_widget)
#         # stack.setCurrentWidget(self.chat_widget)
#         self.setLayout(self.chat_layout)
#         self.show()
#
#         # self.ChatUI = ChatUI(self)
#         # self.setWindowTitle("Chat")
#         # self.setCentralWidget(self.ChatUI)
#         # # self.send_button = self.findChild(QPushButton, 'sendButton')
#         # # self.send_button.clicked.connect(self.crm_button_click)
#         # self.show()
#
#     def crm_button_click(self):
#         # This is executed when the button is pressed
#         print('crm_button_click')
#         uic.loadUi('mainForm.ui', self)
#         self.show()
#         # self.setLayout(self.chat_layout)
#         # self.show()
#         # self.start_chat_ui()
#         # self.crm_button.hide()
#
#     def hr_button_click(self):
#         # This is executed when the button is pressed
#         print('hr_button_click')
#         uic.loadUi('chat.ui', self)
#         self.show()
#
#     def equipment_button_click(self):
#         # This is executed when the button is pressed
#         print('equipment_button_click')
#
#     def staff_button_click(self):
#         # This is executed when the button is pressed
#         print('staff_button_click')
#         # self.crm_button.show()
#
#     def store_button_click(self):
#         # This is executed when the button is pressed
#         print('store_button_click')
#         # self.startUIToolTab()
#
#     def chat_button_click(self):
#         # This is executed when the button is pressed
#         print('chat_button_click')
#         self.start_chat_ui()
#
#
# class Ui2(QMainWindow):
#     def __init__(self, ui):
#         super(Ui, self).__init__()
#         uic.loadUi(ui, self)
#         self.show()
#
#
# app = QApplication(sys.argv)
# window = Ui()
# sys.exit(app.exec())
