# import numpy as np
# import os
# import fluent_tui
#
#
#
#
# whole_jou = ''
#
#
# project_title = 'BYD'
# version_name = 'lin_vent'
# cad_name = 'BYD_lin_vent'
# project_path = r"G:\_HAVC_Project\BYD\BYD_linearity\BYD_lin_vent"
#
# # valve_dir = [0, -1, 0]
# # valve_origin = [5407.69, 869.38, 1022.1]
# # linearity angle setup
# total_angle = 100
# start_angle = 5
# points = 19
#
# end_angle = total_angle-start_angle
#
# angle_array = np.linspace(start_angle, end_angle, points, endpoint=True)   # define your angle range and points
# # angle_array = [round(i, 3) for i in angle_array]
# angle_array = [int(i) for i in angle_array]
#
# print('angle array:', angle_array)
#
#
# txt_name = project_path + '\\%s-%s-repair.jou' %(project_title, version_name)  # txt final path
# print('output journal in:', txt_name)
# jou = open(txt_name, 'w')
#
# CFD = fluent_tui.tui(whole_jou, project_title, version_name, project_path, cad_name)
#
# def remove_result():
#     for i in angle_array:
#         path = project_path + '\\lin_case\\%s-%s-%s\\result' % (project_title, version_name, i)
#         result_file = "%s_%s.txt" % (project_title, i)
#         txt_path = path + '\\' + result_file
#         steamline_path = path + '\\whole_pathline.avz'
#         if os.path.exists(txt_path):
#             os.remove(txt_path)
#         if os.path.exists(steamline_path):
#             os.remove(steamline_path)
#
# # remove_result()
#
# for i in angle_array:
#     print(project_path)
#     CFD.case_out_path = project_path + '\\lin_case\\%s-%s-%s' % (project_title, version_name, i)
#     CFD.setup.read_case_data(plus=i)
#     add_text = r"""/solve/convergence-conditions/conv-reports/delete/"temperature-stable" q q q q"""
#     CFD.whole_jou += add_text
#     CFD.setup.start_calculate(150)
#     CFD.case_out_path = project_path
#     CFD.setup.write_lin_case_data(i)
#     CFD.post.simple_lin_post(i)
#
# whole_jou = CFD.whole_jou
#
# jou.write(whole_jou)
# jou.close()
# os.system(txt_name)

# import os
# import fluent_tui
# jou_out = r'C:\Users\BZMBN4\Desktop'       # txt output root
#
# # txt name
# whole_jou = ''
# project_title = 'D2UX'
# version_name = 'AI_V7'
# cad_name = 'D2UX_AI_V7'
# case_out = r'G:\_HAVC_Project\D2UX\D2UX_ai\D2UX_AI_V7'
#
# jou_title = project_title + '-' + version_name + '-TUI'
# txt_name = jou_out + '\\' + jou_title + '.jou'            # txt final path
# print('output journal in:', txt_name)
# jou = open(txt_name, 'w')
#
#
# CFD = fluent_tui.tui(whole_jou, project_title, version_name, case_out, cad_name)
#
#
# CFD.mesh.import_distrib(min_size=0.6)
# CFD.mesh.general_improve()
# CFD.mesh.fix_slivers()
#
# CFD.mesh.compute_volume_region()
# CFD.mesh.volume_mesh_change_type()
# CFD.mesh.auto_mesh_volume()
# CFD.mesh.auto_node_move(0.85)
# CFD.mesh.rename_cell(zone_list=['ai_duct', 'ai', 'filter', 'cone'])
# CFD.mesh.retype_face(face_list=['inlet'], face_type='inlet-vent')
# CFD.mesh.retype_face(face_list=['ai_in', 'filter*'], face_type='internal')
# # CFD.mesh.retype_face(face_list=['fan_in', 'fan_out', 'evap*'], face_type='internal')
# # CFD.mesh.retype_face(face_list=['fan_in', 'fan_out', 'evap*', 'hc*'], face_type='internal')
# CFD.mesh.retype_face(face_list=['outlet*'], face_type='mass-flow-outlet')
# CFD.mesh.write_mesh()
# CFD.mesh.prepare_for_solve()
# CFD.mesh.switch_to_solver()
#
#
# fan_origin = [2.15225, 0.35303, 0.89591]
# fan_axis = [0, 0, 1]
# rpm = 3750
# evap_d1 = [1, 0, 0]
# evap_d2 = [0, 1, 0]
# hc_d1 = [0.96593, 0.25882, 0]
# hc_d2 = [0, 0, 1]
# filter_d1 = [0, 0, 1]
# filter_d2 = [1, 1, 0]
#
#
# mass_flux_list = ['inlet*', 'outlet*']
# pressure_face_list = ['inlet*', 'ai_in', 'filter*', 'outlet*']
#
# CFD.setup.rescale()
# # CFD.setup.convert_polymesh()
# CFD.setup.turb_models()
# CFD.setup.porous_zone('filter', filter_d1, filter_d2, 4.01e+07, 206)
# CFD.setup.solution_method()
# CFD.setup.report_definition('volume', 'surface-volumeflowrate', ['outlet*'])
# CFD.setup.report_definition('mass-flux', 'surface-massflowrate', mass_flux_list, 'no')
# CFD.setup.report_definition('pressure', 'surface-areaavg', pressure_face_list)
# CFD.setup.convergence_criterion()
# CFD.setup.hyb_initialize()
# CFD.setup.start_calculate(250)
# CFD.setup.write_case_data()
#
#
# volume_face_list = ['inlet*', 'outlet*']
# uni_face_list = ['filter']
#
# CFD.post.create_result_file()
# CFD.post.txt_surface_integrals('volume-flow-rate', volume_face_list)
# CFD.post.txt_mass_flux()
# CFD.post.txt_surface_integrals('uniformity-index-area-weighted', uni_face_list, 'velocity-magnitude')
# CFD.post.txt_surface_integrals('area-weighted-avg', pressure_face_list, 'total-pressure')
# CFD.post.txt_surface_integrals('area-weighted-avg', pressure_face_list, 'pressure')
# CFD.post.create_contour('filter_out', 'filter_out')
# CFD.post.create_streamline('whole_pathline', 'inlet', [0, 15])
# CFD.post.create_view(evap_d1, hc_d1, filter_d1)
# CFD.post.read_view()
# CFD.post.set_background()
# CFD.post.snip_picture('whole_pathline', 'yes', 'yes')
#
# CFD.post.snip_picture('filter_out')
# CFD.post.snip_model('model')
#
#
#
# jou.write(CFD.whole_jou)
# jou.close()
# os.system(txt_name)


