import time


class Scheduler(object):
    def __init__(self, schedule_day, schedule_hour, schedule_min):
        self.schedule_day = int(schedule_day)
        self.schedule_hour = int(schedule_hour)
        self.schedule_min = int(schedule_min)
        # --------------init variable-----------------------
        self.local_time = time.localtime()
        # print(self.local_time)
        self.wait_time = int()
        # --------------init function------------------------
        self.get_wait_time()

    def get_wait_time(self):
        current_day = self.local_time.tm_mday
        current_hour = self.local_time.tm_hour
        current_min = self.local_time.tm_min

        day_diff = self.schedule_day - current_day
        hour_diff = self.schedule_hour - current_hour
        min_diff = self.schedule_min - current_min

        # total_diff =


if __name__ == '__main__':
    day = '1'
    hour = '10'
    min = '50'
    scheduler = Scheduler(day, hour, min)
    tss1 = '2013-10-10 23:40:00'
    # timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
    timeArray = time.localtime()
    timeStamp = time.mktime(timeArray)
    print(time.time())
    print(timeStamp)