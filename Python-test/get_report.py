import txt_to_python, python_to_html
# from root_transfer import add_slash

# designate path
root = r"G:\519(706)\519_vent_150mmfan\706-vent-v7-150mm-pp2\result_706_V7-vent-3400RPM"
path = root + '\\'

# Txt input path
txt_name = path + '519-vent.txt'


# Excel output info
excel_name = "706-pp2-v7-vent-3400RPM"          # Output excel name
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
