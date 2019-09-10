# import os, signal
# import time
#
# path = r'C:\Users\BZMBN4\Desktop\123'
# n = 0
# time_step = 2
#
# while n < 1:
#     if os.path.exists(path) == False:
#         n = n + 1
#         time.sleep(time_step)
#         print('已计算%s秒，正等待计算完成'%(n*time_step))
#     else:
#         print('计算已完成，开始整理报告')
#         break
#
# else:
#     print('程序可能出错，请手动杀死程序')
#     os.kill('EXCEL.EXE', '1')


import os
import sys
import string
import psutil
import signal
#print os.getpid()


def getAllPid():
    pid_dict={}
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        pid_dict[pid]= p.name()
        #print("pid-%d,pname-%s" %(pid,p.name()))
    return pid_dict

pic_dict = getAllPid()
print(pic_dict)