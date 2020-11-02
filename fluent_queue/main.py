import sys
import cgitb
import csv
import subprocess as sp
import os
import configparser

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QTranslator                                 # used by exec(), do not delete
from ui_py.ui_queue_main import Ui_fluent_queue
from func.func_ui_set import UiSet
from func.func_account import AccVerify
from func.func_timer import LoopTimer, SleepOut, current_time, Scheduler
from func.func_list_manage import AddPj
from func.func_short_key import ShortKey
from func.func_run_calculation import Calculate
from func.func_journal import HistoryView
from func.func_setting import Setting
from func.func_trayicon import TrayIcon
from ui_translate.msg_translator import MsgTranslator


class MyMainWindow(QMainWindow, Ui_fluent_queue):
    def __init__(self):
        super().__init__()
        # ---------language set----------------------
        self._parse_config()
        self.msg_trans = MsgTranslator(self.language)
        self.make_trans = self.msg_trans.make_trans
        # -------- prevent multi application----------
        self.prevent_multiapp()
        # ---------init UI set---------------------------
        self.setupUi(self)
        self.ui_alter = UiSet(self)                             # UiSet is the collection of Ui change object
        self.ui_alter.set_all_icon()
        self.ui_alter.ui_user_logoff()                          # change Ui to user logoff status
        self.btn()                                              # enable button function
        # --------- initial variable--------
        self.acc_name = str()
        self.new_pj = dict()
        self.waiting_min = int()
        self.main_path = os.getcwd()
        self.database_path = r".\database"
        self.waiting_list_file = 'waiting_list.csv'
        self.running_list_file = 'running_list.csv'
        self.history_list_file = 'history_list.csv'
        self.account_file = 'account.csv'
        self.mission_list = list()
        self.running_project = list()
        # ----------initial function-----------------
        self.main_path = self.get_abs_path(os.getcwd())
        print("main_path: ", self.main_path)
        self.database_path = self.get_abs_path(self.database_path)
        self.init_data_loading()
        self.init_queue_showing()                                                      # show running and waiting list
        self.timer = LoopTimer()
        self.sleep_time = SleepOut(self, self.timer.signal_sleep_timer, 15) # create timer to logout if not operate for a long time
        self.short_key = ShortKey(self)                                                # create shortcut key
        self.calculation = Calculate(self, self.mission_list, self.running_project)    # start calculation thread
        self.schedule = Scheduler(self.timer.signal_schedule_timer)
        self.manager_authority(False)
        self._translator()
        # ---------signal connection-------------------------
        self.sleep_time.signal_time_exceed.connect(self.user_logout)
        self.calculation.signal_update_finished_log.connect(self.update_finished_list_log)
        self.calculation.signal_update_running_log.connect(self.update_running_list_log)
        self.calculation.signal_license_info.connect(self.show_status_message)
        self.schedule.signal_control_cal.connect(self.set_pause_cal)
        self.schedule.signal_waiting_min.connect(self.waiting_msg)

        self.listWidget_queue.signal_file_receive.connect(self.receive_drop_file)
        self.listWidget_queue.signal_project_exchange.connect(self.exchange_project)
        self.listWidget_queue.signal_drop_reject.connect(self.show_status_msg_trans)
        self.show()

    def btn(self):
        self.action_login.triggered.connect(self._account_verification)
        self.action_logout.triggered.connect(self.user_logout)
        self.action_add.triggered.connect(self.add_project)
        self.action_delete.triggered.connect(self.delete_project)
        self.action_journal.triggered.connect(self.view_history_log)
        self.action_setting.triggered.connect(self.show_setting)

    def _parse_config(self):
        config = configparser.ConfigParser()
        config.read(r'.\config\config.ini')
        self.language = config['Language']['language']

    def _translator(self):
        self.file_basename_list = []
        self.translator_list = []
        file_list = os.listdir('./ui_translate')
        for file in file_list:
            if file.endswith('.qm'):
                file_basename = file.replace('.qm', '')
                self.file_basename_list.append(file_basename)
                exec('self.trans_%s = QTranslator()' % file_basename)
                exec('self.translator_list.append(self.trans_%s)' % file_basename)

        for index, item in enumerate(self.translator_list):
            item.load("./ui_translate/%s.qm" % (self.file_basename_list[index]))

        self.enable_translate(self.language)

    def enable_translate(self, language):
        self.language = language
        self.msg_trans.language = language
        if self.acc_name:
            # show translated title when login
            window_title = self.make_trans('welcome') + self.acc_name
            self.setWindowTitle(window_title)
        _app = QApplication.instance()
        if language == 'English':
            for item in self.translator_list:
                _app.installTranslator(item)
        else:
            for item in self.translator_list:
                _app.removeTranslator(item)
        self.retranslateUi(self)

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
            QMessageBox.warning(self, self.make_trans('warning'), self.make_trans('already_open'))
            sys.exit()

    def get_abs_path(self, path):
        """
        through relative path to create abs path,
        and verify if it exist. If not, make one
        :param path:
        :return: abs_path
        """
        abs_path = os.path.abspath(path)
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
            self.listWidget_running.addItem("User：%s   Project： %s" % (project["account_name"], project["project_name"]))
        if self.mission_list:
            for i in self.mission_list:
                self.listWidget_queue.addItem("User：%s   Project： %s" % (i["account_name"], i["project_name"]))

    def _account_verification(self):
        """
        AccVerify is a sub Ui for user to login
        it will verify if account and password are correct
        if correct, it will return.
        :return: a pyqtsignal(verify_success)
        """
        account_file_path = '%s/%s' % (self.database_path, self.account_file)
        self.acc_ui = AccVerify(account_file_path, self.msg_trans)
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
        window_title = self.make_trans('welcome') + acc_name
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
        self.setWindowTitle(self.make_trans('login_unlock'))
        self.manager_authority(False)

    def add_project(self):
        """
        create add project UI
        connect new project info signal to new project func
        :return:
        """
        self.add_pj_ui = AddPj(self.msg_trans)
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
        self.new_pj["register_time"] = current_time("%Y-%m-%d %H:%M:%S")
        self.mission_list.append(self.new_pj)
        self.update_waiting_list_log()
        self.listWidget_queue.addItem("User：%s   Project： %s" % (self.acc_name, self.new_pj["project_name"]))

    def enable_action_add(self):
        self.action_add.setEnabled(True)

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
            reply = QMessageBox.warning(self, self.make_trans('delete_warning'), self.make_trans('confirm_delete'),
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                del self.mission_list[item_index]
                print('delete mission: ', self.mission_list)
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
            print('update waiting list csv:', self.mission_list)
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
        header = ["account_name", "project_name", "project_address", "journal", "register_time",
                  "start_time"]
        with open(running_list_csv, 'w', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=header)
            csv_writer.writeheader()
            if running_project:
                csv_writer.writerow(running_project[0])

    def show_status_message(self, msg):
        self.statusbar.showMessage(msg)

    def show_status_msg_trans(self, msg):
        self.statusbar.showMessage(self.trans(msg))

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

    def show_setting(self):
        self.setting_ui = Setting(self.calculation.pause, self.calculation.cores,
                                  self.schedule.have_schedule, self.schedule.waiting_min, self.language)
        self.setting_ui.signal_suspend_status.connect(self.set_pause_cal)
        self.setting_ui.signal_core_number.connect(self.define_cores)
        self.setting_ui.signal_schedule_status.connect(self.schedule.enable_schedule)
        self.setting_ui.signal_waiting_min.connect(self.schedule.receive_waiting_min)
        self.setting_ui.signal_cancel_plan.connect(self.show_status_message)
        self.setting_ui.signal_change_language.connect(self.enable_translate)

    def waiting_msg(self, min):
        self.waiting_min = min
        waiting_msg = self.make_trans('plan_launch') + ' %s ' % min + self.make_trans('minutes')
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

        if self.calculation.pause:
            self.calculation.pause = False
        else:
            self.calculation.pause = True

        self.show_status_message(self.make_trans('suspend_next') + '%s' % self.calculation.pause)
        print('calculation queue paused:', self.calculation.pause)

    def set_pause_cal(self, status):
        self.calculation.pause = status
        self.show_status_message(self.make_trans('suspend_next') + '%s' % self.calculation.pause)
        print('calculation queue paused:', self.calculation.pause)

    def define_cores(self, cores):
        self.calculation.cores = cores
        print('calculation cores:', self.calculation.cores)

    def closeEvent(self, event, close_signal=False):
        """
        rewrite close event to tray icon
        :param event:
        :return:
        """
        print(close_signal)
        if close_signal:
            print('here signal: %s' % close_signal)
            event.accept()
        else:
            event.ignore()
            self.hide()
            self.trayicon = TrayIcon(self.msg_trans)
            self.trayicon.signal_show_main.connect(self.show)
            self.trayicon.signal_exit_main.connect(self.close)
            # self.trayicon


if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    app.installEventFilter(myWin)
    sys.exit(app.exec_())

