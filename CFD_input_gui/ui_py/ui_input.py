# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_input.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from func.func_bar_horizontal import HorizontalTabBar


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(481, 499)
        MainWindow.setMaximumSize(QtCore.QSize(1500, 1000))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../.designer/backup/fluent_gui/title_icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStatusTip("")
        MainWindow.setStyleSheet("QToorBar::handle{height:40px; spacing: 10px;}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(-5, -5, 521, 471))
        self.tabWidget.setMinimumSize(QtCore.QSize(500, 450))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.tabWidget.setFont(font)
        self.tabWidget.setStatusTip("")
        self.tabWidget.setWhatsThis("")
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setStyleSheet("QTabBar::tab {height:55px; min-width: 80px;boder:none}\n"
"QTabWidget::tab-bar { alignment: left; }")
        self.tabWidget.setTabBar(HorizontalTabBar())
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(20, 20))
        self.tabWidget.setObjectName("tabWidget")
        self.RPM_tab = QtWidgets.QWidget()
        self.RPM_tab.setAccessibleDescription("")
        self.RPM_tab.setObjectName("RPM_tab")
        self.mode_slider = QtWidgets.QSlider(self.RPM_tab)
        self.mode_slider.setGeometry(QtCore.QRect(320, 90, 31, 291))
        self.mode_slider.setMinimum(1)
        self.mode_slider.setMaximum(7)
        self.mode_slider.setSingleStep(1)
        self.mode_slider.setPageStep(1)
        self.mode_slider.setProperty("value", 1)
        self.mode_slider.setSliderPosition(1)
        self.mode_slider.setOrientation(QtCore.Qt.Vertical)
        self.mode_slider.setInvertedAppearance(True)
        self.mode_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.mode_slider.setTickInterval(1)
        self.mode_slider.setObjectName("mode_slider")
        self.label = QtWidgets.QLabel(self.RPM_tab)
        self.label.setGeometry(QtCore.QRect(20, 19, 321, 41))
        self.label.setObjectName("label")
        self.frame = QtWidgets.QFrame(self.RPM_tab)
        self.frame.setGeometry(QtCore.QRect(30, 60, 291, 361))
        self.frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setContentsMargins(20, 10, 20, 20)
        self.gridLayout_2.setSpacing(10)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.defrost_label = QtWidgets.QLabel(self.frame)
        self.defrost_label.setEnabled(False)
        self.defrost_label.setMinimumSize(QtCore.QSize(50, 0))
        self.defrost_label.setObjectName("defrost_label")
        self.gridLayout_2.addWidget(self.defrost_label, 4, 0, 1, 1)
        self.vent_label = QtWidgets.QLabel(self.frame)
        self.vent_label.setMinimumSize(QtCore.QSize(50, 0))
        self.vent_label.setObjectName("vent_label")
        self.gridLayout_2.addWidget(self.vent_label, 0, 0, 1, 1)
        self.foot_label = QtWidgets.QLabel(self.frame)
        self.foot_label.setEnabled(False)
        self.foot_label.setMinimumSize(QtCore.QSize(50, 0))
        self.foot_label.setObjectName("foot_label")
        self.gridLayout_2.addWidget(self.foot_label, 2, 0, 1, 1)
        self.hil_label = QtWidgets.QLabel(self.frame)
        self.hil_label.setEnabled(False)
        self.hil_label.setMinimumSize(QtCore.QSize(50, 0))
        self.hil_label.setObjectName("hil_label")
        self.gridLayout_2.addWidget(self.hil_label, 7, 0, 1, 1)
        self.vent_slider = QtWidgets.QSlider(self.frame)
        self.vent_slider.setMinimumSize(QtCore.QSize(140, 0))
        self.vent_slider.setMinimum(0)
        self.vent_slider.setMaximum(34)
        self.vent_slider.setPageStep(1)
        self.vent_slider.setProperty("value", 10)
        self.vent_slider.setOrientation(QtCore.Qt.Horizontal)
        self.vent_slider.setObjectName("vent_slider")
        self.gridLayout_2.addWidget(self.vent_slider, 0, 1, 1, 1)
        self.bil_label = QtWidgets.QLabel(self.frame)
        self.bil_label.setEnabled(False)
        self.bil_label.setMinimumSize(QtCore.QSize(50, 0))
        self.bil_label.setObjectName("bil_label")
        self.gridLayout_2.addWidget(self.bil_label, 3, 0, 1, 1)
        self.trl_label = QtWidgets.QLabel(self.frame)
        self.trl_label.setEnabled(False)
        self.trl_label.setMinimumSize(QtCore.QSize(50, 0))
        self.trl_label.setObjectName("trl_label")
        self.gridLayout_2.addWidget(self.trl_label, 6, 0, 1, 1)
        self.defog_label = QtWidgets.QLabel(self.frame)
        self.defog_label.setEnabled(False)
        self.defog_label.setMinimumSize(QtCore.QSize(50, 0))
        self.defog_label.setObjectName("defog_label")
        self.gridLayout_2.addWidget(self.defog_label, 5, 0, 1, 1)
        self.defog_slider = QtWidgets.QSlider(self.frame)
        self.defog_slider.setEnabled(False)
        self.defog_slider.setMinimumSize(QtCore.QSize(140, 0))
        self.defog_slider.setMinimum(0)
        self.defog_slider.setMaximum(34)
        self.defog_slider.setPageStep(1)
        self.defog_slider.setProperty("value", 14)
        self.defog_slider.setOrientation(QtCore.Qt.Horizontal)
        self.defog_slider.setObjectName("defog_slider")
        self.gridLayout_2.addWidget(self.defog_slider, 5, 1, 1, 1)
        self.defrost_slider = QtWidgets.QSlider(self.frame)
        self.defrost_slider.setEnabled(False)
        self.defrost_slider.setMinimumSize(QtCore.QSize(140, 0))
        self.defrost_slider.setMinimum(0)
        self.defrost_slider.setMaximum(34)
        self.defrost_slider.setPageStep(1)
        self.defrost_slider.setProperty("value", 14)
        self.defrost_slider.setOrientation(QtCore.Qt.Horizontal)
        self.defrost_slider.setObjectName("defrost_slider")
        self.gridLayout_2.addWidget(self.defrost_slider, 4, 1, 1, 1)
        self.trl_slider = QtWidgets.QSlider(self.frame)
        self.trl_slider.setEnabled(False)
        self.trl_slider.setMinimumSize(QtCore.QSize(140, 0))
        self.trl_slider.setMinimum(0)
        self.trl_slider.setMaximum(34)
        self.trl_slider.setPageStep(1)
        self.trl_slider.setProperty("value", 14)
        self.trl_slider.setOrientation(QtCore.Qt.Horizontal)
        self.trl_slider.setObjectName("trl_slider")
        self.gridLayout_2.addWidget(self.trl_slider, 6, 1, 1, 1)
        self.bil_slider = QtWidgets.QSlider(self.frame)
        self.bil_slider.setEnabled(False)
        self.bil_slider.setMinimumSize(QtCore.QSize(140, 0))
        self.bil_slider.setMinimum(0)
        self.bil_slider.setMaximum(34)
        self.bil_slider.setPageStep(1)
        self.bil_slider.setProperty("value", 14)
        self.bil_slider.setOrientation(QtCore.Qt.Horizontal)
        self.bil_slider.setObjectName("bil_slider")
        self.gridLayout_2.addWidget(self.bil_slider, 3, 1, 1, 1)
        self.hil_slider = QtWidgets.QSlider(self.frame)
        self.hil_slider.setEnabled(False)
        self.hil_slider.setMinimumSize(QtCore.QSize(140, 0))
        self.hil_slider.setMinimum(0)
        self.hil_slider.setMaximum(34)
        self.hil_slider.setPageStep(1)
        self.hil_slider.setProperty("value", 14)
        self.hil_slider.setOrientation(QtCore.Qt.Horizontal)
        self.hil_slider.setObjectName("hil_slider")
        self.gridLayout_2.addWidget(self.hil_slider, 7, 1, 1, 1)
        self.foot_slider = QtWidgets.QSlider(self.frame)
        self.foot_slider.setEnabled(False)
        self.foot_slider.setMinimumSize(QtCore.QSize(140, 0))
        self.foot_slider.setMinimum(0)
        self.foot_slider.setMaximum(34)
        self.foot_slider.setPageStep(1)
        self.foot_slider.setProperty("value", 14)
        self.foot_slider.setOrientation(QtCore.Qt.Horizontal)
        self.foot_slider.setObjectName("foot_slider")
        self.gridLayout_2.addWidget(self.foot_slider, 2, 1, 1, 1)
        self.vent_edit = QtWidgets.QLineEdit(self.frame)
        self.vent_edit.setMinimumSize(QtCore.QSize(40, 0))
        self.vent_edit.setObjectName("vent_edit")
        self.gridLayout_2.addWidget(self.vent_edit, 0, 2, 1, 1)
        self.foot_edit = QtWidgets.QLineEdit(self.frame)
        self.foot_edit.setEnabled(False)
        self.foot_edit.setMinimumSize(QtCore.QSize(40, 0))
        self.foot_edit.setObjectName("foot_edit")
        self.gridLayout_2.addWidget(self.foot_edit, 2, 2, 1, 1)
        self.bil_edit = QtWidgets.QLineEdit(self.frame)
        self.bil_edit.setEnabled(False)
        self.bil_edit.setMinimumSize(QtCore.QSize(40, 0))
        self.bil_edit.setObjectName("bil_edit")
        self.gridLayout_2.addWidget(self.bil_edit, 3, 2, 1, 1)
        self.defrost_edit = QtWidgets.QLineEdit(self.frame)
        self.defrost_edit.setEnabled(False)
        self.defrost_edit.setMinimumSize(QtCore.QSize(40, 0))
        self.defrost_edit.setObjectName("defrost_edit")
        self.gridLayout_2.addWidget(self.defrost_edit, 4, 2, 1, 1)
        self.defog_edit = QtWidgets.QLineEdit(self.frame)
        self.defog_edit.setEnabled(False)
        self.defog_edit.setMinimumSize(QtCore.QSize(40, 0))
        self.defog_edit.setObjectName("defog_edit")
        self.gridLayout_2.addWidget(self.defog_edit, 5, 2, 1, 1)
        self.trl_edit = QtWidgets.QLineEdit(self.frame)
        self.trl_edit.setEnabled(False)
        self.trl_edit.setMinimumSize(QtCore.QSize(40, 0))
        self.trl_edit.setObjectName("trl_edit")
        self.gridLayout_2.addWidget(self.trl_edit, 6, 2, 1, 1)
        self.hil_edit = QtWidgets.QLineEdit(self.frame)
        self.hil_edit.setEnabled(False)
        self.hil_edit.setMinimumSize(QtCore.QSize(40, 0))
        self.hil_edit.setObjectName("hil_edit")
        self.gridLayout_2.addWidget(self.hil_edit, 7, 2, 1, 1)
        self.tabWidget.addTab(self.RPM_tab, "")
        self.porous_tab = QtWidgets.QWidget()
        self.porous_tab.setObjectName("porous_tab")
        self.label_2 = QtWidgets.QLabel(self.porous_tab)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 280, 20))
        self.label_2.setObjectName("label_2")
        self.frame_2 = QtWidgets.QFrame(self.porous_tab)
        self.frame_2.setGeometry(QtCore.QRect(40, 50, 281, 211))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setHorizontalSpacing(30)
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.evap_label = QtWidgets.QLabel(self.frame_2)
        self.evap_label.setObjectName("evap_label")
        self.gridLayout.addWidget(self.evap_label, 0, 0, 1, 1)
        self.evap_combox = QtWidgets.QComboBox(self.frame_2)
        self.evap_combox.setObjectName("evap_combox")
        self.evap_combox.addItem("")
        self.evap_combox.addItem("")
        self.gridLayout.addWidget(self.evap_combox, 0, 1, 1, 1)
        self.hc_label = QtWidgets.QLabel(self.frame_2)
        self.hc_label.setObjectName("hc_label")
        self.gridLayout.addWidget(self.hc_label, 1, 0, 1, 1)
        self.hc_combox = QtWidgets.QComboBox(self.frame_2)
        self.hc_combox.setObjectName("hc_combox")
        self.hc_combox.addItem("")
        self.hc_combox.addItem("")
        self.gridLayout.addWidget(self.hc_combox, 1, 1, 1, 1)
        self.filter_label = QtWidgets.QLabel(self.frame_2)
        self.filter_label.setObjectName("filter_label")
        self.gridLayout.addWidget(self.filter_label, 2, 0, 1, 1)
        self.filter_combox = QtWidgets.QComboBox(self.frame_2)
        self.filter_combox.setObjectName("filter_combox")
        self.filter_combox.addItem("")
        self.filter_combox.addItem("")
        self.gridLayout.addWidget(self.filter_combox, 2, 1, 1, 1)
        self.tabWidget.addTab(self.porous_tab, "")
        self.outlet_tab = QtWidgets.QWidget()
        self.outlet_tab.setObjectName("outlet_tab")
        self.outlet_scrollarea = QtWidgets.QScrollArea(self.outlet_tab)
        self.outlet_scrollarea.setGeometry(QtCore.QRect(50, 80, 291, 341))
        self.outlet_scrollarea.setStyleSheet("QAbstractScrollArea {\n"
"    background-color: white;\n"
"    border:none\n"
"}\n"
"\n"
"QWidget{\n"
"    background-color: white;\n"
"}")
        self.outlet_scrollarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.outlet_scrollarea.setWidgetResizable(True)
        self.outlet_scrollarea.setObjectName("outlet_scrollarea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 291, 341))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.formLayout = QtWidgets.QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setContentsMargins(20, 10, 20, 20)
        self.formLayout.setHorizontalSpacing(60)
        self.formLayout.setVerticalSpacing(20)
        self.formLayout.setObjectName("formLayout")
        self.outlet_scrollarea.setWidget(self.scrollAreaWidgetContents)
        self.outlet_btn = QtWidgets.QPushButton(self.outlet_tab)
        self.outlet_btn.setGeometry(QtCore.QRect(230, 25, 111, 31))
        self.outlet_btn.setObjectName("outlet_btn")
        self.label_3 = QtWidgets.QLabel(self.outlet_tab)
        self.label_3.setGeometry(QtCore.QRect(20, 30, 201, 21))
        self.label_3.setObjectName("label_3")
        self.tabWidget.addTab(self.outlet_tab, "")
        self.valve_tab = QtWidgets.QWidget()
        self.valve_tab.setObjectName("valve_tab")
        self.label_7 = QtWidgets.QLabel(self.valve_tab)
        self.label_7.setGeometry(QtCore.QRect(20, 30, 381, 20))
        self.label_7.setObjectName("label_7")
        self.valve_table = QtWidgets.QTableWidget(self.valve_tab)
        self.valve_table.setGeometry(QtCore.QRect(50, 90, 241, 231))
        self.valve_table.setStyleSheet("")
        self.valve_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.valve_table.setGridStyle(QtCore.Qt.SolidLine)
        self.valve_table.setRowCount(1)
        self.valve_table.setObjectName("valve_table")
        self.valve_table.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.valve_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.valve_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.valve_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.valve_table.setItem(0, 1, item)
        self.valve_table.horizontalHeader().setDefaultSectionSize(100)
        self.valve_table.horizontalHeader().setStretchLastSection(True)
        self.valve_table.verticalHeader().setDefaultSectionSize(40)
        self.valve_slider = QtWidgets.QSlider(self.valve_tab)
        self.valve_slider.setGeometry(QtCore.QRect(320, 100, 20, 211))
        self.valve_slider.setMaximum(5)
        self.valve_slider.setPageStep(1)
        self.valve_slider.setProperty("value", 1)
        self.valve_slider.setOrientation(QtCore.Qt.Vertical)
        self.valve_slider.setInvertedAppearance(True)
        self.valve_slider.setInvertedControls(False)
        self.valve_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.valve_slider.setTickInterval(1)
        self.valve_slider.setObjectName("valve_slider")
        self.tabWidget.addTab(self.valve_tab, "")
        self.comment_tab = QtWidgets.QWidget()
        self.comment_tab.setObjectName("comment_tab")
        self.comment_edit = QtWidgets.QTextEdit(self.comment_tab)
        self.comment_edit.setGeometry(QtCore.QRect(50, 80, 301, 311))
        self.comment_edit.setObjectName("comment_edit")
        self.label_8 = QtWidgets.QLabel(self.comment_tab)
        self.label_8.setGeometry(QtCore.QRect(20, 30, 381, 20))
        self.label_8.setObjectName("label_8")
        self.tabWidget.addTab(self.comment_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.toolBar.setStyleSheet("QToolButton{height:40px;margin-right:10px}\n"
"QToolBar{spacing:10px;}\n"
"\n"
"    ")
        self.toolBar.setMovable(False)
        self.toolBar.setAllowedAreas(QtCore.Qt.BottomToolBarArea|QtCore.Qt.RightToolBarArea|QtCore.Qt.TopToolBarArea)
        self.toolBar.setIconSize(QtCore.QSize(45, 35))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.toolBar.setFloatable(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionexport = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../icon/export.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionexport.setIcon(icon1)
        self.actionexport.setObjectName("actionexport")
        self.actionimport = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../icon/import.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionimport.setIcon(icon2)
        self.actionimport.setObjectName("actionimport")
        self.actionhelp = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../icon/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionhelp.setIcon(icon3)
        self.actionhelp.setObjectName("actionhelp")
        self.toolBar.addAction(self.actionhelp)
        self.toolBar.addAction(self.actionexport)
        self.toolBar.addAction(self.actionimport)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.evap_combox.setCurrentIndex(0)
        self.hc_combox.setCurrentIndex(0)
        self.filter_combox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CFD-GUI"))
        self.label.setText(_translate("MainWindow", "*请滑动选择存在的模式，并填入相应转速（RPM）"))
        self.defrost_label.setText(_translate("MainWindow", "Defrost"))
        self.vent_label.setText(_translate("MainWindow", "Vent"))
        self.foot_label.setText(_translate("MainWindow", "Foot"))
        self.hil_label.setText(_translate("MainWindow", "Hi-Level"))
        self.bil_label.setText(_translate("MainWindow", "Bi-Level"))
        self.trl_label.setText(_translate("MainWindow", "Tri-Level"))
        self.defog_label.setText(_translate("MainWindow", "Defog"))
        self.vent_edit.setText(_translate("MainWindow", "3000"))
        self.foot_edit.setText(_translate("MainWindow", "3200"))
        self.bil_edit.setText(_translate("MainWindow", "3200"))
        self.defrost_edit.setText(_translate("MainWindow", "3200"))
        self.defog_edit.setText(_translate("MainWindow", "3200"))
        self.trl_edit.setText(_translate("MainWindow", "3200"))
        self.hil_edit.setText(_translate("MainWindow", "3200"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.RPM_tab), _translate("MainWindow", "转速            "))
        self.label_2.setText(_translate("MainWindow", "*请选择拥有的芯体"))
        self.evap_label.setText(_translate("MainWindow", "蒸发器"))
        self.hc_label.setText(_translate("MainWindow", "加热芯"))
        self.filter_label.setText(_translate("MainWindow", "过滤芯"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.porous_tab), _translate("MainWindow", "芯体参数        "))
        self.outlet_btn.setText(_translate("MainWindow", "风阻计算器"))
        self.label_3.setText(_translate("MainWindow", "*请点击计算器，计算各出口风阻"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.outlet_tab), _translate("MainWindow", "出口阻值        "))
        self.label_7.setText(_translate("MainWindow", "*请选择温度风门数量，并填入相应的行程"))
        item = self.valve_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "风门名字"))
        item = self.valve_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "风门行程(°)"))
        __sortingEnabled = self.valve_table.isSortingEnabled()
        self.valve_table.setSortingEnabled(False)
        item = self.valve_table.item(0, 0)
        item.setText(_translate("MainWindow", "temp_valve1"))
        item = self.valve_table.item(0, 1)
        item.setText(_translate("MainWindow", "0"))
        self.valve_table.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.valve_tab), _translate("MainWindow", "风门参数        "))
        self.comment_edit.setPlaceholderText(_translate("MainWindow", "请对不够明确的信息或未填写进行说明                     或对时间节点，目标进行说明"))
        self.label_8.setText(_translate("MainWindow", "*请留下重要的备注信息"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.comment_tab), _translate("MainWindow", "备注"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionexport.setText(_translate("MainWindow", "导出模板"))
        self.actionexport.setToolTip(_translate("MainWindow", "导出模板"))
        self.actionexport.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionimport.setText(_translate("MainWindow", "导入模板"))
        self.actionimport.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionhelp.setText(_translate("MainWindow", "帮助"))
