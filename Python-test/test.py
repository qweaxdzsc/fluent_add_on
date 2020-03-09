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


