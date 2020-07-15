import sys
import cgitb

from PyQt5.QtWidgets import QWidget, QApplication, QTreeWidgetItem, QCheckBox, QSpinBox, QDateTimeEdit
from PyQt5.QtCore import pyqtSignal, QDateTime
from ui_py.ui_setting import Ui_widget_setting


class Setting(QWidget, Ui_widget_setting):
    signal_core_number = pyqtSignal(int)
    signal_suspend_status = pyqtSignal(bool)
    signal_waiting_min = pyqtSignal(int)
    signal_schedule_status = pyqtSignal(bool)
    signal_cancel_plan = pyqtSignal(str)

    def __init__(self, suspend, cores, schedule_status, waiting_min):
        super().__init__()
        self.setupUi(self)
        # ----------init variable------------
        self.suspend = suspend
        self.cores = cores
        self.schedule_status = schedule_status
        self.waiting_min = waiting_min
        # ----------init widget--------------
        self.label_suspend = QTreeWidgetItem()
        self.checkbox_suspend = QCheckBox()
        self.label_cores = QTreeWidgetItem()
        self.edit_cores = QSpinBox()
        self.label_plan = QTreeWidgetItem()
        self.edit_plan_datetime = QDateTimeEdit()
        self.label_about = QTreeWidgetItem()
        # -----------init function----------------
        self.ui_set()
        self.btn()
        self.init_data_show()
        self.show()

    def btn(self):
        self.tree_setting.itemClicked.connect(self.effect_expand)
        self.tree_setting.itemChanged.connect(self.enable_schedule)
        self.checkbox_suspend.stateChanged.connect(self.change_suspend_status)

    def ui_set(self):
        # style
        self.setStyleSheet("QSpinBox{border:1.5px solid #778899;border-radius:4px; padding:2px 2px}"
                           "QDateTimeEdit{border:1.5px solid #778899;border-radius:4px; padding:2px 2px}")
        self.tree_setting.setColumnWidth(0, 180)
        self.tree_setting.expandItem(self.tree_setting.topLevelItem(0))
        self.tree_setting.topLevelItem(1).setCheckState(1, 0)
        self.edit_cores.setMaximumSize(50, 25)
        self.edit_cores.setContentsMargins(0, 4, 0, 0)
        self.edit_cores.setMinimum(1)
        self.label_plan.setDisabled(True)
        self.edit_plan_datetime.setMaximumSize(135, 28)
        self.edit_plan_datetime.setDisabled(True)
        # function
        self.add_tree_item(0, self.label_suspend, "暂停队列", self.checkbox_suspend)
        self.add_tree_item(0, self.label_cores, "使用核数", self.edit_cores)
        self.add_tree_item(1, self.label_plan, "计划启动于", self.edit_plan_datetime)

    def add_tree_item(self, top_level_index, label, label_name, input_edit):
        label.setText(0, label_name)
        self.tree_setting.topLevelItem(top_level_index).addChild(label)
        self.tree_setting.setItemWidget(label, 1, input_edit)

    def effect_expand(self, item, column):
        index = self.tree_setting.indexOfTopLevelItem(item)
        if index >= 0:
            if item.isExpanded():
                item.setExpanded(False)
            else:
                item.setExpanded(True)

    def enable_schedule(self, item, column):
        index = self.tree_setting.indexOfTopLevelItem(item)
        if index == 1:
            check_state = item.checkState(column)
            self.schedule_status = bool(check_state)
            self.label_plan.setDisabled(2 - check_state)
            self.edit_plan_datetime.setEnabled(check_state)
            item.setExpanded(2 - check_state)
            self.reset_date_edit()

    def init_data_show(self):
        self.edit_cores.setValue(self.cores)
        self.checkbox_suspend.setCheckState(self.suspend * 2)
        if self.schedule_status:
            self.tree_setting.topLevelItem(1).setCheckState(1, 2)
            self.label_plan.setDisabled(False)
            self.edit_plan_datetime.setEnabled(True)
            self.tree_setting.topLevelItem(1).setExpanded(True)
            waiting_seconds = self.waiting_min * 60
            self.edit_plan_datetime.setDisplayFormat("yyyy/MM/dd HH:mm")
            self.edit_plan_datetime.setDateTime(QDateTime.currentDateTime().addSecs(waiting_seconds))
        else:
            self.reset_date_edit()

    def reset_date_edit(self):
        self.edit_plan_datetime.setDisplayFormat("yyyy/MM/dd HH:mm")
        self.edit_plan_datetime.setDateTime(QDateTime.currentDateTime())
        self.edit_plan_datetime.setMinimumDateTime(QDateTime.currentDateTime())
        self.edit_plan_datetime.setMaximumDateTime(QDateTime.currentDateTime().addDays(5))
        self.edit_plan_datetime.setCalendarPopup(True)

    def change_suspend_status(self, status):
        self.signal_suspend_status.emit(bool(status))

    def plan_start(self):
        curr_time = QDateTime.currentSecsSinceEpoch()
        schedule_time = self.edit_plan_datetime.dateTime().toSecsSinceEpoch()
        self.waiting_min = int((schedule_time - curr_time) / 60)
        self.signal_waiting_min.emit(self.waiting_min)

    def closeEvent(self, event):
        self.cores = self.edit_cores.value()
        self.signal_core_number.emit(self.cores)
        self.signal_schedule_status.emit(self.schedule_status)
        if self.schedule_status:
            self.plan_start()
            self.signal_suspend_status.emit(True)
        else:
            self.signal_cancel_plan.emit(' ')
        self.close()


if __name__ == '__main__':
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    suspend = True
    cores = 24
    schedule_status = True
    waiting_min = 60
    myWin = Setting(suspend, cores, schedule_status, waiting_min)
    app.installEventFilter(myWin)
    sys.exit(app.exec_())


