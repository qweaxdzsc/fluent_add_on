import subprocess
import time

from PyQt5.QtCore import pyqtSignal, QThread, QFileInfo, QDir
from func.func_ansys_license import LicenseUsage
from func.func_timer import current_time


class Calculate(QThread):
    """ create calculation thread"""
    signal_time_count = pyqtSignal(int)
    signal_update_finished_log = pyqtSignal(dict)
    signal_update_running_log = pyqtSignal(list)
    signal_license_error = pyqtSignal(str)

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

    def run(self):
        """
        Thread main func:
        1. first check if have history running project remain
        2. do while loop to take item from mission_list to running list
        3. in while loop do calculation
        :return:
        """
        time.sleep(2)
        ansys_license = LicenseUsage()
        if not self.ui.pause:
            if ansys_license.is_enough(self.cores):
                if self.running_project:
                        self.calculation()
        while True:
            time.sleep(1)
            if not self.ui.pause:
                if self.mission_list:
                    ansys_license = LicenseUsage()
                    if ansys_license.is_enough(self.cores):
                        self.signal_license_error.emit('')
                        self.running_show()
                        del self.mission_list[0]
                        self.ui.update_waiting_list_log()
                        self.ui.listWidget_queue.takeItem(0)
                        self.calculation()
                    else:
                        self.signal_license_error.emit('not enough license')
                        time.sleep(3)
                else:
                    time.sleep(2)
            else:
                time.sleep(2)

    def running_show(self):
        """
        show project which is running right now
        :return:
        """
        user = self.mission_list[0]["account_name"]
        project = self.mission_list[0]["project_name"]
        self.running_project.append(self.mission_list[0])
        self.signal_update_running_log.emit(self.running_project)
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
        running_journal = self.running_project[0]["journal"]
        project_address = self.running_project[0]['project_address']
        disk = project_address[:2]
        # go to disk first, then go to directory, then launch fluent and its launching options
        p = subprocess.Popen(r'%s &&'
                             r'cd %s &&'
                             r'"C:\Program Files\ANSYS Inc\v191\fluent\ntbin\win64\fluent" 3d -t%s -i %s -mpi=ibmmpi'
                             r' -cnf=C:\Users\BZMBN4\Desktop\host_BZMBN4.txt' %
                             (disk, project_address, self.cores, running_journal),
                             shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True)
        # while p.poll() == None:                                     # block calculation thread until finished
        #     time.sleep(5)
            # line = p.stdout.readline()
        transcript_name = '%s_transcript' % self.running_project[0]['project_name']
        self.calguard = CalGuard(project_address, transcript_name)
        self.calguard.start()
        out, err = p.communicate()
        self.calguard.quit()

        print('finish')
        self.complete_status = self.check_result()
        print(self.complete_status)
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
    def __init__(self, directory, transcript_name):
        super().__init__()
        self.dir = directory
        self.transcript = '%s\%s' % (directory, transcript_name)
        self.wait_time = 60
        self.check_interval = 200

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
        line_count_new = 1
        while line_count_new > line_count:
            time.sleep(check_interval)
            line_count = line_count_new
            with open(self.transcript, 'r') as f:
                content = f.readlines()
                line_count_new = len(content)
                print(line_count_new)

        print('transcript finish')

    def ensure_finish(self, dir):
        folder = QDir(dir)
        file_list = folder.entryInfoList(QDir.Files | QDir.CaseSensitive)
        for i in file_list:
            if i.suffix() == 'bat':
                print(i.absoluteFilePath())
                subprocess.call(i.absoluteFilePath(), shell=True)
        print('no bat file now')
        print('\nall finished')

