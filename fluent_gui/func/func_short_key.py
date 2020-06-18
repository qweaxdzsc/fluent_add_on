from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox
from report.re_get_report import get_report


class short_key(object):
    def __init__(self, ui):
        self.ui = ui                                                      # receive ui
        self.ui.keyPressEvent = self.keyPressEvent                        # rewrite ui's key press event

    def keyPressEvent(self, e):
        """ Event from QT, can be rewrite
        if e.key() = Qt.Key_?,  ? represent short key
        """
        if e.key() == Qt.Key_F1:
            self.name_rule()

        if e.key() == Qt.Key_1:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.ui.quick_distribfc_btn.setChecked(True)

        if e.key() == Qt.Key_2:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.ui.quick_distribfh_btn.setChecked(True)

        if e.key() == Qt.Key_3:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.ui.quick_distribbil_btn.setChecked(True)

        if e.key() == Qt.Key_4:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.ui.quick_distriblin_btn.setChecked(True)

        if e.key() == Qt.Key_Q:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:  # test mod shortcut
                self.ui.actionimport.trigger()
                self.ui.check_part()
                # self.ui.pamt_dict()
                self.ui.need_launch_CAD = False
                self.ui.show_outlet_name()
                self.ui.pamt_GUI()
                self.ui.append_text('进入调试模式')

        if e.key() == Qt.Key_J:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:  # generate script shortcut
                self.ui.create_tui()

        if e.key() == Qt.Key_O:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:  # modify outlet attributes
                self.ui.show_outlet_name()

        if e.key() == Qt.Key_R:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.ui.pamt_GUI()
                get_report(self.ui.pamt['file_path'], self.ui.pamt['project_name'], self.ui.pamt['version'])

    def name_rule(self):
        """when press F1, it shows a naming rule help document"""
        reply = QMessageBox.about(self.ui, '帮助——命名规则', '命名分为体与面的命名：\n'
                                    '请选择存在的体部件或使用快捷模板（ctrl+英文首字母），并点击导入模板\n\n'
                                    '完成后：\n'
                                    '1.对于面：选择面，并在space claim group栏下对相应的名字使用右键-replace\n'
                                    '2.对于体：请复制弹出窗口中 体名字 至space claim模型树中 指定体')

    def quick_distrib_judge(self):
        """
        4 quick button, if being checked, then automatically choose part for you
        """
        if self.ui.quick_distribfc_btn.isChecked():
            self.ui.default_ui.default_part_tree()

        if self.ui.quick_distribfh_btn.isChecked():
            self.ui.default_ui.default_part_tree()
            self.ui.part_tree.topLevelItem(9).setCheckState(0, 2)
            self.ui.distrib_number.setValue(2)

        if self.ui.quick_distribbil_btn.isChecked():
            self.ui.default_ui.default_part_tree()
            self.ui.part_tree.topLevelItem(9).setCheckState(0, 2)
            self.ui.distrib_number.setValue(1)

        if self.ui.quick_distriblin_btn.isChecked():
            self.ui.default_ui.default_part_tree()
            self.ui.part_tree.topLevelItem(9).setCheckState(0, 2)
            self.ui.energy_checkbox.setChecked(True)
            self.ui.distrib_number.setValue(1)
            self.ui.valve_number.setValue(1)