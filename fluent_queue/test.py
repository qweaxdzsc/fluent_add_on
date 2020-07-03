import cgitb
import sys
from ui_py.ui_plan_timer import Ui_set_timer_Form
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QDateTime, QThread, pyqtSignal, QEvent


class Scheduler(QWidget, Ui_set_timer_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.edit_setting()
        self.btn()
        self.launch_thread = QThread()

    def edit_setting(self):
        self.edit_plan_datetime.setDateTime(QDateTime.currentDateTime())
        self.edit_plan_datetime.setMinimumDateTime(QDateTime.currentDateTime())
        self.edit_plan_datetime.setMaximumDateTime(QDateTime.currentDateTime().addDays(5))
        # self.edit_plan_datetime.setCalendarPopup(True)

    def btn(self):
        self.btn_plan_start.clicked.connect(self.plan_start)

    def plan_start(self):
        current_time = self.get_current_time()
        schedule_time = self.get_schedule_time()
        time_waiting = schedule_time - current_time
        self.launch_thread = DelayLauncher(time_waiting)
        self.launch_thread.start()
        self.close()

    def get_current_time(self):
        return QDateTime.currentSecsSinceEpoch()

    def get_schedule_time(self):
        return self.edit_plan_datetime.dateTime().toSecsSinceEpoch()


class DelayLauncher(QThread):
    launch_signal = pyqtSignal(int)

    def __init__(self, delay_time):
        super().__init__()
        self.delay_time = delay_time

    def run(self):
        self.sleep(self.delay_time)
        # self.launch_signal


if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myWin = Scheduler()
    app.installEventFilter(myWin)
    myWin.show()
    sys.exit(app.exec_())