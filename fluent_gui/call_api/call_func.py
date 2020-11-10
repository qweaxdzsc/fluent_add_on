import subprocess
from PyQt5.QtCore import QThread, pyqtSignal
import time


class SCDM(QThread):
    finishCAD = pyqtSignal(str)

    def __init__(self, py_script):
        super(SCDM, self).__init__()
        self.py_script = py_script

    def run(self):
        p = subprocess.Popen(r'cd C:\Program Files\ANSYS Inc\v201\scdm && SpaceClaim.exe /RunScript="%s"' % self.py_script,
                             shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        # out = out.decode()

        self.finishCAD.emit('CAD软件已关闭')


class fluent_mesh(QThread):
    mesh_feedback = pyqtSignal(str)
    mesh_timeuse = pyqtSignal(int)
    mesh_finish = pyqtSignal(str)

    def __init__(self, tui):
        super(fluent_mesh, self).__init__()
        self.tui = tui

    def run(self):
        start_time = time.strftime('%M:%S', time.localtime(time.time()))
        # self.p = subprocess.Popen(r'cd C:\\Program Files\\ANSYS Inc\\v191\\fluent\\ntbin\\win64 && '
        #                    r'fluent 3d -meshing -t4 -gu -i %s' % (self.tui),
        #                           shell=True, stdout=subprocess.PIPE)

        self.p = subprocess.Popen(r'cd C:\\Program Files\\ANSYS Inc\\v201\\fluent\\ntbin\\win64 && '
                                  r'fluent 3d -meshing -t4', shell=True, stdout=subprocess.PIPE)
        nl = 0
        finish_count = 0
        while self.p.poll() == None:
            nl += 1
            line = self.p.stdout.readline()
            self.msg = line.decode()
            print(nl, self.msg)

            if (nl > 30) & (nl <= 50):
                self.stage_report('Cleanup script file is', 'load_time_begin', '载入模型', 29)
            elif (nl > 50) & (nl <= 130):
                self.stage_report('They will be imported in whatever units they were created', 'face_mesh_time_start',
                '处理面网格', 80)
            elif (nl > 130) & (nl <= 200):
                if 'the previous max quality' in self.msg:
                    msg_strip = self.msg.strip()
                    face_mesh_quality = msg_strip[-8:]
                self.stage_report('/objects/volumetric-regions/compute', 'volume_mesh_time_start',
                                  '处理体网格', 83)
            elif (nl > 200) & (nl <= 420):
                self.stage_report('/mesh/check-quality', 'mesh_finish_time', '网格生成完毕', 113)
                if 'Minimum Orthogonal Quality' in self.msg:
                    msg_strip = self.msg.strip()
                    volume_mesh_quality = float(msg_strip[-11:-7])/10.0
            elif (nl > 420) & (finish_count < 2):
                if 'Writing "' in self.msg:
                    finish_count = 1
                if finish_count == 1:
                    if 'Done.' in self.msg:
                        finish_count = 2
                        end_time = time.strftime('%M:%S', time.localtime(time.time()))
                        print(end_time)
                        print('总共有%s行输出语句' % nl)
        else:
            self.mesh_timeuse.emit(120)
            self.mesh_finish.emit('网格生成完毕')

    def stage_report(self, stage_marker, stage_name, report_msg, timeuse):
        if stage_marker in self.msg:
            stage_time = time.strftime('%M:%S', time.localtime(time.time()))
            self.mesh_feedback.emit(report_msg)
            self.mesh_timeuse.emit(timeuse)
            print('%s%s' % (stage_name, stage_time))

    def stop_mesh(self):
        self.p.terminate()


class fluent_solver(QThread):
    solver_feedback = pyqtSignal(str)

    def __init__(self, tui):
        super(fluent_solver, self).__init__()
        self.tui = tui

    def run(self):
        self.p = subprocess.Popen(r'cd C:\\Program Files\\ANSYS Inc\\v191\\fluent\\ntbin\\win64 && '
                           r'fluent 3d -t12 -i %s' % (self.tui), shell=True, stdout=subprocess.PIPE)

        nl = 0
        finish_count = 0
        while self.p.poll() == None:
            line = self.p.stdout.readline()
            self.msg = line.decode()
            print(nl, self.msg)
            nl += 1

        print('总共有%s行输出语句'%nl)

    def stop_solver(self):
        self.p.terminate()