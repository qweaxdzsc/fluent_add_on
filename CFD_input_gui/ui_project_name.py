# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_project_name.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_project_name_widget(object):
    def setupUi(self, project_name_widget):
        project_name_widget.setObjectName("project_name_widget")
        project_name_widget.resize(278, 94)
        self.gridLayout = QtWidgets.QGridLayout(project_name_widget)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setHorizontalSpacing(25)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(project_name_widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.project_name_edit = QtWidgets.QLineEdit(project_name_widget)
        self.project_name_edit.setMinimumSize(QtCore.QSize(100, 0))
        self.project_name_edit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.project_name_edit.setObjectName("project_name_edit")
        self.gridLayout.addWidget(self.project_name_edit, 1, 0, 1, 1)
        self.confirm_btn = QtWidgets.QPushButton(project_name_widget)
        self.confirm_btn.setMaximumSize(QtCore.QSize(80, 16777215))
        self.confirm_btn.setObjectName("confirm_btn")
        self.gridLayout.addWidget(self.confirm_btn, 1, 1, 1, 1)

        self.retranslateUi(project_name_widget)
        QtCore.QMetaObject.connectSlotsByName(project_name_widget)

    def retranslateUi(self, project_name_widget):
        _translate = QtCore.QCoreApplication.translate
        project_name_widget.setWindowTitle(_translate("project_name_widget", "请输入项目名称"))
        self.label.setText(_translate("project_name_widget", "项目名："))
        self.confirm_btn.setText(_translate("project_name_widget", "确   认"))
