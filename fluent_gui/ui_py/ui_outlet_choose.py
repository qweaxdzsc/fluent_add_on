# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outlet.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_outlet_form(object):
    def setupUi(self, outlet_form):
        outlet_form.setObjectName("outlet_form")
        outlet_form.resize(439, 549)
        self.gridLayout = QtWidgets.QGridLayout(outlet_form)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setHorizontalSpacing(30)
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.outlet_tree = QtWidgets.QTreeWidget(outlet_form)
        self.outlet_tree.setObjectName("outlet_tree")
        item_0 = QtWidgets.QTreeWidgetItem(self.outlet_tree)
        item_0.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtWidgets.QTreeWidgetItem(self.outlet_tree)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtWidgets.QTreeWidgetItem(self.outlet_tree)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtWidgets.QTreeWidgetItem(self.outlet_tree)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtWidgets.QTreeWidgetItem(self.outlet_tree)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        self.gridLayout.addWidget(self.outlet_tree, 0, 0, 3, 1)
        self.chosed_label = QtWidgets.QLabel(outlet_form)
        self.chosed_label.setObjectName("chosed_label")
        self.gridLayout.addWidget(self.chosed_label, 0, 1, 1, 1)
        self.chosed_list = QtWidgets.QListView(outlet_form)
        self.chosed_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.chosed_list.setObjectName("chosed_list")
        self.gridLayout.addWidget(self.chosed_list, 1, 1, 1, 1)
        self.chosed_btn = QtWidgets.QPushButton(outlet_form)
        self.chosed_btn.setObjectName("chosed_btn")
        self.gridLayout.addWidget(self.chosed_btn, 2, 1, 1, 1)

        self.retranslateUi(outlet_form)
        QtCore.QMetaObject.connectSlotsByName(outlet_form)

    def retranslateUi(self, outlet_form):
        _translate = QtCore.QCoreApplication.translate
        outlet_form.setWindowTitle(_translate("outlet_form", "出口命名"))
        self.outlet_tree.headerItem().setText(0, _translate("outlet_form", "出口"))
        __sortingEnabled = self.outlet_tree.isSortingEnabled()
        self.outlet_tree.setSortingEnabled(False)
        self.outlet_tree.topLevelItem(0).setText(0, _translate("outlet_form", "vent"))
        self.outlet_tree.topLevelItem(0).child(0).setText(0, _translate("outlet_form", "outlet_vent"))
        self.outlet_tree.topLevelItem(0).child(1).setText(0, _translate("outlet_form", "outlet_vc"))
        self.outlet_tree.topLevelItem(0).child(2).setText(0, _translate("outlet_form", "outlet_vl"))
        self.outlet_tree.topLevelItem(0).child(3).setText(0, _translate("outlet_form", "outlet_vr"))
        self.outlet_tree.topLevelItem(0).child(4).setText(0, _translate("outlet_form", "outlet_vd"))
        self.outlet_tree.topLevelItem(0).child(5).setText(0, _translate("outlet_form", "outlet_vp"))
        self.outlet_tree.topLevelItem(1).setText(0, _translate("outlet_form", "foot"))
        self.outlet_tree.topLevelItem(1).child(0).setText(0, _translate("outlet_form", "outlet_foot"))
        self.outlet_tree.topLevelItem(1).child(1).setText(0, _translate("outlet_form", "outlet_ffl"))
        self.outlet_tree.topLevelItem(1).child(2).setText(0, _translate("outlet_form", "outlet_ffr"))
        self.outlet_tree.topLevelItem(2).setText(0, _translate("outlet_form", "defrost"))
        self.outlet_tree.topLevelItem(2).child(0).setText(0, _translate("outlet_form", "outlet_defrost"))
        self.outlet_tree.topLevelItem(2).child(1).setText(0, _translate("outlet_form", "outlet_dc"))
        self.outlet_tree.topLevelItem(2).child(2).setText(0, _translate("outlet_form", "outlet_dl"))
        self.outlet_tree.topLevelItem(2).child(3).setText(0, _translate("outlet_form", "outlet_dr"))
        self.outlet_tree.topLevelItem(3).setText(0, _translate("outlet_form", "rear-vent"))
        self.outlet_tree.topLevelItem(3).child(0).setText(0, _translate("outlet_form", "outlet_rv"))
        self.outlet_tree.topLevelItem(4).setText(0, _translate("outlet_form", "rear-foot"))
        self.outlet_tree.topLevelItem(4).child(0).setText(0, _translate("outlet_form", "outlet_rfl"))
        self.outlet_tree.topLevelItem(4).child(1).setText(0, _translate("outlet_form", "outlet_rfr"))
        self.outlet_tree.setSortingEnabled(__sortingEnabled)
        self.chosed_label.setText(_translate("outlet_form", "已选择出口"))
        self.chosed_btn.setText(_translate("outlet_form", "确    定"))
