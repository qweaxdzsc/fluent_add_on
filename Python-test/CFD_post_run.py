import os
from CFD_post_command import CfdPost

case_dir = r"G:\_HAVC_Project\D2U-2\D2U-2_trl\distribution_V2"
case_name = r"D2U-2_trl_V2"
result_path = r"G:\_HAVC_Project\D2U-2\D2U-2_trl\distribution_V2\result_D2U-2_trl_V2"
cse_file = ''

cfp = CfdPost(case_dir, case_name, result_path, cse_file)
cfp.load_case()
# cfp.create_view1()
# cfp.create_plane('planeZX1', 'ZX', 0, -0.11, 0)
# cfp.create_contour('contourZX1', 'Temperature', 'planeZX1')
# cfp.show_hide('CONTOUR', 'contourZX1')
# cfp.save_png('_1')
# cfp.show_hide('CONTOUR', 'contourZX1', 'hide')
#
# cfp.create_plane('planeZX5', 'ZX', 0, -0.0122, 0)
# cfp.create_contour('contourZX5', 'Temperature', 'planeZX5')
# cfp.show_hide('CONTOUR', 'contourZX5')
# cfp.save_png('_5')
# cfp.show_hide('CONTOUR', 'contourZX5', 'hide')
#
# cfp.create_plane('planeZX9', 'ZX', 0, 0.0855, 0)
# cfp.create_contour('contourZX9', 'Temperature', 'planeZX9')
# cfp.show_hide('CONTOUR', 'contourZX9')
# cfp.save_png('_9')
# cfp.show_hide('CONTOUR', 'contourZX9', 'hide')
#
#
# cfp.show_hide('CONTOUR', 'contourZX1')
# cfp.show_hide('CONTOUR', 'contourZX5')
# cfp.show_hide('CONTOUR', 'contourZX9')
# cfp.save_avz()

cfp.bat_contour('XY', 'Velocity', 1.1, 1.45)
cfp.bat_contour('YZ', 'Velocity', 2.1, 2.3)
cfp.bat_contour('ZX', 'Velocity', -0.16, 0.16)

# cfp.create_contour('contour2', 'Velocity', 'filter_in filter')


cfp.create_command_file()

# cfp.run_command()
os.system(cfp.script_path)


