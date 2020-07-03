from PyQt5.QtCore import pyqtSignal, QThread, QTimer, QDateTime, QEvent, QTime
from PyQt5.QtWidgets import QMainWindow, QWidget
from ui_py.ui_plan_timer import Ui_set_timer_Form
import time


class timer(QThread):
    """ create timer thread"""
    time_count = pyqtSignal(int)

    def __init__(self, interval):
        super(timer, self).__init__()
        self.step = 0
        self.timer = QTimer()
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self.show_time)

    def run(self):
        pass

    def show_time(self):
        self.step += 1
        self.time_count.emit(self.step)

    def start_timer(self):
        self.timer.start()
        self.time_count.emit(0)

    def stop(self):
        self.timer.stop()


class SleepOut(QMainWindow, QThread):
    time_exceed = pyqtSignal()
    """
    This object is mean to calculate the time without operation
    1. create a timer
    2. rewrite Ui's eventFilter, every move in this application will reset the timer
    3. when time exceed time out, logout the account
    """
    def __init__(self, ui, time_out_minutes):
        super().__init__()
        self.ui = ui
        self.time_out_minutes = time_out_minutes
        self.sleep_time = timer(60000)                                      # 60000 means one minutes
        self.sleep_time.time_count.connect(self.time_out)                   # create sleep timer
        ui.eventFilter = self.eventFilter                                   # rewrite ui's eventFilter function

    def eventFilter(self, watched_obj, event):
        if (event.type() == QEvent.MouseButtonPress) or (event.type() == QEvent.KeyPress) \
                or (event.type() == QEvent.MouseMove):
            self.sleep_time.step = 0
        return QMainWindow.eventFilter(self.ui, watched_obj, event)

    def start_count(self):
        self.sleep_time.start_timer()

    def time_out(self, time):
        if time > self.time_out_minutes:
            self.time_exceed.emit()
            self.sleep_time.stop()


class Scheduler(QWidget, Ui_set_timer_Form):
    signal_control_cal = pyqtSignal(bool)
    signal_waiting_min = pyqtSignal(int)
    signal_cancel_plan = pyqtSignal(str)

    def __init__(self, have_schedule, waiting_min):
        super().__init__()
        self.setupUi(self)
        # ------------init variable--------------
        self.time_waiting = int()
        self.waiting_min = waiting_min
        self.have_schedule = have_schedule
        # ------------init function--------------
        self.ui_setting()
        self.btn()
        self.show()

    def ui_setting(self):
        if self.have_schedule:
            self.frame_launch.hide()
            self.frame_cancel.show()

            days = int(self.waiting_min/24/60)
            hours = int(self.waiting_min/60 - days*24)
            minutes = int(self.waiting_min % 60)
            if days > 0:
                self.edit_rest_time.setDisplayFormat("dd天HH:mm")
                self.edit_rest_time.setDateTime(QDateTime(2020, 5, days, hours, minutes))
            else:
                self.edit_rest_time.setDisplayFormat("HH小时mm分钟")
                self.edit_rest_time.setDateTime(QDateTime(2020, 5, 1, hours, minutes))
        else:
            self.frame_launch.show()
            self.frame_cancel.hide()
            self.edit_plan_datetime.setDateTime(QDateTime.currentDateTime())
            self.edit_plan_datetime.setMinimumDateTime(QDateTime.currentDateTime())
            self.edit_plan_datetime.setMaximumDateTime(QDateTime.currentDateTime().addDays(5))
            self.edit_plan_datetime.setCalendarPopup(True)

        self.setMaximumSize(260, 100)

    def btn(self):
        self.btn_plan_start.clicked.connect(self.plan_start)
        self.btn_cancel_plan.clicked.connect(self.cancel_plan)

    def plan_start(self):
        curr_time = self.get_current_time()
        schedule_time = self.get_schedule_time()
        self.time_waiting = int(schedule_time - curr_time)
        self.signal_control_cal.emit(True)
        self.launch_thread = timer(60000)
        self.launch_thread.time_count.connect(self.thread_time)
        self.launch_thread.start_timer()
        self.close()

    def get_current_time(self):
        return QDateTime.currentSecsSinceEpoch()

    def get_schedule_time(self):
        return self.edit_plan_datetime.dateTime().toSecsSinceEpoch()

    def thread_time(self, min):
        print('delay minutes:', min)
        seconds = min*60
        rest_min = int(self.time_waiting/60 - min)
        self.signal_waiting_min.emit(rest_min)

        if seconds >= self.time_waiting:
            self.launch_thread.stop()
            self.signal_control_cal.emit(False)

    def cancel_plan(self):
        self.launch_thread.stop()           # TODO move launch_thread to main UI
        self.signal_cancel_plan.emit('')
        self.close()


def current_time():
    ct = time.strftime("%Y-%m-%d %H:%M:%S")
    return ct