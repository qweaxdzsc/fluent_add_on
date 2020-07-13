from PyQt5.QtCore import pyqtSignal, QThread, QTimer, QDateTime, QEvent, QTime
from PyQt5.QtWidgets import QMainWindow, QWidget
from ui_py.ui_plan_timer import Ui_set_timer_Form
import time


class LoopTimer(QThread):
    """ create timer thread"""
    signal_sleep_timer = pyqtSignal()
    signal_journal_timer = pyqtSignal()
    signal_schedule_timer = pyqtSignal()

    def __init__(self):
        super(LoopTimer, self).__init__()
        self.start()
        self.step = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)                    # emit for every second
        self.timer.timeout.connect(self.register_time_emitter)
        self.timer.start()

    def run(self):
        pass

    def register_time_emitter(self):
        self.step += 1
        # print("timer's seconds:", self.step)
        self.signal_emit(self.signal_sleep_timer, 60)
        self.signal_emit(self.signal_journal_timer, 20)
        self.signal_emit(self.signal_schedule_timer, 60)

    def signal_emit(self, signal, seconds):
        if self.step % seconds == 0:
            signal.emit()

    def stop(self):
        self.timer.stop()


class SleepOut(QMainWindow):
    signal_time_exceed = pyqtSignal()
    """
    This object is mean to calculate the time without operation
    1. create a timer
    2. rewrite Ui's eventFilter, every move in this application will reset the timer
    3. when time exceed time out, logout the account
    """
    def __init__(self, ui, signal_timer, time_out_minutes):
        super().__init__()
        self.ui = ui
        self.time_out_minutes = time_out_minutes
        self.sleep_time = 0
        signal_timer.connect(self.time_add)                                 # create sleep timer
        ui.eventFilter = self.eventFilter                                   # rewrite ui's eventFilter function

    def eventFilter(self, watched_obj, event):
        if (event.type() == QEvent.MouseButtonPress) or (event.type() == QEvent.KeyPress) \
                or (event.type() == QEvent.MouseMove):
            self.sleep_time = 0
        return QMainWindow.eventFilter(self.ui, watched_obj, event)

    def time_add(self):
        self.sleep_time += 1
        print('no movement detected: %s minutes' % self.sleep_time)
        if self.sleep_time >= self.time_out_minutes:
            self.signal_time_exceed.emit()
            self.sleep_time = 0


class Scheduler(QWidget, Ui_set_timer_Form):
    signal_control_cal = pyqtSignal(bool)
    signal_waiting_min = pyqtSignal(int)
    signal_cancel_plan = pyqtSignal(str)

    def __init__(self, signal_timer):
        super().__init__()
        self.setupUi(self)
        # ------------init variable--------------
        self.waiting_min = 0
        self.have_schedule = False
        # ------------init function--------------
        self.btn()
        signal_timer.connect(self.left_time)

    def btn(self):
        self.btn_plan_start.clicked.connect(self.plan_start)
        self.btn_cancel_plan.clicked.connect(self.cancel_plan)

    def show_ui(self):
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
        self.show()

    def plan_start(self):
        curr_time = self.get_current_time()
        schedule_time = self.get_schedule_time()
        self.waiting_min = int((schedule_time - curr_time) / 60)
        print(self.waiting_min)
        self.signal_control_cal.emit(True)
        self.have_schedule = True
        self.close()

    def get_current_time(self):
        return QDateTime.currentSecsSinceEpoch()

    def get_schedule_time(self):
        return self.edit_plan_datetime.dateTime().toSecsSinceEpoch()

    def left_time(self):
        self.waiting_min -= 1
        print('等待时间:', self.waiting_min)
        if self.have_schedule:
            self.signal_waiting_min.emit(self.waiting_min)

            if self.waiting_min <= 0:
                self.signal_control_cal.emit(False)
                self.have_schedule = False

    def cancel_plan(self):
        self.signal_cancel_plan.emit('')
        self.have_schedule = False
        self.close()


def current_time():
    ct = time.strftime("%Y-%m-%d %H:%M:%S")
    return ct