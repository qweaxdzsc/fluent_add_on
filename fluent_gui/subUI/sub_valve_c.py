from ui_py.ui_valve import Ui_valve_form
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal, QSize
import sys
import cgitb


class subUI_valve(Ui_valve_form, QWidget):
    signal_valve_dict = pyqtSignal(dict)

    def __init__(self, valve_dict, valve_number):
        super().__init__()
        self.setupUi(self)
        self.valve_dict = valve_dict
        self.valve_number = valve_number
        self.create_input_widget()
        self.fill_parameter()

    def create_input_widget(self):
        for i in range(self.valve_number):
            self.valve_td_label = QLabel(self.valve_c)
            self.valve_td_label.setMinimumSize(QSize(80, 0))
            self.valve_td_label.setMaximumSize(QSize(80, 16777215))
            self.valve_td_label.setObjectName("valve%s_td_label" % (i + 1))
            self.valve_td_label.setText('风门%s行程' % (i + 1))
            self.gridLayout_4.addWidget(self.valve_td_label, i + 1, 0, 1, 1)
            self.valve_td_edit = QLineEdit(self.valve_c)
            self.valve_td_edit.setMinimumSize(QSize(100, 22))
            self.valve_td_edit.setMaximumSize(QSize(100, 22))
            self.valve_td_edit.setObjectName("valve%s_td_edit" % (i + 1))
            self.gridLayout_4.addWidget(self.valve_td_edit, i + 1, 1, 1, 1)

    def fill_parameter(self):
        for key, value in self.valve_dict.items():
            line_edit_name = key + '_edit'
            line_edit = self.valve_c.findChild(QLineEdit, line_edit_name)
            if line_edit:
                line_edit.setText(value)

    def closeEvent(self, event):
        self.valve_dict = {}
        self.valve_dict['valve_rp'] = self.valve_rp_edit.text()
        for i in range(self.valve_number):
            key_name = 'valve%s_td' % (i + 1)
            line_edit_name = key_name + '_edit'
            line_edit = self.valve_c.findChild(QLineEdit, line_edit_name)
            if line_edit.text():
                self.valve_dict[key_name] = line_edit.text()
            else:
                self.valve_dict[key_name] = '0'
        self.signal_valve_dict.emit(self.valve_dict)
        print('valve_dict is:', self.valve_dict)


if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    valve_dict = {'valve_rp': '10', 'valve1_td': '20', 'valve2_td': '30', 'valve3_td': '40'}
    valve_number = 4
    myWin = subUI_valve(valve_dict, valve_number)
    myWin.show()
    sys.exit(app.exec_())
