#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import cgitb

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, QFileInfo
from PyQt5.QtGui import QTextCursor

from ui_py.ui_main import Ui_MainWindow
from func.func_default_ui_set import default_ui
from func.func_short_key import short_key
from func.func_timer import launch_time_count, mesh_clock
from func.func_advanced import advanced_func
from func.func_check import check_func
from func.func_IEport import IEport
from func.func_porous_d2 import porous_d2
from func.func_scdm_script import create_import_script, create_rotate_script
from subUI.sub_unit_converter import subUI_unit_converter
from subUI.sub_porous_model import subUI_porous
from subUI.sub_k_test import subUI_outlet_assign
from fluent_command.tui_run import GetTui
from call_api.call_func import SCDM, fluent_mesh, fluent_solver


class MyMainWindow(QMainWindow, Ui_MainWindow):
    time_running = pyqtSignal(int)

    def __init__(self, app, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.default_ui = default_ui(self)
        self.advFunc = advanced_func(self, app)
        # ----------init parameter----------
        self.pamt = {}
        self.outlet_dict = {}
        self.K_dict = {}
        self.outlet_list = []
        self.body_list = []
        self.script_address = str()
        self.mesh_type = 'tet'
        self.show_c_on = False
        self.snip_on = True
        self.actionstop.setEnabled(False)
        self.import_outlet = False
        # --------init function---------
        self.short_key = short_key(self)
        self.check_func = check_func(self)
        self.IEport = IEport(self)
        self.btn()

    def btn(self):
        """
        Connect Signal and slot
        include all button and action signal
        :return:
        """
        # ------------menu action btn-----------------
        self.actionimport.triggered.connect(self.import_info)
        self.actionexport.triggered.connect(self.export_pamt)
        self.actionsolve.triggered.connect(self.advFunc.direct_solve)
        self.actionstop.triggered.connect(self.advFunc.force_stop)
        self.actiondarkstyle.triggered.connect(self.advFunc.darkstyle)
        self.action_mesh_poly.triggered.connect(lambda: self.choose_mesh_type('poly'))
        self.action_mesh_tet.triggered.connect(lambda: self.choose_mesh_type('tet'))

        self.cad_address_explore.clicked.connect(self.cad_address)
        # ------------quick mode radio btn------------
        self.quick_distribfc_btn.toggled.connect(self.short_key.quick_distrib_judge)
        self.quick_distribfh_btn.toggled.connect(self.short_key.quick_distrib_judge)
        self.quick_distribbil_btn.toggled.connect(self.short_key.quick_distrib_judge)
        self.quick_distriblin_btn.toggled.connect(self.short_key.quick_distrib_judge)
        self.finish_mode_info_btn.clicked.connect(self.into_CAD)
        # ------------parameter or launch related btn-------------------
        self.unit_btn.clicked.connect(self.unit_convert)
        self.choose_evap_btn.clicked.connect(lambda: self.porous_choose('evap'))
        self.choose_hc_btn.clicked.connect(lambda: self.porous_choose('hc'))
        self.choose_filter_btn.clicked.connect(lambda: self.porous_choose('filter'))
        self.start_btn.clicked.connect(self.begin)
        self.return_btn.clicked.connect(self.default_ui.mode_ui_default)
        self.solver_btn.clicked.connect(self.solver)
        # ------------ unavailable test btn------------------
        self.show_workflow_btn.clicked.connect(self.test)
        self.actionalter_default_parameter.triggered.connect(lambda: self.append_text('功能未开放,敬请期待'))

    def test(self):
        self.append_text('功能未开放,敬请期待')
        pass

    def append_text(self, msg):
        self.interact_edit.append(msg)
        self.interact_edit.moveCursor(QTextCursor.End)

    def into_CAD(self):
        self.confirm_info = self.project_info_check()
        self.need_launch_CAD = True

        if self.confirm_info:
            self.check_part()
            self.show_outlet_name()

    def project_info_check(self):
        self.pamt_dict()
        confirm_info = self.check_func.pjt_info_check(self.pamt)
        return confirm_info

    def check_part(self):
        body_list = []
        face_list = ['inlet']
        porous_list = []
        up_list = []
        dead_zone_list = []

        self.face_list, self.body_list, self.porous_list, self.up_list, self.dead_zone_list, self.internal_face = \
            self.check_func.part_check(body_list, face_list, porous_list, up_list, dead_zone_list)

    def show_outlet_name(self):
        self.outlet_assign = subUI_outlet_assign(self.outlet_dict)
        self.outlet_assign.show()
        self.outlet_assign.outlet_K_signal.connect(self.receive_outlet_info)

    def receive_outlet_info(self, outlet_dict):
        print('outlet_dict', outlet_dict)
        self.outlet_list = list(outlet_dict.keys())
        self.face_list.extend(self.outlet_list)
        for i in outlet_dict.keys():
            self.K_dict[i] = outlet_dict[i][-1]
        self.outlet_dict = outlet_dict
        # print(self.outlet_dict)
        # print(self.K_dict)
        self.pamt_dict()
        print(self.pamt['cad_name'])
        self.script_address = create_import_script(self.pamt['file_path'], self.pamt['open_cad_name'],
                                                   self.body_list, self.face_list, self.pamt['cad_save_path'])

        if self.need_launch_CAD:
            self.launchCAD()
            self.need_launch_CAD = False

    def show_c(self):
        dic = {}
        dic['evap'] = self.evap_c
        dic['hc'] = self.hc_c
        dic['filter'] = self.filter_c
        dic['valve1'] = self.valve_c
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

    def pamt_GUI(self):
        self.mode_info_frame.hide()
        self.return_btn.show()
        self.start_btn.show()
        self.show_c()

    def launchCAD(self):
        self.pamt_GUI()                                                 # show parameter GUI
        self.launch_time = launch_time_count(self, 35)                  # create thread must have self.
        self.append_text('正在打开CAD, 请大佬耐心等待')
        self.CAD_thread = SCDM(self.script_address)
        self.CAD_thread.start()
        self.CAD_thread.finishCAD.connect(self.append_text)

    def import_info(self):
        path = QFileDialog.getOpenFileName(self, '选择要输入的参数模板',
                                           r'C:\Users\BZMBN4\Desktop', 'CSV Files (*.csv)')
        self.import_outlet, self.outlet_dict, self.K_dict, self.outlet_dict = \
            self.IEport.import_pamt(path)

    def cad_address(self):
        get_file = QFileDialog.getOpenFileName(self, '选择模型文件', 'C:/Users/BZMBN4/Desktop/'
                                               )
        cad_path = get_file[0]
        self.cad_address_edit.setText(cad_path)

    def export_pamt(self):
        self.pamt_dict()
        try:
            self.pamt.update(self.outlet_dict)
        except Exception as e:
            print(e)

        path = QFileDialog.getSaveFileName(self, directory='%s'%(self.cad_address_edit.text()),
                                           filter='CSV, *.csv')
        self.IEport.export_pamt(path, self.pamt)

    def unit_convert(self):
        self.volume_unit = subUI_unit_converter()
        self.volume_unit.show()
        self.volume_unit.unit_convert_result.connect(self.volume_input)

    def volume_input(self, msg):
        self.mass_inlet_edit.setText(msg)

    def porous_choose(self, btn_name):
        self.porous_model = subUI_porous()
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

    def pamt_dict(self):
        self.pamt = dict()
        self.pamt['project_name'] = self.project_name_edit.text()
        self.pamt['version'] = self.version_name_edit.text()
        cad_path = QFileInfo(self.cad_address_edit.text())
        self.pamt['file_path'] = cad_path.absolutePath()
        self.pamt['open_cad_name'] = cad_path.fileName()
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
                porous_d2(self.pamt['evap_x1'], self.pamt['evap_y1'], self.pamt['evap_z1'])

        if 'hc' in self.body_list:
            self.pamt['hc_c1'] = self.hc_c1_edit.text()
            self.pamt['hc_c2'] = self.hc_c2_edit.text()
            self.pamt['hc_x1'] = self.hc_x1_edit.text()
            self.pamt['hc_y1'] = self.hc_y1_edit.text()
            self.pamt['hc_z1'] = self.hc_z1_edit.text()
            self.pamt['hc_x2'], self.pamt['hc_y2'], self.pamt['hc_z2'] = \
                porous_d2(self.pamt['hc_x1'], self.pamt['hc_y1'], self.pamt['hc_z1'])

        if 'filter' in self.body_list:
            self.pamt['filter_c1'] = self.filter_c1_edit.text()
            self.pamt['filter_c2'] = self.filter_c2_edit.text()
            self.pamt['filter_x1'] = self.filter_x1_edit.text()
            self.pamt['filter_y1'] = self.filter_y1_edit.text()
            self.pamt['filter_z1'] = self.filter_z1_edit.text()
            self.pamt['filter_x2'], self.pamt['filter_y2'], self.pamt['filter_z2'] = \
                porous_d2(self.pamt['filter_x1'], self.pamt['filter_y1'], self.pamt['filter_z1'])

        if 'valve1' in self.body_list:
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

    def choose_mesh_type(self, mesh_type):
        self.mesh_type = mesh_type

    def create_tui(self):
        self.check_part()
        self.pamt_dict()
        self.energy_check = self.energy_checkbox.isChecked()
        if 'valve1' in self.body_list:
            valve_number = 0
            for i in self.body_list:
                if 'valve' in i:
                    valve_number += 1
            create_rotate_script(self.pamt['file_path'], self.pamt['open_cad_name'], self.pamt['valve_td'],
                                 self.pamt['valve_rp'], valve_number)
        self.tui = GetTui(self.pamt, self.body_list, self.energy_check, self.K_dict,
                          self.porous_list, self.up_list, self.dead_zone_list, self.internal_face,
                          self.mesh_type)

    def begin(self):
        self.start_btn.setDisabled(True)
        self.create_tui()
        self.mesh_condition = '启动fluent'
        self.append_text(self.mesh_condition)

        self.mesh_thread = fluent_mesh(self.tui.jou_mesh_path)
        self.mesh_thread.start()
        self.mesh_clock = mesh_clock(self, 120)
        self.mesh_thread.mesh_feedback.connect(self.mesh_msg)
        self.mesh_thread.mesh_timeuse.connect(self.mesh_time_use)
        self.mesh_thread.mesh_finish.connect(self.mesh_finish_msg)

        self.actionstop.setEnabled(True)

    def mesh_msg(self, msg):
        self.mesh_condition = msg

    def mesh_time_use(self, msg):
        self.mesh_clock.mesh_timer.step = msg

    def mesh_finish_msg(self, msg):
        self.interact_edit.undo()
        self.append_text(msg)
        # self.solver_btn.click()   # auto start calculation

    def solver(self):
        self.start_btn.setDisabled(True)
        self.solver_btn.setDisabled(True)
        self.actionstop.setEnabled(True)

        self.solver_condition = '启动fluent...'
        self.append_text(self.solver_condition)

        self.solver_thread = fluent_solver(self.tui.jou_solve_path)
        self.solver_thread.start()
        # self.solver_clock()
        # self.solver_thread.solver_feedback.connect(self.solver_msg)
        # self.solver_thread.solver_timeuse.connect(self.solver_time_use)
        # self.solver_thread.solver_finish.connect(self.solver_finish_msg)


if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    myWin = MyMainWindow(app)
    myWin.show()
    sys.exit(app.exec_())


