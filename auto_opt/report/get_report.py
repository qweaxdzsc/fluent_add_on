from . import txt_to_python
from . import python_to_html
from . import data_to_excel
import cgitb


class GetReport(object):
    def __init__(self, result_path):
        self.result_path = result_path + '\\'
        split_list = result_path.split('\\')
        self.report_name = split_list[-1].replace('result_', '')  # Output excel name
        self.parse_data()

    def parse_data(self):
        txt_name = self.result_path + 'total_result.txt'
        self.data_matrix = txt_to_python.process_data(txt_name)

    def get_html(self):
        html_output_path = self.result_path
        title = self.report_name
        python_to_html.get_html(self.data_matrix, title, html_output_path)

    def get_excel(self):
        # Excel output info
        excel_name = self.report_name
        sheet_name = self.report_name  # The sheet in excel
        data_name = self.report_name   # get a title for your data
        data_to_excel.get_xls(self.result_path, self.data_matrix, sheet_name, excel_name, data_name)


if __name__ == '__main__':
    result_path = r'G:\test\auto_diffuser\ad_v2\ad_V1\result_ad_V1'
    report = GetReport(result_path)
    report.get_html()
    report.get_excel()
    cgitb.enable(format='text')
