from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from ui_py.ui_cores import Ui_widget_cores


class ChangeCore(QWidget, Ui_widget_cores):
    signal_change_core = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.btn()

    def btn(self):
        self.btn_confirm.clicked.connect(self.confirm_change)

    def confirm_change(self):
        core = int(self.edit_cores.text())
        self.signal_change_core.emit(core)
        self.close()