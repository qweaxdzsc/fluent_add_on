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

#
# import matplotlib.pyplot as plt
# import numpy as np
# #潘海东,2014/1/13
#
# x = np.arange(1, 17, 1)
# y = np.array([4.00, 6.40, 8.00, 8.80, 9.22, 9.50, 9.70, 9.86, 10.00, 10.20, 10.32, 10.42, 10.50, 10.55, 10.58, 10.60])
# z1 = np.polyfit(x, y, 3)#用3次多项式拟合
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
# plt.savefig('p1.png')
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

import logging
import sys
from PyQt5 import QtWidgets, QtCore
# make the example runnable without the need to install


import qdarkstyle
import example_pyqt5_ui as example_ui


def main():
    """
    Application entry point
    """
    logging.basicConfig(level=logging.DEBUG)
    # create the application and the main window
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    # setup ui
    # ui = example_ui.Ui_MainWindow()
    # ui.setupUi(window)
    # ui.bt_delay_popup.addActions([
    #     ui.actionAction,
    #     ui.actionAction_C
    # ])
    # ui.bt_instant_popup.addActions([
    #     ui.actionAction,
    #     ui.actionAction_C
    # ])
    # ui.bt_menu_button_popup.addActions([
    #     ui.actionAction,
    #     ui.actionAction_C
    # ])
    # item = QtWidgets.QTableWidgetItem("Test")
    # item.setCheckState(QtCore.Qt.Checked)
    # ui.tableWidget.setItem(0, 0, item)
    # window.setWindowTitle("QDarkStyle example")

    # tabify dock widgets to show bug #6
    # window.tabifyDockWidget(ui.dockWidget1, ui.dockWidget2)

    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # auto quit after 2s when testing on travis-ci
    if "--travis" in sys.argv:
        QtCore.QTimer.singleShot(2000, app.exit)

    # run
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()