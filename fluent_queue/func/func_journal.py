import sys
import cgitb
import csv
import os

from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import pyqtSignal

from ui_py.ui_journal import Ui_widget_journal


class HistoryView(QWidget, Ui_widget_journal):
    """
    SubUi object to view history csv
    """
    signal_viewer_closed = pyqtSignal()

    def __init__(self, csv_path, signal_timer):
        super().__init__()
        # -----------init variable-------------
        self.csv_path = csv_path
        self.finished_list = list()
        self.csv_exist = self.verify_csv()
        # -----------init function-------------
        self.setupUi(self)
        self.table_journal.setEditTriggers(QAbstractItemView.NoEditTriggers)
        signal_timer.connect(self.show_log)
        self.show_log()
        self.show()                                                             # show window

    def verify_csv(self):
        if os.path.exists(self.csv_path):
            return True
        else:
            return False

    def show_log(self):
        if self.csv_exist:
            print('show_log launch')
            self.read_csv()
            self.list_to_ui()

    def read_csv(self):
        self.finished_list = []
        with open(self.csv_path, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                self.finished_list.append(row)

    def list_to_ui(self):
        self.table_journal.clear()
        header = self.finished_list[0]
        data = self.finished_list[1:]
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
        self.signal_viewer_closed.emit()
        self.close()


if __name__ == "__main__":
    cgitb.enable(format='text')
    csv_path = r"S:\PE\Engineering database\CFD\03_Tools\queue_backup\history_list.csv"
    app = QApplication(sys.argv)
    # myWin = HistoryView(csv_path)
    # myWin.show()
    sys.exit(app.exec_())

