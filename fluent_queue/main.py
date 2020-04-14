import sys
import cgitb
import csv

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
# from PyQt5.QtCore import pyqtSignal

from ui_py.ui_queue_main import Ui_fluent_queue
from func.func_ui_set import UiSet
from func.func_account import AccVerify
from func.func_timer import SleepOut, current_time
from func.func_list_manage import AddPj
from func.func_short_key import ShortKey
from func.func_run_calculation import Calculate


class MyMainWindow(QMainWindow, Ui_fluent_queue):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.ui_alter = UiSet(self)                             # UiSet is the collection of Ui change object
        self.ui_alter.set_all_icon()
        self.ui_alter.ui_user_logoff()                          # change Ui to user logoff status
        self.btn()                                              # enable button function
        self.sleep_time = SleepOut(self, 15)                    # create timer to logout if not operate for a long time
        self.sleep_time.time_exceed.connect(self.user_logout)
        self.short_key = ShortKey(self)                         # create shortcut key
        # --------- initial_variable--------
        self.acc_name = str()
        self.new_pj = dict()
        self.mission_list = self.read_csv('waiting_list.csv')
        self.running_project = self.read_csv('running_list.csv')
        # ------------------------------------
        self.init_queue_showing()                               # show running and waiting list
        self.calculation = Calculate(self, self.mission_list, self.running_project)   # start calculation thread
        self.calculation.start()
        self.manager_authority(False)
        print('whether have manager authority?: ', self.listWidget_queue.drag_permission)

    def read_csv(self, csv_name):
        read_list = list()
        log_path = r'S:\PE\Engineering database\CFD\03_Tools\queue_backup'
        csv_path = log_path + "\\" + csv_name
        with open(csv_path, 'r') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                read_list.append(row)

        return read_list

    def init_queue_showing(self):
        if self.running_project:
            project = self.running_project[0]
            self.listWidget_running.addItem("用户：%s   项目： %s" % (project["account_name"],
                                                                project["project_name"]))
        if self.mission_list:
            for i in self.mission_list:
                self.listWidget_queue.addItem("用户：%s   项目： %s" % (i["account_name"], i["project_name"]))

    def btn(self):
        self.action_login.triggered.connect(self.account_verification)
        self.action_logout.triggered.connect(self.user_logout)
        self.action_add.triggered.connect(self.add_project)
        self.action_delete.triggered.connect(self.delete_project)

    def account_verification(self):
        """
        AccVerify is a sub Ui for user to login
        it will verify if account and password are correct
        if correct, it will return.
        :return: a pyqtsignal(verify_success)
        """
        self.acc_ui = AccVerify()
        self.acc_ui.verify_success.connect(self.user_login)

    def user_login(self, acc_name):
        """
        When login success, this func will be triggered.
        1. receive account name and set window title with it, also the using time
        2. change Ui to user login mode
        :param acc_name:
        :return: none
        """
        self.acc_name = acc_name
        window_title = '欢迎用户' + acc_name
        self.setWindowTitle(window_title)
        self.sleep_time.start_count()
        self.ui_alter.ui_user_logoff(False)

    def user_logout(self):
        """
        1. set Ui to user logoff mode
        2. change window title
        :return: none
        """
        self.ui_alter.ui_user_logoff()
        self.setWindowTitle('未登录-请登陆后使用添加删除功能')
        self.manager_authority(False)

    def add_project(self):
        """
        create add project UI
        connect new project info signal to new project func
        :return:
        """
        self.add_pj_ui = AddPj()
        self.add_pj_ui.signal_add_pj.connect(self.new_project)

    def new_project(self, new_pj_dict):
        self.new_pj = {"account_name": '', "project_name": '', "project_address": '', "journal": '',
                       "register_time": ''}
        self.new_pj.update(new_pj_dict)
        self.new_pj["account_name"] = self.acc_name
        self.new_pj["register_time"] = current_time()
        self.mission_list.append(self.new_pj)
        self.update_waiting_list_log()
        self.listWidget_queue.addItem("用户：%s   项目： %s" % (self.acc_name, self.new_pj["project_name"]))

    def delete_project(self):
        """
        connected by delete action
        if an item was selected, verify other information and delete
        :return:
        """
        cur_index = self.listWidget_queue.currentIndex().row()
        if cur_index == -1:
            pass
        else:
            self.verify_delete(cur_index)

    def verify_delete(self, item_index):
        """
        before delete:
        1. verify if the item belongs to current user
        2. let user confirm delete action first
        :param item_index:
        :return: delete item
        """
        item_belongs = self.mission_list[item_index]['account_name']
        if self.acc_name == item_belongs:
            reply = QMessageBox.warning(self, '删除警告', '删除后无法恢复，是否确认删除', QMessageBox.Yes| QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                del self.mission_list[item_index]
                print(self.mission_list)
                self.update_waiting_list_log()
                self.listWidget_queue.takeItem(item_index)

    def update_waiting_list_log(self):
        waiting_list_csv = r'S:\PE\Engineering database\CFD\03_Tools\queue_backup\waiting_list.csv'
        header = ["account_name", "project_name", "project_address", "journal", "register_time"]
        with open(waiting_list_csv, 'w', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=header)
            csv_writer.writeheader()
            print(self.mission_list)
            if self.mission_list:
                for i in self.mission_list:
                    csv_writer.writerow(i)

    def manager_authority(self, switch):
        self.listWidget_queue.drag_permission = switch


if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    app.installEventFilter(myWin)
    myWin.show()
    sys.exit(app.exec_())

