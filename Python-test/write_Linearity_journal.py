import os
import fluent_tui
import numpy as np
# jou_out = r'C:\Users\BZMBN4\Desktop'       # txt output root

# txt name
whole_jou = ''
project_title = 'MQBA1'
version_name = 'V6_lin_defrost'
cad_name = 'MQBA1_V6_defrost'
case_out = r'G:\_HAVC_Project\MQBA1\MQBA1_V6_lin_defrost'

angle_array = [30, 40, 50, 60]

print('angle array:', angle_array)

jou_out = case_out
jou_title = project_title + '-' + version_name + '-TUI'
txt_name = jou_out + '\\' + jou_title + '.jou'            # txt final path
print('output journal in:', txt_name)
jou = open(txt_name, 'w')

CFD = fluent_tui.tui(whole_jou, project_title, version_name, case_out, cad_name)

for i in angle_array:
    CFD.mesh.delete_cell('*distrib*')
    CFD.mesh.face_zone_delete('*valve*')
    cad_lin_name = 'valve_%s' % i
    CFD.mesh.import_distrib(cad_name=cad_lin_name, append='yes')
    CFD.mesh.object_merge('*')
    CFD.mesh.fix_slivers()
    CFD.mesh.fix_slivers()
    CFD.mesh.compute_volume_region()
    CFD.mesh.volume_mesh_change_type(dead_zone_list=['*valve*'])
    CFD.mesh.auto_fill_volume('*distrib*')
    CFD.mesh.auto_node_move(0.85)
    CFD.mesh.rename_cell(zone_list=['diffuser', 'distrib', 'evap', 'hc', 'rear_duct'])
    CFD.mesh.retype_face(face_list=['inlet'], face_type='mass-flow-inlet')
    CFD.mesh.retype_face(face_list=['evap*', 'hc*', 'dct*'], face_type='internal')
    CFD.mesh.retype_face(face_list=['hc*'], face_type='radiator')
    CFD.mesh.retype_face(face_list=['outlet*'], face_type='outlet-vent')
    CFD.mesh.prepare_for_solve()
    CFD.mesh.write_lin_mesh(i)


jou.write(CFD.whole_jou)
jou.close()
os.system(txt_name)