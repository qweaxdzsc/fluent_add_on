import subprocess
import threading

p = subprocess.Popen(r'cd C:\\Program Files\\ANSYS Inc\\v191\\fluent\\ntbin\\win64 && '
                          r'fluent 3d -t12 -gu' , shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                     stderr=subprocess.PIPE, universal_newlines=True)

msg = ''


def read_line(p):

    nl = 0
    finish_count = 0
    global msg

    while p.poll() == None:
        line = p.stdout.readline()
        msg = line
        print(nl, msg)
        nl += 1

    print('总共有%s行输出语句' % nl)


def into_fluent(p):
    while True:
        if 'Cleanup script file' in msg:
            print('receive')
            p.stdin.write("/file/read G:\_HAVC_Project\D2U-2\D2U-2_vent\D2U-2_distribution_V1\D2U-2_vent_V1_mesh.msh yes")
            p.stdin.flush()


read_thread = threading.Thread(target=read_line, args=[p])
read_thread.start()
in_thread = threading.Thread(target=into_fluent, args=[p])
in_thread.start()


