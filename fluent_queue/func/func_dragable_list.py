from PyQt5.QtWidgets import QListWidget, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor


class DragListWidget(QListWidget):
    """
    rewrite the Qlistwidget
    it is imported by ui_queue_main.py file
    1. it make list widget dragable and dropable
    2. if have drag permission, false by default, can alter the sequence of list item
    """
    def __init__(self, central_widget):
        super(DragListWidget, self).__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)                                   # 开启拖出功能
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 开启多选模式
        self.setDefaultDropAction(Qt.MoveAction)                    # 设置drop事件默认为移动事件
        self.drag_permission = False

    def dropEvent(self, event):
        """
        rewrite dropEvent
        effect when have permission
        :param event:
        :return:
        """
        if self.drag_permission:
            print('yes')
            items = self.selectedItems()
            print(items)
            for i in items:
                self.takeItem(self.indexFromItem(i).row())          # 先删除再加回来，不能存在两个指向同一内存的对象
                pts = self.mapFromGlobal(QCursor.pos())
                last_pos_item = self.indexAt(pts).row()
                print(last_pos_item)
                if last_pos_item == -1:
                    self.addItem(i)
                else:
                    self.insertItem(last_pos_item, i)

            print('有东西拖入')
