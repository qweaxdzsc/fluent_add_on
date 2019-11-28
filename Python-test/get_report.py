import txt_to_python, python_to_html

import time
time_start = time.time()
# designate path
root = r"G:\GE2_REAR\GE2-rear-round3\GE2-rear-V20-FH\result_GE2-rear3_V20-FH"
path = root + '\\'

# Txt input path
txt_name = path + 'GE2-rear3.txt'


# Excel output info
excel_name = 'GE2-rear3-V20-FH'          # Output excel name
sheet_name = excel_name                  # The sheet in excel
data_name = excel_name                   # get a title for your data

# Html output info
html_output_path = path
title = data_name

# run module get excel
data_matrix = txt_to_python.process_data(txt_name, path)
txt_to_python.get_xls(path, sheet_name, excel_name, data_name)

# run module get html
python_to_html.get_html(data_matrix, title, html_output_path)

# get fan efficiency
time_end = time.time()

print('time cost', time_end - time_start)