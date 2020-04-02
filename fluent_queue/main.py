import sys
import os
import cgitb
import time

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QEvent
# from PyQt5.QtCore import pyqtSignal
# from PyQt5.QtGui import QTextCursor

from ui_py.ui_queue_main import Ui_fluent_queue
from func.func_ui_set import UiSet
from func.func_account import AccVerify
from func.func_timer import SleepOut


class MyMainWindow(QMainWindow, Ui_fluent_queue):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.ui_alter = UiSet(self)                             # UiSet is the collection of Ui change object
        self.ui_alter.set_all_icon()
        self.ui_alter.ui_user_logoff()                          # change Ui to user logoff status
        self.btn()                                              # enable button function
        self.sleep_time = SleepOut(self, 10)                    # create timer to logout if not operate for a long time
        self.sleep_time.time_exceed.connect(self.user_logout)
        # --------- initial_variable--------
        self.acc_name = str()
        self.mission_list = list()

    def btn(self):
        self.action_login.triggered.connect(self.account_verification)
        self.action_logout.triggered.connect(self.user_logout)
        # self.action_logout.setStatusTip()

    def account_verification(self):
        """
        AccVerify is a sub Ui for user to login
        it will verify if account and password are correct
        if correct, it will return.
        :return: a pyqtsignal(verify_success)
        """
        self.acc_ui = AccVerify()
        self.acc_ui.verify_success.connect(self.user_login)

    def user_login(self, acc_name):
        """
        When login success, this func will be triggered.
        1. receive account name and set window title with it, also the using time
        2. change Ui to user login mode
        :param acc_name:
        :return: none
        """
        self.acc_name = acc_name
        window_title = '欢迎用户' + acc_name
        self.setWindowTitle(window_title)
        self.sleep_time.start_count()
        self.ui_alter.ui_user_logoff(False)

    def user_logout(self):
        """
        1. set Ui to user logoff mode
        2. change window title
        :return: none
        """
        self.ui_alter.ui_user_logoff()
        self.setWindowTitle('未登录-请登陆后使用添加删除功能')


if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    app.installEventFilter(myWin)
    myWin.show()
    sys.exit(app.exec_())

