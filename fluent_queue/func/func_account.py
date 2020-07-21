import sys
import cgitb
import csv
import os

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import pyqtSignal, Qt

from ui_py.ui_login import Ui_Widget_account


class AccVerify(QWidget, Ui_Widget_account):
    """
    SubUi object to verify account
    """
    verify_success = pyqtSignal(str)

    def __init__(self, account_file_path, msg_translator):
        super().__init__()
        self.setupUi(self)
        # ----------init variable--------------
        self.account_csv_path = account_file_path
        self.msg_trans = msg_translator
        self.make_trans = self.msg_trans.make_trans
        # ----------init
        self.btn()
        self.verify_path()
        self.show()                                 # show window

    def btn(self):
        self.btn_login.clicked.connect(self.verify_account)

    def verify_path(self):
        if not os.path.exists(self.account_csv_path):
            with open(self.account_csv_path, 'w', newline='') as csvfile:
                header = ['Account', 'Password']
                writer = csv.DictWriter(csvfile, fieldnames=header)
                writer.writeheader()

    def verify_account(self):
        """
        1. get account name and password from LineEdit
        2. get exist account dict from database, a csv file
        3. compare whether the account and password correct
        :return:
        """
        acc = self.edit_account.text()
        pwd = self.edit_password.text()
        account_dict = self.account_info()
        if acc in account_dict:
            if pwd == account_dict[acc]:
                self.verify_success.emit(acc)               # emit account name
                self.close()                                # close this window itself
            else:
                self.label_tip.setText(self.make_trans('pwd_error'))
        else:
            self.label_tip.setText(self.make_trans('acc_error'))

    def account_info(self):
        """
        1. open account database, csv file
        2. read it as a dict
        :return: account dict
        """
        with open(self.account_csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)                # read csv by Dict method, it will using csv header
            account_dict = dict()
            for row in reader:
                account_dict[row['Account']] = row['Password']   # relate account name and password to account dict

        return account_dict

    def keyPressEvent(self, e):
        """ Event from QT, can be rewrite
        if e.key() = Qt.Key_?,  ? represent short key
        """
        if e.key() == Qt.Key_Return:  # used for test
            # if QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.btn_login.click()


if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myWin = AccVerify('./account.csv')
    myWin.show()
    sys.exit(app.exec_())

