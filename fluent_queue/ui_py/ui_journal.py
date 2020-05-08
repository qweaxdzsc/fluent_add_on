# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_journal.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widget_journal(object):
    def setupUi(self, widget_journal):
        widget_journal.setObjectName("widget_journal")
        widget_journal.resize(1400, 600)
        self.horizontalLayout = QtWidgets.QHBoxLayout(widget_journal)
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.table_journal = QtWidgets.QTableWidget(widget_journal)
        self.table_journal.setObjectName("table_journal")
        self.table_journal.setColumnCount(0)
        self.table_journal.setRowCount(0)
        self.horizontalLayout.addWidget(self.table_journal)

        self.retranslateUi(widget_journal)
        QtCore.QMetaObject.connectSlotsByName(widget_journal)

    def retranslateUi(self, widget_journal):
        _translate = QtCore.QCoreApplication.translate
        widget_journal.setWindowTitle(_translate("widget_journal", "已完成项目信息"))
