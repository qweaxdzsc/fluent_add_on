from ui_project_name import Ui_project_name_widget
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, QTranslator
import sys


class Ui_project_name(Ui_project_name_widget, QWidget):
    def __init__(self, main_window):
        super(Ui_project_name, self).__init__()
        self.setupUi(self)
        self.btn()
        self.validate()
        self.trans = QTranslator()
        self.language = 'CN'
        self.main_window = main_window

    def btn(self):
        self.confirm_btn.clicked.connect(self.name_confirm)
        self.language_combox.activated.connect(self._translate)

    def validate(self):
        re = QRegExp("[a-zA-Z0-9_]+")
        validator = QRegExpValidator(re)
        self.project_name_edit.setValidator(validator)
        self.project_name_edit.setMaxLength(12)

    def name_confirm(self):
        project_name = self.project_name_edit.text()
        self.myMain = self.main_window()
        self.myMain.setWindowTitle(project_name)
        self.myMain.project_name = project_name
        self.myMain._translate(self.language)
        self.myMain.porous_model.translate(self.language)
        self.myMain.show()
        self.close()

    def _translate(self, i):
        language = self.language_combox.currentText()
        lauguage_file_dict = {' Chinese': 'CN', ' English': 'EN'}
        self.trans.load("ui_project_name_%s" % lauguage_file_dict[language])
        _app = QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)
        self.language = lauguage_file_dict[language]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # myWin = Ui_project_name()
    # myWin.show()
    sys.exit(app.exec_())
