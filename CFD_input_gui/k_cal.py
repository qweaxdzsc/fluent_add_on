from ui_k_cal2 import Ui_k_form
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem
import sys
import cgitb


class Ui_porous(Ui_k_form, QWidget):
    def __init__(self):
        super(Ui_k_form, self).__init__()
        self.setupUi(self)
        self.outlet_tree.expandAll()
        self.btn()
        self.R_btn.click()
        self.outlet_list_create()

    def btn(self):
        self.outlet_tree.itemChanged['QTreeWidgetItem*', 'int'].connect(self.check_change)
        self.R_btn.toggled.connect(self.cal_method_choose)

    def outlet_list_create(self):
        self.outlet_list = []
        self.vent_list = []
        self.foot_list = []
        self.defrost_list = []
        self.mode_list_dict = {'vent': self.vent_list, 'foot': self.foot_list, 'defrost': self.defrost_list}

    def check_change(self, item):
        father_node = ['vent', 'foot', 'defrost']
        if item.text(0) in father_node:
            self.check_child_influence(item)
        else:
            parent = item.parent()
            self.outlet_list_change(item, parent)
            self.table_row_change(item, parent)
            self.check_parent_influence(parent)

    def outlet_list_change(self, item, parent):
        if item.checkState(0) == 2:
            self.outlet_list.append(item.text(0))
            self.mode_list_dict[parent.text(0)].append(item.text(0))
        else:
            self.outlet_list.remove(item.text(0))
            self.mode_list_dict[parent.text(0)].remove(item.text(0))

    def table_row_change(self, item, parent):
        vent_number = len(self.vent_list)
        foot_number = len(self.foot_list)
        defrost_number = len(self.defrost_list)

        number_dict = {'vent': vent_number,
                       'foot': foot_number + vent_number,
                       'defrost': vent_number + foot_number + defrost_number
                       }
        print(number_dict)
        if item.checkState(0) == 2:
            self.k_table.insertRow(number_dict[parent.text(0)]-1)
            new_item = QTableWidgetItem(item.text(0))
            self.k_table.setVerticalHeaderItem(number_dict[parent.text(0)]-1, new_item)
        else:
            self.k_table.removeRow(number_dict[parent.text(0)])

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
            self.k_table.hideColumn(2)
            self.k_table.hideColumn(3)
            self.k_table.showColumn(1)
        else:
            self.k_table.hideColumn(1)
            self.k_table.showColumn(2)
            self.k_table.showColumn(3)


if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myWin = Ui_porous()
    myWin.show()
    sys.exit(app.exec_())

