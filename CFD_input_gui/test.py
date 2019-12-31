import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TreeWidget(QWidget):
    def __init__(self):
        super(TreeWidget, self).__init__()
        self.setWindowTitle('TreeWidget')

        self.tree = QTreeWidget()  # 实例化一个TreeWidget对象
        self.tree.setColumnCount(2)  # 设置部件的列数为2
        self.tree.setDropIndicatorShown(True)

        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tree.setHeaderLabels(['Key', 'Value'])  # 设置头部信息对应列的标识符

        # 设置root为self.tree的子树，故root是根节点
        root = QTreeWidgetItem(self.tree)
        root.setText(0, 'root')  # 设置根节点的名称
        root.setCheckState(0, Qt.Unchecked);

        # 为root节点设置子结点
        child1 = QTreeWidgetItem(root)
        child1.setText(0, 'child1')
        child1.setText(1, 'name1')
        child1.setCheckState(0, Qt.Unchecked);

        child2 = QTreeWidgetItem(root)
        child2.setText(0, 'child2')
        child2.setText(1, 'name2')
        child2.setCheckState(0, Qt.Unchecked);

        child3 = QTreeWidgetItem(root)
        child3.setText(0, 'child3')
        child3.setCheckState(0, Qt.Unchecked);

        child4 = QTreeWidgetItem(child3)

        child4.setText(0, 'child4')
        child4.setToolTip(0, 'child4')
        # child4.statusTip(0)
        QToolTip.setFont(QFont('OldEnglish', 30))

        child4.setText(1, 'name4')
        child4.setToolTip(1, 'name4')
        child4.setCheckState(0, Qt.Unchecked);

        button = QPushButton("test")
        lay = QVBoxLayout()
        lay.addWidget(button)
        lay.addWidget(self.tree)

        button.clicked.connect(self.getText)
        self.tree.itemChanged.connect(self.handleChanged)
        self.tree.itemDoubleClicked.connect(self.getText)

        self.tree.addTopLevelItem(root)
        self.setLayout(lay)  # 将tree部件设置为该窗口的核心框架

    def handleChanged(self, item, column):
        count = item.childCount()
        # print dir(item)
        if item.checkState(column) == Qt.Checked:
            # print "checked", item, item.text(column)
            for f in range(count):
                item.child(f).setCheckState(0, Qt.Checked)
        if item.checkState(column) == Qt.Unchecked:
            # print "unchecked", item, item.text(column)
            for f in range(count):
                item.child(f).setCheckState(0, Qt.Unchecked)

    def getText(self):
        # print self.tree.currentItem().text(1)

        Item_list = self.tree.selectedItems()
        for ii in Item_list:
            print
            ii.text(0)


app = QApplication(sys.argv)
# app.aboutToQuit.connect(app.deleteLater)
tp = TreeWidget()
tp.show()
# app.installEventFilter(tp)
app.exec_()
