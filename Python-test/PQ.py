import os
import fluent_tui
import numpy as np

project_title = 'PQ_9BUX'
version_name = 'V5_2800RPM'
cad_name = 'PQ_9BUX_V5'
project_path = r"G:\_volute_PQ\9BUX\9BUX_V5\9BUX_2800RPM"

RPM_list = [2800]
print('used RPM list', RPM_list)

# K_formal = np.linspace(1, 1.02, 20)
P_list = [300,
          # 325,
          350,
          # 360,
          # 380,
          400,
          # 430,
          # 450,
          ]

print('used K_list', P_list)

mesh_jou_name = f'{project_path}\\{project_title}_{version_name}_mesh.jou'          # txt final path
print('output journal in:', mesh_jou_name)
mesh_jou = open(mesh_jou_name, 'w')
whole_jou = ''

CFD = fluent_tui.tui(whole_jou, project_title, version_name, project_path, cad_name)

CFD.mesh.import_CAD()
CFD.mesh.size_scope_global(0.3, 16)
CFD.mesh.size_scope_curv('fan_blade_curv', 'fan_blade', 0.4, 3, 1.2, 16)
CFD.mesh.size_scope_prox('fan_blade_prox', 'fan_blade', 0.8, 4, 1.2, 2)
CFD.mesh.size_scope_curv('fan_out_curv', 'fan_out', 1, 4, 1.2, 18)
CFD.mesh.size_scope_curv('volute_curv', 'volute', 0.7, 4, 1.2, 16)
CFD.mesh.size_scope_prox('volute_prox', 'volute', 0.8, 5, 1.2, 2)
CFD.mesh.size_scope_curv('box_curv', 'box', 1, 15, 1.25, 16)
CFD.mesh.size_scope_prox('box_prox', 'box', 1, 15, 1.25, 2)
CFD.mesh.size_scope_curv('point_curv', 'pressure_points', 0.5, 1, 1.2, 16)
CFD.mesh.size_scope_prox('point_prox', 'pressure_points', 0.5, 1, 1.2, 2)
CFD.mesh.size_scope_prox('global_prox', '', 0.8, 7, 1.2, 1)
CFD.mesh.size_scope_soft('inlet', '*inlet*', 14)

CFD.mesh.compute_size_field()
CFD.mesh.write_size_field()
CFD.mesh.import_surface_mesh()

CFD.mesh.general_improve()
CFD.mesh.fix_slivers()
CFD.mesh.compute_volume_region()
CFD.mesh.volume_mesh_change_type(dead_zone_list=['fan_blade'])
CFD.mesh.auto_mesh_volume(1.25)
CFD.mesh.auto_node_move(0.85, 6)
CFD.mesh.rename_cell(zone_list=['ai', 'fan', 'volute', 'box'])
CFD.mesh.retype_face(face_list=['inlet'], face_type='pressure-inlet')
CFD.mesh.retype_face(face_list=['fan_in', 'fan_out', 'volute_out'], face_type='internal')
CFD.mesh.retype_face(face_list=['outlet*'], face_type='pressure-outlet')
CFD.mesh.prepare_for_solve()
CFD.mesh.write_mesh()
# CFD.mesh.switch_to_solver()
mesh_jou.write(CFD.whole_jou)
mesh_jou.close()


solve_jou_name = f'{project_path}\\{project_title}_{version_name}_solve.jou'          # txt final path
print('output journal in:', solve_jou_name)
solve_jou = open(solve_jou_name, 'w')
whole_jou = ''

CFD = fluent_tui.tui(whole_jou, project_title, version_name, project_path, cad_name)
fan_origin = [2.18137, 0.355, 1.22597]
fan_axis = [0, 0, 1]
CFD.setup.start_transcript()
CFD.setup.read_mesh()
CFD.setup.rescale()
CFD.setup.turb_models()
CFD.setup.rotation_volume(RPM_list[0], fan_origin, fan_axis, 'fan')
CFD.setup.BC_pressure_inlet('inlet')
CFD.setup.BC_type('outlet', 'pressure-outlet')
CFD.setup.BC_pressure_outlet(['outlet'], P_list[0])
# CFD.setup.BC_outlet_vent(P_list[0], 'outlet')
CFD.setup.solution_method()
CFD.setup.report_definition('volume', 'surface-volumeflowrate', ['outlet*'])
CFD.setup.report_definition('mass-flux', 'surface-massflowrate', ['inlet*', 'outlet*'], 'no')
CFD.setup.report_definition('pressure', 'surface-areaavg', ['pressure_points'])
CFD.setup.convergence_criterion('volume')
CFD.setup.hyb_initialize()
CFD.setup.start_calculate(1500)
CFD.setup.write_case_data()

CFD.post.create_result_file()
CFD.post.txt_surface_integrals('volume-flow-rate', ['inlet'])
CFD.post.txt_mass_flux()
CFD.post.txt_surface_integrals('area-weighted-avg', ['inlet*', 'outlet*', 'pressure*'], 'pressure')
CFD.post.txt_moment(fan_origin, fan_axis)


K_reverse_list = P_list[::-1]
combox_list = []

for RPM in RPM_list:
    if RPM_list.index(RPM) % 2 == 0:
        for P in P_list:
            combox_list.append([RPM, P])
    else:
        for P in K_reverse_list:
            combox_list.append([RPM, P])

print(combox_list)
for i in combox_list[1:]:
    CFD.setup.rotation_volume(i[0], fan_origin, fan_axis, 'fan')
    CFD.setup.BC_pressure_outlet(['outlet'], i[1])
    # CFD.setup.BC_outlet_vent(i[1], 'outlet')
    CFD.setup.hyb_initialize()
    CFD.setup.start_calculate(1500)
    CFD.version_name = '%s-%s' % (i[0], i[1])
    CFD.setup.write_case_data()

    CFD.txt_out = CFD.result_path + '\\' + CFD.version_name + '.txt'
    CFD.post.txt_surface_integrals('volume-flow-rate', ['inlet'])
    CFD.post.txt_mass_flux()
    CFD.post.txt_surface_integrals('area-weighted-avg', ['inlet*', 'outlet*', 'pressure*'], 'pressure')
    CFD.post.txt_moment(fan_origin, fan_axis)


solve_jou.write(CFD.whole_jou)
solve_jou.close()
os.system(mesh_jou_name)
os.system(solve_jou_name)