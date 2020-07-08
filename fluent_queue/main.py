import sys
import cgitb
import csv
import subprocess as sp
import os

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
# from PyQt5.QtCore import pyqtSignal
from ui_py.ui_queue_main import Ui_fluent_queue
from func.func_ui_set import UiSet
from func.func_account import AccVerify
from func.func_timer import LoopTimer, SleepOut, current_time, Scheduler
from func.func_list_manage import AddPj
from func.func_short_key import ShortKey
from func.func_run_calculation import Calculate
from func.func_journal import HistoryView


class MyMainWindow(QMainWindow, Ui_fluent_queue):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        # -------- prevent multi application----------
        self.app = app
        self.prevent_multiapp()
        self.ui_alter = UiSet(self)                             # UiSet is the collection of Ui change object
        self.ui_alter.set_all_icon()
        self.ui_alter.ui_user_logoff()                          # change Ui to user logoff status
        self.btn()                                              # enable button function
        # --------- initial variable--------
        self.acc_name = str()
        self.new_pj = dict()
        self.waiting_min = int()
        self.have_schedule = False
        self.pause = True
        self.database_path = r".\database"
        self.waiting_list_file = 'waiting_list.csv'
        self.running_list_file = 'running_list.csv'
        self.history_list_file = 'history_list.csv'
        self.account_file = 'account.csv'
        self.mission_list = list()
        self.running_project = list()
        # ----------initial function-----------------
        self.database_path = self.get_abs_path(self.database_path)
        self.init_data_loading()
        self.init_queue_showing()                                                      # show running and waiting list
        self.timer = LoopTimer()
        self.sleep_time = SleepOut(self, self.timer.signal_sleep_timer, 15) # create timer to logout if not operate for a long time
        self.short_key = ShortKey(self)                                                # create shortcut key
        self.calculation = Calculate(self, self.mission_list, self.running_project)    # start calculation thread
        self.schedule = Scheduler(self.timer.signal_schedule_timer)
        self.manager_authority(False)
        print('whether have manager authority?: ', self.listWidget_queue.drag_permission)
        # ---------signal connection-------------------------
        self.sleep_time.signal_time_exceed.connect(self.user_logout)
        self.calculation.signal_update_finished_log.connect(self.update_finished_list_log)
        self.calculation.signal_update_running_log.connect(self.update_running_list_log)
        self.calculation.signal_license_error.connect(self.show_status_message)
        self.schedule.signal_control_cal.connect(self.set_pause_cal)
        self.schedule.signal_waiting_min.connect(self.waiting_msg)
        self.schedule.signal_cancel_plan.connect(self.show_status_message)
        self.listWidget_queue.signal_file_receive.connect(self.receive_drop_file)
        self.listWidget_queue.signal_project_exchange.connect(self.exchange_project)
        self.show()

    def btn(self):
        self.action_login.triggered.connect(self.account_verification)
        self.action_logout.triggered.connect(self.user_logout)
        self.action_add.triggered.connect(self.add_project)
        self.action_delete.triggered.connect(self.delete_project)
        self.action_journal.triggered.connect(self.view_history_log)
        self.action_setting.triggered.connect(self.set_schedule)

    def prevent_multiapp(self):
        file_name = os.path.basename(sys.argv[0])
        rindex = file_name.rindex('.')
        application_name = file_name[:rindex]
        print('application_name:', application_name)
        count = sp.run("powershell -command $(get-process -Name %s | Group -Property name).count" % application_name,
                   stdout=sp.PIPE, stderr=sp.PIPE).stdout
        count = int(count)
        print('application_count:', count)
        if count > 1:
            QMessageBox.warning(self, '警告', '进程已经打开，请勿重复开启')
            sys.exit()

    def get_abs_path(self, relative_path):
        """
        through relative path to create abs path,
        and verify if it exist. If not, make one
        :param relative_path:
        :return: abs_path
        """
        abs_path = os.path.abspath(relative_path)
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)
        return abs_path

    def init_data_loading(self):
        self.mission_list = self.read_csv(self.waiting_list_file)
        self.running_project = self.read_csv(self.running_list_file)

    def read_csv(self, csv_name):
        """
        check if have unfinished project
        read log csv in net disk path
        :param csv_name:
        :return: read_list
        """
        read_list = list()
        csv_path = self.database_path + "\\" + csv_name
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    read_list.append(row)

        return read_list

    def init_queue_showing(self):
        """
        show unfinished items in 2 list widget
        :return:
        """
        if self.running_project:
            project = self.running_project[0]
            self.listWidget_running.addItem("用户：%s   项目： %s" % (project["account_name"],
                                                                project["project_name"]))
        if self.mission_list:
            for i in self.mission_list:
                self.listWidget_queue.addItem("用户：%s   项目： %s" % (i["account_name"], i["project_name"]))

    def account_verification(self):
        """
        AccVerify is a sub Ui for user to login
        it will verify if account and password are correct
        if correct, it will return.
        :return: a pyqtsignal(verify_success)
        """
        account_file_path = '%s/%s' % (self.database_path, self.account_file)
        self.acc_ui = AccVerify(account_file_path)
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
        self.ui_alter.ui_user_logoff(False)
        # self.action_login.setEnabled()

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
        self.add_pj_ui.signal_enable_action_add.connect(self.enable_action_add)
        self.action_add.setDisabled(True)

    def new_project(self, new_pj_dict):
        """
        When received signal from add project UI, it form new project dict
        add project to mission list, update waiting list log, add item in UI list
        :param new_pj_dict:
        :return:
        """
        self.new_pj = {"account_name": '', "project_name": '', "project_address": '', "journal": '',
                       "register_time": ''}
        self.new_pj.update(new_pj_dict)
        self.new_pj["account_name"] = self.acc_name
        self.new_pj["register_time"] = current_time()
        self.mission_list.append(self.new_pj)
        self.update_waiting_list_log()
        self.listWidget_queue.addItem("用户：%s   项目： %s" % (self.acc_name, self.new_pj["project_name"]))

    def enable_action_add(self):
        self.action_add.setEnabled(True)

    def delete_project(self):
        """
        connected by delete action
        if an item was selected, verify other information and delete
        :return:
        """
        cur_index = self.listWidget_queue.currentIndex().row()
        print(cur_index)
        if cur_index == -1:
            pass
        else:
            self.verify_delete(cur_index)

    def exchange_project(self, exchange_dict):
        original_pos = exchange_dict['original_index']
        after_pos = exchange_dict['after_index']
        project = self.mission_list[original_pos]
        del self.mission_list[original_pos]
        if after_pos == -1:
            self.mission_list.append(project)
        else:
            self.mission_list.insert(after_pos, project)
        self.update_waiting_list_log()

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
            reply = QMessageBox.warning(self, '删除警告', '删除后无法恢复，是否确认删除',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                del self.mission_list[item_index]
                print(self.mission_list)
                self.update_waiting_list_log()
                self.listWidget_queue.takeItem(item_index)

    def update_waiting_list_log(self):
        """
        use csv to record waiting list, in case main program closed accidentally.
        This func overwrite csv every time when mission list is updated.
        :return:
        """
        waiting_list_csv = r'%s\%s' % (self.database_path, self.waiting_list_file)
        header = ["account_name", "project_name", "project_address", "journal", "register_time"]
        with open(waiting_list_csv, 'w', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=header)
            csv_writer.writeheader()
            print(self.mission_list)
            if self.mission_list:
                for i in self.mission_list:
                    csv_writer.writerow(i)

    def update_finished_list_log(self, finished_project):
        """
        append new finished project to log csv
        :return:
        """
        log_csv = r'%s\%s' % (self.database_path, self.history_list_file)
        header = ["account_name", "project_name", "project_address", "journal", "register_time",
                  "start_time", "using_time", "complete_status"]
        with open(log_csv, 'a+', newline='') as f:
            f.seek(0, 0)                                           # move cursor to the beginning of file
            csv_reader = csv.reader(f)
            csv_writer = csv.DictWriter(f, fieldnames=header)
            if not [row for row in csv_reader]:
                csv_writer.writeheader()
            if finished_project:
                csv_writer.writerow(finished_project)

    def update_running_list_log(self, running_project):
        """
        update running project to log csv
        :return:
        """
        running_list_csv = r'%s\%s' % (self.database_path, self.running_list_file)
        header = ["account_name", "project_name", "project_address", "journal", "register_time"]
        with open(running_list_csv, 'w', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=header)
            csv_writer.writeheader()
            if running_project:
                csv_writer.writerow(running_project[0])

    def show_status_message(self, msg):
        self.statusbar.showMessage(msg)

    def manager_authority(self, switch):
        """
        set manager authority:
        1. able to drag item in queue list(change sequence)
        :param switch:
        :return:
        """
        self.listWidget_queue.drag_permission = switch
        print("management authority: %s" % switch)

    def view_history_log(self):
        csv_file = '%s/%s' % (self.database_path, self.history_list_file)
        self.Hist_viewer = HistoryView(csv_file, self.timer.signal_journal_timer)
        self.Hist_viewer.signal_viewer_closed.connect(self.reboot_journal_func)
        self.action_journal.setDisabled(True)

    def reboot_journal_func(self):
        self.action_journal.setEnabled(True)

    def set_schedule(self):
        self.schedule.show_ui()

    def waiting_msg(self, min):
        self.waiting_min = min
        waiting_msg = '计划任务将在%s分钟后启动' % min
        self.show_status_message(waiting_msg)

    def receive_drop_file(self, file):
        if self.action_add.isEnabled():
            self.action_add.trigger()
            if '.jou' in file:
                self.add_pj_ui.btn_extend.click()
                self.add_pj_ui.checkbox_journal.click()
                self.add_pj_ui.edit_journal_address.setText(file)
            else:
                self.add_pj_ui.edit_project_address.setText(file)

    def toggle_pause_cal(self):
        if self.pause:
            self.pause = False
        else:
            self.pause = True

        self.show_status_message('后续计算任务停止：%s' % self.pause)
        print('calculation queue paused:', self.pause)

    def set_pause_cal(self, status):
        self.pause = status
        self.have_schedule = status
        self.show_status_message('后续计算任务停止：%s' % self.pause)
        print('calculation queue paused:', self.pause)


if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myWin = MyMainWindow(app)
    app.installEventFilter(myWin)
    sys.exit(app.exec_())

