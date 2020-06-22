from PyQt5 import QtWidgets, QtCore


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


if __name__ == "__main__":
    pass
    # self.tabWidget.setTabBar(HorizontalTabBar())