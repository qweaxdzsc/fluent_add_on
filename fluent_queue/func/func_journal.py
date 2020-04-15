import sys
import cgitb
import csv
import time

from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal, QThread

from ui_py.ui_journal import Ui_widget_journal


class HistoryView(QWidget, Ui_widget_journal):
    """
    SubUi object to view history csv
    """
    viewer_closed = pyqtSignal()

    def __init__(self, csv_path):
        super(HistoryView, self).__init__()
        self.setupUi(self)
        self.log_show = CsvReader(csv_path)
        self.log_show.content_list.connect(self.list_to_ui)
        self.log_show.start()
        self.show()                                                             # show window

    def list_to_ui(self, finished_list):
        header = finished_list[0]
        data = finished_list[1:]
        column_count = len(header)
        row_count = len(data)
        self.table_journal.setColumnCount(column_count)
        self.table_journal.setHorizontalHeaderLabels(header)
        self.table_journal.setRowCount(row_count)
        for row in range(row_count):
            for col in range(column_count):
                new_item = QTableWidgetItem(data[row][col])
                self.table_journal.setItem(row, col, new_item)

        self.table_journal.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_journal.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def closeEvent(self, event):
        self.viewer_closed.emit()
        self.log_show.stop()


class CsvReader(QThread):
    """ create timer thread"""
    content_list = pyqtSignal(list)

    def __init__(self, csv_path):
        super(CsvReader, self).__init__()
        self.csv_path = csv_path
        self.runnable = True

    def run(self):
        while self.runnable:
            finished_list = list()
            with open(self.csv_path, 'r') as f:
                csv_reader = csv.reader(f, delimiter=',')
                for row in csv_reader:
                    finished_list.append(row)
            self.content_list.emit(finished_list)
            time.sleep(10)

    def stop(self):
        self.runnable = False
        self.quit()


if __name__ == "__main__":
    cgitb.enable(format='text')
    csv_path = r"S:\PE\Engineering database\CFD\03_Tools\queue_backup\history_list.csv"
    app = QApplication(sys.argv)
    myWin = HistoryView(csv_path)
    myWin.show()
    sys.exit(app.exec_())

