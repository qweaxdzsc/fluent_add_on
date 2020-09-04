from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
import sys


class TrayIcon(QSystemTrayIcon):
    signal_show_main = pyqtSignal()
    signal_exit_main = pyqtSignal(bool)

    def __init__(self, msg_translator):
        super().__init__()
        self.setIcon(QIcon(r"./icon/shrink.png"))
        self.msg_translator = msg_translator
        self.make_trans = self.msg_translator.make_trans
        self._createMenu()
        self._btn()
        self.show()

    def _createMenu(self):
        self.tray_menu = QMenu()
        self.action_maximize = QAction(self.make_trans('show_main'), self)
        self.action_exit = QAction(self.make_trans('exit_main'), self)

        self.tray_menu.addAction(self.action_maximize)
        self.tray_menu.addAction(self.action_exit)
        self.setContextMenu(self.tray_menu)

    def _btn(self):
        self.activated.connect(self.onIconClicked)
        self.action_maximize.triggered.connect(self.show_main)
        self.action_exit.triggered.connect(self.application_exit)

    def show_main(self):
        self.signal_show_main.emit()

    def application_exit(self):
        self.signal_exit_main.emit(True)
        # app = QApplication(sys.argv)
        # sys.exit(app.exec_())

    # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
    def onIconClicked(self, reason):
        if reason == 2:
            self.show_main()

