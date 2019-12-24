from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QSpinBox, \
    QTableWidgetItem
from ui_input import Ui_MainWindow
from porous_model import Ui_porous
import cgitb
import sys
import csv


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.signal_slot()

    def signal_slot(self):
        self.mode_slider.valueChanged.connect(self.mode_choose)
        self.valve_slider.valueChanged.connect(self.valve_number)

    def mode_choose(self):
        value = self.mode_slider.value()
        mode_dict = {
            2: ['foot_label', 'foot_spinbox'],
            3: ['bil_label', 'bil_spinbox'],
            4: ['defrost_label', 'defrost_spinbox'],
            5: ['defog_label', 'defog_spinbox'],
            6: ['trl_label', 'trl_spinbox'],
            7: ['hil_label', 'hil_spinbox']
                     }
        for key in mode_dict.keys():
            label = self.RPM_tab.findChild(QLabel, mode_dict[key][0])
            spinbox = self.RPM_tab.findChild(QSpinBox, mode_dict[key][1])
            if key > value:
                label.setDisabled(True)
                spinbox.setDisabled(True)
            else:
                label.setEnabled(True)
                spinbox.setEnabled(True)

    def valve_number(self):
        value = self.valve_slider.value()
        self.valve_table.setRowCount(value)
        for i in range(value):
            table_item = QTableWidgetItem('温度风门%s' % (i+1))
            self.valve_table.setItem(i, 0, table_item)

    def porous_choose(self, btn_name):
        self.porous_model = Ui_porous()
        self.porous_model.show()
        self.porous_model.load_btn.clicked.connect(lambda: self.porous_import(btn_name))


if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())


