from ui_py.ui_outlet_assign import Ui_outlet_assign
from PyQt5.QtWidgets import QWidget, QApplication
import cgitb
import sys



class subUI_outlet_assign(Ui_outlet_assign, QWidget):
    def __init__(self):
        super(subUI_outlet_assign, self).__init__()
        self.setupUi(self)



if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myWin = subUI_outlet_assign(app)
    myWin.show()
    sys.exit(app.exec_())