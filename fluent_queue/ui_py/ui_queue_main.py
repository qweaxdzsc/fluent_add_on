# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_queue_main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from func.func_dragable_list import DragListWidget


class Ui_fluent_queue(object):
    def setupUi(self, fluent_queue):
        fluent_queue.setObjectName("fluent_queue")
        fluent_queue.resize(471, 642)
        fluent_queue.setMinimumSize(QtCore.QSize(400, 550))
        fluent_queue.setMaximumSize(QtCore.QSize(550, 900))
        fluent_queue.setIconSize(QtCore.QSize(30, 30))
        self.centralwidget = QtWidgets.QWidget(fluent_queue)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(30, 20, 30, 25)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget_running = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_running.setEnabled(True)
        self.listWidget_running.setMaximumSize(QtCore.QSize(500, 25))
        self.listWidget_running.setToolTip("")
        self.listWidget_running.setStyleSheet("border-top: 0px;\n"
"background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,\n"
"                                      stop: 0 #9ACD32, stop: 1 #FFFFF0);")
        self.listWidget_running.setObjectName("listWidget_running")
        self.verticalLayout.addWidget(self.listWidget_running)
        self.listWidget_queue = DragListWidget(self.centralwidget)
        self.listWidget_queue.setEnabled(True)
        self.listWidget_queue.setToolTip("")
        self.listWidget_queue.setStyleSheet("border-top: 0px")
        self.listWidget_queue.setObjectName("listWidget_queue")
        self.verticalLayout.addWidget(self.listWidget_queue)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 50)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.BottomToTop)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        fluent_queue.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(fluent_queue)
        self.statusbar.setObjectName("statusbar")
        fluent_queue.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(fluent_queue)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setStyleSheet("QToolBar {\n"
"    spacing:5px;\n"
"    \n"
"    padding:8px;\n"
"\n"
"}\n"
"")
        self.toolBar.setIconSize(QtCore.QSize(50, 40))
        self.toolBar.setObjectName("toolBar")
        fluent_queue.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_login = QtWidgets.QAction(fluent_queue)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icon/login.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_login.setIcon(icon)
        self.action_login.setObjectName("action_login")
        self.action_logout = QtWidgets.QAction(fluent_queue)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../icon/logoff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_logout.setIcon(icon1)
        self.action_logout.setObjectName("action_logout")
        self.action_add = QtWidgets.QAction(fluent_queue)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../icon/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_add.setIcon(icon2)
        self.action_add.setObjectName("action_add")
        self.action_journal = QtWidgets.QAction(fluent_queue)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../icon/dialog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_journal.setIcon(icon3)
        self.action_journal.setObjectName("action_journal")
        self.action_delete = QtWidgets.QAction(fluent_queue)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../icon/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_delete.setIcon(icon4)
        self.action_delete.setObjectName("action_delete")
        self.action_help = QtWidgets.QAction(fluent_queue)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../icon/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_help.setIcon(icon5)
        self.action_help.setObjectName("action_help")
        self.toolBar.addAction(self.action_login)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_logout)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_add)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_delete)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_journal)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_help)
        self.toolBar.addSeparator()

        self.retranslateUi(fluent_queue)
        QtCore.QMetaObject.connectSlotsByName(fluent_queue)

    def retranslateUi(self, fluent_queue):
        _translate = QtCore.QCoreApplication.translate
        fluent_queue.setWindowTitle(_translate("fluent_queue", "未登陆-请登陆后使用更多功能"))
        self.listWidget_running.setStatusTip(_translate("fluent_queue", "正在计算的项目"))
        self.listWidget_queue.setStatusTip(_translate("fluent_queue", "待处理项目队列"))
        self.progressBar.setStatusTip(_translate("fluent_queue", "总进度"))
        self.progressBar.setFormat(_translate("fluent_queue", "%p%"))
        self.toolBar.setWindowTitle(_translate("fluent_queue", "未登陆-请登陆后使用更多功能"))
        self.action_login.setText(_translate("fluent_queue", "登陆"))
        self.action_logout.setText(_translate("fluent_queue", "注销"))
        self.action_add.setText(_translate("fluent_queue", "添加项目"))
        self.action_journal.setText(_translate("fluent_queue", "项目日志"))
        self.action_journal.setToolTip(_translate("fluent_queue", "完成项目记录"))
        self.action_delete.setText(_translate("fluent_queue", "删除项目"))
        self.action_delete.setToolTip(_translate("fluent_queue", "删除选中项目"))
        self.action_help.setText(_translate("fluent_queue", "帮助"))
        self.action_help.setToolTip(_translate("fluent_queue", "帮助文档"))



