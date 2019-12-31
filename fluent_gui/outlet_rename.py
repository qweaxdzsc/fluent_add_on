from PyQt5.QtCore import QStringListModel
from outlet import Ui_outlet_form
from PyQt5.QtWidgets import QWidget, QApplication
import sys


class ui_outlet_rename(QWidget, Ui_outlet_form):
    def __init__(self, parent=None):
        super(ui_outlet_rename, self).__init__(parent)
        self.setupUi(self)
        self.init_set()
        self.item_check()

    def init_set(self):
        self.outlet_tree.expandAll()
        self.outlet_list = []
        self.list_model = QStringListModel()
        self.chosed_btn.clicked.connect(self.close)

    def item_check(self):
        self.outlet_tree.itemChanged['QTreeWidgetItem*', 'int'].connect(self.list_add)

    def list_add(self, item):
        if item.checkState(0) == 0:
            self.outlet_list.remove(item.text(0))
            self.list_model.setStringList(self.outlet_list)
            self.chosed_list.setModel(self.list_model)
        else:
            self.outlet_list.append(item.text(0))
            self.list_model.setStringList(self.outlet_list)
            self.chosed_list.setModel(self.list_model)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = ui_outlet_rename()
    myWin.show()
    sys.exit(app.exec_())