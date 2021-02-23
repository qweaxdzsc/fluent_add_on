import os
from fluent_tui import fluent_tui

# jou_out = r'C:\Users\BZMBN4\Desktop'       # txt output root

# txt name
whole_jou = ''
project_title = 'K2'
version_name = 'V4_vent'
cad_name = 'K2_V4_vent_200428'
case_out = r'G:\_HAVC_Project\K2\K2_VENT\K2_V4_VENT'


jou_out = case_out
jou_title = project_title + '-' + version_name + '-TUI'
txt_name = jou_out + '\\' + jou_title + '.jou'            # txt final path
print('output journal in:', txt_name)
jou = open(txt_name, 'w')


CFD = fluent_tui.tui(whole_jou, project_title, version_name, case_out, cad_name)

# CFD.mesh.simple_import(['ai', 'volute'], ['evap', 'filter'])
CFD.mesh.simple_import(['ai', 'volute'], ['evap', 'filter', 'hc'])
# CFD.mesh.simple_import(['volute'], ['evap'])
# CFD.mesh.simple_import(['volute'], ['evap', 'hc'])
# CFD.mesh.import_distrib()
CFD.mesh.general_improve()
CFD.mesh.fix_slivers()

CFD.mesh.compute_volume_region()
CFD.mesh.volume_mesh_change_type()
# CFD.mesh.volume_mesh_change_type(dead_zone_list=['fan_blade'])
CFD.mesh.auto_mesh_volume(mesh_type='tet')
CFD.mesh.auto_node_move(skewness=0.85)
CFD.mesh.rename_cell(zone_list=['ai', 'evap', 'fan', 'volute', 'filter', 'hc', 'distrib1', 'distrib2', 'cone'])
# CFD.mesh.rename_cell(zone_list=['ai', 'ai_duct', 'filter', 'cone', 'evap', 'fan', 'volute', 'distrib'])
# CFD.mesh.rename_cell(zone_list=['ai', 'evap', 'fan', 'volute', 'distrib'])
# CFD.mesh.rename_cell(zone_list=['ai', 'evap', 'hc', 'fan', 'volute'])
# CFD.mesh.retype_face(face_list=['inlet', 'inlet2'], face_type='pressure-inlet')
CFD.mesh.retype_face(face_list=['inlet'], face_type='inlet-vent')
CFD.mesh.retype_face(face_list=['fan_in', 'fan_out', 'evap*', 'filter*', 'hc*'], face_type='internal')
# CFD.mesh.retype_face(face_list=['ai_in', 'fan_in', 'fan_out', 'evap*', 'filter*'], face_type='internal')
# CFD.mesh.retype_face(face_list=['fan_in', 'fan_out', 'evap*'], face_type='internal')
# CFD.mesh.retype_face(face_list=['ai_in', 'fan_in', 'fan_out', 'evap*', 'hc*'], face_type='internal')
CFD.mesh.retype_face(face_list=['outlet*'], face_type='outlet-vent')
CFD.mesh.write_mesh()
CFD.mesh.prepare_for_solve()
CFD.mesh.switch_to_solver()

fan_origin = [0.14943, -0.88991, 0.19135]
fan_axis = [0.17365, 0, -0.98481]
rpm = 3700
evap_d1 = [0.97815, -0.00001, -0.20791]
evap_d2 = [0, 1, 0]
hc_d1 = [-0.96592, 0, -0.25882]
hc_d2 = [0, 1, 0]
filter_d1 = [0, 0, 1]
filter_d2 = [1, 1, 0]


mass_flux_list = ['inlet*', 'outlet*']
pressure_face_list = ['inlet*', 'filter*', 'fan_in', 'fan_out', 'evap_in', 'evap_out', 'hc*', 'outlet*']

CFD.setup.rescale()
# CFD.setup.convert_polymesh()
CFD.setup.turb_models()
CFD.setup.rotation_volume(rpm, fan_origin, fan_axis, 'fan')
CFD.setup.porous_zone('evap', evap_d1, evap_d2, 3.22e+07, 547.9)
CFD.setup.porous_zone('filter', filter_d1, filter_d2, 4.01e+07, 206)
CFD.setup.porous_zone('hc', hc_d1, hc_d2, 5.86e+07, 674.4)
CFD.setup.BC_type('inlet*()', 'pressure-inlet')
# CFD.setup.BC_type('inlet', 'mass-flow-inlet')
# CFD.setup.BC_type('outlet*()', 'outlet-vent')
# CFD.setup.BC_type('outlet_vr', 'outlet-vent')
# CFD.setup.BC_pressure_inlet('inlet')
# CFD.setup.BC_mass_flow_inlet('inlet', 0.0735)
CFD.setup.BC_inlet_vent('inlet', 8.5)
CFD.setup.BC_outlet_vent(5.117, 'outlet_cdl')
CFD.setup.BC_outlet_vent(5.117, 'outlet_cdr')
CFD.setup.BC_outlet_vent(27.46, 'outlet_sdl')
CFD.setup.BC_outlet_vent(27.46, 'outlet_sdr')

CFD.setup.BC_outlet_vent(17.8, 'outlet_svl')
CFD.setup.BC_outlet_vent(17.8, 'outlet_svr')
CFD.setup.BC_outlet_vent(2.6, 'outlet_ffl')
CFD.setup.BC_outlet_vent(2.6, 'outlet_ffr')
CFD.setup.BC_outlet_vent(3.65, 'outlet_rfl')
CFD.setup.BC_outlet_vent(3.65, 'outlet_rfr')

CFD.setup.solution_method()
CFD.setup.report_definition('volume', 'surface-volumeflowrate', ['outlet*'])
CFD.setup.report_definition('mass-flux', 'surface-massflowrate', mass_flux_list, 'no')
# CFD.setup.report_definition('pressure', 'surface-areaavg', pressure_face_list)
CFD.setup.convergence_criterion()
CFD.setup.hyb_initialize()
CFD.setup.start_calculate(1500)
# CFD.setup.start_calculate(230)
CFD.setup.write_case_data()


volume_face_list = ['inlet*', 'outlet*']
uni_face_list = ['evap_in', 'evap_out', 'hc_out']


CFD.post.create_result_file()
CFD.post.txt_surface_integrals('volume-flow-rate', volume_face_list)
CFD.post.txt_mass_flux()
CFD.post.txt_surface_integrals('uniformity-index-area-weighted', uni_face_list, 'velocity-magnitude')
CFD.post.txt_surface_integrals('area-weighted-avg', pressure_face_list, 'total-pressure')
CFD.post.txt_surface_integrals('area-weighted-avg', pressure_face_list, 'pressure')
CFD.post.txt_moment(fan_origin, fan_axis)
CFD.post.create_contour('evap_out', 'evap_out')
CFD.post.create_contour('filter_out', 'filter_out')
# CFD.post.create_contour('evap_out_0-2', 'evap_out', [0, 2])
CFD.post.create_contour('hc_out', 'hc_out')
CFD.post.create_streamline('whole_pathline', 'inlet')
CFD.post.create_streamline('distrib_pathline', 'evap_out', [0, 15])
CFD.post.create_view(evap_d1, hc_d1, filter_d1)
CFD.post.read_view()
CFD.post.set_background()
CFD.post.snip_picture('whole_pathline', 'yes', 'yes')
CFD.post.snip_picture('distrib_pathline', 'yes')
CFD.post.snip_picture('evap_out')
CFD.post.snip_picture('hc_out')
# CFD.post.snip_picture(8, 'evap_out_0-2')
CFD.post.snip_picture('filter_out')
CFD.post.snip_model('model')
# CFD.post.simple_lin_post(47.97)
CFD.post.snip_mode_off()


jou.write(CFD.whole_jou)
jou.close()
os.system(txt_name)