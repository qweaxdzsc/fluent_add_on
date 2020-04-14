import csv
import time
import subprocess

from PyQt5.QtCore import pyqtSignal, QThread, QFileInfo

from func.func_timer import current_time


class Calculate(QThread):
    """ create calculation thread"""
    time_count = pyqtSignal(int)

    def __init__(self, ui, mission_list, running_project):
        super(Calculate, self).__init__()
        self.ui = ui
        self.mission_list = mission_list
        self.running_project = running_project
        # ------------init variable------------
        self.finished_project = dict()
        self.start_time = float()
        self.start_time_str = str()
        self.finish_time = float()
        self.use_time = float()
        self.complete_status = 'complete'

    def run(self):
        """
        Thread main func:
        1. first check if have history running project remain
        2. do while loop to take item from mission_list to running list
        3. in while loop do calculation
        :return:
        """
        if self.running_project:
            time.sleep(1)
            self.calculation()
        while True:
            time.sleep(1)
            if self.mission_list:
                self.running_show()
                del self.mission_list[0]
                self.ui.update_waiting_list_log()
                self.ui.listWidget_queue.takeItem(0)
                # time.sleep(20)
                self.calculation()

    def running_show(self):
        """
        show project which is running right now
        :return:
        """
        user = self.mission_list[0]["account_name"]
        project = self.mission_list[0]["project_name"]
        self.running_project.append(self.mission_list[0])
        self.update_running_list_log()
        self.ui.listWidget_running.addItem("用户：%s   项目： %s" % (user, project))

    def calculation(self):
        """
        used for fluent calculation
        1. open a pipe to run fluent with journal script
        2. check running status by while loop, end loop when pipe closed
        3. when loop done, check result and call finish function
        :return:
        """
        self.start_time = time.time()
        self.start_time_str = current_time()
        cores = 12
        running_journal = self.running_project[0]["journal"]

        p = subprocess.Popen(r'cd C:\Program Files\ANSYS Inc\v201\fluent\ntbin\win64 && '
                             r'fluent 3d -t%s -i %s' % (cores, running_journal), shell=True,
                             stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True)
        while p.poll() == None:                         # block calculation thread until finished
            time.sleep(5)
            line = p.stdout.readline()
            msg = line
            print(msg)

        print('finish')
        self.complete_status = self.check_result()
        print(self.complete_status)
        # TODO determine whether it is finished
        self.finish_time = time.time()
        self.finish_cal()

    def finish_cal(self):
        """
        take item in running list, both ui and list
        append finished_list_log
        :return:
        """
        self.ui.listWidget_running.takeItem(0)
        self.form_finish_project_info()
        self.update_finished_list_log()
        self.running_project.clear()
        self.update_running_list_log()

    def form_finish_project_info(self):
        """
        when finished, form finished project dict
        1. record project info inherited from running project dict
        2. record finished time, use time
        3. record complete status
        :return:
        """
        self.finished_project = self.running_project[0]
        use_time = self.finish_time - self.start_time
        print(use_time)
        using_hour = int(use_time / 3600)
        using_min = int((use_time % 3600) / 60)
        using_seconds = int(use_time % 60)
        self.use_time = "%s小时%s分钟%s秒" % (using_hour, using_min, using_seconds)

        self.finished_project["start_time"] = self.start_time_str
        self.finished_project["using_time"] = self.use_time
        self.finished_project["complete_status"] = self.complete_status
    
    def update_finished_list_log(self):
        """
        append new finished project to log csv
        :return:
        """
        log_csv = r'S:\PE\Engineering database\CFD\03_Tools\queue_backup\history_list.csv'
        header = ["account_name", "project_name", "project_address", "journal", "register_time",
                  "start_time", "using_time", "complete_status"]
        with open(log_csv, 'a+', newline='') as f:
            f.seek(0, 0)                                           # move cursor to the beginning of file
            csv_reader = csv.reader(f)
            csv_writer = csv.DictWriter(f, fieldnames=header)
            if not [row for row in csv_reader]:
                csv_writer.writeheader()
            # print(self.finished_project)
            if self.finished_project:
                csv_writer.writerow(self.finished_project)

    def update_running_list_log(self):
        """
        update running project to log csv
        :return:
        """
        running_list_csv = r'S:\PE\Engineering database\CFD\03_Tools\queue_backup\running_list.csv'
        header = ["account_name", "project_name", "project_address", "journal", "register_time"]
        with open(running_list_csv, 'w', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=header)
            csv_writer.writeheader()
            # print(self.running_project)
            if self.running_project:
                csv_writer.writerow(self.running_project[0])

    def check_result(self):
        """
        check if fluent produced result
        :return: str(describe result)
        """
        case_path = self.running_project[0]["project_address"]
        case_name = self.running_project[0]["project_name"]
        result_txt = case_path + "\\%s_result\\totalresult.txt" % case_name
        result_file = QFileInfo(result_txt)
        if result_file.exists():
            return 'result produced'
        else:
            return 'no result'


class CheckResult(QThread):
    """ create checking thread"""
    def __init__(self):
        super(CheckResult, self).__init__()
        pass


class CheckLicense(QThread):
    """ create checking thread"""
    def __init__(self):
        super(CheckLicense, self).__init__()
        pass
