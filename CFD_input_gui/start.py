from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QSlider, QLineEdit, QTableWidgetItem
)
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
        self.porous_db_init()
        self.porous_item_update()

    def signal_slot(self):
        self.mode_slider.valueChanged.connect(self.mode_choose)
        self.valve_slider.valueChanged.connect(self.valve_number)
        self.RPM_slider_signal()
        self.evap_combox.activated.connect(lambda: self.porous_choose(self.evap_combox.currentIndex(), 'evap'))
        self.hc_combox.activated.connect(lambda: self.porous_choose(self.hc_combox.currentIndex(), 'hc'))
        self.filter_combox.activated.connect(lambda: self.porous_choose(self.filter_combox.currentIndex(), 'filter'))
        self.outlet_btn.clicked.connect(self.outlet_ui_show)

    def RPM_slider_signal(self):
        modes = ['vent', 'foot', 'bil', 'defrost', 'defog', 'trl', 'hil']
        for i in modes:
            slider = self.RPM_tab.findChild(QSlider, i+'_slider')
            slider.valueChanged.connect(lambda: self.RPM_slider_value(self.sender()))

    def RPM_slider_value(self, slider):
        value = slider.value()*50 + 2500
        edit = self.RPM_tab.findChild(QLineEdit, slider.objectName()[:-7]+'_edit')
        edit.setText('%s' % value)

    def porous_db_init(self):
        self.porous_model = Ui_porous()
        self.porous_index_dict = {'evap': 0, 'hc': 0, 'filter': 0}
        self.porous_model.db_change.connect(self.porous_item_update)

    def porous_item_update(self):
        porous_dict = self.porous_model.db_dict
        self.evap_combox.clear()
        self.evap_combox.addItem('添加')
        self.evap_combox.addItems(porous_dict.keys())
        self.evap_combox.setCurrentIndex(self.porous_index_dict['evap'])
        self.evap_combox.addItem('无')
        self.hc_combox.clear()
        self.hc_combox.addItem('添加')
        self.hc_combox.addItems(porous_dict.keys())
        self.hc_combox.setCurrentIndex(self.porous_index_dict['hc'])
        self.hc_combox.addItem('无')
        self.filter_combox.clear()
        self.filter_combox.addItem('添加')
        self.filter_combox.addItems(porous_dict.keys())
        self.filter_combox.setCurrentIndex(self.porous_index_dict['filter'])
        self.filter_combox.addItem('无')

    def mode_choose(self):
        value = self.mode_slider.value()
        mode_dict = {
            2: ['foot_label', 'foot_slider', 'foot_edit'],
            3: ['bil_label', 'bil_slider', 'bil_edit'],
            4: ['defrost_label', 'defrost_slider', 'defrost_edit'],
            5: ['defog_label', 'defog_slider', 'defog_edit'],
            6: ['trl_label', 'trl_slider', 'trl_edit'],
            7: ['hil_label', 'hil_slider', 'hil_edit']
                     }
        for key in mode_dict.keys():
            label = self.RPM_tab.findChild(QLabel, mode_dict[key][0])
            slider = self.RPM_tab.findChild(QSlider, mode_dict[key][1])
            edit = self.RPM_tab.findChild(QLineEdit, mode_dict[key][2])
            if key > value:
                label.setDisabled(True)
                slider.setDisabled(True)
                edit.setDisabled(True)
            else:
                label.setEnabled(True)
                slider.setEnabled(True)
                edit.setEnabled(True)

    def porous_choose(self, i, porous_type):
        if i == self.evap_combox.count() - 1:
            pass
        elif i == 0:
            self.porous_model.show()
            self.porous_model.add_mode()
            self.porous_model.model_combox.setCurrentIndex(0)
        else:
            self.porous_model.show()
            self.porous_model.read_mode(i)
            self.porous_model.model_combox.setCurrentIndex(i)
            self.porous_index_dict[porous_type] = i

    def outlet_ui_show(self):
        pass



    def valve_number(self):
        value = self.valve_slider.value()
        self.valve_table.setRowCount(value)
        for i in range(value):
            table_item = QTableWidgetItem('温度风门%s' % (i+1))
            self.valve_table.setItem(i, 0, table_item)



if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())


