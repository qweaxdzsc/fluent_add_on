import txt_to_python, python_to_html

import time
time_start = time.time()
# designate path
root = r"G:\458-front\458-foot\458-v2-foot\result_458-front_v2-foot-outletR"
path = root + '\\'

# Txt input path
txt_name = path + '458-front.txt'


# Excel output info
excel_name = '458-front-v2-foot'          # Output excel name
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