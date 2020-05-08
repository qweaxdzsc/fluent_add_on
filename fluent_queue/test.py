# import sys
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# import cgitb
#
#
# cgitb.enable(format='text')
#
#
# class DropInList(QListWidget):
#     def __init__(self):
#         super(DropInList, self).__init__()
#         self.setAcceptDrops(True)                               # 开启接受拖入事件
#         self.setDragEnabled(True)                                      # 开启拖出功能
#         # self.right_widget.setDragDropOverwriteMode(False)                         # 不能拖入
#         self.setSelectionMode(QAbstractItemView.ExtendedSelection)     # 开启多选模式
#         self.setDefaultDropAction(Qt.MoveAction)                       # 设置drop事件默认为移动事件
#         # widget.right_widget.dropEvent = self.dropEvent
#
#     def dropEvent(self, event):
#         source_Widget = event.source()                        # 获取拖入元素的父组件
#         print('yes')
#         items = source_Widget.selectedItems()
#         # items = self.selectedItems()
#         print(event.mimeData())
#         print(items)
#         for i in items:
#             self.takeItem(self.indexFromItem(i).row())          # 先删除再加回来，不能存在两个指向同一内存的对象
#             pts = self.mapFromGlobal(QCursor.pos())
#             last_pos_item = self.indexAt(pts).row()
#             print(last_pos_item)
#             if last_pos_item == -1:
#                 self.addItem(i)
#             else:
#                 self.insertItem(last_pos_item, i)
#
#         print('有东西拖入')
#
#
# class MainWidget(QWidget):
#     def __init__(self):
#         super(MainWidget, self).__init__()
#         self.setWindowTitle('检测拖入')
#         self.main_layout = QHBoxLayout()
#         self.left_widget = DropInList()
#         # self.right_widget = QListWidget()
#         self.right_widget = DropInList()
#         pre_list = ['a', 'b', 'c', 'd']
#         self.right_widget.addItems(pre_list)
#         self.main_layout.addWidget(self.left_widget)
#         self.main_layout.addWidget(self.right_widget)
#         self.setLayout(self.main_layout)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     m = MainWidget()
#     m.show()
#     sys.exit(app.exec_())

# import time
#
# time_start = time.time()
# time.sleep(10)
# time_end = time.time()
# use_time = (time_end - time_start)/60
#
# print('totally cost', use_time)
# import subprocess
# import time
# cores = 12
# running_journal = r'F:\luo\aest.jou'
# project_address = r'F:\luo'
# disk = project_address[:2]
# print(disk)
#
# p = subprocess.Popen(r'%s &&'
#                      r'cd %s &&'
#                      r'"C:\Program Files\ANSYS Inc\v201\fluent\ntbin\win64\fluent" 3d -t%s -i %s' %
#                      (disk, project_address, cores, running_journal),
#                      shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
#                      stderr=subprocess.PIPE, universal_newlines=True)
# while p.poll() == None:                         # block calculation thread until finished
#     # time.sleep(5)
#     line = p.stdout.readline()
#     msg = line
#     print('cmd output', msg)
# import subprocess
# # import time
# # import os
# # journal =
# p = subprocess.Popen(r'"C:\Program Files\ANSYS Inc\v201\fluent\ntbin\win64\fluent" 3d -t24',
#                      shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#                      universal_newlines=True)
# # p = os.system(r'"C:\Program Files\ANSYS Inc\v201\fluent\ntbin\win64\fluent" 3d -t12')
# # while p.poll() == None:                                     # block calculation thread until finished
# #     time.sleep(1)
# line = p.stdout.readline()
# #     p.stdout.flush()
# # p.wait()
# # p.communicate()
#
# print('yes')
#
#
# print('finish')

# fluent idle time_out
