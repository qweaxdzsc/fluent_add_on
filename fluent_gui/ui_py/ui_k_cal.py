# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'K_cal.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_K_calculator(object):
    def setupUi(self, K_calculator):
        K_calculator.setObjectName("K_calculator")
        K_calculator.resize(476, 265)
        self.gridLayout_2 = QtWidgets.QGridLayout(K_calculator)
        self.gridLayout_2.setContentsMargins(20, 20, 20, 20)
        self.gridLayout_2.setHorizontalSpacing(10)
        self.gridLayout_2.setVerticalSpacing(15)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.method_box = QtWidgets.QGroupBox(K_calculator)
        self.method_box.setObjectName("method_box")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.method_box)
        self.verticalLayout.setObjectName("verticalLayout")
        self.R_btn = QtWidgets.QRadioButton(self.method_box)
        self.R_btn.setObjectName("R_btn")
        self.verticalLayout.addWidget(self.R_btn)
        self.QP_btn = QtWidgets.QRadioButton(self.method_box)
        self.QP_btn.setObjectName("QP_btn")
        self.verticalLayout.addWidget(self.QP_btn)
        self.gridLayout_2.addWidget(self.method_box, 0, 0, 1, 1)
        self.c_box = QtWidgets.QGroupBox(K_calculator)
        self.c_box.setObjectName("c_box")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.c_box)
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.area_label = QtWidgets.QLabel(self.c_box)
        self.area_label.setMinimumSize(QtCore.QSize(140, 0))
        self.area_label.setObjectName("area_label")
        self.horizontalLayout.addWidget(self.area_label)
        self.area_edit = QtWidgets.QLineEdit(self.c_box)
        self.area_edit.setMinimumSize(QtCore.QSize(100, 0))
        self.area_edit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.area_edit.setObjectName("area_edit")
        self.horizontalLayout.addWidget(self.area_edit)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.R_frame = QtWidgets.QFrame(self.c_box)
        self.R_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.R_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.R_frame.setObjectName("R_frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.R_frame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.R_label = QtWidgets.QLabel(self.R_frame)
        self.R_label.setMinimumSize(QtCore.QSize(140, 0))
        self.R_label.setObjectName("R_label")
        self.horizontalLayout_2.addWidget(self.R_label)
        self.R_edit = QtWidgets.QLineEdit(self.R_frame)
        self.R_edit.setMinimumSize(QtCore.QSize(100, 0))
        self.R_edit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.R_edit.setObjectName("R_edit")
        self.horizontalLayout_2.addWidget(self.R_edit)
        self.verticalLayout_2.addWidget(self.R_frame)
        self.QP_frame = QtWidgets.QFrame(self.c_box)
        self.QP_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.QP_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.QP_frame.setObjectName("QP_frame")
        self.gridLayout = QtWidgets.QGridLayout(self.QP_frame)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.taget_volume_label = QtWidgets.QLabel(self.QP_frame)
        self.taget_volume_label.setMinimumSize(QtCore.QSize(140, 0))
        self.taget_volume_label.setObjectName("taget_volume_label")
        self.gridLayout.addWidget(self.taget_volume_label, 0, 0, 1, 1)
        self.volume_edit = QtWidgets.QLineEdit(self.QP_frame)
        self.volume_edit.setMinimumSize(QtCore.QSize(100, 0))
        self.volume_edit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.volume_edit.setObjectName("volume_edit")
        self.gridLayout.addWidget(self.volume_edit, 0, 1, 1, 1)
        self.pressure_label = QtWidgets.QLabel(self.QP_frame)
        self.pressure_label.setMinimumSize(QtCore.QSize(140, 0))
        self.pressure_label.setObjectName("pressure_label")
        self.gridLayout.addWidget(self.pressure_label, 1, 0, 1, 1)
        self.pressure_edit = QtWidgets.QLineEdit(self.QP_frame)
        self.pressure_edit.setMinimumSize(QtCore.QSize(100, 0))
        self.pressure_edit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pressure_edit.setObjectName("pressure_edit")
        self.gridLayout.addWidget(self.pressure_edit, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.QP_frame)
        self.gridLayout_2.addWidget(self.c_box, 0, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(286, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 2)
        self.K_cal_btn = QtWidgets.QPushButton(K_calculator)
        self.K_cal_btn.setObjectName("K_cal_btn")
        self.gridLayout_2.addWidget(self.K_cal_btn, 1, 2, 1, 1)

        self.retranslateUi(K_calculator)
        QtCore.QMetaObject.connectSlotsByName(K_calculator)

    def retranslateUi(self, K_calculator):
        _translate = QtCore.QCoreApplication.translate
        K_calculator.setWindowTitle(_translate("K_calculator", "风道阻力K计算器"))
        self.method_box.setTitle(_translate("K_calculator", "计算方式"))
        self.R_btn.setText(_translate("K_calculator", "R值"))
        self.QP_btn.setText(_translate("K_calculator", "目标风量与压强"))
        self.c_box.setTitle(_translate("K_calculator", "计算参数"))
        self.area_label.setText(_translate("K_calculator", "出口截面积（mm2）"))
        self.R_label.setText(_translate("K_calculator", "R值"))
        self.taget_volume_label.setText(_translate("K_calculator", "目标风量 (L/S)"))
        self.pressure_label.setText(_translate("K_calculator", "压强 (Pa）"))
        self.K_cal_btn.setText(_translate("K_calculator", "确 认"))
