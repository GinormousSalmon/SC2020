from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys

uifile_1 = 'mainForm.ui'
form_1, base_1 = uic.loadUiType(uifile_1)

uifile_2 = 'chat.ui'
form_2, base_2 = uic.loadUiType(uifile_2)


class Example(base_1, form_1):
    def __init__(self):
        super(base_1, self).__init__()
        self.setupUi(self)
        self.crmButton.clicked.connect(self.change)

    def change(self):
        self.main = MainPage()
        self.main.show()
        self.close()


class MainPage(base_2, form_2):
    def __init__(self):
        super(base_2, self).__init__()
        self.setupUi(self)
        self.sendButton.clicked.connect(self.change)

    def change(self):
        self.main = Example()
        self.main.show()
        self.close()


app = QApplication(sys.argv)
ex = Example()
ex.show()
sys.exit(app.exec_())
