import time
import threading


queue_list = [i for i in range(10)]


def execute_mission(queue_list):
    while True:
        if queue_list:
            queue_list.pop(0)

        print(queue_list)
        time.sleep(3)


def queue_add(queue_list):
    while True:
        item = input('Please input item:')
        queue_list.append(item)
        print(queue_list)
        time.sleep(1)


thread1 = threading.Thread(target=execute_mission, args=(queue_list,))
thread1.start()

thread2 = threading.Thread(target=queue_add, args=(queue_list,))
thread2.start()