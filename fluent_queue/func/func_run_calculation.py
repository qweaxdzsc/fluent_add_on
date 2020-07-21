import subprocess
import time
import configparser
# import os

from PyQt5.QtCore import pyqtSignal, QThread, QFileInfo, QDir
from func.func_timer import current_time


class Calculate(QThread):
    """ create calculation thread"""
    signal_time_count = pyqtSignal(int)
    signal_update_finished_log = pyqtSignal(dict)
    signal_update_running_log = pyqtSignal(list)
    signal_license_info = pyqtSignal(str)

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
        self.cores = 24
        self.complete_status = 'complete'
        self.pause = True
        # --------------------------------------
        self.start()

    def run(self):
        """
        Thread main func:
        1. first check if have history running project remain
        2. do while loop to take item from mission_list to running list
        3. in while loop do calculation
        :return:
        """
        if self.running_project:
            self.calguard = CalGuard(self.running_project[0]['project_address'],
                                     self.running_project[0]['project_name'])
            self.calguard.start()
            while self.calguard.isRunning():
                time.sleep(4)
            self.finish_cal()
        while True:
            time.sleep(1)
            if not self.pause:
                if self.mission_list:
                    # MISSION
                    if self.enough_license(self.cores):
                        self.signal_license_info.emit('')
                        self.running_show()
                        del self.mission_list[0]
                        self.ui.update_waiting_list_log()
                        self.ui.listWidget_queue.takeItem(0)
                        # -------do task---------
                        self.do_task()
                        # ------------
                        self.finish_cal()
                    else:
                        self.signal_license_info.emit(self.ui.make_trans('no_license'))
                        time.sleep(3)
                else:
                    time.sleep(2)
            else:
                time.sleep(2)

    def enough_license(self, cores, command='-c'):
        path = r'cd app'
        config = configparser.ConfigParser()
        config.read(r'.\config\config.ini')
        app = config['license']['exe']
        p = subprocess.getoutput('cd app&%s %s %s' % (app, command, cores))
        return eval(p)

    def running_show(self):
        """
        show project which is running right now
        :return:
        """
        self.start_time = time.time()
        self.start_time_str = current_time("%Y-%m-%d %H:%M:%S")
        user = self.mission_list[0]["account_name"]
        project = self.mission_list[0]["project_name"]
        self.running_project.append(self.mission_list[0])
        self.running_project[0]['start_time'] = self.start_time_str
        self.signal_update_running_log.emit(self.running_project)
        self.ui.listWidget_running.addItem("User：%s   Project： %s" % (user, project))

    def do_task(self):
        """
        used for fluent calculation
        1. open a pipe to run fluent with journal script
        2. check running status by while loop, end loop when pipe closed
        3. when loop done, check result and call finish function
        :return:
        """
        project_address = self.running_project[0]['project_address']
        disk = project_address[:2]
        # used in eval(command)
        script = self.running_project[0]["journal"]
        cores = self.cores
        main_path = self.ui.main_path
        # parser command from config file
        config = configparser.ConfigParser()
        config.read(r'.\config\config.ini')
        software_path = config['Software']['Software_path']
        exe_name = config['Software']['exe_name']
        command = eval(config['Software']['command'])
        # go to disk first, then go to directory, then launch fluent and its launching options
        p = subprocess.Popen(r'%s &&'
                             r'cd %s &&'
                             r'"%s\%s" %s' %
                             (disk, project_address, software_path, exe_name, command),
                             shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True)
        # while p.poll() == None:
        #     time.sleep(5)
        #      line = p.stdout.readline()
        self.calguard = CalGuard(project_address,  self.running_project[0]['project_name'])
        self.calguard.start()
        out, err = p.communicate()                           # block calculation thread until finished
        self.calguard.quit()

    def finish_cal(self):
        """
        take item in running list, both ui and list
        append finished_list_log
        :return:
        """
        self.complete_status = self.check_result()
        print('result status:', self.complete_status)
        self.finish_time = time.time()
        self.ui.listWidget_running.takeItem(0)
        self.form_finish_project_info()
        self.signal_update_finished_log.emit(self.finished_project)
        self.running_project.clear()
        self.signal_update_running_log.emit(self.running_project)

    def form_finish_project_info(self):
        """
        when finished, form finished project dict
        1. record project info inherited from running project dict
        2. record finished time, use time
        3. record complete status
        :return:
        """
        start_time_str = self.running_project[0]['start_time']
        start_time_tuple = time.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        start_time = time.mktime(start_time_tuple)
        use_time = self.finish_time - start_time
        using_hour = int(use_time / 3600)
        using_min = int((use_time % 3600) / 60)
        using_seconds = int(use_time % 60)
        self.use_time = "%sH%sM%sS" % (using_hour, using_min, using_seconds)
        self.finished_project = self.running_project[0]
        self.finished_project["start_time"] = self.start_time_str
        self.finished_project["using_time"] = self.use_time
        self.finished_project["complete_status"] = self.complete_status

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


class CalGuard(QThread):
    """thread ensures calculation normally"""
    def __init__(self, directory, project_name):
        super().__init__()
        self.dir = directory
        transcript_name = '%s_transcript.txt' % project_name
        self.transcript = '%s\\%s' % (directory, transcript_name)
        print('transcript path:', self.transcript)
        self.wait_time = 50
        self.check_interval = 150

    def run(self):
        print('start Guard')
        time.sleep(self.wait_time)
        file_transcript = QFileInfo(self.transcript)
        if file_transcript.isFile():
            print('have transcript')
            self.check_transcript(self.check_interval)
            self.ensure_finish(self.dir)
        else:
            print('Warning: Error, transcript dose not exist')

    def check_transcript(self, check_interval):
        line_count = 0
        line_count_new = self.get_line_count()

        while line_count_new > line_count:
            time.sleep(check_interval)
            line_count = line_count_new
            line_count_new = self.get_line_count()

    def get_line_count(self):
        with open(self.transcript, 'r') as f:
            content = f.readlines()
            line_count_new = len(content)
            print('transcript line Count:', line_count_new)

        return line_count_new

    def ensure_finish(self, dir):
        folder = QDir(dir)
        file_list = folder.entryInfoList(QDir.Files | QDir.CaseSensitive)
        bat_file_name = ''
        with open(self.transcript, 'r') as f:
            content = f.readlines()
            for line in content:
                if 'host' in line:
                    line = line.split()
                    host_name = line[1]
                    pid = line[3]
                    bat_file_name = 'cleanup-fluent-%s-%s.bat' % (host_name, pid)

        for i in file_list:
            if i.fileName() == bat_file_name:
                print('.bat address', i.absoluteFilePath())
                subprocess.call(i.absoluteFilePath(), shell=True)
        print('\nall finished')
        self.quit()

