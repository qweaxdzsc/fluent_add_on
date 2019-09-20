import txt_to_python, python_to_html
from root_transfer import add_slash

# designate path
root = r"G:\GE2_REAR\GE2-rear-round2\GE2-rear-V9-FC\result_GE2-rear2_V9-FC"
path = add_slash(root)

# Txt input path
txt_name = path + 'GE2-rear2.txt'


# Excel output
excel_name = "GE2-rear2-V9-FC"    # Output excel name
sheet_name = excel_name                  # The sheet in excel
data_name = excel_name                  # get a title for your data

# Html output
html_output_path = path
title = data_name

# run module get excel
data_matrix = txt_to_python.process_data(txt_name, path)
txt_to_python.get_xls(path, sheet_name, excel_name, data_name)

# run module get html
python_to_html.get_html(data_matrix, title, html_output_path)

# get fan efficiency
