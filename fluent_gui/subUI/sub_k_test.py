from ui_py.ui_k_test import Ui_k_form
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QTreeWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import sys
import cgitb
import time


class subUI_outlet_assign(Ui_k_form, QWidget):
    outlet_K_signal = pyqtSignal(dict)

    def __init__(self, k_dict, R_method=True):
        super(Ui_k_form, self).__init__()
        self.setupUi(self)
        self.outlet_tree.expandAll()
        self.btn()
        if R_method:
            self.R_btn.click()
        else:
            self.R_btn.click()
            self.PQ_btn.click()
        self.outlet_list_create()
        self.k_dict = k_dict
        self.receive_outlet_info()
        self.auto_calculate()

    def btn(self):
        self.outlet_tree.itemChanged['QTreeWidgetItem*', 'int'].connect(self.check_change)
        self.R_btn.toggled.connect(self.cal_method_choose)

    def outlet_list_create(self):
        self.outlet_list = []
        self.vent_list = []
        self.foot_list = []
        self.defrost_list = []
        self.other_list = []
        self.mode_list_dict = {'vent': self.vent_list, 'foot': self.foot_list, 'defrost': self.defrost_list,
                               'other': self.other_list}

    def outlet_number(self):
        vent_number = len(self.vent_list)
        foot_number = len(self.foot_list)
        defrost_number = len(self.defrost_list)
        other_number = len(self.other_list)

        number_dict = {'vent': vent_number,
                       'foot': foot_number + vent_number,
                       'defrost': vent_number + foot_number + defrost_number,
                       'other': vent_number + foot_number + defrost_number + other_number
                       }
        return number_dict

    def auto_calculate(self):
        self.auto_cal_thread = Auto_cal(self)
        self.auto_cal_thread.start()
        self.auto_cal_thread.k_list_signal.connect(self.set_K)

    def check_change(self, item):
        father_node = ['vent', 'foot', 'defrost', 'other']
        if item.text(0) in father_node:
            self.check_child_influence(item)
        else:
            parent = item.parent()
            self.table_row_change(item, parent)
            self.outlet_list_change(item, parent)
            self.check_parent_influence(parent)

    def outlet_list_change(self, item, parent):
        if item.checkState(0) == 2:
            self.outlet_list.append(item.text(0))
            self.mode_list_dict[parent.text(0)].append(item.text(0))
        else:
            self.outlet_list.remove(item.text(0))
            self.mode_list_dict[parent.text(0)].remove(item.text(0))

    def table_row_change(self, item, parent):
        number_dict = self.outlet_number()
        if item.checkState(0) == 2:
            self.k_table.insertRow(number_dict[parent.text(0)])
            new_item = QTableWidgetItem(item.text(0))
            self.k_table.setItem(number_dict[parent.text(0)], 0, new_item)
            for i in range(1, 5):
                new_item = QTableWidgetItem('0.0001')
                self.k_table.setItem(number_dict[parent.text(0)], i, new_item)
        else:
            row_number = number_dict[parent.text(0)] - len(self.mode_list_dict[parent.text(0)]) + \
                self.mode_list_dict[parent.text(0)].index(item.text(0))
            self.k_table.removeRow(row_number)

    def check_child_influence(self, item):
        if item.checkState(0) == 1:
            pass
        else:
            for i in range(item.childCount()):
                item.child(i).setCheckState(0, item.checkState(0))

    def check_parent_influence(self, parent):
        child_number = parent.childCount()
        allcheck_indicator = 0
        for i in range(child_number):
            allcheck_indicator += parent.child(i).checkState(0)
        if allcheck_indicator == 0:
            parent.setCheckState(0, 0)
        elif allcheck_indicator == 2 * child_number:
            parent.setCheckState(0, 2)

    def cal_method_choose(self):
        if self.R_btn.isChecked():
            self.k_table.hideColumn(3)
            self.k_table.hideColumn(4)
            self.k_table.showColumn(2)
        else:
            self.k_table.hideColumn(2)
            self.k_table.showColumn(3)
            self.k_table.showColumn(4)

    def set_K(self, k_list):
        self.k_list = k_list
        if k_list:
            for i in range(len(k_list)):
                new_item = QTableWidgetItem(str(k_list[i]))
                new_item.setFlags(Qt.ItemIsEditable)
                self.k_table.setItem(i, 5, new_item)

    def receive_outlet_info(self):
        # self.outlet_list = list(self.k_dict.keys())
        # self.outlet_K = list(self.k_dict.values())
        for i in self.k_dict.keys():
            item = self.outlet_tree.findItems(i, Qt.MatchExactly | Qt.MatchRecursive)

            if item:
                item[0].setCheckState(0, 2)
                number_dict = self.outlet_number()
                for j in self.k_dict[i]:
                    new_item = QTableWidgetItem(j)
                    self.k_table.setItem(number_dict[item[0].parent().text(0)]-1, self.k_dict[i].index(j)+1, new_item)
                # self.k_table.item(number_dict[item[0].parent().text(0)]-1, 5).setText(self.k_dict[i])
            else:
                other_node = self.outlet_tree.topLevelItem(3)
                other_outlet = QTreeWidgetItem(other_node)
                other_outlet.setText(0, i)
                other_outlet.setCheckState(0, 2)
                number_dict = self.outlet_number()
                for j in self.k_dict[i]:
                    new_item = QTableWidgetItem(j)
                    self.k_table.setItem(number_dict[other_node.text(0)]-1, self.k_dict[i].index(j)+1, new_item)

    def closeEvent(self, event):
        outlet_k_dict = dict()
        for row in range(self.k_table.rowCount()):
            value = [0, 0, 0, 0, 0]
            for i in range(len(value)):
                value[i] = self.k_table.item(row, i+1).text()
            value = tuple(value)
            outlet_name = self.k_table.item(row, 0).text()
            outlet_k_dict[outlet_name] = value
        self.outlet_K_signal.emit(outlet_k_dict)


class Auto_cal(QThread):
    k_list_signal = pyqtSignal(list)

    def __init__(self, main_content, parent=None):
        super(Auto_cal, self).__init__(parent)
        self.main = main_content

    def run(self):
        while True:
            if self.main.R_btn.isChecked():
                self.R_method()
            else:
                self.QP_method()

            self.k_list_signal.emit(self.K)
            time.sleep(0.2)

    def QP_method(self):
        k_table = self.main.k_table
        row_count = k_table.rowCount()
        K = [0 for i in range(row_count)]

        for i in range(row_count):
            try:
                ls = float(k_table.item(i, 4).text())
                mm2 = float(k_table.item(i, 1).text())
                p = float(k_table.item(i, 3).text())
            except Exception as e:
                pass
            else:
                rho = 1.225
                m3s = ls / 1000
                m2 = mm2/1000/1000
                v = m3s/m2

                K[i] = round(2*p/rho/v**2, 4)

        self.K = K

    def R_method(self):
        k_table = self.main.k_table
        row_count = k_table.rowCount()
        K = [0 for i in range(row_count)]

        for i in range(row_count):
            try:
                r = float(k_table.item(i, 2).text())
                mm2 = float(k_table.item(i, 1).text())
            except Exception as e:
                pass
            else:
                rho = 1.225
                m2 = mm2 / 1000 / 1000
                K[i] = round(1000*2*r*m2**2/rho, 4)

        self.K = K


if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    init_k_dict = {'outlet_test2': ['0.0001', '0.0001', '0.0001', '0.0001']}
    myWin = subUI_outlet_assign(init_k_dict, R_method=False)
    myWin.show()
    sys.exit(app.exec_())

