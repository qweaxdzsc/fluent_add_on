import subprocess
import threading
import time
import os

ansysPath = os.environ["AWP_ROOT201"]
fluentExe = ansysPath + r"/fluent/ntbin/win64"
print(fluentExe)
p = subprocess.Popen(r'cd %s && fluent 3d -t4 -gu' % fluentExe,
                     shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                     stderr=subprocess.PIPE)
# , universal_newlines=True

msg = ''


def read_line(p):
    nl = 0
    finish_count = 0
    global msg

    while p.poll() == None:
        line = p.stdout.readline()
        msg = line.decode()
        print(nl, msg, flush=True)
        nl += 1
        p.stdout.flush()

    print('总共有%s行输出语句' % nl)


def into_fluent(p):
    pass
    # while True:
        # time.sleep(1)
        # a = r"/file/read G:\_HAVC_Project\D2U-2\D2U-2_vent\D2U-2_distribution_V1\D2U-2_vent_V1_mesh.msh yes"
        # p.stdin.write(a)
        # p.stdin.flush()
#         if 'Cleanup script file' in msg:
#             print('receive')
#             p.stdin.write("""
# # /file/start-transcript G:/test/queue_test2\queue_test2_transcript.txt ok
# # /file/set-idle-timeout yes 1 no
# # /file/read-case/ G:/test/queue_test2/queue_test2.cas yes
# # """)
# #             p.stdin.flush()


if __name__ == '__main__':
    read_thread = threading.Thread(target=read_line, args=[p])
    read_thread.start()
    # in_thread = threading.Thread(target=into_fluent, args=[p])
    # in_thread.start()
    import tkinter as tk  # 导入TKinter模块

    ytm = tk.Tk()  # 创建Tk对象
    ytm.title("INPUT")  # 设置窗口标题
    ytm.geometry("300x100")  # 设置窗口尺寸
    user_text = tk.Entry()  # 创建文本框
    user_text.pack()


    def get_input():
        input_info = user_text.get()  # 获取文本框内容
        print(input_info, flush=True)
        p.stdin.write(input_info.encode())
        p.stdin.flush()


    tk.Button(ytm, text="输入", command=get_input).pack()  # command绑定获取文本框内容方法
    ytm.mainloop()  # 进入主循环

