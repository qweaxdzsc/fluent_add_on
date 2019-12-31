import os
import fluent_tui
import numpy as np

project_title = '137DGR'
version_name = 'V1'
cad_name = '137DGR'
project_path = r"G:\volute_PQ\137DGR"

RPM_list = [2400+i*200 for i in range(10)]
print('used RPM list', RPM_list)

K_formal = np.linspace(1, 1.02, 20)
K_list = [round(i**500, 2) for i in K_formal]

print('used K_list', K_list)

whole_jou = ''
jou_out = project_path
jou_title = project_title + '-' + version_name + '-TUI'
txt_name = jou_out + '\\' + jou_title + '.jou'            # txt final path
print('output journal in:', txt_name)
jou = open(txt_name, 'w')

CFD = fluent_tui.tui(whole_jou, project_title, version_name, project_path, cad_name)

CFD.mesh.import_CAD()
CFD.mesh.size_scope_global()
CFD.mesh.size_scope_curv('fan_blade_curv', 'fan_blade', 0.4, 4, 1.2, 16)
CFD.mesh.size_scope_prox('fan_blade_prox', 'fan_blade', 0.8, 4, 1.2, 2)
CFD.mesh.size_scope_curv('fan_out_curv', 'fan_out', 1, 4.5, 1.2, 18)
CFD.mesh.size_scope_curv('volute_curv', 'volute', 0.8, 5.2, 1.2, 16)
CFD.mesh.size_scope_prox('volute_prox', 'volute', 0.8, 5.2, 1.2, 2)
CFD.mesh.size_scope_prox('global_prox', '', 0.8, 5.5, 1.2, 1)
CFD.mesh.size_scope_soft('inlet', '*inlet*', 14)
CFD.mesh.compute_size_field()
CFD.mesh.write_size_field()
CFD.mesh.import_surface_mesh()

CFD.mesh.general_improve(0.75)
CFD.mesh.fix_slivers()
CFD.mesh.compute_volume_region()
CFD.mesh.volume_mesh_change_type(dead_zone_list=['fan_blade'])
CFD.mesh.auto_mesh_volume(1.25)
CFD.mesh.auto_node_move(0.8, 6)
CFD.mesh.rename_cell(zone_list=['ai', 'fan', 'volute'])
CFD.mesh.retype_face(face_list=['inlet'], face_type='pressure-inlet')
CFD.mesh.retype_face(face_list=['fanin, fan_out'], face_type='internal')
CFD.mesh.retype_face(face_list=['outlet*'], face_type='outlet-vent')
CFD.mesh.prepare_for_solve()
CFD.mesh.write_case()
CFD.mesh.switch_to_solver()

fan_origin = [4.95264, 0.83289, 1.16223]
fan_axis = [0, -1, 0]

CFD.setup.rescale()
CFD.setup.turb_models()
CFD.setup.rotation_volume(RPM_list[0], fan_origin, fan_axis, 'fan')
CFD.setup.BC_pressure_inlet('inlet')
CFD.setup.BC_outlet_vent(K_list[0], 'outlet')
CFD.setup.solution_method()
CFD.setup.report_definition('volume', 'surface-volumeflowrate', ['outlet*'])
CFD.setup.report_definition('mass-flux', 'surface-massflowrate', ['inlet*', 'outlet*'], 'no')
CFD.setup.convergence_criterion('volume')
CFD.setup.hyb_initialize()
CFD.setup.start_calculate(600)
CFD.setup.write_case_data()

CFD.post.create_result_file()
CFD.post.txt_surface_integrals('volume-flow-rate', ['inlet'])
CFD.post.txt_mass_flux()
CFD.post.txt_surface_integrals('area-weighted-avg', ['inlet*', 'outlet*'], 'pressure')
CFD.post.txt_moment(fan_origin, fan_axis)


K_reverse_list = K_list[::-1]
combox_list = []

for RPM in RPM_list:
    if RPM_list.index(RPM) % 2 == 0:
        for K in K_list:
            combox_list.append([RPM, K])
    else:
        for K in K_reverse_list:
            combox_list.append([RPM, K])

for i in combox_list[1:]:
    CFD.setup.rotation_volume(i[0], fan_origin, fan_axis, 'fan')
    CFD.setup.BC_outlet_vent(i[1], 'outlet')
    CFD.setup.start_calculate(400)

    CFD.version_name = '%s-%s' % (i[0], i[1])
    CFD.setup.write_case_data()

    CFD.txt_out = CFD.result_path + '\\' + CFD.version_name + '.txt'
    CFD.post.txt_surface_integrals('volume-flow-rate', ['inlet'])
    CFD.post.txt_mass_flux()
    CFD.post.txt_surface_integrals('area-weighted-avg', ['inlet*', 'outlet*'], 'pressure')
    CFD.post.txt_moment(fan_origin, fan_axis)


jou.write(CFD.whole_jou)
jou.close()
os.system(txt_name)