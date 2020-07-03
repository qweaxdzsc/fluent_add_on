# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_plan_timer.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_set_timer_Form(object):
    def setupUi(self, set_timer_Form):
        set_timer_Form.setObjectName("set_timer_Form")
        set_timer_Form.resize(240, 215)
        set_timer_Form.setMinimumSize(QtCore.QSize(240, 100))
        set_timer_Form.setMaximumSize(QtCore.QSize(240, 215))
        self.verticalLayout = QtWidgets.QVBoxLayout(set_timer_Form)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(5, 10, 5, 10)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_launch = QtWidgets.QFrame(set_timer_Form)
        self.frame_launch.setMinimumSize(QtCore.QSize(200, 95))
        self.frame_launch.setMaximumSize(QtCore.QSize(1500, 95))
        self.frame_launch.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_launch.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_launch.setObjectName("frame_launch")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_launch)
        self.gridLayout_2.setContentsMargins(15, 10, 15, 10)
        self.gridLayout_2.setSpacing(10)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.edit_plan_datetime = QtWidgets.QDateTimeEdit(self.frame_launch)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.edit_plan_datetime.setFont(font)
        self.edit_plan_datetime.setObjectName("edit_plan_datetime")
        self.gridLayout_2.addWidget(self.edit_plan_datetime, 0, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(92, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.btn_plan_start = QtWidgets.QPushButton(self.frame_launch)
        self.btn_plan_start.setMinimumSize(QtCore.QSize(0, 28))
        self.btn_plan_start.setMaximumSize(QtCore.QSize(110, 30))
        self.btn_plan_start.setObjectName("btn_plan_start")
        self.gridLayout_2.addWidget(self.btn_plan_start, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.frame_launch)
        self.frame_cancel = QtWidgets.QFrame(set_timer_Form)
        self.frame_cancel.setMinimumSize(QtCore.QSize(200, 95))
        self.frame_cancel.setMaximumSize(QtCore.QSize(16777215, 95))
        self.frame_cancel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_cancel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_cancel.setObjectName("frame_cancel")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_cancel)
        self.gridLayout_3.setContentsMargins(15, 10, 15, 10)
        self.gridLayout_3.setSpacing(10)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.frame_cancel)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(75, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 1, 0, 1, 1)
        self.edit_rest_time = QtWidgets.QDateTimeEdit(self.frame_cancel)
        self.edit_rest_time.setObjectName("edit_rest_time")
        self.gridLayout_3.addWidget(self.edit_rest_time, 0, 1, 1, 1)
        self.btn_cancel_plan = QtWidgets.QPushButton(self.frame_cancel)
        self.btn_cancel_plan.setMinimumSize(QtCore.QSize(0, 28))
        self.btn_cancel_plan.setMaximumSize(QtCore.QSize(16777215, 30))
        self.btn_cancel_plan.setObjectName("btn_cancel_plan")
        self.gridLayout_3.addWidget(self.btn_cancel_plan, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.frame_cancel)

        self.retranslateUi(set_timer_Form)
        QtCore.QMetaObject.connectSlotsByName(set_timer_Form)

    def retranslateUi(self, set_timer_Form):
        _translate = QtCore.QCoreApplication.translate
        set_timer_Form.setWindowTitle(_translate("set_timer_Form", "延时启动任务"))
        self.btn_plan_start.setText(_translate("set_timer_Form", "计划启动"))
        self.label.setText(_translate("set_timer_Form", "计划任务延时"))
        self.btn_cancel_plan.setText(_translate("set_timer_Form", "确认取消"))
