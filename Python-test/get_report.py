import txt_to_python
import python_to_html
import data_to_excel
import cgitb


# designate path
root = r"G:\_HAVC_Project\GEM\GEM_04_defrost\GEM_V5_defrost\result_GEM_9BQX_V5_defrost"
path = root + '\\'

# Txt input path
txt_name = path + 'total_result.txt'

# Excel output info
split_list = root.split('\\')
excel_name = split_list[-1].replace('result_', '')          # Output excel name
sheet_name = excel_name                                     # The sheet in excel
data_name = excel_name                                      # get a title for your data

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
