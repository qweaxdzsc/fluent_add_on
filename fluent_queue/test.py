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
#
#     def dropEvent(self, event):
#         # source_Widget = event.source()                        # 获取拖入元素的父组件
#         # items = source_Widget.selectedItems()
#         items = self.selectedItems()
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
#         # self.left_widget = DropInList()
#         self.right_widget = DropInList()
#         pre_list = ['a', 'b', 'c', 'd']
#         self.right_widget.addItems(pre_list)
#         self.right_widget.setDragEnabled(True)                                      # 开启拖出功能
#         # self.right_widget.setDragDropOverwriteMode(False)                         # 不能拖入
#         self.right_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)     # 开启多选模式
#         self.right_widget.setDefaultDropAction(Qt.MoveAction)                       # 设置drop事件默认为移动事件
#         # self.main_layout.addWidget(self.left_widget)
#         self.main_layout.addWidget(self.right_widget)
#         self.setLayout(self.main_layout)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     m = MainWidget()
#     m.show()
#     sys.exit(app.exec_())

