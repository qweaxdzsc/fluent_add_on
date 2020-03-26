import time
import os
import random


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
        self.main_ui.valve_c.hide()
        self.main_ui.temp_c.hide()
        self.main_ui.fan_c.hide()

    def default_part_tree(self):
        """default setting for which model part in the tree should be checked"""
        self.main_ui.part_tree.topLevelItem(0).setCheckState(0, 0)   # 0 means unchecked, 2 means checked
        self.main_ui.part_tree.topLevelItem(1).setCheckState(0, 2)
        self.main_ui.part_tree.topLevelItem(2).setCheckState(0, 0)
        self.main_ui.part_tree.topLevelItem(3).setCheckState(0, 0)
        self.main_ui.part_tree.topLevelItem(4).setCheckState(0, 0)
        self.main_ui.part_tree.topLevelItem(5).setCheckState(0, 0)
        self.main_ui.part_tree.topLevelItem(6).setCheckState(0, 0)
        self.main_ui.part_tree.topLevelItem(7).setCheckState(0, 2)
        self.main_ui.part_tree.topLevelItem(8).setCheckState(0, 2)
        self.main_ui.part_tree.topLevelItem(9).setCheckState(0, 0)
        self.main_ui.part_tree.topLevelItem(10).setCheckState(0, 0)
        self.main_ui.part_tree.topLevelItem(11).setCheckState(0, 0)
        self.main_ui.distrib_number.setValue(1)
        self.main_ui.valve_number.setValue(0)
