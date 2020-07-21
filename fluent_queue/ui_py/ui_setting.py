# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_setting.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widget_setting(object):
    def setupUi(self, widget_setting):
        widget_setting.setObjectName("widget_setting")
        widget_setting.resize(414, 486)
        self.verticalLayout = QtWidgets.QVBoxLayout(widget_setting)
        self.verticalLayout.setContentsMargins(25, 30, 25, 25)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tree_setting = QtWidgets.QTreeWidget(widget_setting)
        self.tree_setting.setStyleSheet("QTreeWidget::Item{height: 30px}")
        self.tree_setting.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tree_setting.setHeaderHidden(True)
        self.tree_setting.setExpandsOnDoubleClick(False)
        self.tree_setting.setObjectName("tree_setting")
        item_0 = QtWidgets.QTreeWidgetItem(self.tree_setting)
        item_0 = QtWidgets.QTreeWidgetItem(self.tree_setting)
        item_0 = QtWidgets.QTreeWidgetItem(self.tree_setting)
        item_0 = QtWidgets.QTreeWidgetItem(self.tree_setting)
        item_0 = QtWidgets.QTreeWidgetItem(self.tree_setting)
        self.tree_setting.header().setVisible(False)
        self.tree_setting.header().setDefaultSectionSize(220)
        self.tree_setting.header().setMinimumSectionSize(60)
        self.verticalLayout.addWidget(self.tree_setting)

        self.retranslateUi(widget_setting)
        QtCore.QMetaObject.connectSlotsByName(widget_setting)

    def retranslateUi(self, widget_setting):
        _translate = QtCore.QCoreApplication.translate
        widget_setting.setWindowTitle(_translate("widget_setting", "设置"))
        self.tree_setting.headerItem().setText(0, _translate("widget_setting", "label"))
        self.tree_setting.headerItem().setText(1, _translate("widget_setting", "input"))
        __sortingEnabled = self.tree_setting.isSortingEnabled()
        self.tree_setting.setSortingEnabled(False)
        self.tree_setting.topLevelItem(0).setText(0, _translate("widget_setting", "计算设置"))
        self.tree_setting.topLevelItem(1).setText(0, _translate("widget_setting", "计划任务"))
        self.tree_setting.topLevelItem(2).setText(0, _translate("widget_setting", "语言"))
        self.tree_setting.topLevelItem(3).setText(0, _translate("widget_setting", "帮助"))
        self.tree_setting.topLevelItem(4).setText(0, _translate("widget_setting", "关于"))
        self.tree_setting.setSortingEnabled(__sortingEnabled)
