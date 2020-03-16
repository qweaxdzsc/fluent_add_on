from ui_py.ui_k_cal import Ui_K_calculator
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal


class subUI_cal_K(Ui_K_calculator, QWidget):
    K_result = pyqtSignal(str)

    def __init__(self):
        super(Ui_K_calculator, self).__init__()
        self.setupUi(self)
        self.cal_method()
        self.QP_btn.click()

    def initialize(self):
        self.R_frame.hide()
        self.QP_frame.hide()

    def cal_method(self):
        self.R_btn.clicked.connect(lambda: self.choosen_method(self.R_frame, self.R_method))
        self.QP_btn.clicked.connect(lambda: self.choosen_method(self.QP_frame, self.QP_method))

    def choosen_method(self, show_frame, method):
        self.initialize()
        show_frame.show()
        self.K_cal_btn.disconnect()
        self.K_cal_btn.clicked.connect(method)

    def QP_method(self):
        ls = float(self.volume_edit.text())
        mm2 = float(self.area_edit.text())
        p = float(self.pressure_edit.text())
        rho = 1.225

        m3s = ls / 1000
        m2 = mm2/1000/1000
        v = m3s/m2

        K = 2*p/rho/v**2
        self.K_result.emit("%.3f" % K)

    def R_method(self):
        r = float(self.R_edit.text())
        mm2 = float(self.area_edit.text())
        rho = 1.225
        m2 = mm2 / 1000 / 1000
        K = 1000*2*r*m2**2/rho
        self.K_result.emit("%.3f" % K)