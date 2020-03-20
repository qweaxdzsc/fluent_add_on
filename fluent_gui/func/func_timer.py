from PyQt5.QtCore import pyqtSignal, QThread, QTimer
import os


class test_timer(QThread):
    """ create timer thread"""
    time_count = pyqtSignal(int)
    
    def __init__(self, second):
        super(test_timer, self).__init__()
        self.second = second
        self.step = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)                # set timer to send signal every one second
        self.timer.timeout.connect(self.show_time)
        self.timer.start()

    def run(self):
        pass

    def show_time(self):
        if self.step < self.second:                 # stop if reach goal seconds, otherwise keep emit signal
            self.step += 1
            self.time_count.emit(self.step)
        else:
            self.timer.stop()
        

class launch_time_count(object):
    """ used for showing the process of launching Space claim"""
    def __init__(self, ui, seconds):
        self.ui = ui
        self.launch_progress_display(seconds)

    def launch_progress_display(self, seconds):
        self.launch_time = test_timer(seconds)                  # create time thread
        self.launch_time.start()
        self.launch_time.time_count.connect(self.time_bar)      

    def time_bar(self, seconds):
        """showing progress of time running, the sign ' (⊙_⊙) ' will add up"""
        self.ui.interact_edit.undo()
        cad_progress = '正在打开CAD, 请大佬耐心等待' + ' (⊙_⊙) ' * (seconds + 1)
        self.ui.append_text(cad_progress)


class mesh_clock(object):
    """ used for showing the process of meshing"""
    def __init__(self, ui, total_time):
        self.ui = ui
        self.total_time = total_time

    def mesh_time(self):
        """use timer to count time, and may use file size to predict mesh time in future"""
        try:
            size = self.get_FileSize(self.ui.pamt['cad_save_path'])
            print("文件路径：%s\n大小：%s MB" % (self.ui.pamt['cad_save_path'], size))
        except Exception as e:
            self.ui.append_text('模型文件未找到，请检查')

        self.mesh_timer = test_timer(self.total_time)
        self.mesh_timer.time_count.connect(self.mesh_clock_show)

    def get_FileSize(self, file_path):
        fsize = os.path.getsize(file_path)
        fsize = fsize / float(1024 * 1024)
        return round(fsize, 3)

    def mesh_clock_show(self, step):
        """ showing mesh stage and remain time and a fun dot visual effect"""
        dot_list = ['.   ', '..  ', '... ', '....']
        remain_time = self.total_time - step
        dot_circle = dot_list[step % 4]
        remain_time_string = '   网格阶段剩余%s秒' % (remain_time)
        clock_msg = self.ui.mesh_condition + dot_circle + remain_time_string

        self.ui.interact_edit.undo()
        self.ui.append_text(clock_msg)

