# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_login.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame_account(object):
    def setupUi(self, Frame_account):
        Frame_account.setObjectName("Frame_account")
        Frame_account.resize(200, 130)
        Frame_account.setMinimumSize(QtCore.QSize(200, 130))
        Frame_account.setMaximumSize(QtCore.QSize(240, 150))
        self.gridLayout = QtWidgets.QGridLayout(Frame_account)
        self.gridLayout.setContentsMargins(15, 15, 15, 15)
        self.gridLayout.setSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.edit_account = QtWidgets.QLineEdit(Frame_account)
        self.edit_account.setMinimumSize(QtCore.QSize(100, 25))
        self.edit_account.setMaximumSize(QtCore.QSize(100, 25))
        self.edit_account.setObjectName("edit_account")
        self.gridLayout.addWidget(self.edit_account, 0, 1, 1, 1)
        self.edit_password = QtWidgets.QLineEdit(Frame_account)
        self.edit_password.setMinimumSize(QtCore.QSize(100, 25))
        self.edit_password.setMaximumSize(QtCore.QSize(100, 25))
        self.edit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.edit_password.setObjectName("edit_password")
        self.gridLayout.addWidget(self.edit_password, 1, 1, 1, 1)
        self.label_account = QtWidgets.QLabel(Frame_account)
        self.label_account.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_account.setObjectName("label_account")
        self.gridLayout.addWidget(self.label_account, 0, 0, 1, 1)
        self.btn_login = QtWidgets.QPushButton(Frame_account)
        self.btn_login.setMinimumSize(QtCore.QSize(0, 28))
        self.btn_login.setMaximumSize(QtCore.QSize(120, 16777215))
        self.btn_login.setObjectName("btn_login")
        self.gridLayout.addWidget(self.btn_login, 2, 1, 1, 1)
        self.label_password = QtWidgets.QLabel(Frame_account)
        self.label_password.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_password.setObjectName("label_password")
        self.gridLayout.addWidget(self.label_password, 1, 0, 1, 1)
        self.label_tip = QtWidgets.QLabel(Frame_account)
        self.label_tip.setText("")
        self.label_tip.setObjectName("label_tip")
        self.gridLayout.addWidget(self.label_tip, 2, 0, 1, 1)

        self.retranslateUi(Frame_account)
        QtCore.QMetaObject.connectSlotsByName(Frame_account)

    def retranslateUi(self, Frame_account):
        _translate = QtCore.QCoreApplication.translate
        Frame_account.setWindowTitle(_translate("Frame_account", "登陆"))
        self.label_account.setText(_translate("Frame_account", "账号"))
        self.btn_login.setText(_translate("Frame_account", "登  陆"))
        self.label_password.setText(_translate("Frame_account", "密码"))
