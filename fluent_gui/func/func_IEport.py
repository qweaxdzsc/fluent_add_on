import csv
import os
from PyQt5.QtWidgets import QLineEdit


class IEport(object):
    """This class contains import and export function"""
    def __init__(self, ui):
        self.ui = ui
    
    def import_pamt(self, path):
        """import parameter from csv file, 
            then use name to find all corresponding QLineEdit,
            and put data into LineEdit,
            Also return outlet info if exist
            outlet_dict contains outlet name, area size, R, P, Q, K
            K_dict contains outlet name and K
            """
        outlet_dict = {}
        K_dict = {}
        outlet_list = []
        valve_dict = {}
        
        if path[0] != '':
            csv_path = path[0]
            info = self.csv_import(csv_path)
            
            for i in info:
                name = i + '_edit'
                widget = self.ui.findChild(QLineEdit, name)
                if widget != None:
                    widget.setText(str(info[i]))
                if 'outlet' in i:
                    outlet_list.append(i)
                    outlet_dict[i] = eval(info[i])
                if 'valve' in i:
                    valve_dict[i] = info[i]

            for i in outlet_dict.keys():
                K_dict[i] = outlet_dict[i][-1]
                # outlet_dict[i].remove(outlet_dict[i][-1])

            self.ui.project_name_edit.setText(info['project_name'])
            self.ui.version_name_edit.setText('V')
    
            self.ui.append_text('参数模板:%s导入成功' % path[0])
        
        return outlet_list, outlet_dict, K_dict, valve_dict
    
    def csv_import(self, excel_path):
        """import csv as a dict(info)"""
        with open(excel_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            info = {}
            for row in reader:
                info[row[0]] = row[1]
    
        return info

    def export_pamt(self, path, pamt):
        """ export parameter to a designated csv file"""
        try:
            csv_save_path = path[0]
            self.write_csv(csv_save_path, pamt)
            os.system(csv_save_path)
        except Exception as e:
            print('export error:', e)
            print('Error in file:', e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print('Error in line:', e.__traceback__.tb_lineno)  # 发生异常所在的行数
            self.ui.append_text('导出地址有错误，请重新选择')

    def write_csv(self, csv_path, pamt):
        """use (pamt)dict to write csv file"""
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            for i in pamt.keys():
                writer.writerow([i, pamt[i]])

        self.ui.append_text('已创建新参数表:%s ' % csv_path)
