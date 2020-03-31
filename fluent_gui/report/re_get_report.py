from report import re_data_to_excel, re_txt_to_python, re_python_to_html


def get_report(root, project_name, verison_name):
    result_path = root + '\\' + 'result_' + project_name + '_' + verison_name
    path = result_path + '\\'

    # Txt input path
    txt_name = path + project_name + '.txt'

    # Excel output info
    excel_name = project_name + verison_name         # Output excel name
    sheet_name = excel_name                  # The sheet in excel
    data_name = excel_name                   # get a title for your data

    # Html output info
    html_output_path = path
    title = data_name

    # run module get excel
    data_matrix = re_txt_to_python.process_data(txt_name)
    re_data_to_excel.get_xls(path, data_matrix, sheet_name, excel_name, data_name)

    # run module get html
    re_python_to_html.get_html(data_matrix, title, html_output_path)


