#
# import os
# os.removedirs(r'C:\Users\BZMBN4\Desktop\project_test\result')
# import subprocess
# import threading
# import time
#
#
# class process(object):
#     def __init__(self):
#         self.p = subprocess.Popen('cd C:\\Program Files\\ANSYS Inc\\v191\\fluent\\ntbin\\win64 && fluent 3d -gu -t12', shell=True,
#                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         self.w = threading.Thread(target=self.monitor)
#         self.w.start()
#         self.f = threading.Thread(target=self.feedback)
#         self.f.start()
#
#     def feedback(self):
#         while True:
#             if 'Cleanup script file is' in self.msg:
#                 self.p.stdin.write(b'/file/read-journal/C:/Users/BZMBN4/Desktop/test.jou\r\n')
#                 self.p.stdin.flush()
#                 # out, err = p.communicate(b'exit')
#                 print(self.p.stdout.readline().decode())
#
#
#     def monitor(self):
#         self.msg=''
#         while self.p.poll() == None:
#             line = self.p.stdout.readline()
#             self.msg = line.decode()
#             print(self.msg)
#
# go = process()

# from cmd import Cmd
# import os
# import sys
#
#
# class Client(Cmd):
#     u"""help
#     这是doc
#     """
#     prompt = 'pyFun>'
#     intro = 'Welcom to pyFun!'
#
#     def __init(self):
#         Cmd.__init__(self)
#
#     def do_hello(self,arg):
#         print('hello',arg)
#
#     def do_exit(self,arg):
#         print('Bye!')
#         return True #返回True，直接输入exit命令将会退出
#
#     def preloop(self):
#         r'cd C:\\Program Files\\ANSYS Inc\\v191\\fluent\\ntbin\\win64 && fluent 3d -gu -t12'
#
#     def postloop(self):
#         # print 'Bye!'
#         print("print this line after leaving the loop")
#
#
# if __name__ == '__main__':
#     try:
#         client = Client()
#         client.cmdloop()
#     except:
#         exit()

# print(p.stdout.read())
# print('returen code:', p.returncode)



# import sys
# import time
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit
# from PyQt5.QtCore import QThread, pyqtSignal
#
#
# class Demo(QMainWindow):
#     def __init__(self):
#         super(Demo, self).__init__()
#         self.init_ui()
#
#     def init_ui(self):
#         self.resize(500, 500)
#         self.setWindowTitle('Demo')
#         self.setFixedSize(self.width(), self.height())
#         self.textEdit = QTextEdit(self)
#         self.textEdit.setGeometry(20, 20, 460, 250)
#         self.btn_start = QPushButton('start', self)
#         self.btn_start.setGeometry(200, 350, 100, 50)
#         self.btn_start.clicked.connect(self.slot_btn_start)
#
#     def slot_btn_start(self):
#         self.thread_1 = ThreadDemo()
#         self.thread_1.trigger.connect(self.print_in_textEdit)
#         self.thread_1.start()
#
#     def print_in_textEdit(self, msg):
#         self.textEdit.undo()
#         self.textEdit.append(msg)
#
#
#
# class ThreadDemo(QThread):
#     trigger = pyqtSignal(str)
#
#     def __init__(self):
#         super(ThreadDemo, self).__init__()
#
#     def run(self):
#         for i in range(10):
#             # print(i)
#             self.trigger.emit(str(i))
#             time.sleep(1)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = Demo()
#     w.show()
#     sys.exit(app.exec_())

# a = r'C:\Program Files\ANSYS Inc\v191'
# b = a.rindex('\\')
# c = a[:b]
# print(c)


# import os
#
#
# def get_FileSize(filePath):
#     fsize = os.path.getsize(filePath)
#     fsize = fsize / float(1024 * 1024)
#
#     return round(fsize, 2)
# #
#
# if __name__ == '__main__':
#     size = get_FileSize(r"C:\Users\BZMBN4\Desktop\test\458-rear_V4-FH_190830.scdoc")
#     print("文件大小：%.2f MB" % (size))


# import matplotlib.pyplot as plt
# import numpy as np
# #潘海东,2014/1/13
#
# x = np.arange(0, 17, 1)
# y = np.array([0.0, 4.00, 6.40, 8.00, 8.80, 9.22, 9.50, 9.70, 9.86, 10.00, 10.20, 10.32, 10.42, 10.50, 10.55, 10.58, 10.60])
# z1 = np.polyfit(x, y, 2)#用3次多项式拟合
# print(z1)
# p1 = np.poly1d(z1)
# print(p1) #在屏幕上打印拟合多项式
#
# yvals=p1(x)#也可以使用yvals=np.polyval(z1,x)
# plot1=plt.plot(x, y, '*',label='original values')
# plot2=plt.plot(x, yvals, 'r',label='polyfit values')
# plt.xlabel('x axis')
# plt.ylabel('y axis')
# plt.legend(loc=4)#指定legend的位置,读者可以自己help它的用法
# plt.title('polyfitting')
# plt.show()
# # plt.savefig('p1.png')

# -*- coding: utf-8 -*-

# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QProgressBar, QPushButton
# from PyQt5.QtCore import QBasicTimer
#
#
# class Example(QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#
#         self.pbar = QProgressBar(self)
#         self.pbar.setGeometry(30, 40, 200, 25)
#
#         self.setGeometry(300, 300, 280, 170)
#         self.setWindowTitle('进度条')
#         self.show()
#
#         self.timer = QBasicTimer()
#         self.step = 0
#         self.timer.start(1000, self)
#
#     def timerEvent(self, e):
#         if self.step >= 100:
#             self.timer.stop()
#             return
#         self.step = self.step + 1
#         self.pbar.setValue(self.step)
#

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())

# import ctypes
#
# from PyQt5.QtCore import QThread, pyqtSignal
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QPushButton
# import win32con
# from win32process import SuspendThread, ResumeThread
#
#
#
# class Worker(QThread):
#
#     valueChanged = pyqtSignal(int)  # 值变化信号
#     handle = -1
#
#     def run(self):
#         try:
#         # 这个目前我没弄明白这里写法
#             self.handle = ctypes.windll.kernel32.OpenThread(  # @UndefinedVariable
#                 win32con.PROCESS_ALL_ACCESS, False, int(QThread.currentThreadId()))
#         except Exception as e:
#             print('get thread handle failed', e)
#         print('thread id', int(QThread.currentThreadId()))
#         # 循环发送信号
#         for i in range(1, 101):
#             print('value', i)
#             self.valueChanged.emit(i)
#             QThread.sleep(1)
#
#
# class Window(QWidget):
#
#     def __init__(self, *args, **kwargs):
#         super(Window, self).__init__(*args, **kwargs)
#         # 垂直布局
#         layout = QVBoxLayout(self)
#         self.progressBar = QProgressBar(self)
#         self.progressBar.setRange(0, 100)
#         layout.addWidget(self.progressBar)
#         self.startButton = QPushButton('开启线程', self, clicked=self.onStart)
#         layout.addWidget(self.startButton)
#         self.suspendButton = QPushButton('挂起线程', self, clicked=self.onSuspendThread, enabled=False)
#         layout.addWidget(self.suspendButton)
#         self.resumeButton = QPushButton('恢复线程', self, clicked=self.onResumeThread, enabled=False)
#         layout.addWidget(self.resumeButton)
#         self.stopButton = QPushButton('终止线程', self, clicked=self.onStopThread, enabled=False)
#         layout.addWidget(self.stopButton)
#
#         # 当前线程id
#         print('main id', int(QThread.currentThreadId()))
#
#         # 子线程
#         self._thread = Worker(self)
#         self._thread.finished.connect(self._thread.deleteLater)
#         self._thread.valueChanged.connect(self.progressBar.setValue)
#
#     def onStart(self):
#         print('main id', int(QThread.currentThreadId()))
#         self._thread.start()  # 启动线程
#         self.startButton.setEnabled(False)
#         self.suspendButton.setEnabled(True)
#         self.stopButton.setEnabled(True)
#
#     def onSuspendThread(self):
#         if self._thread.handle == -1:
#             return print('handle is wrong')
#         ret = SuspendThread(self._thread.handle)
#         print('挂起线程', self._thread.handle, ret)
#         self.suspendButton.setEnabled(False)
#         self.resumeButton.setEnabled(True)
#
#     def onResumeThread(self):
#         if self._thread.handle == -1:
#             return print('handle is wrong')
#         ret = ResumeThread(self._thread.handle)
#         print('恢复线程', self._thread.handle, ret)
#         self.suspendButton.setEnabled(True)
#         self.resumeButton.setEnabled(False)
#
#     def onStopThread(self):
#         self.startButton.setEnabled(False)
#         self.suspendButton.setEnabled(False)
#         self.resumeButton.setEnabled(False)
#         ret = ctypes.windll.kernel32.TerminateThread(  # @UndefinedVariable
#             self._thread.handle, 0)
#         print('终止线程', self._thread.handle, ret)
#         self.stopButton.setEnabled(False)
#
#     def closeEvent(self, event):
#         if self._thread.isRunning():
#             self._thread.quit()
#             # 强制
#             # self._thread.terminate()
#         del self._thread
#         super(Window, self).closeEvent(event)


# if __name__ == '__main__':
#     import sys
#     import os
#     print('pid', os.getpid())
#     from PyQt5.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     w = Window()
#     w.show()
#     sys.exit(app.exec_())

# import sys
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
#
#
# class ComboxDemo(QWidget):
#     def __init__(self, parent=None):
#         super(ComboxDemo, self).__init__(parent)
#         self.setWindowTitle("combox 例子")
#         self.resize(300, 90)
#         layout = QVBoxLayout()
#         self.lbl = QLabel("")
#
#         self.cb = QComboBox()
#         self.cb.addItem("C")
#         self.cb.addItem("C++")
#         self.cb.addItems(["Java", "C#", "Python"])
#
#         self.cb.activated(self.selectionchange)
#         layout.addWidget(self.cb)
#         layout.addWidget(self.lbl)
#         self.setLayout(layout)
#
#     def selectionchange(self, i):
#         self.lbl.setText(self.cb.currentText())
#         self.lbl.adjustSize()
#
#         print("Items in the list are :")
#         print("Current index", i, "selection changed ", self.cb.currentText())
#         for count in range(self.cb.count()):
#             print('item' + str(count) + '=' + self.cb.itemText(count))
#
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     comboxDemo = ComboxDemo()
#     comboxDemo.show()
#     sys.exit(app.exec_())


# import timeit
#
#
# # 待测试的函数
# def add():
#     import webbrowser
# # stmt 需要测试的函数或语句，字符串形式
# # setup 运行的环境，本例子中表示 if __name__ == '__main__':
# # number 被测试的函数或语句，执行的次数，本例表示执行100000次add()。省缺则默认是10000次
# # repeat 测试做100次
# # 综上：此函数表示 测试 在if __name__ == '__main__'的条件下，执行100000次add()消耗的时间，并把这个测试做100次,并求出平均值
#
# t = timeit.repeat(stmt="add()", setup="from __main__ import add", number=1, repeat=1)
# print(t)
# print(sum(t) / len(t))

#
# import win32con, win32api
# win32api.SetFileAttributes(r'C:\Users\BZMBN4\Desktop\test.csv', win32con.FILE_ATTRIBUTE_HIDDEN)
# -*- coding: utf-8 -*-
# 导入模块
# import sys
# from PyQt5.QtWidgets import *
#
#
# class Combo(QComboBox):
#     def __init__(self, title, parent):
#         super(Combo, self).__init__(parent)
#         # 设置为可接受拖曳操作文本
#         self.setAcceptDrops(True)
#
#     # 当执行一个拖曳控件操作，并且鼠标指针进入该控件时，这个事件将会被触发。
#     # 在这个事件中可以获得被操作的窗口控件，还可以有条件地接受或拒绝该拖曳操作
#     def dragEnterEvent(self, e):
#         # 检测拖曳进来的数据是否包含文本，如有则接受，无则忽略
#         if e.mimeData().hasText():
#             e.accept()
#         else:
#             e.ignore()
#
#     # 当拖曳操作在其目标控件上被释放时，这个事件将被触发
#     def dropEvent(self, e):
#         # 添加拖曳文本到条目中
#         self.addItem(e.mimeData().text())
#
#
# class Example(QWidget):
#     def __init__(self):
#         super(Example, self).__init__()
#         self.initUI()
#
#     def initUI(self):
#         # 表单布局，添加控件
#         lo = QFormLayout()
#         lo.addRow(QLabel('请把左边的文本拖曳到右边的下拉菜单中'))
#
#         # 实例化单行文本框，设置为允许拖曳操作
#         edit = QLineEdit()
#         edit.setDragEnabled(True)
#
#         # 实例化Combo对象，添加控件到布局中
#         com = Combo('Button', self)
#         lo.addRow(edit, com)
#
#         # 设置主窗口布局及标题
#         self.setLayout(lo)
#         self.setWindowTitle('简单的拖曳例子')
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     ex.show()
#     sys.exit(app.exec_())

# printer是嵌套函数

