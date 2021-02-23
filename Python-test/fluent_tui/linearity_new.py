import numpy as np
import os
from fluent_tui import fluent_tui

project_title = 'BN'
version_name = 'V2_lin_bil'
cad_name = 'BN_V2_lin_bil'
project_path = r"G:\_HAVC_Project\BAONENG\BAONENG_lin_bil\BN_V2_lin_bil"

# valve_dir = [0, -1, 0]
# valve_origin = [5407.69, 869.38, 1022.1]
# linearity angle setup
total_angle = 70
start_angle = 7
points = 10


angle_array = np.linspace(start_angle, total_angle, points, endpoint=True)   # define your angle range and points
# angle_array = [round(i, 3) for i in angle_array]
angle_array = [int(i) for i in angle_array]

print('angle array:', angle_array)


mesh_jou_name = f'{project_path}\\{project_title}_{version_name}_mesh.jou'          # txt final path
print('output journal in:', mesh_jou_name)
mesh_jou = open(mesh_jou_name, 'w')
whole_jou = ''

CFD = fluent_tui.tui(whole_jou, project_title, version_name, project_path, cad_name)

# j = 0


for i in angle_array:
    # cad_lin_name = '%s_%s' % (cad_name, i)
    # rotate_angle = round(angle_array[j] - angle_array[j - 1], 3)
    # j = j + 1
    CFD.mesh.import_distrib(cad_name=cad_name)
    CFD.mesh.general_improve(0.75)
    CFD.mesh.fix_combo()
    CFD.mesh.compute_volume_region()
    CFD.mesh.volume_mesh_change_type(dead_zone_list=['valve'])
    # CFD.mesh.auto_mesh_volume(1.25)
    CFD.mesh.auto_mesh_volume(1.23, 'poly')
    CFD.mesh.auto_node_move(0.85, 6)
    CFD.mesh.rename_cell(zone_list=['ai', 'distrib1', 'distrib2', 'evap', 'hc'])
    CFD.mesh.retype_face(face_list=['inlet'], face_type='mass-flow-inlet')
    CFD.mesh.retype_face(face_list=['evap*', 'hc*'], face_type='internal')
    CFD.mesh.retype_face(face_list=['hc*'], face_type='radiator')
    CFD.mesh.retype_face(face_list=['outlet*'], face_type='outlet-vent')
    CFD.mesh.prepare_for_solve()
    CFD.mesh.write_lin_mesh(i)

CFD.close_fluent()

mesh_jou.write(CFD.whole_jou)
mesh_jou.close()
os.system(mesh_jou_name)


solve_jou_name = f'{project_path}\\{project_title}_{version_name}_solve.jou'          # txt final path
print('output journal in:', solve_jou_name)
solve_jou = open(solve_jou_name, 'w')
whole_jou = ''

CFD = fluent_tui.tui(whole_jou, project_title, version_name, project_path, cad_name)

mass_flux_list = ['inlet*', 'outlet*']

evap_d1 = [0.99756, -0.00144, 0.06975]
evap_d2 = [0, 1, 0]
hc_d1 = [-0.71643, 0, -0.69765]
hc_d2 = [0, 1, 0]

# CFD.mesh.switch_to_solver()
CFD.setup.start_transcript()
# CFD.setup.replace_lin_mesh(start_angle)
# CFD.setup.read_lin_mesh(start_angle)
CFD.case_out_path = project_path + '\\lin_mesh'
CFD.setup.read_mesh()
CFD.case_out_path = project_path
CFD.setup.rescale()
CFD.setup.turb_models()

CFD.setup.porous_zone('evap', evap_d1, evap_d2, 2.82e+07, 455.67)
CFD.setup.porous_zone('hc', hc_d1, hc_d2, 4.07e+07, 580.7)
# CFD.setup.BC_type('inlet', 'pressure-inlet')
CFD.setup.BC_type('inlet*()', 'mass-flow-inlet')
CFD.setup.BC_type('outlet*()', 'outlet-vent')
CFD.setup.solution_method()
CFD.setup.energy_eqt('yes')
# CFD.setup.BC_pressure_inlet('inlet')
CFD.setup.BC_mass_flow_inlet('inlet', 0.077)
CFD.setup.init_temperature('mass-flow-inlet', 'outlet-vent', 273.15)
# CFD.setup.BC_pressure_outlet('outlet1', 300)
CFD.setup.BC_outlet_vent(6.854, 'outlet_vent')
CFD.setup.BC_outlet_vent(3.934, 'outlet_foot')
# CFD.setup.BC_outlet_vent(0, 'outlet_sdl')
# CFD.setup.BC_outlet_vent(0, 'outlet_sdr')
# CFD.setup.BC_outlet_vent(0, 'outlet_cdl')
# CFD.setup.BC_outlet_vent(0, 'outlet_cdr')
# CFD.setup.BC_outlet_vent(0, 'outlet_ffl')
# CFD.setup.BC_outlet_vent(0, 'outlet_ffr')
# CFD.setup.BC_outlet_vent(0, 'outlet_rfl')
# CFD.setup.BC_outlet_vent(0, 'outlet_rfr')

CFD.setup.heat_flux('hc_out', 280.15)
CFD.setup.heat_flux('hc_in', 280.15)
# CFD.setup.heat_flux('hc_out', 0, 0, heat_flux=angle_array[0] / 85 * 3500 / 0.0225)
# CFD.setup.heat_flux('hc_in', 0, 0, heat_flux=angle_array[0] / 85 * 3500 / 0.0225)
CFD.setup.report_definition('temperature', 'surface-areaavg', ['outlet*'], 'yes', 'temperature')
CFD.setup.report_definition('mass-flux', 'surface-massflowrate', mass_flux_list, 'no')
CFD.setup.convergence_criterion()
CFD.setup.hyb_initialize()
CFD.setup.start_calculate(300)
CFD.setup.write_lin_case_data(start_angle)
CFD.post.simple_lin_post(start_angle)
# CFD.post.txt_moment([0.073, -0.129, 0.082], [0, 0, 1], 'valve_up valve_bottom')

for i in angle_array[1:]:
    # CFD.setup.replace_lin_mesh(i)
    # CFD.setup.rescale()
    # CFD.setup.init_temperature('mass-flow-inlet', 'outlet-vent', 273.15)
    CFD.setup.heat_flux('hc_out', i+273.15)
    CFD.setup.heat_flux('hc_in', i+273.15)
    CFD.setup.hyb_initialize()
    CFD.setup.start_calculate(300)
    CFD.setup.write_lin_case_data(i)
    CFD.post.simple_lin_post(i)
    # CFD.post.txt_surface_integrals('area-weighted-avg', ['dct*'], 'temperature')
    # CFD.post.txt_moment([0.073, -0.129, 0.082], [0, 0, 1], 'valve_up valve_bottom')

solve_jou.write(CFD.whole_jou)
solve_jou.close()
os.system(solve_jou_name)