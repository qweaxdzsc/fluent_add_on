import os
from CFD_post_command import CfdPost

case_dir = r"G:\_HAVC_Project\D2UX\D2UX_ai\D2UX_AI_V7"
case_name = r"D2UX_AI_V7"
result_path = r"G:\_HAVC_Project\D2UX\D2UX_ai\D2UX_AI_V7\result_D2UX_AI_V7"
cse_file = ''

cfp = CfdPost(case_dir, case_name, result_path, cse_file)
cfp.load_case()
cfp.create_contour('contour1', 'Velocity', 'filter_out filter')
cfp.create_contour('contour2', 'Velocity', 'filter_in filter')
cfp.save_avz()

cfp.create_command_file()

# cfp.run_command()
# os.system(cfp.script_path)


