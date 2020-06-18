from PyQt5.QtCore import pyqtSignal, QThread, QTimer
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QMainWindow
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
        print(self.step)
        self.step += 1
        self.time_count.emit(self.step)

    def star_timer(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()


class SleepOut(QMainWindow):
    time_exceed = pyqtSignal()
    """
    This object is mean to calculate the time without operation
    1. create a timer
    2. rewrite Ui's eventFilter, every move in this application will reset the timer
    3. when time exceed time out, logout the account
    """
    def __init__(self, ui, time_out_minutes):
        super(QMainWindow, self).__init__()
        self.ui = ui
        self.time_out_minutes = time_out_minutes
        self.sleep_time = timer(60000)                                      # 60000 means one minutes
        self.sleep_time.time_count.connect(self.time_out)                   # create sleep timer
        ui.eventFilter = self.eventFilter                                   # rewrite ui's eventFilter function

    def eventFilter(self, watched_obj, event):
        if (event.type() == QEvent.MouseButtonPress) or (event.type() == QEvent.KeyPress) \
                or (event.type() == QEvent.MouseMove):
            self.sleep_time.step = 0
        return QMainWindow.eventFilter(self, watched_obj, event)

    def start_count(self):
        self.sleep_time.star_timer()

    def time_out(self, time):
        if time > self.time_out_minutes:
            self.time_exceed.emit()
            self.sleep_time.stop()


def current_time():
    ct = time.strftime("%Y-%m-%d %H:%M:%S")
    return ct