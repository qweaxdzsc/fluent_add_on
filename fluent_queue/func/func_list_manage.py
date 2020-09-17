import sys
import cgitb

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, QFileInfo
from PyQt5.QtGui import QIcon, QPixmap

from ui_py.ui_add_project import Ui_Widget_add


class AddPj(QWidget, Ui_Widget_add):
    """
    This object is used to add new project
    1. choose case file; will check if it is cas or msh and whether exist
    2. designate iterations
    3. choose whether use own journal; will check if it is journal and whether exist
    """
    signal_add_pj = pyqtSignal(dict)
    signal_enable_action_add = pyqtSignal()

    def __init__(self, msg_translator):
        super().__init__()
        self.setupUi(self)
        self.btn()
        self.init_ui()
        self.set_all_icon()
        # self._translate()
        self.show()
        # -------------init variable--------------
        self.pj_dict = dict()
        self.edit_iteration.setText('1000')
        self.msg_translator = msg_translator
        self.make_trans = self.msg_translator.make_trans

    def btn(self):
        self.btn_extend.clicked.connect(self.show_ui)
        self.btn_project_address.clicked.connect(self.open_pj_file)
        self.checkbox_journal.clicked.connect(self.use_journal)
        self.btn_journal_address.clicked.connect(self.open_jou_file)
        self.btn_add.clicked.connect(self.generate_pj_info)

    def init_ui(self):
        self.resize(510, 80)
        self._set_icon('extend.png', self.btn_extend)
        self.frame_advanced.hide()
        self.label_journal_address.hide()             # hide journal functions, because it controls by checkbox
        self.edit_journal_address.hide()
        self.btn_journal_address.hide()

    def show_ui(self):
        """
        when toggle extend button, the window will be expanded
        1. judge whether extend button checked
        2. if checked, show advance functions
        3. if not checked, hide advanced functions
        :return:
        """
        if self.btn_extend.isChecked():
            self.resize(510, 200)
            self._set_icon('shrink.png', self.btn_extend)
            self.frame_advanced.show()
        else:
            # self.adjustSize()
            self.resize(510, 80)
            self._set_icon('extend.png', self.btn_extend)
            self.frame_advanced.hide()

    def _set_icon(self, pict, action):
        """
        function to set icon to tool button
        :param pict:
        :param action:
        :return:
        """
        icon = QIcon()
        icon.addPixmap(QPixmap("./icon/%s" % (pict)), QIcon.Normal, QIcon.Off)
        action.setIcon(icon)

    def set_all_icon(self):
        """
        use _set_icon to set all icon
        :return:
        """
        self._set_icon('openfile.png', self.btn_project_address)
        self._set_icon('openfile.png', self.btn_journal_address)
        self._set_icon('extend.png', self.btn_extend)

    def open_pj_file(self):
        """
        easy GUI way to choose project file function provided by QFileDialog
        Only filter .cas and .msh file
        :return:
        """
        path = QFileDialog.getOpenFileName(self, self.make_trans('choose_project'),
                                           r'C:',
                                           'Fluent Case(*.cas*);;Fluent Mesh(*.msh)',
                                           'Fluent Case(*.cas*)')
        self.edit_project_address.setText(path[0])

    def use_journal(self):
        """
        use checkbox to determine whether show journal function
        :return:
        """
        if self.checkbox_journal.isChecked():
            self.label_journal_address.show()
            self.edit_journal_address.show()
            self.btn_journal_address.show()
            self.edit_project_address.setDisabled(True)
            self.edit_iteration.setDisabled(True)
            self.label_iteration.setDisabled(True)
            self.label_project_address.setDisabled(True)
        else:
            self.label_journal_address.hide()
            self.edit_journal_address.hide()
            self.btn_journal_address.hide()
            self.edit_project_address.setDisabled(False)
            self.edit_iteration.setDisabled(False)
            self.label_iteration.setDisabled(False)
            self.label_project_address.setDisabled(False)

    def open_jou_file(self):
        """
        easy GUI way to choose journal file function provided by QFileDialog
        :return:
        """
        path = QFileDialog.getOpenFileName(self, self.make_trans('choose_journal'),
                                           r'C:',
                                           'Fluent journal(*.jou)')
        self.edit_journal_address.setText(path[0])

    def generate_pj_info(self):
        """
        triggered by button add
        1. create new project info dict every time
        2. extract project name and address from LineEdit; check if exist and if it is cas and msh file
        3. when second step done, get journal path from get_journal function
        :return: signal_add_pj(dict)
        """
        self.pj_dict = {"project_name": '', "project_address": '', "journal": ''}
        if self.checkbox_journal.isChecked():
            case_path = QFileInfo(self.edit_journal_address.text())
        else:
            case_path = QFileInfo(self.edit_project_address.text())          # QFileInfo can deeply analyze path info
        accepted_file_type = ['cas', 'msh', 'h5', 'jou']

        if (case_path.exists()) and (case_path.suffix() in accepted_file_type):
            self.pj_dict["project_name"] = case_path.fileName().rsplit('.', 1)[0]
            self.pj_dict["project_address"] = case_path.absolutePath()
            self.pj_dict['journal'] = self.get_journal(case_path, case_path.fileName())
            self.signal_add_pj.emit(self.pj_dict)
            self.close()
            print('generate new project:', self.pj_dict)
        else:
            QMessageBox.warning(self, self.make_trans('warning'), self.make_trans('no_case_mesh'),
                                QMessageBox.Yes, QMessageBox.Yes)
            print('file not exists')

    def get_journal(self, case_path, file_type):
        """
        if checbox checked, it will use own journal which fill in the LineEdit_journal
        if not checked, it will use default_journal func to get default journal
        :param case_path:
        :return: journal file path
        """
        if self.checkbox_journal.isChecked():
            jou_path = QFileInfo(self.edit_journal_address.text())
            if (jou_path.exists()) and (jou_path.suffix() == "jou"):
                return jou_path.filePath()
            else:
                QMessageBox.warning(self, self.make_trans('warning'), self.make_trans('no_journal'),
                                    QMessageBox.Yes, QMessageBox.Yes)
        else:
            jou_file = self.default_journal(case_path, file_type)
            return jou_file

    def default_journal(self, case_path, file_type):
        """
        create default journal for calculation only
        :param case_path:
        :return:
        """
        if '.cas' in file_type:
            read_type = 'read-case/'
        else:
            read_type = 'read'
        jou_file = case_path.absolutePath() + '\\' + case_path.baseName() + '.jou'
        transcript = case_path.absolutePath() + '\\%s_transcript.txt' % case_path.baseName()
        time_out_min = 1
        content = """
/file/start-transcript {transcript} ok
/file/set-idle-timeout yes {time_out} no
/file/{read_type} {case_path} yes
/solve/initialize/hyb-initialization yes
/solve/iterate/{iteration} yes
/file/write-case-data/ {case_path} yes
/exit yes
""".format(iteration=self.edit_iteration.text(), case_path=case_path.filePath(), transcript=transcript,
           time_out=time_out_min, read_type=read_type)
        with open(jou_file, 'w') as jou:
            jou.write(content)

        return jou_file

    def closeEvent(self, event):
        self.signal_enable_action_add.emit()


if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myWin = AddPj()
    myWin.show()
    sys.exit(app.exec_())