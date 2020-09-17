from PyQt5.QtCore import QFileInfo, QDir
import subprocess
#
# class CalGuard(QThread):
#     """thread ensures calculation normally"""
#     def __init__(self, directory, project_name):
#         super().__init__()
#         self.dir = directory
#         transcript_name = '%s_transcript.txt' % project_name
#         self.transcript = '%s\\%s' % (directory, transcript_name)
#         print('transcript path:', self.transcript)
#         self.wait_time = 50
#         self.check_interval = 150
#
#     def run(self):
#         print('start Guard')
#         time.sleep(self.wait_time)
#         file_transcript = QFileInfo(self.transcript)
#         if file_transcript.isFile():
#             print('have transcript')
#             self.check_transcript(self.check_interval)
#             self.ensure_finish(self.dir)
#         else:
#             print('Warning: Error, transcript dose not exist')
#
#     def check_transcript(self, check_interval):
#         line_count = 0
#         line_count_new = self.get_line_count()
#
#         while line_count_new > line_count:
#             time.sleep(check_interval)
#             line_count = line_count_new
#             line_count_new = self.get_line_count()
#
#     def get_line_count(self):
#         with open(self.transcript, 'r') as f:
#             content = f.readlines()
#             line_count_new = len(content)
#             print('transcript line Count:', line_count_new)
#
#         return line_count_new
#
#     def ensure_finish(self, dir):
#         print('no new line in transcript')
#         folder = QDir(dir)
#         file_list = folder.entryInfoList(QDir.Files | QDir.CaseSensitive)
#         bat_file_name = ''
#         with open(self.transcript, 'r') as f:
#             content = f.readlines()
#             for line in content:
#                 if 'host' in line:
#                     line = line.split()
#                     host_name = line[1]
#                     pid = line[3]
#                     bat_file_name = 'cleanup-fluent-%s-%s.bat' % (host_name, pid)
#                     print(f'run .bat file: {bat_file_name}')
#
#         for i in file_list:
#             if i.fileName() == bat_file_name:
#                 print('.bat address', i.absoluteFilePath())
#                 subprocess.call(i.absoluteFilePath(), shell=True)
#         print('\nall finished')
#         self.quit()
import os
dir = r'G:\_HAVC_Project\GEM\GEM_01_vent\GEM_V7.2_vent\GEM_V7.2_vent_mesh.cas.h5'
case_path = QFileInfo(dir)
file_name = case_path.fileName()
base_name = file_name.rsplit('.jou', 1)
print(base_name)
(filename, extension) = os.path.splitext(case_path.fileName())
print(case_path.fileName())
print(filename)
