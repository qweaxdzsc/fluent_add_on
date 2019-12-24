# # -*- coding: utf-8 -*-
# from PyQt5 import QtCore, QtGui, QtWidgets,QtSql
# import sys,time
# from PyQt5.QtCore import  Qt
# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(991, 719)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
#         self.tableWidget.setGeometry(QtCore.QRect(50, 30, 721, 491))
#         self.tableWidget.setObjectName("tableWidget")
#         self.tableWidget.setColumnCount(0)
#         self.tableWidget.setRowCount(0)
#         self.pushButton = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton.setGeometry(QtCore.QRect(810, 40, 75, 23))
#         self.pushButton.setObjectName("pushButton")
#         self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton_2.setGeometry(QtCore.QRect(810, 80, 75, 23))
#         self.pushButton_2.setObjectName("pushButton_2")
#         self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton_3.setGeometry(QtCore.QRect(810, 120, 75, 23))
#         self.pushButton_3.setObjectName("pushButton_3")
#         self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton_4.setGeometry(QtCore.QRect(810, 160, 75, 23))
#         self.pushButton_4.setObjectName("pushButton_4")
#         self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton_5.setGeometry(QtCore.QRect(810, 200, 75, 23))
#         self.pushButton_5.setObjectName("pushButton_5")
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 991, 23))
#         self.menubar.setObjectName("menubar")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)
#
#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
#         self.openConn()
#         self.load_widget()
#         self.pushButton.clicked.connect(self.edit)
#         self.pushButton_2.clicked.connect(self.add)
#
#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         self.pushButton.setText(_translate("MainWindow", "PushButton"))
#         self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
#         self.pushButton_3.setText(_translate("MainWindow", "PushButton"))
#         self.pushButton_4.setText(_translate("MainWindow", "PushButton"))
#         self.pushButton_5.setText(_translate("MainWindow", "PushButton"))
#
#     def openConn(self):
#         try:
#             db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
#             db.setDatabaseName('abc.db')
#             if db.open():
#                 print('打开数据库成功')
#             else:
#                 print('连接数据库失败:' + db.lastError().text())
#         except Exception as e:
#             print(e.args)
#
#     def sel(self, sql):
#         sqlmodel=QtSql.QSqlQueryModel()
#         sqlmodel.setQuery(sql)
#         rows=sqlmodel.rowCount()
#         columns=sqlmodel.columnCount()
#         print(rows, columns)
#         for i in range(rows):
#             for j in range(columns):
#                 newItem=QtWidgets.QTableWidgetItem(str( sqlmodel.record(i).value(j)))
#                 self.tableWidget.setItem(i, j, newItem)
#
#     def load_widget(self):
#         self.tableWidget.horizontalHeader().setVisible(True)#行头
#         self.tableWidget.verticalHeader().setVisible(False) #列头
#         self.tableWidget.setSortingEnabled(True)#头排序
#         self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)#单行
#         self.tableWidget.setRowCount(10)#行数
#         self.tableWidget.setColumnCount(10)#列数
#         self.tableWidget.setHorizontalHeaderLabels(['id','date','name','content','num','msg','enable']) #字段名
#         self.sel('select * from table1') #查询
#
#         combox = QtWidgets.QComboBox()
#         combox.addItem('xxx')
#         self.tableWidget.setCellWidget(0,1,combox)
#
#         check=QtWidgets.QCheckBox()
#         check.setText('选中我')#文字
#         check.setEnabled(True) #不能修改
#         check.setCheckState(QtCore.Qt.Unchecked) #默认非选中
#         self.tableWidget.setCellWidget(0, 2, check)
#
#         self.tableWidget.setIconSize(QtCore.QSize(150,150)) #设置ico大小
#         self.tableWidget.setRowHeight(1, 150)
#         self.tableWidget.setColumnWidth(1, 150)
#         image=QtWidgets.QTableWidgetItem()
#         image.setFlags(QtCore.Qt.ItemIsEnabled) #选中不高亮
#         image.setIcon(QtGui.QIcon('../res/a.jpg'))
#
#         self.tableWidget.setItem(1,1,image)
#         self.btn=QtWidgets.QPushButton()
#         self.btn.setText('save')
#         self.btn.clicked.connect(self.add)
#         self.tableWidget.setCellWidget(0,4,self.btn)#按钮
#
#         self.tableWidget.setAlternatingRowColors(True)
#         self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section{background:yellow;}")
#         #一列不能编辑
#         for i in range(self.tableWidget.rowCount()):
#             item0=QtWidgets.QTableWidgetItem(self.tableWidget.item(i,0)) #设置单元格不能编辑
#             item0.setFlags(QtCore.Qt.ItemIsEnabled)
#             self.tableWidget.setItem(i, 0, item0) #设置不能编辑
#
#     def edit(self):
#
#         index = self.tableWidget.currentIndex()
#         rows = self.tableWidget.currentRow()
#         columns = self.tableWidget.currentColumn()
#         print(rows, columns)
#
#     def add(self):
#         self.tableWidget.insertRow(self.tableWidget.rowCount())
#
#
# if __name__ == '__main__':
#
#     app=QtWidgets.QApplication(sys.argv)
#     mainwindow=QtWidgets.QMainWindow()
#     ui=Ui_MainWindow()
#     ui.setupUi(mainwindow)
#     mainwindow.show()
#     sys.exit(app.exec_())

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class SliderDemo(QWidget):
    def __init__(self, parent=None):
        super(SliderDemo, self).__init__(parent)
        self.setWindowTitle("QSlider 例子")
        self.resize(300, 100)

        layout = QVBoxLayout()
        self.l1 = QLabel("Hello PyQt5")
        self.l1.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.l1)
        # 水平方向
        self.sl = QSlider(Qt.Horizontal)
        # 设置最小值
        self.sl.setMinimum(10)
        # 设置最大值
        self.sl.setMaximum(50)
        # 步长
        self.sl.setSingleStep(10)
        # 设置当前值
        self.sl.setValue(20)
        # 刻度位置，刻度在下方
        self.sl.setTickPosition(QSlider.TicksBelow)
        # 设置刻度间隔
        self.sl.setTickInterval(10)
        layout.addWidget(self.sl)
        # 连接信号槽
        self.sl.valueChanged.connect(self.valuechange)
        self.setLayout(layout)

    def valuechange(self):
        ten_digit = int(self.sl.value() / 10)
        single_digit = self.sl.value() % 10
        if single_digit < 5:
            self.sl.setValue(ten_digit*10)
        else:
            self.sl.setValue((ten_digit+1)*10)

        print('current slider value=%s' % self.sl.value())
        size = self.sl.value()
        self.l1.setFont(QFont("Arial", size))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = SliderDemo()
    demo.show()
    sys.exit(app.exec_())
