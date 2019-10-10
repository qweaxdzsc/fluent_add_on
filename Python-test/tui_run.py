import os
import fluent_tui
jou_out = r'C:\Users\BZMBN4\Desktop'       # txt output root

# txt name
whole_jou = ''
project_title = '706'
version_name = 'V7-pp2-defrost'
cad_name = '706-v7-pp2-defrost'
case_out = r'G:\519(706)\519-defrost\706-defrost-pp2-v7'

jou_title = project_title + '-' + version_name + '-TUI'
txt_name = jou_out + '\\' + jou_title + '.jou'            # txt final path
print('output journal in:', txt_name)
jou = open(txt_name, 'w')


CFD = fluent_tui.tui(whole_jou, project_title, version_name, case_out, cad_name)

CFD.mesh.simple_import('volute', '*evap* *hc* *filter*')
# CFD.mesh.simple_import('volute', '*evap*')
# CFD.mesh.simple_import('volute', '*evap* *hc*')
# CFD.mesh.import_distrib()
CFD.mesh.general_improve()
CFD.mesh.fix_slivers()

CFD.mesh.compute_volume_region()
CFD.mesh.volume_mesh_change_type(dead_zone_list=['fan_blade'])
CFD.mesh.auto_mesh_volume()
CFD.mesh.auto_node_move()
CFD.mesh.rename_cell(zone_list=['ai', 'evap', 'fan', 'hc', 'volute', 'filter', 'distrib', 'cone'])
# CFD.mesh.rename_cell(zone_list=['ai', 'evap', 'fan', 'volute'])
# CFD.mesh.rename_cell(zone_list=['ai', 'evap', 'hc', 'fan', 'volute'])
CFD.mesh.retype_face(face_list=['inlet', 'inlet2'], face_type='pressure-inlet')
# CFD.mesh.retype_face(face_list=['inlet'], face_type='pressure-inlet')
CFD.mesh.retype_face(face_list=['fan_in', 'fan_out', 'evap*', 'hc*', 'filter*'], face_type='internal')
# CFD.mesh.retype_face(face_list=['fan_in', 'fan_out', 'evap*'], face_type='internal')
# CFD.mesh.retype_face(face_list=['fan_in', 'fan_out', 'evap*', 'hc*'], face_type='internal')
CFD.mesh.retype_face(face_list=['outlet*'], face_type='outlet-vent')
CFD.mesh.write_case()
CFD.mesh.prepare_for_solve()
CFD.mesh.switch_to_solver()


fan_origin = [2.13586, 0.38647, 0.81608]
fan_axis = [0, 0, 1]
rpm = 3650
evap_d1 = [1, 0, 0]
evap_d2 = [0, 1, 0]
hc_d1 = [1, 0, 0]
hc_d2 = [0, 1, 0]
filter_d1 = [0, 0, 1]
filter_d2 = [1, 1, 0]


mass_flux_list = ['inlet*', 'outlet*']
pressure_face_list = ['inlet*', 'fan_in', 'fan_out', 'evap_in', 'evap_out', 'hc*', 'outlet*']

CFD.setup.rescale()
# CFD.setup.convert_polymesh()
CFD.setup.turb_models()
CFD.setup.rotation_volume(rpm, fan_origin, fan_axis, 'fan')
CFD.setup.porous_zone('evap', evap_d1, evap_d2, 2.68e+07, 484.96)
CFD.setup.porous_zone('filter', filter_d1, filter_d2, 6.86e+07, 457.7)
CFD.setup.porous_zone('hc', hc_d1, hc_d2, 3.49e+07, 623.3)
# CFD.setup.BC_type('inlet*()', 'pressure-inlet')
CFD.setup.BC_type('inlet*', 'pressure-inlet')
# CFD.setup.BC_type('inlet', 'mass-flow-inlet')
CFD.setup.BC_type('outlet*', 'outlet-vent')
# CFD.setup.BC_type('outlet_vr', 'outlet-vent')
CFD.setup.BC_pressure_inlet('inlet')
# CFD.setup.BC_mass_flow_inlet('inlet', 0.0735)
CFD.setup.BC_outlet_vent(4.1, 'outlet_foot')
# CFD.setup.BC_outlet_vent(23.19, 'outlet_p')
# CFD.setup.BC_outlet_vent(40.73, 'outlet_d')
CFD.setup.solution_method()
CFD.setup.report_definition('volume', 'surface-volumeflowrate', ['outlet*'])
CFD.setup.report_definition('mass-flux', 'surface-massflowrate', mass_flux_list, 'no')
# CFD.setup.report_definition('pressure', 'surface-areaavg', pressure_face_list)
CFD.setup.convergence_criterion()
CFD.setup.hyb_initialize()
CFD.setup.start_calculate(900)
# CFD.setup.start_calculate(230)
CFD.setup.write_case_data()


volume_face_list = ['inlet*', 'outlet*']
uni_face_list = ['evap_in', 'evap_out', 'hc_out']
view_path = r'G:\GE2_REAR\GE2-rear-command\GE2.vw'


CFD.post.create_result_file()
CFD.post.txt_surface_integrals('volume-flow-rate', volume_face_list)
CFD.post.txt_mass_flux()
CFD.post.txt_surface_integrals('uniformity-index-area-weighted', uni_face_list, 'velocity-magnitude')
CFD.post.txt_surface_integrals('area-weighted-avg', pressure_face_list, 'total-pressure')
CFD.post.txt_surface_integrals('area-weighted-avg', pressure_face_list, 'pressure')
CFD.post.txt_moment(fan_origin, fan_axis)
CFD.post.create_contour('evap_out', 'evap_out')
# CFD.post.create_contour('evap_out_0-2', 'evap_out', [0, 2])
CFD.post.create_contour('hc_out', 'hc_out')
CFD.post.create_streamline('whole_pathline', 'inlet')
CFD.post.create_streamline('distrib_pathline', 'evap_out', [0, 10])
CFD.post.read_view(view_path)
CFD.post.set_background()
CFD.post.snip_picture(5, 'whole_pathline', 'yes', 'yes')
CFD.post.snip_picture(6,  'distrib_pathline', 'yes')
CFD.post.snip_picture(7, 'evap_out')
# CFD.post.snip_picture(8, 'evap_out_0-2')
CFD.post.snip_picture(9, 'hc_out')
CFD.post.snip_model(10, 'model')
# CFD.post.simple_lin_post(47.97)
CFD.post.snip_mode_off()


jou.write(CFD.whole_jou)
jou.close()
os.system(txt_name)