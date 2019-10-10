import txt_to_python, python_to_html
from root_transfer import add_slash

# designate path
root = r"G:\CD539\706-rear-vent\706-rear-V2-FH\result_706-rear_V2-FH"
path = add_slash(root)

# Txt input path
txt_name = path + '706-rear.txt'


# Excel output
excel_name = "706-rear-V2-FH"          # Output excel name
sheet_name = excel_name                  # The sheet in excel
data_name = excel_name                   # get a title for your data

# Html output
html_output_path = path
title = data_name

# run module get excel
data_matrix = txt_to_python.process_data(txt_name, path)
txt_to_python.get_xls(path, sheet_name, excel_name, data_name)

# run module get html
python_to_html.get_html(data_matrix, title, html_output_path)

# get fan efficiency
