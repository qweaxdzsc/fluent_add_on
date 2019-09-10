from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.openfile()

    def openfile(self):

        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', 'C:/Users/BZMBN4/Desktop/', '*.xlsx ; *.xls')
        print(openfile_name)
        path_openfile_name = openfile_name[0]
        print(path_openfile_name)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())