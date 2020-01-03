from ui_project_name import Ui_project_name_widget
from PyQt5.QtWidgets import QWidget, QApplication
import sys


class Ui_project_name(Ui_project_name_widget, QWidget):

    def __init__(self, main_window):
        super(Ui_project_name, self).__init__()
        self.setupUi(self)
        self.btn()
        self.main_window = main_window

    def btn(self):
        self.confirm_btn.clicked.connect(self.name_confirm)

    def name_confirm(self):
        project_name = self.project_name_edit.text()
        myMain = self.main_window()
        myMain.setWindowTitle(project_name)
        myMain.project_name = project_name
        myMain.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # myWin = Ui_project_name()
    # myWin.show()
    sys.exit(app.exec_())
