from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication


class ShortKey(object):
    def __init__(self, ui):
        self.ui = ui
        self.ui.keyPressEvent = self.keyPressEvent

    def keyPressEvent(self, e):
        """ Event from QT, can be rewrite
        if e.key() = Qt.Key_?,  ? represent short key
        """
        if e.key() == Qt.Key_T:                                                     # used for test
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                acc_name = "BZMBN4"
                new_pj_dict = {"project_name": 'GE2-rear2-V33-FC',
                               "project_address": r'G:\_fluent_setup_test',
                               "journal": r'G:\_fluent_setup_test\GE2-rear2-V33-FC.jou'}
                self.ui.user_login(acc_name)
                self.ui.new_project(new_pj_dict)
                self.ui.manager_authority(True)
    #             self.ui.calculation.run = self.run

        # if e.key() == Qt.Key_P:                                                     # used for test
        #     if QApplication.keyboardModifiers() == Qt.ControlModifier:
        #         print('', self.ui.Hist_viewer.log_show.isFinished())
    #
    # def run(self):
    #     if self.running_project:
    #         time.sleep(1)
    #     while True:
    #         time.sleep(1)
    #         if self.mission_list:
    #             self.running_show()
    #             del self.mission_list[0]
    #             self.ui.update_waiting_list_log()
    #             self.ui.listWidget_queue.takeItem(0)
    #             time.sleep(20)


