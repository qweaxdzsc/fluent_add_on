from PyQt5.QtCore import pyqtSignal, QThread, QTimer, QDateTime, QEvent
from PyQt5.QtWidgets import QMainWindow, QWidget
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


class Scheduler(QWidget):
    signal_control_cal = pyqtSignal(bool)
    signal_waiting_min = pyqtSignal(int)

    def __init__(self, signal_timer):
        super().__init__()
        # ------------init variable--------------
        self.waiting_min = 0
        self.have_schedule = False
        # ------------init function--------------
        signal_timer.connect(self.left_time)

    def left_time(self):
        self.waiting_min -= 1
        print('等待时间:', self.waiting_min)
        if self.have_schedule:
            self.signal_waiting_min.emit(self.waiting_min)

            if self.waiting_min <= 0:
                self.signal_control_cal.emit(False)
                self.have_schedule = False

    def enable_schedule(self, status):
        self.have_schedule = status
        print('have schedule:', self.have_schedule)

    def receive_waiting_min(self, waiting_min):
        self.waiting_min = waiting_min
        print('received waiting minutes:', waiting_min)


def current_time():
    ct = time.strftime("%Y-%m-%d %H:%M:%S")
    return ct