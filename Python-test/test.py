from PyQt5 import QtWidgets, QtCore
import sys
import cgitb


class HorizontalTabBar(QtWidgets.QTabBar):
    def __init__(self, *args, **kwargs):
        super(HorizontalTabBar, self).__init__(*args, **kwargs)

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        option = QtWidgets.QStyleOptionTab()

        painter.begin(self)

        for index in range(self.count()):
            self.initStyleOption(option, index)
            tabRect = self.tabRect(index)
            tabRect.moveLeft(10)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, option)
            painter.drawText(tabRect, QtCore.Qt.AlignVCenter | QtCore.Qt.TextDontClip, self.tabText(index))

        painter.end()


cgitb.enable(format='text')
app = QtWidgets.QApplication(sys.argv)
tabs = QtWidgets.QTabWidget()
tabs.setFixedSize(600, 600)
widget1 = QtWidgets.QWidget()
widget2 = QtWidgets.QWidget()
widget3 = QtWidgets.QWidget()
widget4 = QtWidgets.QWidget()

tabs.setTabBar(HorizontalTabBar())

tabs.addTab(widget1, "转速")
tabs.addTab(widget2, "芯体参数")
tabs.addTab(widget3, "风门参数")
tabs.addTab(widget4, "出口阻值")

tabs.setStyleSheet("""
QTabBar::tab {height:50px;min-width: 100px;}
""")
tabs.setTabPosition(2)
tabs.show()
sys.exit(app.exec_())
