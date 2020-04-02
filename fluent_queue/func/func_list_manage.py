import sys
import cgitb
import csv

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtCore import pyqtSignal, QFileInfo
from PyQt5.QtGui import QIcon, QPixmap

from ui_py.ui_add_project import Ui_Widget_add


class AddPj(QWidget, Ui_Widget_add):
    def __init__(self, parent=None):
        super(AddPj, self).__init__(parent)
        self.setupUi(self)
        self.btn()
        self.show_ui()
        self.set_all_icon()

    def btn(self):
        self.btn_extend.clicked.connect(self.show_ui)
        self.btn_project_address.clicked.connect(self.open_pj_file)
        self.checkbox_journal.clicked.connect(self.use_journal)
        self.btn_journal_address.clicked.connect(self.open_jou_file)

    def show_ui(self):
        if self.btn_extend.isChecked():
            self.resize(510, 200)
            self.label_journal_address.hide()
            self.edit_journal_address.hide()
            self.btn_journal_address.hide()
            self.frame_advanced.show()
        else:
            # self.adjustSize()
            self.resize(510, 80)
            self.frame_advanced.hide()

    def _set_icon(self, pict, action):
        icon = QIcon()
        icon.addPixmap(QPixmap("../icon/%s" % (pict)), QIcon.Normal, QIcon.Off)
        action.setIcon(icon)

    def set_all_icon(self):
        self._set_icon('openfile.png', self.btn_project_address)
        self._set_icon('openfile.png', self.btn_journal_address)
        self._set_icon('extend.png', self.btn_extend)

    def open_pj_file(self):
        path = QFileDialog.getOpenFileName(self, '选择要计算文件',
                                           r'C:\Users\BZMBN4\Desktop',
                                           'ALL(*.*);;Fluent Case(*.cas);;Fluent Mesh(*.msh)',
                                           'Fluent Case(*.cas)')
        case_path = QFileInfo(path[0])
        if case_path.exists():
            file_name = case_path.fileName()
            project_address = case_path.absolutePath()
            self.edit_project_address.setText(path[0])
        else:
            print('file not exists')

    def use_journal(self):
        if self.checkbox_journal.isChecked():
            self.label_journal_address.show()
            self.edit_journal_address.show()
            self.btn_journal_address.show()
        else:
            self.label_journal_address.hide()
            self.edit_journal_address.hide()
            self.btn_journal_address.hide()

    def open_jou_file(self):
        path = QFileDialog.getOpenFileName(self, '选择要journal文件',
                                           r'C:\Users\BZMBN4\Desktop',
                                           'Fluent journal(*.jou)')
        jou_path = QFileInfo(path[0])
        if jou_path.exists():
            self.edit_journal_address.setText(path[0])
        else:
            print('file not exists')







if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myWin = AddPj()
    myWin.show()
    sys.exit(app.exec_())