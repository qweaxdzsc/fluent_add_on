# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMessageBox
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt

from nameselection import Ui_Form
from rename_tip import Ui_tip_widget


class MyMainWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.btn()

    def btn(self):
        self.finish_btn.clicked.connect(self.check_part)
        self.quick_distribfc_btn.toggled.connect(self.quick_distrib_judge)
        self.quick_distribfh_btn.toggled.connect(self.quick_distrib_judge)
        self.finish_btn.clicked.connect(self.show_msg)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_F1:
            self.name_rule()

        if e.key() == Qt.Key_1:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.quick_distribfc_btn.setChecked(True)
                self.quick_distrib_judge()
                self.finish_btn.click()

        if e.key() == Qt.Key_2:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.quick_distribfh_btn.setChecked(True)
                self.quick_distrib_judge()
                self.finish_btn.click()

        if e.key() == Qt.Key_Q:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                print('quick')

    def name_rule(self):
        reply = QMessageBox.about(self, '帮助——命名规则', '命名分为体与面的命名：\n'
                                                    '请选择存在的体部件或使用快捷模板（ctrl+英文首字母），并点击导入模板\n\n'
                                                    '完成后：\n'
                                                    '1.对于面：选择面，并在space claim group栏下对相应的名字使用右键-replace\n'
                                                    '2.对于体：请复制弹出窗口中 体名字 至space claim模型树中 指定体')

    def quick_distrib_judge(self):
        if self.quick_distribfc_btn.isChecked() == True:
            self.part_tree.topLevelItem(0).setCheckState(0, QtCore.Qt.Unchecked)
            self.part_tree.topLevelItem(1).setCheckState(0, QtCore.Qt.Checked)
            self.part_tree.topLevelItem(2).setCheckState(0, QtCore.Qt.Unchecked)
            self.part_tree.topLevelItem(3).setCheckState(0, QtCore.Qt.Unchecked)
            self.part_tree.topLevelItem(4).setCheckState(0, QtCore.Qt.Unchecked)
            self.part_tree.topLevelItem(5).setCheckState(0, QtCore.Qt.Unchecked)
            self.part_tree.topLevelItem(6).setCheckState(0, QtCore.Qt.Unchecked)
            self.part_tree.topLevelItem(7).setCheckState(0, QtCore.Qt.Checked)
            self.part_tree.topLevelItem(8).setCheckState(0, QtCore.Qt.Checked)
            self.part_tree.topLevelItem(9).setCheckState(0, QtCore.Qt.Unchecked)
        if self.quick_distribfh_btn.isChecked() == True:
            self.part_tree.topLevelItem(0).setCheckState(0, QtCore.Qt.Unchecked)
            self.part_tree.topLevelItem(1).setCheckState(0, QtCore.Qt.Checked)
            self.part_tree.topLevelItem(2).setCheckState(0, QtCore.Qt.Unchecked)
            self.part_tree.topLevelItem(3).setCheckState(0, QtCore.Qt.Unchecked)
            self.part_tree.topLevelItem(4).setCheckState(0, QtCore.Qt.Unchecked)
            self.part_tree.topLevelItem(5).setCheckState(0, QtCore.Qt.Unchecked)
            self.part_tree.topLevelItem(6).setCheckState(0, QtCore.Qt.Unchecked)
            self.part_tree.topLevelItem(7).setCheckState(0, QtCore.Qt.Checked)
            self.part_tree.topLevelItem(8).setCheckState(0, QtCore.Qt.Checked)
            self.part_tree.topLevelItem(9).setCheckState(0, QtCore.Qt.Checked)

    def check_part(self):
        body_list = []
        face_list = ['inlet']
        if self.inlet_number.value() > 1:
            for i in range(self.inlet_number.value()-1):
                face_list.append('inlet%s'%(i+2))
        if self.part_tree.topLevelItem(0).checkState(0) == QtCore.Qt.Checked:
            body_list.append('inlet_sphere')
        if self.part_tree.topLevelItem(1).checkState(0) == QtCore.Qt.Checked:
            body_list.append('ai')
            if self.part_tree.topLevelItem(0).checkState(0) == QtCore.Qt.Checked:
                face_list.append('ai_in')
        if self.part_tree.topLevelItem(2).checkState(0) == QtCore.Qt.Checked:
            if self.part_tree.topLevelItem(3).checkState(0) == QtCore.Qt.Unchecked:
                print('filter and cone should be all checked')
            else:
                body_list.append('filter')
                body_list.append('cone')
                face_list.append('filter_in')
                face_list.append('filter_out')
        if self.part_tree.topLevelItem(4).checkState(0) == QtCore.Qt.Checked:
            if self.part_tree.topLevelItem(5).checkState(0) == QtCore.Qt.Unchecked:
                print('volute and fan should be all checked')
            else:
                body_list.append('volute')
                body_list.append('fan')
                if self.part_tree.topLevelItem(0).checkState(0) == QtCore.Qt.Checked:
                    face_list.append('fan_in')
                face_list.append('fan_out')
                face_list.append('fan_blade')
        if self.part_tree.topLevelItem(6).checkState(0) == QtCore.Qt.Checked:
            body_list.append('diffuser')
            if self.part_tree.topLevelItem(4).checkState(0) == QtCore.Qt.Checked:
                face_list.append('volute_out')
        if self.part_tree.topLevelItem(7).checkState(0) == QtCore.Qt.Checked:
            body_list.append('evap')
            face_list.append('evap_in')
            face_list.append('evap_out')
        if self.part_tree.topLevelItem(8).checkState(0) == QtCore.Qt.Checked:
            body_list.append('distrib')

        if self.part_tree.topLevelItem(9).checkState(0) == QtCore.Qt.Checked:
            body_list.append('hc')
            face_list.append('hc_in')
            face_list.append('hc_out')

        face_list.append('outlet')
        if self.outlet_number.value() > 1:
            for i in range(self.inlet_number.value()-1):
                face_list.append('outlet%s'%(i+2))
        print('body_list:%s\nface_list:%s'%(body_list, face_list))
        self.face_list = face_list
        self.body_list = body_list

    def show_msg(self):
        self.dialog_tip = Ui_tip()
        self.msg()
        self.dialog_tip.show()

        # self.dialog_tip.exec_()

    def msg(self):
        self.dialog_tip.exit_btn.clicked.connect(self.close)
        # hor_resize = len(self.body_list)*50+210
        # self.dialog_tip.resize(hor_resize, 150)
        self.dialog_tip.label_tip.setText("面命名模板创建完成\n请复制以下体名字至模型树")

        for i in range(len(self.body_list)):
            self.dialog_tip.lineEdit = QtWidgets.QLineEdit(self.dialog_tip)
            self.dialog_tip.lineEdit.setObjectName("lineEdit%s" %(i+1))
            self.dialog_tip.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
            self.dialog_tip.lineEdit.setText(self.body_list[i])
            # line_size = len(self.body_list[i])*8+5
            # print(line_size)
            self.dialog_tip.lineEdit.setMinimumSize(100, 20)
            self.dialog_tip.lineEdit.setMaximumSize(QtCore.QSize(150, 25))
            self.dialog_tip.verticalLayout.addWidget(self.dialog_tip.lineEdit)

        # self.center(self.dialog_tip)

    def center(self, object):
        qr = object.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        object.move(qr.topLeft())


class Ui_tip(Ui_tip_widget, QWidget):
    def __init__(self):
        super(Ui_tip_widget, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywin = MyMainWindow()
    mywin.show()
    sys.exit(app.exec_())



