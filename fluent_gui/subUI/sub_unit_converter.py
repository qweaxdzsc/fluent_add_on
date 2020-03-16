from ui_py.ui_unit_convertor import Ui_unit_converter
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal


class subUI_unit_converter(Ui_unit_converter, QWidget):
    unit_convert_result = pyqtSignal(str)

    def __init__(self):
        super(subUI_unit_converter, self).__init__()
        self.setupUi(self)
        self.unit_btn()
        self.default_state()

    def default_state(self):
        self.l_btn.click()
        self.s_btn.click()

    def unit_btn(self):
        self.kg_btn.clicked.connect(lambda: self.volume_label_show('Kg', 1))
        self.m3_btn.clicked.connect(lambda: self.volume_label_show('M3', 1.225))
        self.l_btn.clicked.connect(lambda: self.volume_label_show('L', 0.001225))

        self.h_btn.clicked.connect(lambda: self.time_label_show('H', 3600))
        self.min_btn.clicked.connect(lambda: self.time_label_show('Min', 60))
        self.s_btn.clicked.connect(lambda: self.time_label_show('S', 1))

        self.confirm_btn.clicked.connect(self.calculate)

    def volume_label_show(self, text, factor):
        self.volume_label.setText(text)
        self.volume_factor = factor

    def time_label_show(self, text, factor):
        self.time_label.setText(text)
        self.time_factor = factor

    def calculate(self):
        if self.value_edit.text() == '':
            value = 0
        else:
            value = float(self.value_edit.text())
        result = round(value*self.volume_factor/self.time_factor, 5)
        self.unit_convert_result.emit(str(result))
