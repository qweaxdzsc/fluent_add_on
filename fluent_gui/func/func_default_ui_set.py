import time
import os
import random
from PyQt5.QtWidgets import QLabel, QGroupBox, QGridLayout, QSpacerItem, QSizePolicy, QLineEdit
from PyQt5.QtCore import QSize


class default_ui(object):
    def __init__(self, main_ui):
        self.main_ui = main_ui                                          # receive ui
        self.get_date()
        self.account_info()
        self.mode_ui_default()

    def get_date(self):
        """use time module to get today's date,
            then print it on the main ui"""
        today = time.strftime('%y%m%d', time.localtime(time.time()))
        self.main_ui.version_date_edit.setText(today)

    def account_info(self):
        """get system's account name and print it.
            Also randomly print welcome word"""
        user = os.environ.get("USERNAME")
        self.main_ui.username_label.setText('欢迎大佬%s' % user)
        welcome_list = ['Hi,大佬%s，我们又见面了' % user, 'Hello,欢迎大佬%s' % user]

        welcome_word = random.choice(welcome_list)
        self.main_ui.interact_edit.append(welcome_word)

    def mode_ui_default(self):
        """default ui setup, decide which should be hide"""
        self.main_ui.mode_info_frame.show()
        self.main_ui.start_btn.hide()
        self.main_ui.mass_inlet_c.hide()
        self.main_ui.return_btn.hide()
        self.main_ui.evap_c.hide()
        self.main_ui.hc_c.hide()
        self.main_ui.filter_c.hide()
        self.main_ui.solver_btn.hide()
        self.main_ui.temp_c.hide()
        self.main_ui.fan_c.hide()
        self.without_valve()

    def default_part_tree(self):
        """default setting for which model part in the tree should be checked"""
        self.main_ui.part_tree.topLevelItem(0).setCheckState(0, 0)   # 0 means unchecked, 2 means checked
        self.main_ui.part_tree.topLevelItem(1).setCheckState(0, 0)
        self.main_ui.part_tree.topLevelItem(2).setCheckState(0, 0)
        self.main_ui.part_tree.topLevelItem(3).setCheckState(0, 0)
        self.main_ui.part_tree.topLevelItem(4).setCheckState(0, 0)
        self.main_ui.part_tree.topLevelItem(5).setCheckState(0, 0)
        self.main_ui.part_tree.topLevelItem(6).setCheckState(0, 2)
        self.main_ui.part_tree.topLevelItem(7).setCheckState(0, 2)
        self.main_ui.part_tree.topLevelItem(8).setCheckState(0, 2)
        self.main_ui.part_tree.topLevelItem(9).setCheckState(0, 0)
        self.main_ui.part_tree.topLevelItem(10).setCheckState(0, 0)
        self.main_ui.energy_checkbox.setChecked(False)
        self.main_ui.distrib_number.setValue(1)
        self.main_ui.valve_number.setValue(0)

    def without_valve(self):
        try:
            valve_box = self.main_ui.findChild(QGroupBox, 'valve_c')
            valve_box.deleteLater()
        except Exception as e:
            print(e)

    def add_valve_c(self, area, layout, valve_number):
        self.valve_c = QGroupBox(area)
        self.valve_c.setObjectName("valve_c")
        self.gridLayout_4 = QGridLayout(self.valve_c)
        self.gridLayout_4.setContentsMargins(40, 10, 40, 10)
        self.gridLayout_4.setHorizontalSpacing(40)
        self.gridLayout_4.setVerticalSpacing(10)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.valve_rp_edit = QLineEdit(self.valve_c)
        self.valve_rp_edit.setMinimumSize(QSize(132, 22))
        self.valve_rp_edit.setMaximumSize(QSize(132, 22))
        self.valve_rp_edit.setObjectName("valve_rp_edit")
        self.gridLayout_4.addWidget(self.valve_rp_edit, 0, 1, 1, 1)
        self.valve_rp_label = QLabel(self.valve_c)
        self.valve_rp_label.setMinimumSize(QSize(100, 0))
        self.valve_rp_label.setMaximumSize(QSize(100, 16777215))
        self.valve_rp_label.setObjectName("valve_rp_label")
        self.gridLayout_4.addWidget(self.valve_rp_label, 0, 0, 1, 1)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 2, 1, 1)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 0, 3, 1, 1)
        layout.addWidget(self.valve_c)
        self.valve_c.setTitle("风门转动参数")
        self.valve_rp_label.setText("每转比例(%)")
        for i in range(valve_number):
            row = int(i / 2)
            col = (i % 2) * 2
            self.valve_td_label = QLabel(self.valve_c)
            self.valve_td_label.setMinimumSize(QSize(100, 0))
            self.valve_td_label.setMaximumSize(QSize(100, 16777215))
            self.valve_td_label.setObjectName("valve%s_td_label" % (i + 1))
            self.valve_td_label.setText('风门%s行程' % (i + 1))
            self.gridLayout_4.addWidget(self.valve_td_label, row + 1, col, 1, 1)
            self.valve_td_edit = QLineEdit(self.valve_c)
            self.valve_td_edit.setMinimumSize(QSize(132, 22))
            self.valve_td_edit.setMaximumSize(QSize(132, 22))
            self.valve_td_edit.setObjectName("valve%s_td_edit" % (i + 1))
            self.gridLayout_4.addWidget(self.valve_td_edit, row + 1, col + 1, 1, 1)

        return self.valve_c