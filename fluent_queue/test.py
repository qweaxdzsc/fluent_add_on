from PyQt5.QtCore import pyqtSignal, QThread, QFileInfo, QDir
# from func.func_ansys_license import LicenseAnsys
from func.func_timer import current_time

path = r'G:\test\queue_test1'
a = QFileInfo(path + '\\test2.jou')
print(a.fileName())
folder = QDir(path)
file_list = folder.entryInfoList(QDir.Files | QDir.CaseSensitive)
print(file_list[0].fileName())