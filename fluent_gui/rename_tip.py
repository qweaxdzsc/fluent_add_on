# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rename_tip.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_tip_widget(object):
    def setupUi(self, tip_widget):
        tip_widget.setObjectName("tip_widget")
        tip_widget.resize(432, 134)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(tip_widget.sizePolicy().hasHeightForWidth())
        tip_widget.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(tip_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.rename_table = QtWidgets.QTableWidget(tip_widget)
        self.rename_table.setMinimumSize(QtCore.QSize(410, 75))
        self.rename_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.rename_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rename_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rename_table.setRowCount(0)
        self.rename_table.setColumnCount(3)
        self.rename_table.setObjectName("rename_table")
        item = QtWidgets.QTableWidgetItem()
        self.rename_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.rename_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.rename_table.setHorizontalHeaderItem(2, item)
        self.rename_table.horizontalHeader().setCascadingSectionResizes(False)
        self.rename_table.horizontalHeader().setSortIndicatorShown(False)
        self.rename_table.horizontalHeader().setStretchLastSection(True)
        self.rename_table.verticalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.rename_table)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(304, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.rename_btn = QtWidgets.QPushButton(tip_widget)
        self.rename_btn.setObjectName("rename_btn")
        self.horizontalLayout.addWidget(self.rename_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(tip_widget)
        QtCore.QMetaObject.connectSlotsByName(tip_widget)

    def retranslateUi(self, tip_widget):
        _translate = QtCore.QCoreApplication.translate
        tip_widget.setWindowTitle(_translate("tip_widget", "进出口命名及阻力设置"))
        item = self.rename_table.horizontalHeaderItem(0)
        item.setText(_translate("tip_widget", "进口名称"))
        item = self.rename_table.horizontalHeaderItem(1)
        item.setText(_translate("tip_widget", "出口名称"))
        item = self.rename_table.horizontalHeaderItem(2)
        item.setText(_translate("tip_widget", "出口K值"))
        self.rename_btn.setText(_translate("tip_widget", "确  认"))
