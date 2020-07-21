# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_cores.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widget_cores(object):
    def setupUi(self, widget_cores):
        widget_cores.setObjectName("widget_cores")
        widget_cores.resize(167, 85)
        widget_cores.setMaximumSize(QtCore.QSize(200, 100))
        self.gridLayout = QtWidgets.QGridLayout(widget_cores)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setHorizontalSpacing(15)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.label_cores = QtWidgets.QLabel(widget_cores)
        self.label_cores.setObjectName("label_cores")
        self.gridLayout.addWidget(self.label_cores, 0, 0, 1, 1)
        self.edit_cores = QtWidgets.QLineEdit(widget_cores)
        self.edit_cores.setMinimumSize(QtCore.QSize(0, 25))
        self.edit_cores.setMaximumSize(QtCore.QSize(80, 30))
        self.edit_cores.setObjectName("edit_cores")
        self.gridLayout.addWidget(self.edit_cores, 0, 1, 1, 1)
        self.btn_confirm = QtWidgets.QPushButton(widget_cores)
        self.btn_confirm.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_confirm.setMaximumSize(QtCore.QSize(80, 16777215))
        self.btn_confirm.setObjectName("btn_confirm")
        self.gridLayout.addWidget(self.btn_confirm, 1, 1, 1, 1)

        self.retranslateUi(widget_cores)
        QtCore.QMetaObject.connectSlotsByName(widget_cores)

    def retranslateUi(self, widget_cores):
        _translate = QtCore.QCoreApplication.translate
        widget_cores.setWindowTitle(_translate("widget_cores", "Form"))
        self.label_cores.setText(_translate("widget_cores", "使用核数"))
        self.btn_confirm.setText(_translate("widget_cores", "确   认"))
