import txt_to_python
import python_to_html
import data_to_excel
import cgitb


# designate path
root = r"G:\_HAVC_Project\D2UX\D2UX_vent\D2UX_vent_ainew\result_D2UX_vent_ainew_R250_3600RPM"
path = root + '\\'

# Txt input path
txt_name = path + 'D2UX.txt'


# Excel output info
excel_name = 'D2UX_vent_ainew_R250_3600RPM'         # Output excel name
sheet_name = excel_name                  # The sheet in excel
data_name = excel_name                   # get a title for your data

# Html output info
html_output_path = path
title = data_name

# run module get excel
data_matrix = txt_to_python.process_data(txt_name)
data_to_excel.get_xls(path, data_matrix, sheet_name, excel_name, data_name)

# run module get html
python_to_html.get_html(data_matrix, title, html_output_path)

# get fan efficiency
cgitb.enable(format='text')

