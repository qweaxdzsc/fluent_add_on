
from queue import Queue
import random
import threading
import time


# Producer thread
class Producer(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def run(self):
        for i in range(5):
            print("%s: %s is producing %d to the queue!" % (time.ctime(), self.getName(), i))
            self.data.put(i)
            time.sleep(random.randrange(10) / 5)
        print("%s: %s finished!" % (time.ctime(), self.getName()))


# Consumer thread
class Consumer(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def run(self):
        for i in range(5):
            val = self.data.get()
            print("%s: %s is consuming. %d in the queue is consumed!" % (time.ctime(), self.getName(), val))
            time.sleep(random.randrange(10))
        print("%s: %s finished!" % (time.ctime(), self.getName()))


# Main thread
def main():
    queue = Queue()
    producer = Producer('Pro.', queue)
    consumer = Consumer('Con.', queue)
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()
    print('All threads terminate!')


import threading
import time

mission = [1, 2, 3, 4, 5, 6, 8, 7, 9]


def func(mission_list):
    while True:
        if mission_list:
            mission = mission_list[0]
            mission_list.remove(mission_list[0])
            print('\nstart mission %s' % mission)
            time.sleep(10)
            print('\nfinish mission %s' % mission)


def man_mission(mission_list):
    while True:
        order = input('\nplease give order(append or remove)')
        obj = input('\ncurrent list: %s\nplease enter object you want to manipulate: ' % mission_list)
        try:
            eval("mission_list.%s(%s)" % (order, obj))
        except Exception as e:
            print(e)
            print('\nWarning: unsuccess, current list: %s' % mission_list)
        print('\noperation success, current list: %s' % mission_list)


if __name__ == '__main__':
    cal_thread = threading.Thread(target=func, args=[mission])
    cal_thread.start()
    man_thread = threading.Thread(target=man_mission, args=[mission])
    man_thread.start()



