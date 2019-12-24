#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import time
import csv
import cgitb

from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QMessageBox, QTableWidgetItem, QFileDialog, QMenu, QLineEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QBasicTimer
from PyQt5.QtGui import QTextCursor
import qdarkstyle

from ui_main import Ui_MainWindow
from ui_rename_outlet import Ui_tip_widget
from ui_k_cal import Ui_K_calculator
from ui_unit_convertor import Ui_unit_converter
from porous_model import Ui_porous


class MyMainWindow(QMainWindow, Ui_MainWindow):
    time_running = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.mode_ui_default()
        self.account_info()
        self.get_date()
        self.pamt = {}
        self.K_dict = {}
        self.body_list = []
        self.show_c_on = False
        self.snip_on = True
        self.btn()

    def mode_ui_default(self):
        self.mode_info_frame.show()
        self.start_btn.hide()
        self.mass_inlet_c.hide()
        self.return_btn.hide()
        self.evap_c.hide()
        self.hc_c.hide()
        self.solver_btn.hide()
        self.valve_c.hide()
        self.temp_c.hide()
        self.fan_c.hide()
        self.snip_c.hide()
        self.actionstop.setEnabled(False)
        self.import_outlet = False

    def account_info(self):
        user = os.environ.get("USERNAME")
        self.username_label.setText('欢迎大佬%s' % (user))
        welcome_list = ['Hi,大佬%s，我们又见面了' % (user), 'Hello,欢迎大佬%s' % (user)]
        import random
        welcome_word = random.choice(welcome_list)
        self.interact_edit.append(welcome_word)

    def get_date(self):
        today = time.strftime('%y%m%d', time.localtime(time.time()))
        self.version_date_edit.setText(today)

    def btn(self):
        self.actionimport.triggered.connect(self.import_info)
        self.actionexport.triggered.connect(self.export_pamt)
        self.actionsolve.triggered.connect(self.quick_solve)
        self.actionstop.triggered.connect(self.force_stop)
        self.actiondarkstyle.triggered.connect(self.darkstyle)
        self.actionsnip.triggered.connect(self.show_snip_setting)
        self.project_address_explore.clicked.connect(self.case_address)

        self.quick_distribfc_btn.toggled.connect(self.quick_distrib_judge)
        self.quick_distribfh_btn.toggled.connect(self.quick_distrib_judge)
        self.quick_distribbil_btn.toggled.connect(self.quick_distrib_judge)
        self.quick_distriblin_btn.toggled.connect(self.quick_distrib_judge)
        self.finish_mode_info_btn.clicked.connect(self.into_CAD)

        self.unit_btn.clicked.connect(self.unit_convert)
        self.choose_evap_btn.clicked.connect(lambda: self.porous_choose('evap'))
        self.choose_hc_btn.clicked.connect(lambda: self.porous_choose('hc'))
        self.start_btn.clicked.connect(self.begin)
        self.return_btn.clicked.connect(self.mode_ui_default)
        self.solver_btn.clicked.connect(self.solver)

        self.show_workflow_btn.clicked.connect(self.test)
        self.actionalter_default_parameter.triggered.connect(lambda: self.append_text('功能未开放,敬请期待'))

    def default_part_tree(self):
        self.part_tree.topLevelItem(0).setCheckState(0, 0)   # 0 means unchecked, 2 means checked
        self.part_tree.topLevelItem(1).setCheckState(0, 2)
        self.part_tree.topLevelItem(2).setCheckState(0, 0)
        self.part_tree.topLevelItem(3).setCheckState(0, 0)
        self.part_tree.topLevelItem(4).setCheckState(0, 0)
        self.part_tree.topLevelItem(5).setCheckState(0, 0)
        self.part_tree.topLevelItem(6).setCheckState(0, 0)
        self.part_tree.topLevelItem(7).setCheckState(0, 2)
        self.part_tree.topLevelItem(8).setCheckState(0, 2)
        self.part_tree.topLevelItem(9).setCheckState(0, 0)
        self.part_tree.topLevelItem(10).setCheckState(0, 0)
        self.part_tree.topLevelItem(11).setCheckState(0, 0)
        self.distrib_number.setValue(1)
        self.outlet_number.setValue(1)

    def test(self):

        self.append_text('功能未开放,敬请期待')
        pass

    def darkstyle(self):
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.actiondarkstyle.setDisabled(True)
        self.append_text('进入暗色主题')

    def append_text(self, msg):
        self.interact_edit.append(msg)
        self.interact_edit.moveCursor(QTextCursor.End)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F1:
            self.name_rule()

        if e.key() == Qt.Key_1:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.quick_distribfc_btn.setChecked(True)

        if e.key() == Qt.Key_2:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.quick_distribfh_btn.setChecked(True)

        if e.key() == Qt.Key_3:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.quick_distribbil_btn.setChecked(True)

        if e.key() == Qt.Key_4:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.quick_distriblin_btn.setChecked(True)

        if e.key() == Qt.Key_Q:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:              # test mod shortcut
                self.actionimport.trigger()
                self.check_part()
                self.pamt_dict()
                self.need_launch_CAD = False
                self.show_outlet_name()
                self.pamt_GUI()
                self.append_text('进入调试模式')

        if e.key() == Qt.Key_J:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:              # test mod shortcut
                self.create_tui()

    def name_rule(self):
        reply = QMessageBox.about(self, '帮助——命名规则', '命名分为体与面的命名：\n'
                                    '请选择存在的体部件或使用快捷模板（ctrl+英文首字母），并点击导入模板\n\n'
                                    '完成后：\n'
                                    '1.对于面：选择面，并在space claim group栏下对相应的名字使用右键-replace\n'
                                    '2.对于体：请复制弹出窗口中 体名字 至space claim模型树中 指定体')

    def quick_solve(self):
        confirm_info = self.project_info_check()

        if confirm_info:
            self.check_part()
            self.pamt_GUI()
            self.start_btn.setText('网   格')
            self.start_btn.setEnabled(True)
            self.solver_btn.show()
            self.solver_btn.setEnabled(True)
            self.append_text('警告：进入补算模式，请先确认正确的模型或网格')

    def force_stop(self):
        try:
            if self.mesh_thread.isRunning():
                self.mesh_thread.stop_mesh()
                self.clock.stop()
                self.append_text('网格划分已经被终止')

            if self.solver_thread.isRunning():
                self.solver_thread.stop_solver()
                self.append_text('计算已经被终止')
        except Exception as e:
            print('not yet being running')

    def quick_distrib_judge(self):
        if self.quick_distribfc_btn.isChecked():
            self.default_part_tree()

        if self.quick_distribfh_btn.isChecked():
            self.default_part_tree()
            self.part_tree.topLevelItem(9).setCheckState(0, 2)
            self.distrib_number.setValue(2)
            self.outlet_number.setValue(1)

        if self.quick_distribbil_btn.isChecked():
            self.default_part_tree()
            self.part_tree.topLevelItem(9).setCheckState(0, 2)
            self.distrib_number.setValue(1)
            self.outlet_number.setValue(2)

        if self.quick_distriblin_btn.isChecked():
            self.default_part_tree()
            self.part_tree.topLevelItem(9).setCheckState(0, 2)
            self.part_tree.topLevelItem(11).setCheckState(0, 2)
            self.energy_checkbox.setChecked(True)
            self.outlet_number.setValue(1)
            self.distrib_number.setValue(1)

    def show_snip_setting(self):
        if self.actionsnip.isChecked():
            self.snip_on = True
        else:
            self.snip_on = False

        self.snip_switch()

    def snip_switch(self):
        if self.snip_on and self.show_c_on:
            self.snip_c.show()
        else:
            self.snip_c.hide()

    def into_CAD(self):
        confirm_info = self.project_info_check()
        self.need_launch_CAD = True

        if confirm_info:
            self.check_part()
            self.show_outlet_name()

    def project_info_check(self):
        self.pamt_dict()
        if (self.pamt['project_name'] == '') | (self.pamt['version'] == '') | (self.pamt['file_path'] == ''):
            self.append_text('请大佬将项目信息填写完全')
            return False

        if not os.path.exists('%s' % (self.pamt['file_path'])):
            self.append_text('项目路径不存在，请大佬检查路径信息')
            return False
        else:
            if os.path.exists('%s/project_info.py' % (self.pamt['file_path'])):
                os.remove('%s/project_info.py' % (self.pamt['file_path']))

        if os.path.exists(self.pamt['cad_save_path']):
            reply = QMessageBox.warning(self, "警告", "检测到路径下已存在CAD文件%s,是否覆盖？" % (self.pamt['cad_name']),
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                result_file = 'result' + self.pamt['project_name'] + '_' + self.pamt['version']
                result_path = self.pamt['file_path'] + '\\' + result_file
                txt_out = result_path + '\\' + self.pamt['project_name'] + '.txt'
                if os.path.exists(txt_out):
                    os.remove(txt_out)
                return True
            elif reply == QMessageBox.No:
                return False

        return True

    def check_part(self):
        body_list = []
        face_list = ['inlet']
        porous_list =[]
        up_list = []
        dead_zone_list = []

        if self.inlet_number.value() > 1:
            for i in range(self.inlet_number.value()-1):
                face_list.append('inlet%s' % (i+2))
        if self.part_tree.topLevelItem(0).checkState(0) == 2:
            body_list.append('inlet_sphere')
        if self.part_tree.topLevelItem(1).checkState(0) == 2:
            body_list.append('ai')
            if self.part_tree.topLevelItem(0).checkState(0) == 2:
                face_list.append('ai_in')
        if self.part_tree.topLevelItem(2).checkState(0) == 2:
            if self.part_tree.topLevelItem(3).checkState(0) == 0:
                print('filter and cone should be all checked')
            else:
                body_list.append('filter')
                body_list.append('cone')
                porous_list.append('filter')
                up_list.append('ai')
                face_list.append('filter_in')
                face_list.append('filter_out')
        if self.part_tree.topLevelItem(4).checkState(0) == 2:
            if self.part_tree.topLevelItem(5).checkState(0) == 0:
                print('volute and fan should be all checked')
            else:
                body_list.append('volute')
                up_list.append('volute')
                body_list.append('fan')
                dead_zone_list.append('fan_blade')
                if self.part_tree.topLevelItem(0).checkState(0) == 2:
                    face_list.append('fan_in')
                if self.part_tree.topLevelItem(1).checkState(0) == 2:
                    face_list.append('fan_in')
                face_list.append('fan_out')
                face_list.append('fan_blade')
        if self.part_tree.topLevelItem(6).checkState(0) == 2:
            body_list.append('diffuser')
            if self.part_tree.topLevelItem(4).checkState(0) == 2:
                face_list.append('volute_out')
        if self.part_tree.topLevelItem(7).checkState(0) == 2:
            body_list.append('evap')
            porous_list.append('evap')
            face_list.append('evap_in')
            face_list.append('evap_out')
        if self.part_tree.topLevelItem(8).checkState(0) == 2:
            body_list.append('distrib')

        if self.part_tree.topLevelItem(9).checkState(0) == 2:
            body_list.append('hc')
            porous_list.append('hc')
            face_list.append('hc_in')
            face_list.append('hc_out')

        if self.part_tree.topLevelItem(10).checkState(0) == 2:
            body_list.append('ptc')
            porous_list.append('ptc')
            face_list.append('ptc_in')
            face_list.append('ptc_out')
        if self.part_tree.topLevelItem(11).checkState(0) == 2:
            body_list.append('valve')
            dead_zone_list.append('valve')

        if self.distrib_number.value() > 1:
            distrib_index = body_list.index('distrib')
            body_list[distrib_index] = 'distrib1'
            for i in range(self.distrib_number.value() - 1):
                body_list.append('distrib%s' % (i + 2))

        print('body_list:%s\nface_list:%s' % (body_list, face_list))

        internal_face = face_list.copy()
        for i in face_list:
            if 'fan_blade' is i or 'inlet' is i:
                internal_face.remove(i)

        self.face_list = face_list
        self.body_list = body_list
        self.porous_list = porous_list
        self.up_list = up_list
        self.dead_zone_list = dead_zone_list
        self.internal_face = internal_face

    def show_outlet_name(self):
        if self.import_outlet:
            self.outlet_name_and_K()
        else:
            from outlet_rename import outlet_rename_ui
            self.outlet_rename = outlet_rename_ui()
            self.outlet_rename.show()
            self.outlet_rename.chosed_btn.clicked.connect(self.receive_outlet_name)
            self.outlet_rename.chosed_btn.clicked.connect(self.outlet_name_and_K)

    def receive_outlet_name(self):
        self.outlet_list = self.outlet_rename.outlet_list
        self.outlet_K = [0 for i in self.outlet_list]

    def outlet_name_and_K(self):
        self.dialog_tip = Ui_tip()
        self.dialog_tip.show()

        self.dialog_tip.rename_btn.clicked.connect(self.dialog_tip.close)
        self.dialog_tip.rename_btn.clicked.connect(self.update_project_info)
        if self.need_launch_CAD:
            self.dialog_tip.rename_btn.clicked.connect(self.launchCAD)

        self.inlet_n = self.inlet_number.value()
        self.outlet_n = len(self.outlet_list)

        self.dialog_tip.rename_table.setRowCount(max(self.inlet_n, self.outlet_n))
        self.dialog_tip.rename_table.setFixedHeight(max(self.inlet_n, self.outlet_n)*35+35)

        for i in range(self.inlet_n):
            new_item = QTableWidgetItem("%s" % (self.face_list[i]))
            self.dialog_tip.rename_table.setItem(i, 0, new_item)

        for i in range(len(self.outlet_list)):
            new_item = QTableWidgetItem("%s" % (self.outlet_list[i]))
            self.dialog_tip.rename_table.setItem(i, 1, new_item)

            new_item = QTableWidgetItem("%s" % (self.outlet_K[i]))
            self.dialog_tip.rename_table.setItem(i, 2, new_item)

        self.dialog_tip.rename_table.customContextMenuRequested.connect(self.generate_cal_menu)

    def generate_cal_menu(self, pos):
        column_num = -1
        for i in self.dialog_tip.rename_table.selectionModel().selection().indexes():
            column_num = i.column()
            self.K_row = i.row()

        if column_num == 2:
            cal_menu = QMenu()
            cal_action = cal_menu.addAction(u"计算K值")
            action = cal_menu.exec_(self.dialog_tip.rename_table.mapToGlobal(pos))
            if action == cal_action:
                self.K_cal = Ui_cal_K()
                self.K_cal.show()
                self.K_cal.K_result.connect(self.K_result)

    def K_result(self, K):
        modify_item = QTableWidgetItem(K)
        self.dialog_tip.rename_table.setItem(self.K_row, 2, modify_item)
        self.K_cal.close()

    def update_project_info(self):
        self.outlet_list, self.K_list = [], []

        for i in range(self.inlet_n):
            self.face_list[i] = self.dialog_tip.rename_table.item(i, 0).text()

        for i in range(self.outlet_n):
            try:
                self.outlet_list.append(self.dialog_tip.rename_table.item(i, 1).text())
                self.K_list.append(self.dialog_tip.rename_table.item(i, 2).text())
            except Exception as e:
                continue
        self.face_list.extend(self.outlet_list)
        self.K_dict = dict(zip(self.outlet_list, self.K_list))

        self.f = open('%s/project_info.py' % (self.pamt['file_path']), 'w')
        message = """
print('start script')
body_list = %s
body_number = len(body_list)

selection = Selection.Create(GetRootPart().GetAllBodies())
result = RenameObject.Execute(selection,"solid")

result = Copy.ToClipboard(Selection.Create(GetRootPart().GetAllBodies()))
result = Paste.FromClipboard()

# Delete Selection
selection = Selection.Create(GetRootPart().Components[:])
result = Delete.Execute(selection)

for i in range(body_number):
    result = Copy.ToClipboard(Selection.Create(GetRootPart().Bodies[0]))
    result = Paste.FromClipboard()

for i in range(body_number):
    selection = Selection.Create(GetRootPart().Bodies[-1-i])
    result = RenameObject.Execute(selection, body_list[i])

selection = Selection.Create(GetRootPart().Bodies[-body_number:])
result = ComponentHelper.CreateSeparateComponents(selection, None)

for i in range(body_number):
    selection = Selection.CreateByNames(body_list[i])
    result = Delete.Execute(selection)

# face rename
face_list = %s
for i in range(len(face_list)):
    primarySelection = Selection.Create(GetRootPart())
    secondarySelection = Selection()
    result = NamedSelection.Create(primarySelection, secondarySelection)

for i in range(len(face_list)):
    result = NamedSelection.Rename("Group%%s"%%(i+1), face_list[i])

# options = ShareTopologyOptions()
# options.Tolerance = MM(0.01)
# result = ShareTopology.FindAndFix(options)

# save file
options = ExportOptions.Create()
DocumentSave.Execute(r"%s", options)
print('script finished')
""" % (self.body_list, self.face_list, self.pamt['cad_save_path'])
        self.f.write(message)
        self.f.close()

    def show_c(self):
        dic = {}
        dic['evap'] = self.evap_c
        dic['hc'] = self.hc_c
        dic['valve'] = self.valve_c
        dic['fan'] = self.fan_c

        for i in self.body_list:
            try:
                dic[i].show()
            except Exception as e:
                pass
        if 'fan' not in self.body_list:
            self.mass_inlet_c.show()
        if self.energy_checkbox.isChecked():
            self.temp_c.show()

        self.show_c_on = True
        self.snip_switch()

    def pamt_GUI(self):
        self.mode_info_frame.hide()
        self.return_btn.show()
        self.start_btn.show()
        self.show_c()

        self.view_path_init()

    def launchCAD(self):
        self.pamt_GUI()
        self.launch_progress_display(35)
        self.append_text('正在打开CAD, 请大佬耐心等待')
        self.CAD_thread = SCDM()
        self.CAD_thread.start()
        self.CAD_thread.finishCAD.connect(self.append_text)

    def launch_progress_display(self, seconds):
        self.launch_time = timer(seconds)
        self.launch_time.start()
        self.launch_time.time_count.connect(self.time_bar)

    def time_bar(self, msg):
        self.interact_edit.undo()

        cad_progress = '正在打开CAD, 请大佬耐心等待' + ' (⊙_⊙) ' * (msg + 1)
        self.append_text(cad_progress)

    def import_info(self):
        path = QFileDialog.getOpenFileName(self, '选择要输入的参数模板',
                                           r'C:\Users\BZMBN4\Desktop', 'CSV Files (*.csv)')
        if path[0] != '':
            csv_path = path[0]
            info = self.csv_import(csv_path)
            self.outlet_list = []
            self.outlet_K = []
            for i in info:
                name = i + '_edit'
                widget = self.findChild(QLineEdit, name)
                if widget != None:
                    widget.setText(str(info[i]))
                if 'outlet' in i:
                    self.import_outlet = True
                    self.outlet_list.append(i)
                    self.outlet_K.append(str(info[i]))
                    self.K_dict[i] = str(info[i])

            self.outlet_number.setValue(len(self.outlet_list))
            self.project_name_edit.setText(info['project_name'])
            self.version_name_edit.setText('V')

            self.append_text('参数模板:%s导入成功' % path[0])

    def csv_import(self, excel_path):
        with open(excel_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            info = {}
            for row in reader:
                info[row[0]] = row[1]

        return info

    def case_address(self):
        case_out = QFileDialog.getExistingDirectory(self, '选择项目路径', 'C:/Users/BZMBN4/Desktop/')
        self.case_path = case_out
        self.project_address_edit.setText(self.case_path)

    def export_pamt(self):
        self.pamt_dict()
        try:
            self.pamt.update(self.K_dict)
        except Exception as e:
            print(e)

        path = QFileDialog.getSaveFileName(self, directory='%s'%(self.project_address_edit.text()),
                                           filter='CSV, *.csv')
        try:
            csv_save_path = path[0]
            self.write_CSV(csv_save_path)
            os.system(csv_save_path)
        except Exception as e:
            print('export error:', e)
            print('Error in file:', e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print('Error in line:', e.__traceback__.tb_lineno)  # 发生异常所在的行数
            self.append_text('导出地址有错误，请重新选择')

    def write_CSV(self, csv_path):
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            for i in self.pamt.keys():
                writer.writerow([i, self.pamt[i]])

        self.append_text('已创建新参数表:%s ' % (csv_path))
        self.interact_edit.moveCursor(QTextCursor.End)

    def unit_convert(self):
        self.volume_unit = Ui_unit()
        self.volume_unit.show()
        self.volume_unit.unit_convert_result.connect(self.volume_input)

    def porous_choose(self, btn_name):
        self.porous_model = Ui_porous()
        self.porous_model.show()
        self.porous_model.load_btn.clicked.connect(lambda: self.porous_import(btn_name))

    def porous_import(self, btn_name):
        C1 = self.porous_model.c1_edit.text()
        C2 = self.porous_model.c2_edit.text()
        c1_edit = btn_name + '_c1_edit'
        c2_edit = btn_name + '_c2_edit'
        widget1 = self.findChild(QLineEdit, c1_edit)
        widget2 = self.findChild(QLineEdit, c2_edit)
        widget1.setText(str(C1))
        widget2.setText(str(C2))
        self.porous_model.close()

    def volume_input(self, msg):
        self.mass_inlet_edit.setText(msg)

    def pamt_dict(self):
        self.pamt['project_name'] = self.project_name_edit.text()
        self.pamt['version'] = self.version_name_edit.text()
        self.pamt['file_path'] = self.project_address_edit.text()
        self.pamt['edit_time'] = self.version_date_edit.text()
        self.pamt['cad_name'] = self.pamt['project_name'] + '_' + self.pamt['version'] + '_' + self.pamt['edit_time']
        self.pamt['cad_save_path'] = self.pamt['file_path'] + '/' + self.pamt['cad_name'] + '.scdoc'
        self.pamt['mass_inlet'] = self.mass_inlet_edit.text()

        if 'evap' in self.body_list:
            self.pamt['evap_c1'] = self.evap_c1_edit.text()
            self.pamt['evap_c2'] = self.evap_c2_edit.text()
            self.pamt['evap_x1'] = self.evap_x1_edit.text()
            self.pamt['evap_y1'] = self.evap_y1_edit.text()
            self.pamt['evap_z1'] = self.evap_z1_edit.text()
            self.pamt['evap_x2'], self.pamt['evap_y2'], self.pamt['evap_z2'] = \
                self.porous_d2(self.pamt['evap_x1'], self.pamt['evap_y1'], self.pamt['evap_z1'])

        if 'hc' in self.body_list:
            self.pamt['hc_c1'] = self.hc_c1_edit.text()
            self.pamt['hc_c2'] = self.hc_c2_edit.text()
            self.pamt['hc_x1'] = self.hc_x1_edit.text()
            self.pamt['hc_y1'] = self.hc_y1_edit.text()
            self.pamt['hc_z1'] = self.hc_z1_edit.text()
            self.pamt['hc_x2'], self.pamt['hc_y2'], self.pamt['hc_z2'] = \
                self.porous_d2(self.pamt['hc_x1'], self.pamt['hc_y1'], self.pamt['hc_z1'])

        if 'valve' in self.body_list:
            self.pamt['valve_td'] = self.valve_td_edit.text()
            self.pamt['valve_rp'] = self.valve_rp_edit.text()

        if 'fan' in self.body_list:
            self.pamt['fan_ox'] = self.fan_ox_edit.text()
            self.pamt['fan_oy'] = self.fan_oy_edit.text()
            self.pamt['fan_oz'] = self.fan_oz_edit.text()
            self.pamt['fan_dx'] = self.fan_dx_edit.text()
            self.pamt['fan_dy'] = self.fan_dy_edit.text()
            self.pamt['fan_dz'] = self.fan_dz_edit.text()
            self.pamt['RPM'] = self.RPM_edit.text()

        if self.energy_checkbox.isChecked():
            self.pamt['temp_inlet'] = self.temp_inlet_edit.text()
            self.pamt['temp_hc'] = self.temp_hc_edit.text()

    def porous_d2(self, x, y, z):
        try:
            x = float(x)
            y = float(y)
            z = float(z)
            d1 = [x, y, z]
            d2 = [0, 0, 0]

            for i in d1:
                if i == 0:
                    d2[d1.index(i)] = 1
                    return d2
            d2[1] = -z / y
            d2[2] = 1
            return d2
        except Exception as e:
            print('porous_c contains zero')
            return [None, None, None]

    def view_path_init(self):
        self.view_path_db = {}
        view_path_file = r'C:\Users\BZMBN4\Desktop\fluent-command\view_path.csv'

        with open(view_path_file, 'r', newline='') as f:
            view_path_csv = csv.DictReader(f)
            for row in view_path_csv:
                self.view_path_db[row['project_name']] = row['view_path']
            self.view_path_combox.clear()
            self.view_path_combox.addItems(self.view_path_db.keys())

        self.view_path_choose()
        self.view_path_combox.activated.connect(self.view_path_choose)

    def view_path_choose(self):
        view_file_name = self.view_path_combox.currentText()
        self.view_path = self.view_path_db[view_file_name]

    def create_tui(self):
        self.check_part()
        self.pamt_dict()
        self.energy_check = self.energy_checkbox.isChecked()
        from tui_run import get_tui
        try:
            get_tui(self.pamt, self.body_list, self.energy_check, self.K_dict,
                self.porous_list, self.up_list, self.dead_zone_list, self.internal_face, self.view_path)
        except Exception as e:
            print('error:', e)
            print('error in file:', e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print('error in line:', e.__traceback__.tb_lineno)  # 发生异常所在的行数

    def begin(self):
        self.start_btn.setDisabled(True)
        self.create_tui()

        self.mesh_condition = '启动fluent'
        self.append_text(self.mesh_condition)

        self.mesh_thread = fluent_mesh(self.jou_mesh_path)
        self.mesh_thread.start()
        self.mesh_clock()
        self.mesh_thread.mesh_feedback.connect(self.mesh_msg)
        self.mesh_thread.mesh_timeuse.connect(self.mesh_time_use)
        self.mesh_thread.mesh_finish.connect(self.mesh_finish_msg)

        self.actionstop.setEnabled(True)

    def mesh_clock(self):
        try:
            size = self.get_FileSize(self.pamt['cad_save_path'])
            print("文件路径：%s\n大小：%s MB" % (self.pamt['cad_save_path'], size))
        except Exception as e:
            self.append_text('模型文件未找到，请检查')
        mesh_time = 120
        self.timer(mesh_time)
        self.time_running.connect(self.mesh_clock_show)

    def get_FileSize(self, file_path):
        fsize = os.path.getsize(file_path)
        fsize = fsize / float(1024 * 1024)
        return round(fsize, 3)

    def mesh_clock_show(self, msg):
        dot_list = ['.   ', '..  ', '... ', '....']
        remain_time = self.total_time - msg
        dot_circle = dot_list[msg % 4]
        remain_time_string = '   网格阶段剩余%s秒' % (remain_time)
        clock_msg = self.mesh_condition + dot_circle + remain_time_string

        self.interact_edit.undo()
        self.append_text(clock_msg)

    def mesh_msg(self, msg):
        self.mesh_condition = msg

    def mesh_time_use(self, msg):
        self.step = msg

    def mesh_finish_msg(self, msg):
        self.interact_edit.undo()
        self.append_text(msg)
        self.solver_btn.click()

    def solver(self):
        self.start_btn.setDisabled(True)
        self.solver_btn.setDisabled(True)
        self.actionstop.setEnabled(True)

        self.solver_condition = '启动fluent...'
        self.append_text(self.solver_condition)

        self.solver_thread = fluent_solver(self.jou_solve_path)
        self.solver_thread.start()
        # self.solver_clock()
        # self.solver_thread.solver_feedback.connect(self.solver_msg)
        # self.solver_thread.solver_timeuse.connect(self.solver_time_use)
        # self.solver_thread.solver_finish.connect(self.solver_finish_msg)

    def timer(self, total_seconds):
        self.clock = QBasicTimer()
        self.step = 0
        self.clock.start(1000, self)
        self.total_time = total_seconds

    def timerEvent(self, e):
        if self.step >= self.total_time:
            self.clock.stop()
            return

        self.step = self.step + 1
        self.time_running.emit(self.step)


class Ui_tip(Ui_tip_widget, QWidget):
    def __init__(self):
        super(Ui_tip_widget, self).__init__()
        self.setupUi(self)


class Ui_cal_K(Ui_K_calculator, QWidget):
    K_result = pyqtSignal(str)

    def __init__(self):
        super(Ui_K_calculator, self).__init__()
        self.setupUi(self)
        self.cal_method()
        self.QP_btn.click()

    def initialize(self):
        self.R_frame.hide()
        self.QP_frame.hide()

    def cal_method(self):
        self.R_btn.clicked.connect(lambda: self.choosen_method(self.R_frame, self.R_method))
        self.QP_btn.clicked.connect(lambda: self.choosen_method(self.QP_frame, self.QP_method))

    def choosen_method(self, show_frame, method):
        self.initialize()
        show_frame.show()
        self.K_cal_btn.disconnect()
        self.K_cal_btn.clicked.connect(method)

    def QP_method(self):
        ls = float(self.volume_edit.text())
        mm2 = float(self.area_edit.text())
        p = float(self.pressure_edit.text())
        rho = 1.225

        m3s = ls / 1000
        m2 = mm2/1000/1000
        v = m3s/m2

        K = 2*p/rho/v**2
        self.K_result.emit("%.3f" % K)

    def R_method(self):
        r = float(self.R_edit.text())
        mm2 = float(self.area_edit.text())
        rho = 1.225

        m2 = mm2 / 1000 / 1000

        K = 1000*2*r*m2**2/rho
        self.K_result.emit("%.3f" % K)


class Ui_unit(Ui_unit_converter, QWidget):
    unit_convert_result = pyqtSignal(str)

    def __init__(self):
        super(Ui_unit, self).__init__()
        self.setupUi(self)
        self.unit_btn()
        self.default_state()

    def default_state(self):
        self.l_btn.click()
        self.s_btn.click()

    def unit_btn(self):
        self.kg_btn.clicked.connect(lambda: self.volume_label_show('Kg', 1))
        self.m3_btn.clicked.connect(lambda: self.volume_label_show('M3', 1.225))
        self.l_btn.clicked.connect(lambda: self.volume_label_show('L', 0.001225))

        self.h_btn.clicked.connect(lambda: self.time_label_show('H', 3600))
        self.min_btn.clicked.connect(lambda: self.time_label_show('Min', 60))
        self.s_btn.clicked.connect(lambda: self.time_label_show('S', 1))

        self.confirm_btn.clicked.connect(self.calculate)

    def volume_label_show(self, text, factor):
        self.volume_label.setText(text)
        self.volume_factor = factor

    def time_label_show(self, text, factor):
        self.time_label.setText(text)
        self.time_factor = factor

    def calculate(self):
        if self.value_edit.text() == '':
            value = 0
        else:
            value = float(self.value_edit.text())
        result = round(value*self.volume_factor/self.time_factor, 5)
        self.unit_convert_result.emit(str(result))


class SCDM(QThread):
    finishCAD = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SCDM, self).__init__(parent)

    def run(self):
        import subprocess
        p = subprocess.Popen(r'C:\Program Files\ANSYS Inc\v191\scdm\SpaceClaim.exe', shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        # out = out.decode()

        self.finishCAD.emit('CAD软件已关闭')


class timer(QThread):
    time_count = pyqtSignal(int)

    def __init__(self, second):
        super(timer, self).__init__()
        self.second = second
        self.timer = QBasicTimer()
        self.step = 0
        self.timer.start(1000, self)

    def run(self):
        pass

    def timerEvent(self, e):
        if self.step >= self.second:
            self.timer.stop()
            return

        self.step = self.step + 1
        self.time_count.emit(self.step)


class fluent_mesh(QThread):
    mesh_feedback = pyqtSignal(str)
    mesh_timeuse = pyqtSignal(int)
    mesh_finish = pyqtSignal(str)

    def __init__(self, tui):
        super(fluent_mesh, self).__init__()
        self.tui = tui

    def run(self):
        start_time = time.strftime('%M:%S', time.localtime(time.time()))
        import subprocess
        self.p = subprocess.Popen(r'cd C:\\Program Files\\ANSYS Inc\\v191\\fluent\\ntbin\\win64 && '
                           r'fluent 3d -meshing -t4 -gu -i %s' % (self.tui),
                                  shell=True, stdout=subprocess.PIPE)

        nl = 0
        finish_count = 0
        while self.p.poll() == None:
            nl += 1
            line = self.p.stdout.readline()
            self.msg = line.decode()
            print(nl, self.msg)

            if (nl > 30) & (nl <= 50):
                self.stage_report('Cleanup script file is', 'load_time_begin', '载入模型', 29)
            elif (nl > 50) & (nl <= 130):
                self.stage_report('They will be imported in whatever units they were created', 'face_mesh_time_start',
                '处理面网格', 80)
            elif (nl > 130) & (nl <= 200):
                if 'the previous max quality' in self.msg:
                    msg_strip = self.msg.strip()
                    face_mesh_quality = msg_strip[-8:]
                self.stage_report('/objects/volumetric-regions/compute', 'volume_mesh_time_start',
                                  '处理体网格', 83)
            elif (nl > 200) & (nl <= 420):
                self.stage_report('/mesh/check-quality', 'mesh_finish_time', '网格生成完毕', 113)
                if 'Minimum Orthogonal Quality' in self.msg:
                    msg_strip = self.msg.strip()
                    volume_mesh_quality = float(msg_strip[-11:-7])/10.0
            elif (nl > 420) & (finish_count < 2):
                if 'Writing "' in self.msg:
                    finish_count = 1
                if finish_count == 1:
                    if 'Done.' in self.msg:
                        finish_count = 2
                        end_time = time.strftime('%M:%S', time.localtime(time.time()))
                        print(end_time)
                        print('总共有%s行输出语句' % nl)
        else:
            self.mesh_timeuse.emit(120)
            self.mesh_finish.emit('网格生成完毕')

    def stage_report(self, stage_marker, stage_name, report_msg, timeuse):
        if stage_marker in self.msg:
            stage_time = time.strftime('%M:%S', time.localtime(time.time()))
            self.mesh_feedback.emit(report_msg)
            self.mesh_timeuse.emit(timeuse)
            print('%s%s' % (stage_name, stage_time))

    def stop_mesh(self):
        self.p.terminate()
    

class fluent_solver(QThread):
    solver_feedback = pyqtSignal(str)

    def __init__(self, tui):
        super(fluent_solver, self).__init__()
        self.tui = tui

    def run(self):
        import subprocess
        self.p = subprocess.Popen(r'cd C:\\Program Files\\ANSYS Inc\\v191\\fluent\\ntbin\\win64 && '
                           r'fluent 3d -t12 -gu -i %s' % (self.tui), shell=True, stdout=subprocess.PIPE)

        nl = 0
        finish_count = 0
        while self.p.poll() == None:
            line = self.p.stdout.readline()
            self.msg = line.decode()
            print(nl, self.msg)
            nl += 1

        print('总共有%s行输出语句'%nl)

    def stop_solver(self):
        self.p.terminate()


if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())


