import numpy as np
import os
import fluent_tui



whole_jou = ''
project_title = 'GE2-rear3'
version_name = 'ppb-lin'
cad_name = 'GE2-rear3_ppb-lin'
project_path = r"G:\GE2_REAR\GE2-rear-round3\GE2-test-lin"

# valve_dir = [0, -1, 0]
# valve_origin = [5407.69, 869.38, 1022.1]
# linearity angle setup
total_angle = 100
start_angle = 10
points = 9

end_angle = total_angle-start_angle

angle_array = np.linspace(start_angle, end_angle, points, endpoint=True)   # define your angle range and points
# angle_array = [round(i, 3) for i in angle_array]
angle_array = [int(i) for i in angle_array]

print('angle array:', angle_array)

jou_out = project_path
cad_path = project_path + '\\' + cad_name
case_out = project_path + '\\lin_case'
mesh_out_path = project_path + '\\lin_mesh'
# result_path = case_out

jou_title = project_title + '-' + version_name + '-TUI'
txt_name = jou_out + '\\' + jou_title + '.jou'            # txt final path
print('output journal in:', txt_name)
jou = open(txt_name, 'w')

CFD = fluent_tui.tui(whole_jou, project_title, version_name, project_path, cad_name)
j = 0


for i in angle_array:
    cad_lin_name = '%s_%s' % (cad_name, i)

    # rotate_angle = round(angle_array[j] - angle_array[j - 1], 3)
    j = j + 1
    CFD.mesh.import_distrib(cad_name=cad_lin_name)
    CFD.mesh.general_improve(0.75)
    CFD.mesh.fix_slivers()
    CFD.mesh.compute_volume_region()
    CFD.mesh.volume_mesh_change_type(dead_zone_list=['valve1', 'valve2', 'valve3', 'valve4'])
    CFD.mesh.auto_mesh_volume(1.25)
    # CFD.mesh.auto_mesh_volume(1.25, 'poly')
    CFD.mesh.auto_node_move(0.8, 6)
    CFD.mesh.rename_cell(zone_list=['ai', 'distrib', 'evap', 'hc'])
    CFD.mesh.retype_face(face_list=['inlet'], face_type='mass-flow-inlet')
    CFD.mesh.retype_face(face_list=['evap*'], face_type='internal')
    CFD.mesh.retype_face(face_list=['hc*'], face_type='radiator')
    CFD.mesh.retype_face(face_list=['outlet*'], face_type='outlet-vent')
    CFD.mesh.prepare_for_solve()
    CFD.mesh.write_lin_mesh(i)


mass_flux_list = ['inlet*', 'outlet*']

evap_d1 = [0.84805, 0, 0.52992]
evap_d2 = [0, 1, 0]
hc_d1 = [0.85717, 0, 0.51504]
hc_d2 = [0, 1, 0]

CFD.mesh.switch_to_solver()
CFD.setup.replace_lin_mesh(start_angle)
# CFD.setup.read_lin_mesh(start_angle)
CFD.setup.rescale()
# CFD.setup.convert_polymesh()
CFD.setup.turb_models()

CFD.setup.porous_zone('evap', evap_d1, evap_d2, 2.82e+07, 455.67)
CFD.setup.porous_zone('hc', hc_d1, hc_d2, 6.62e+07, 505.43)
# CFD.setup.BC_type('inlet', 'pressure-inlet')
CFD.setup.BC_type('inlet*()', 'mass-flow-inlet')
CFD.setup.BC_type('outlet*()', 'outlet-vent')
CFD.setup.solution_method()
CFD.setup.energy_eqt('yes')
# CFD.setup.BC_pressure_inlet('inlet')
CFD.setup.init_temperature('mass-flow-inlet', 'outlet-vent', 273.15)
CFD.setup.BC_mass_flow_inlet('inlet', 0.055125)
CFD.setup.BC_outlet_vent(11.2, 'outlet_d')
CFD.setup.BC_outlet_vent(8.037, 'outlet_p')
CFD.setup.heat_flux('hc_in', 348.15)
CFD.setup.heat_flux('hc_out', 348.15)
CFD.setup.report_definition('temperature', 'surface-areaavg', ['outlet*'], 'yes', 'temperature')
CFD.setup.report_definition('mass-flux', 'surface-massflowrate', mass_flux_list, 'no')
CFD.setup.convergence_criterion()
CFD.setup.hyb_initialize()
CFD.setup.start_calculate(270)
CFD.setup.write_lin_case_data(start_angle)
CFD.post.simple_lin_post(start_angle)

for i in angle_array[1:]:
    CFD.setup.replace_lin_mesh(i)
    CFD.setup.rescale()
    CFD.setup.init_temperature('mass-flow-inlet', 'outlet-vent', 273.15)
    CFD.setup.BC_mass_flow_inlet('inlet', 0.055125)
    CFD.setup.heat_flux('hc_in', 348.15)
    CFD.setup.heat_flux('hc_out', 348.15)
    CFD.setup.hyb_initialize()
    CFD.setup.start_calculate(260)
    CFD.setup.write_lin_case_data(i)
    CFD.post.simple_lin_post(i)

jou.write(CFD.whole_jou)
jou.close()
os.system(txt_name)