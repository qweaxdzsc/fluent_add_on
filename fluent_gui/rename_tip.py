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
        tip_widget.resize(292, 135)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(tip_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_tip = QtWidgets.QLabel(tip_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_tip.sizePolicy().hasHeightForWidth())
        self.label_tip.setSizePolicy(sizePolicy)
        self.label_tip.setMinimumSize(QtCore.QSize(200, 0))
        self.label_tip.setAlignment(QtCore.Qt.AlignCenter)
        self.label_tip.setObjectName("label_tip")
        self.verticalLayout_2.addWidget(self.label_tip)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(75, -1, 75, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.exit_btn = QtWidgets.QPushButton(tip_widget)
        self.exit_btn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.exit_btn.setObjectName("exit_btn")
        self.horizontalLayout.addWidget(self.exit_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(tip_widget)
        self.exit_btn.clicked.connect(tip_widget.close)
        QtCore.QMetaObject.connectSlotsByName(tip_widget)

    def retranslateUi(self, tip_widget):
        _translate = QtCore.QCoreApplication.translate
        tip_widget.setWindowTitle(_translate("tip_widget", "提示"))
        self.label_tip.setText(_translate("tip_widget", "TextLabel"))
        self.exit_btn.setText(_translate("tip_widget", "确认"))
