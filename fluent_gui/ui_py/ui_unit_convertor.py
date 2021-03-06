# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_unit_convertor.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_unit_converter(object):
    def setupUi(self, unit_converter):
        unit_converter.setObjectName("unit_converter")
        unit_converter.resize(445, 169)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(unit_converter.sizePolicy().hasHeightForWidth())
        unit_converter.setSizePolicy(sizePolicy)
        unit_converter.setMinimumSize(QtCore.QSize(230, 90))
        unit_converter.setMaximumSize(QtCore.QSize(1600, 1600))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(unit_converter)
        self.horizontalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.volume_group = QtWidgets.QGroupBox(unit_converter)
        self.volume_group.setObjectName("volume_group")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.volume_group)
        self.verticalLayout.setObjectName("verticalLayout")
        self.kg_btn = QtWidgets.QRadioButton(self.volume_group)
        self.kg_btn.setChecked(False)
        self.kg_btn.setObjectName("kg_btn")
        self.verticalLayout.addWidget(self.kg_btn)
        self.m3_btn = QtWidgets.QRadioButton(self.volume_group)
        self.m3_btn.setObjectName("m3_btn")
        self.verticalLayout.addWidget(self.m3_btn)
        self.l_btn = QtWidgets.QRadioButton(self.volume_group)
        self.l_btn.setChecked(True)
        self.l_btn.setObjectName("l_btn")
        self.verticalLayout.addWidget(self.l_btn)
        self.horizontalLayout_2.addWidget(self.volume_group)
        self.time_group = QtWidgets.QGroupBox(unit_converter)
        self.time_group.setObjectName("time_group")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.time_group)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.h_btn = QtWidgets.QRadioButton(self.time_group)
        self.h_btn.setObjectName("h_btn")
        self.verticalLayout_2.addWidget(self.h_btn)
        self.min_btn = QtWidgets.QRadioButton(self.time_group)
        self.min_btn.setObjectName("min_btn")
        self.verticalLayout_2.addWidget(self.min_btn)
        self.s_btn = QtWidgets.QRadioButton(self.time_group)
        self.s_btn.setChecked(True)
        self.s_btn.setObjectName("s_btn")
        self.verticalLayout_2.addWidget(self.s_btn)
        self.horizontalLayout_2.addWidget(self.time_group)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 20, -1, -1)
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 5, -1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.volume_label = QtWidgets.QLabel(unit_converter)
        self.volume_label.setMinimumSize(QtCore.QSize(20, 0))
        self.volume_label.setMaximumSize(QtCore.QSize(20, 16777215))
        self.volume_label.setObjectName("volume_label")
        self.horizontalLayout.addWidget(self.volume_label)
        self.mid_label = QtWidgets.QLabel(unit_converter)
        self.mid_label.setMinimumSize(QtCore.QSize(15, 0))
        self.mid_label.setMaximumSize(QtCore.QSize(20, 30))
        self.mid_label.setObjectName("mid_label")
        self.horizontalLayout.addWidget(self.mid_label)
        self.time_label = QtWidgets.QLabel(unit_converter)
        self.time_label.setMinimumSize(QtCore.QSize(30, 0))
        self.time_label.setMaximumSize(QtCore.QSize(30, 16777215))
        self.time_label.setObjectName("time_label")
        self.horizontalLayout.addWidget(self.time_label)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.value_edit = QtWidgets.QLineEdit(unit_converter)
        self.value_edit.setMinimumSize(QtCore.QSize(120, 30))
        self.value_edit.setObjectName("value_edit")
        self.gridLayout.addWidget(self.value_edit, 1, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.confirm_btn = QtWidgets.QPushButton(unit_converter)
        self.confirm_btn.setMinimumSize(QtCore.QSize(30, 0))
        self.confirm_btn.setObjectName("confirm_btn")
        self.gridLayout.addWidget(self.confirm_btn, 2, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)

        self.retranslateUi(unit_converter)
        QtCore.QMetaObject.connectSlotsByName(unit_converter)

    def retranslateUi(self, unit_converter):
        _translate = QtCore.QCoreApplication.translate
        unit_converter.setWindowTitle(_translate("unit_converter", "单位转换器"))
        self.volume_group.setTitle(_translate("unit_converter", "流量单位"))
        self.kg_btn.setText(_translate("unit_converter", "千克"))
        self.m3_btn.setText(_translate("unit_converter", "立方米"))
        self.l_btn.setText(_translate("unit_converter", "升"))
        self.time_group.setTitle(_translate("unit_converter", "时间单位"))
        self.h_btn.setText(_translate("unit_converter", "每小时"))
        self.min_btn.setText(_translate("unit_converter", "每分钟"))
        self.s_btn.setText(_translate("unit_converter", "每秒"))
        self.volume_label.setText(_translate("unit_converter", "L"))
        self.mid_label.setText(_translate("unit_converter", "/"))
        self.time_label.setText(_translate("unit_converter", "S"))
        self.confirm_btn.setText(_translate("unit_converter", "确    认"))
