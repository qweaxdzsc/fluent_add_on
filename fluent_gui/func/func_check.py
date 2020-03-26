import os
from PyQt5.QtWidgets import QMessageBox


class check_func():
    def __init__(self, ui):
        self.ui = ui

    def pjt_info_check(self, pamt):
        if (pamt['project_name'] == '') | (pamt['version'] == '') | (pamt['file_path'] == ''):
            self.ui.append_text('请大佬将项目信息填写完全')
            return False
    
        if not os.path.exists('%s' % (pamt['file_path'])):
            self.ui.append_text('项目路径不存在，请大佬检查路径信息')
            return False
        else:
            if os.path.exists('%s/project_info.py' % (pamt['file_path'])):
                os.remove('%s/project_info.py' % (pamt['file_path']))
    
        if os.path.exists(pamt['cad_save_path']):
            reply = QMessageBox.warning(self.ui, "警告", "检测到路径下已存在CAD文件%s,是否覆盖？" % (pamt['cad_name']),
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                result_file = 'result' + pamt['project_name'] + '_' + pamt['version']
                result_path = pamt['file_path'] + '\\' + result_file
                txt_out = result_path + '\\' + pamt['project_name'] + '.txt'
                if os.path.exists(txt_out):
                    os.remove(txt_out)
                return True
            elif reply == QMessageBox.No:
                return False
    
        return True
    
    def part_check(self, body_list, face_list, porous_list, up_list, dead_zone_list):
        ui = self.ui
        if ui.inlet_number.value() > 1:
            for i in range(ui.inlet_number.value() - 1):
                face_list.append('inlet%s' % (i + 2))
        if ui.part_tree.topLevelItem(0).checkState(0) == 2:
            body_list.append('inlet_sphere')
        if ui.part_tree.topLevelItem(1).checkState(0) == 2:
            body_list.append('ai')
            if ui.part_tree.topLevelItem(0).checkState(0) == 2:
                face_list.append('ai_in')
        if ui.part_tree.topLevelItem(2).checkState(0) == 2:
            if ui.part_tree.topLevelItem(3).checkState(0) == 0:
                print('filter and cone should be all checked')
            else:
                body_list.append('filter')
                body_list.append('cone')
                porous_list.append('filter')
                up_list.append('ai')
                face_list.append('filter_in')
                face_list.append('filter_out')
        if ui.part_tree.topLevelItem(4).checkState(0) == 2:
            if ui.part_tree.topLevelItem(5).checkState(0) == 0:
                print('volute and fan should be all checked')
            else:
                body_list.append('volute')
                up_list.append('volute')
                body_list.append('fan')
                dead_zone_list.append('fan_blade')
                if ui.part_tree.topLevelItem(0).checkState(0) == 2:
                    face_list.append('fan_in')
                if ui.part_tree.topLevelItem(1).checkState(0) == 2:
                    face_list.append('fan_in')
                face_list.append('fan_out')
                face_list.append('fan_blade')
        if ui.part_tree.topLevelItem(6).checkState(0) == 2:
            body_list.append('diffuser')
            if ui.part_tree.topLevelItem(4).checkState(0) == 2:
                face_list.append('volute_out')
        if ui.part_tree.topLevelItem(7).checkState(0) == 2:
            body_list.append('evap')
            porous_list.append('evap')
            face_list.append('evap_in')
            face_list.append('evap_out')
        if ui.part_tree.topLevelItem(8).checkState(0) == 2:
            body_list.append('distrib')

        if ui.part_tree.topLevelItem(9).checkState(0) == 2:
            body_list.append('hc')
            porous_list.append('hc')
            face_list.append('hc_in')
            face_list.append('hc_out')

        if ui.part_tree.topLevelItem(10).checkState(0) == 2:
            body_list.append('ptc')
            porous_list.append('ptc')
            face_list.append('ptc_in')
            face_list.append('ptc_out')
        if ui.part_tree.topLevelItem(11).checkState(0) == 2:
            body_list.append('valve')
            dead_zone_list.append('valve')

        if ui.distrib_number.value() > 1:
            distrib_index = body_list.index('distrib')
            body_list[distrib_index] = 'distrib1'
            for i in range(ui.distrib_number.value() - 1):
                body_list.append('distrib%s' % (i + 2))

        if ui.valve_number.value() > 1:
            valve_index = body_list.index('valve')
            body_list[valve_index] = 'valve1'
            for i in range(ui.valve_number.value() - 1):
                body_list.append('valve%s' % (i + 2))


        internal_face = face_list.copy()
        for i in face_list:
            if 'fan_blade' is i or 'inlet' is i:
                internal_face.remove(i)
        
        return face_list, body_list, porous_list, up_list, dead_zone_list, internal_face
