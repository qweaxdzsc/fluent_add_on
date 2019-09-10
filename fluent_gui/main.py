#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QBasicTimer
from PyQt5.QtGui import QTextCursor

from easy_test import Ui_MainWindow
from rename_tip import Ui_tip_widget
from unit_convertor import Ui_unit_converter
import time
import os
sys.path.append(r'C:/Users/BZMBN4/Desktop/Python-test')
import fluent_tui


class MyMainWindow(QMainWindow, Ui_MainWindow):
    time_running = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.mode_ui()
        self.account_info()
        self.get_date()

        self.pamt = {}
        self.body_list = []
        self.btn()

    def mode_ui(self):
        self.mode_info_frame.show()
        self.start_btn.hide()
        self.mass_inlet.hide()
        self.return_btn.hide()
        self.evap_c.hide()
        self.hc_c.hide()
        self.solver_btn.hide()
        self.valve_c.hide()
        self.temp_c.hide()

    def default_part_tree(self):
        self.part_tree.topLevelItem(0).setCheckState(0, QtCore.Qt.Unchecked)
        self.part_tree.topLevelItem(1).setCheckState(0, QtCore.Qt.Checked)
        self.part_tree.topLevelItem(2).setCheckState(0, QtCore.Qt.Unchecked)
        self.part_tree.topLevelItem(3).setCheckState(0, QtCore.Qt.Unchecked)
        self.part_tree.topLevelItem(4).setCheckState(0, QtCore.Qt.Unchecked)
        self.part_tree.topLevelItem(5).setCheckState(0, QtCore.Qt.Unchecked)
        self.part_tree.topLevelItem(6).setCheckState(0, QtCore.Qt.Unchecked)
        self.part_tree.topLevelItem(7).setCheckState(0, QtCore.Qt.Checked)
        self.part_tree.topLevelItem(8).setCheckState(0, QtCore.Qt.Checked)
        self.part_tree.topLevelItem(9).setCheckState(0, QtCore.Qt.Unchecked)
        self.part_tree.topLevelItem(10).setCheckState(0, QtCore.Qt.Unchecked)
        self.part_tree.topLevelItem(11).setCheckState(0, QtCore.Qt.Unchecked)
        self.distrib_number.setValue(1)
        self.outlet_number.setValue(1)

    def account_info(self):
        user = os.environ.get("USERNAME")
        self.username_label.setText('欢迎大佬%s' % (user))
        welcome_list = ['Hi,大佬%s，我们又见面了' % (user), 'Hello,欢迎大佬%s' % (user)]
        import random
        welcome_word = random.choice(welcome_list)
        self.interact_edit.append(welcome_word)

    def get_date(self):
        import time
        today = time.strftime('%y%m%d', time.localtime(time.time()))
        self.version_date_edit.setText(today)

    def btn(self):
        self.actionimport.triggered.connect(self.import_info)
        self.actionexport.triggered.connect(self.export_pamt)
        self.actionsolve.triggered.connect(self.quick_solve)
        self.project_address_explore.clicked.connect(self.case_address)

        self.quick_distribfc_btn.toggled.connect(self.quick_distrib_judge)
        self.quick_distribfh_btn.toggled.connect(self.quick_distrib_judge)
        self.quick_distribbil_btn.toggled.connect(self.quick_distrib_judge)
        self.quick_distriblin_btn.toggled.connect(self.quick_distrib_judge)
        self.finish_mode_info_btn.clicked.connect(self.into_CAD)

        self.unit_btn.clicked.connect(self.unit_convert)
        self.start_btn.clicked.connect(self.begin)
        self.return_btn.clicked.connect(self.mode_ui)
        self.solver_btn.clicked.connect(self.solver)

        self.show_workflow_btn.clicked.connect(lambda: self.append_text('功能未开放,敬请期待'))
        self.choose_evap_btn.clicked.connect(lambda: self.append_text('功能未开放,敬请期待'))
        self.actionalter_default_parameter.triggered.connect(lambda: self.append_text('功能未开放,敬请期待'))

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
                self.quick_distribfh_btn.click()
                self.version_name_edit.setText('V4-FH')
                self.project_address_edit.setText('C:/Users/BZMBN4/Desktop/test/test1')
                self.check_part()
                self.pamt_GUI()
                self.append_text('进入调试模式')

        if e.key() == Qt.Key_J:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:              # test mod shortcut
                self.create_tui()
                self.open_tui()

    def name_rule(self):
        reply = QMessageBox.about(self, '帮助——命名规则', '命名分为体与面的命名：\n'
                                                    '请选择存在的体部件或使用快捷模板（ctrl+英文首字母），并点击导入模板\n\n'
                                                    '完成后：\n'
                                                    '1.对于面：选择面，并在space claim group栏下对相应的名字使用右键-replace\n'
                                                    '2.对于体：请复制弹出窗口中 体名字 至space claim模型树中 指定体')

    def quick_solve(self):
        confirm_info = self.project_info_check()

        if confirm_info == True:
            self.check_part()
            self.pamt_GUI()
            self.start_btn.setText('网   格')
            self.solver_btn.show()
            self.append_text('警告：进入补算模式，请先确认正确的模型或网格')

    def quick_distrib_judge(self):
        if self.quick_distribfc_btn.isChecked() == True:
            self.default_part_tree()

        if self.quick_distribfh_btn.isChecked() == True:
            self.default_part_tree()
            self.part_tree.topLevelItem(9).setCheckState(0, QtCore.Qt.Checked)
            self.distrib_number.setValue(2)
            self.outlet_number.setValue(1)

        if self.quick_distribbil_btn.isChecked() == True:
            self.default_part_tree()
            self.part_tree.topLevelItem(9).setCheckState(0, QtCore.Qt.Checked)
            self.distrib_number.setValue(1)
            self.outlet_number.setValue(2)

        if self.quick_distriblin_btn.isChecked() == True:
            self.default_part_tree()
            self.part_tree.topLevelItem(9).setCheckState(0, QtCore.Qt.Checked)
            self.part_tree.topLevelItem(11).setCheckState(0, QtCore.Qt.Checked)
            self.energy_checkbox.setChecked(True)
            self.outlet_number.setValue(1)
            self.distrib_number.setValue(1)

    def into_CAD(self):
        confirm_info = self.project_info_check()

        if confirm_info == True:
            self.check_part()
            self.show_msg()
            self.launchCAD()
            self.pamt_GUI()
            self.launch_progress_display(35)

    def project_info_check(self):
        self.pamt_dict()
        if (self.pamt['project'] == '') | (self.pamt['version'] == '') | (self.pamt['file_path'] == ''):
            self.append_text('请大佬将项目信息填写完全')
            return False

        if self.pamt['version'][0] != 'V':
            self.append_text('大佬，版本号首字母必须为大写V')
            return False

        if os.path.exists('%s' % (self.pamt['file_path'])) is False:
            self.append_text('项目路径不存在，请大佬检查路径信息')
            return False
        else:
            if os.path.exists('%s/project_info.py' % (self.pamt['file_path'])) is True:
                os.remove('%s/project_info.py' % (self.pamt['file_path']))

        if os.path.exists(self.pamt['cad_save_path']) == True:
            reply = QMessageBox.warning(self, "警告", "检测到路径下已存在CAD文件%s,是否覆盖？" % (self.pamt['cad_name']),
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                result_file = 'result' + self.pamt['project'] + '_' + self.pamt['version']
                result_path = self.pamt['file_path'] + '\\' + result_file
                txt_out = result_path + '\\' + self.pamt['project'] + '.txt'
                if os.path.exists(txt_out):
                    os.remove(txt_out)
                return True
            elif reply == QMessageBox.No:
                return False

        return True

    def check_part(self):
        body_list = []
        face_list = ['inlet']
        if self.inlet_number.value() > 1:
            for i in range(self.inlet_number.value()-1):
                face_list.append('inlet%s' % (i+2))
        if self.part_tree.topLevelItem(0).checkState(0) == QtCore.Qt.Checked:
            body_list.append('inlet_sphere')
        if self.part_tree.topLevelItem(1).checkState(0) == QtCore.Qt.Checked:
            body_list.append('ai')
            if self.part_tree.topLevelItem(0).checkState(0) == QtCore.Qt.Checked:
                face_list.append('ai_in')
        if self.part_tree.topLevelItem(2).checkState(0) == QtCore.Qt.Checked:
            if self.part_tree.topLevelItem(3).checkState(0) == QtCore.Qt.Unchecked:
                print('filter and cone should be all checked')
            else:
                body_list.append('filter')
                body_list.append('cone')
                face_list.append('filter_in')
                face_list.append('filter_out')
        if self.part_tree.topLevelItem(4).checkState(0) == QtCore.Qt.Checked:
            if self.part_tree.topLevelItem(5).checkState(0) == QtCore.Qt.Unchecked:
                print('volute and fan should be all checked')
            else:
                body_list.append('volute')
                body_list.append('fan')
                if self.part_tree.topLevelItem(0).checkState(0) == QtCore.Qt.Checked:
                    face_list.append('fan_in')
                face_list.append('fan_out')
                face_list.append('fan_blade')
        if self.part_tree.topLevelItem(6).checkState(0) == QtCore.Qt.Checked:
            body_list.append('diffuser')
            if self.part_tree.topLevelItem(4).checkState(0) == QtCore.Qt.Checked:
                face_list.append('volute_out')
        if self.part_tree.topLevelItem(7).checkState(0) == QtCore.Qt.Checked:
            body_list.append('evap')
            face_list.append('evap_in')
            face_list.append('evap_out')
        if self.part_tree.topLevelItem(8).checkState(0) == QtCore.Qt.Checked:
            body_list.append('distrib')

        if self.part_tree.topLevelItem(9).checkState(0) == QtCore.Qt.Checked:
            body_list.append('hc')
            face_list.append('hc_in')
            face_list.append('hc_out')

        if self.part_tree.topLevelItem(10).checkState(0) == QtCore.Qt.Checked:
            body_list.append('ptc')
            face_list.append('ptc_in')
            face_list.append('ptc_out')
        if self.part_tree.topLevelItem(11).checkState(0) == QtCore.Qt.Checked:
            body_list.append('valve')

        face_list.append('outlet')
        if self.outlet_number.value() > 1:
            for i in range(self.outlet_number.value()-1):
                face_list.append('outlet%s'%(i+2))
        if self.distrib_number.value() > 1:
            distrib_index = body_list.index('distrib')
            body_list[distrib_index] = 'distrib1'
            for i in range(self.distrib_number.value() - 1):
                body_list.append('distrib%s' % (i + 2))

        print('body_list:%s\nface_list:%s'%(body_list, face_list))

        self.face_list = face_list
        self.body_list = body_list

    def show_msg(self):
        self.dialog_tip = Ui_tip()
        self.msg()
        self.dialog_tip.show()

    def msg(self):
        self.dialog_tip.exit_btn.clicked.connect(self.dialog_tip.close)
        self.dialog_tip.label_tip.setText("面命名模板创建完成\n请复制以下体名字至模型树")

        for i in range(len(self.body_list)):
            self.dialog_tip.lineEdit = QtWidgets.QLineEdit(self.dialog_tip)
            self.dialog_tip.lineEdit.setObjectName("lineEdit%s" % (i + 1))
            self.dialog_tip.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
            self.dialog_tip.lineEdit.setText(self.body_list[i])

            self.dialog_tip.lineEdit.setMinimumSize(100, 20)
            self.dialog_tip.lineEdit.setMaximumSize(QtCore.QSize(150, 25))
            self.dialog_tip.verticalLayout.addWidget(self.dialog_tip.lineEdit)

    def show_c(self):
        dic = {}

        dic['evap'] = self.evap_c
        dic['hc'] = self.hc_c
        dic['valve'] = self.valve_c

        for i in self.body_list:
            try:
                dic[i].show()
            except Exception as e:
                pass

        if self.energy_checkbox.isChecked() is True:
            self.temp_c.show()

    def pamt_GUI(self):
        self.mode_info_frame.hide()
        self.return_btn.show()
        self.mass_inlet.show()
        self.show_c()

        self.start_btn.show()

    def launchCAD(self):
        self.f = open('%s/project_info.py' % (self.pamt['file_path']), 'w')
        message = """   
print('start script')
body_list = %s
body_number = len(body_list)

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

selection = Selection.Create(GetRootPart().Bodies[:])
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
    
options = ShareTopologyOptions()
options.Tolerance = MM(0.01)
result = ShareTopology.FindAndFix(options)

# save file
options = ExportOptions.Create()
DocumentSave.Execute(r"%s", options)
print('script finished')
""" % (self.body_list, self.face_list, self.pamt['cad_save_path'])
        self.f.write(message)
        self.f.close()
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
        path = QFileDialog.getOpenFileName(self, '选择要输入的Excel模板',
                                           r'C:\Users\BZMBN4\Desktop\test\test1\V4-FH.xlsx', 'Excel Files (*.xlsx; *.xls; *.xlsm)')
        if path[0] != '':
            excel_path = path[0]
            info, squence = self.excel_import(excel_path)

            self.project_name_edit.setText(info['project'])
            self.version_name_edit.setText('V')
            self.mass_inlet_edit.setText(str(info['massflowin']))
            self.evap_c1_edit.setText(str(info['evap_C1']))
            self.evap_c2_edit.setText(str(info['evap_C2']))
            self.evap_x1_edit.setText(str(info['evap_dx1']))
            self.evap_y1_edit.setText(str(info['evap_dy1']))
            self.evap_z1_edit.setText(str(info['evap_dz1']))
            self.evap_x2_edit.setText(str(info['evap_dx2']))
            self.evap_y2_edit.setText(str(info['evap_dy2']))
            self.evap_z2_edit.setText(str(info['evap_dz2']))
            if 'hc_C1' in info.keys():
                self.hc_c1_edit.setText(str(info['hc_C1']))
                self.hc_c2_edit.setText(str(info['hc_C2']))
                self.hc_x1_edit.setText(str(info['hc_dx1']))
                self.hc_y1_edit.setText(str(info['hc_dy1']))
                self.hc_z1_edit.setText(str(info['hc_dz1']))
                self.hc_x2_edit.setText(str(info['hc_dx2']))
                self.hc_y2_edit.setText(str(info['hc_dy2']))
                self.hc_z2_edit.setText(str(info['hc_dz2']))

            self.append_text('Excel:%s导入成功' % path[0])

    def excel_import(self, excel_path):
        import xlrd
        wb = xlrd.open_workbook(excel_path)
        sheet = wb.sheet_by_name('info')

        nrows = sheet.nrows
        row_squence = list(range(1, nrows + 1))

        info = dict(zip(sheet.col_values(0), sheet.col_values(1)))
        squence = dict(zip(sheet.col_values(0), row_squence))

        return info, squence

    def case_address(self):
        case_out = QFileDialog.getExistingDirectory(self, '选择项目路径', 'C:/Users/BZMBN4/Desktop/')
        self.case_path = case_out
        self.project_address_edit.setText(self.case_path)

    def export_pamt(self):
        self.pamt_dict()

        path = QFileDialog.getSaveFileName(self, directory='%s'%(self.project_address_edit.text()),
                                           filter='Excel, *.xlsx')
        try:
            excel_save_path = path[0]
            print(excel_save_path)
            self.create_excel(excel_save_path)
            os.system(excel_save_path)
        except Exception as e:
            self.append_text('导出地址有错误，请重新选择')

    def create_excel(self, excel_name):
        import openpyxl
        workbook = openpyxl.Workbook()
        worksheet = workbook.create_sheet(title='info', index=0)
        excel_info = list(self.pamt.keys())
        excel_pamt = list(self.pamt.values())
        for i in range(len(excel_info)):
            worksheet.cell(i+1, 1, excel_info[i])
            worksheet.cell(i+1, 2, excel_pamt[i])

        worksheet.column_dimensions['A'].width = 15
        worksheet.column_dimensions['B'].width = 40

        workbook.save(filename=excel_name)
        self.append_text('已创建新Excel:%s 新表名: info' % (excel_name))
        self.interact_edit.moveCursor(QTextCursor.End)

    def unit_convert(self):
        self.volume_unit = Ui_unit()
        self.volume_unit.show()
        self.volume_unit.unit_convert_result.connect(self.volume_input)

    def volume_input(self, msg):
        self.mass_inlet_edit.setText(msg)

    def pamt_dict(self):
        self.pamt['project'] = self.project_name_edit.text()
        self.pamt['version'] = self.version_name_edit.text()
        self.pamt['file_path'] = self.project_address_edit.text()
        self.pamt['edit_time'] = self.version_date_edit.text()
        self.pamt['cad_name'] = self.pamt['project'] + '_' + self.pamt['version'] + '_' + self.pamt['edit_time']
        self.pamt['cad_save_path'] = self.pamt['file_path'] + '/' + self.pamt['cad_name'] + '.scdoc'
        self.pamt['massflowin'] = self.mass_inlet_edit.text()

        if 'evap' in self.body_list:
            self.pamt['evap_C1'] = self.evap_c1_edit.text()
            self.pamt['evap_C2'] = self.evap_c2_edit.text()
            self.pamt['evap_dx1'] = self.evap_x1_edit.text()
            self.pamt['evap_dy1'] = self.evap_y1_edit.text()
            self.pamt['evap_dz1'] = self.evap_z1_edit.text()
            self.pamt['evap_dx2'] = self.evap_x2_edit.text()
            self.pamt['evap_dy2'] = self.evap_y2_edit.text()
            self.pamt['evap_dz2'] = self.evap_z2_edit.text()

        if 'hc' in self.body_list:
            self.pamt['hc_C1'] = self.hc_c1_edit.text()
            self.pamt['hc_C2'] = self.hc_c2_edit.text()
            self.pamt['hc_dx1'] = self.hc_x1_edit.text()
            self.pamt['hc_dy1'] = self.hc_y1_edit.text()
            self.pamt['hc_dz1'] = self.hc_z1_edit.text()
            self.pamt['hc_dx2'] = self.hc_x2_edit.text()
            self.pamt['hc_dy2'] = self.hc_y2_edit.text()
            self.pamt['hc_dz2'] = self.hc_z2_edit.text()

        if 'valve' in self.body_list:
            self.pamt['valve_ox'] = self.valve_ox_edit.text()
            self.pamt['valve_oy'] = self.valve_oy_edit.text()
            self.pamt['valve_oz'] = self.valve_oz_edit.text()
            self.pamt['valve_dx'] = self.valve_dx_edit.text()
            self.pamt['valve_dy'] = self.valve_dy_edit.text()
            self.pamt['valve_dz'] = self.valve_dz_edit.text()
            self.pamt['valve_td'] = self.valve_td_edit.text()
            self.pamt['valve_rp'] = self.valve_rp_edit.text()
            self.pamt['valve_sa'] = self.valve_sa_edit.text()
            self.pamt['valve_fa'] = self.valve_fa_edit.text()

        if self.energy_checkbox.isChecked() is True:
            self.pamt['temp_inlet'] = self.temp_inlet_edit.text()
            self.pamt['temp_hc'] = self.temp_hc_edit.text()

    def create_tui(self):
        self.pamt_dict()
        d = self.pamt
        print(d['file_path'])
        self.check_part()

        whole_jou = ''
        project_title = d['project']
        version_name = d['version']
        cad_name = d['cad_name']

        case_out = d['file_path']

        self.jou_mesh_path = d['file_path'] + '/' + project_title + '-' + version_name + '-mesh-TUI.jou'  # txt final path
        print('output journal in:', d['file_path'])
        jou_mesh = open(self.jou_mesh_path, 'w')

        if 'hc' in self.body_list:
            internal_list = ['evap*', 'hc*']

            uni_face_list = ['evap_in', 'evap_out', 'hc_out']
            pressure_face_list = ['*inlet*', 'evap_in', 'evap_out', 'hc_in', 'hc_out', '*outlet*']

        else:
            internal_list = ['evap*']
            uni_face_list = ['evap_in', 'evap_out']
            pressure_face_list = ['*inlet*', 'evap_in', 'evap_out', '*outlet*']
        mesh_zone_list = self.body_list
        dead_zone_list = []
        if 'valve' in self.body_list:
            dead_zone_list.append('valve')

        CFD = fluent_tui.tui(whole_jou, project_title, version_name, case_out, cad_name)
        CFD.mesh.import_distrib()
        CFD.mesh.general_improve()
        CFD.mesh.fix_slivers()
        CFD.mesh.general_improve()
        CFD.mesh.compute_volume_region(dead_zone_list)
        CFD.mesh.volume_mesh_change_type()
        CFD.mesh.auto_mesh_volume()
        CFD.mesh.auto_node_move(0.7, 10)
        CFD.mesh.rename_cell(zone_list=mesh_zone_list)
        CFD.mesh.retype_face(face_list=['inlet*'], face_type='pressure-inlet')
        CFD.mesh.retype_face(face_list=internal_list, face_type='internal')

        if self.energy_checkbox.isChecked() is True:
            CFD.mesh.retype_face(face_list=['hc*'], face_type='radiator')

        CFD.mesh.retype_face(face_list=['outlet*'], face_type='outlet-vent')
        CFD.mesh.check_quality()
        CFD.mesh.prepare_for_solve()
        CFD.mesh.write_mesh()
        CFD.close_fluent()

        jou_mesh.write(CFD.whole_jou)
        jou_mesh.close()

        self.jou_solve_path = d['file_path'] + '/' + project_title + '-' + version_name + '-solve-TUI.jou'
        print('output journal in:', d['file_path'])
        jou_solve = open(self.jou_solve_path, 'w')

        evap_d1 = [d['evap_dx1'], d['evap_dy1'], d['evap_dz1']]
        evap_d2 = [d['evap_dx2'], d['evap_dy2'], d['evap_dz2']]
        mass_flux_list = ['inlet*', 'outlet*']

        CFD = fluent_tui.tui(whole_jou, project_title, version_name, case_out, cad_name)
        CFD.setup.read_mesh()
        CFD.setup.rescale()
        CFD.setup.turb_models()
        CFD.setup.porous_zone('evap', evap_d1, evap_d2, d['evap_C1'], d['evap_C2'])
        if 'hc' in self.body_list:
            hc_d1 = [d['hc_dx1'], d['hc_dy1'], d['hc_dz1']]
            hc_d2 = [d['hc_dx2'], d['hc_dy2'], d['hc_dz2']]
            CFD.setup.porous_zone('hc', hc_d1, hc_d2, d['hc_C1'], d['hc_C2'])
        CFD.setup.BC_type('inlet', 'mass-flow-inlet')
        CFD.setup.BC_type('outlet*()', 'outlet-vent')
        CFD.setup.BC_mass_flow_inlet('inlet', d['massflowin'])
        CFD.setup.BC_outlet_vent()
        CFD.setup.solution_method()
        if self.energy_checkbox.isChecked() is True:
            CFD.setup.energy_eqt('yes')
            CFD.setup.init_temperature('mass-flow-inlet', 'outlet-vent', d['temp_inlet'])
            CFD.setup.BC_outlet_vent(3.84, 'outlet_foot')
            CFD.setup.BC_outlet_vent(7, 'outlet_vent')
            CFD.setup.heat_flux('hc_in', 348.15)
            CFD.setup.heat_flux('hc_out', 348.15)
            CFD.setup.report_definition('temperature', 'surface-areaavg', ['outlet*'], 'yes', 'temperature')

        CFD.setup.report_definition('volume', 'surface-volumeflowrate', ['inlet*'])
        CFD.setup.report_definition('mass-flux', 'surface-massflowrate', mass_flux_list, 'no')
        CFD.setup.report_definition('pressure', 'surface-areaavg', ['evap_in'])
        CFD.setup.convergence_criterion()
        CFD.setup.hyb_initialize()
        CFD.setup.start_calculate(230)
        CFD.setup.write_case_data()

        volume_face_list = ['inlet*', 'outlet*']

        CFD.post.create_result_file()
        self.txt_surface_integrals('area-weighted-avg', ['outlet*'], 'temperature')
        CFD.post.txt_surface_integrals('volume-flow-rate', volume_face_list)
        CFD.post.txt_mass_flux()
        CFD.post.txt_surface_integrals('uniformity-index-area-weighted', uni_face_list, 'velocity-magnitude')
        CFD.post.txt_surface_integrals('area-weighted-avg', pressure_face_list, 'total-pressure')
        CFD.post.txt_surface_integrals('area-weighted-avg', pressure_face_list, 'pressure')
        CFD.post.create_contour('evap_out', 'evap_out')
        if 'hc' in self.body_list:
            CFD.post.create_contour('hc_out', 'hc_out')
        CFD.post.create_streamline('whole_pathline', 'inlet')
        CFD.post.create_streamline('distrib_pathline', 'evap_out', [0, 15])
        CFD.post.set_background()
        CFD.post.snip_avz(5, 'whole_pathline')
        CFD.post.snip_avz(6, 'distrib_pathline')
        CFD.post.snip_avz(7, 'evap_out')
        if 'hc' in self.body_list:
            CFD.post.snip_avz(9, 'hc_out')
        CFD.post.snip_model(10, 'model')
        CFD.close_fluent()

        jou_solve.write(CFD.whole_jou)
        jou_solve.close()

    def open_tui(self):
        os.system(self.jou_mesh_path)

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

    def mesh_clock(self):
        size = self.get_FileSize(self.pamt['cad_save_path'])
        print("文件路径：%s\n大小：%s MB" % (self.pamt['cad_save_path'], size))
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
        p = subprocess.Popen(r'C:\Program Files\ANSYS Inc\v191\scdm\SpaceClaim.exe', shell=True,
                             stdout=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode()
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
        print(start_time)
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
    

class fluent_solver(QThread):
    solver_feedback = pyqtSignal(str)

    def __init__(self, tui):
        super(fluent_solver, self).__init__()
        self.tui = tui

    def run(self):

        import subprocess
        self.p = subprocess.Popen(r'cd C:\\Program Files\\ANSYS Inc\\v191\\fluent\\ntbin\\win64 && '
                           r'fluent 3d -t4 -gu -i %s' % (self.tui), shell=True, stdout=subprocess.PIPE)

        nl = 0
        finish_count = 0
        while self.p.poll() == None:
            line = self.p.stdout.readline()
            self.msg = line.decode()
            print(nl, self.msg)
            nl += 1

        print('总共有%s行输出语句'%nl)


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        myWin = MyMainWindow()
        myWin.show()
        sys.exit(app.exec_())
    except:
        import traceback
        traceback.print_exc()