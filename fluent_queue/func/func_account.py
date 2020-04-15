import sys
import cgitb
import csv

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import pyqtSignal, Qt

from ui_py.ui_login import Ui_Frame_account


class AccVerify(QWidget, Ui_Frame_account):
    """
    SubUi object to verify account
    """
    verify_success = pyqtSignal(str)

    def __init__(self, parent=None):
        super(AccVerify, self).__init__(parent)
        self.setupUi(self)
        self.btn()
        self.show()                                 # show window

    def btn(self):
        self.btn_login.clicked.connect(self.verify)

    def verify(self):
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
                self.label_tip.setText('密码错误')
        else:
            self.label_tip.setText('账号错误')

    def account_info(self):
        """
        1. open account database, csv file
        2. read it as a dict
        :return: account dict
        """
        account_csv_path = r'S:\PE\Engineering database\CFD\01_Standard\.account.csv'
        with open(account_csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)                # read csv by Dict method, it will using csv header
            account = dict()
            for row in reader:
                account[row['Account']] = row['Password']   # relate account name and password to account dict

        return account

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
    myWin = AccVerify()
    myWin.show()
    sys.exit(app.exec_())

