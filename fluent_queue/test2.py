# coding = 'utf-8'
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from test import Ui_MainWindow


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, MainWindow, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.ui = MainWindow
        self.createMenu()

    def createMenu(self):
        self.menu = QtWidgets.QMenu()
        self.showAction1 = QtWidgets.QAction("启动", self, triggered=self.show_window)
        self.quitAction = QtWidgets.QAction("退出", self, triggered=self.quit)

        self.menu.addAction(self.showAction1)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)

        # 设置图标
        self.setIcon(QtGui.QIcon(r".\icon\help.png"))
        # self.icon = self.MessageIcon()

        # 把鼠标点击图标的信号和槽连接
        self.activated.connect(self.onIconClicked)

    def show_window(self):
        # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
        self.ui.showNormal()
        self.ui.activateWindow()

    def quit(self):
        QtWidgets.qApp.quit()

    # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
    def onIconClicked(self, reason):
        if reason == 2:
            # self.showMessage("Message", "skr at here", self.icon)
            if self.ui.isMinimized() or not self.ui.isVisible():
                # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
                self.ui.showNormal()
                self.ui.activateWindow()
                self.ui.setWindowFlags(QtCore.Qt.Window)
                self.ui.show()
            else:
                # 若不是最小化，则最小化
                self.ui.showMinimized()
                self.ui.setWindowFlags(QtCore.Qt.SplashScreen)
                self.ui.show()
                # self.ui.show()


class Dialog(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.Window)

    def closeEvent(self, event):
        event.ignore()
        # 最小化到托盘
        self.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint)
        self.showMinimized()
        self.ti = TrayIcon(self)
        self.ti.show()


if __name__ == '__main__':
    # 创建一个应用对象
    app = QtWidgets.QApplication(sys.argv)
    # 创建UI对象
    MainWindow = Dialog()
    MainWindow.show()

    # 结束程序
    sys.exit(app.exec_())