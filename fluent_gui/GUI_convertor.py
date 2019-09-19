import os
import shutil

ui_path = r'C:\Users\BZMBN4\Desktop\fluent_add_on\ui'
py_folder = r'C:\Users\BZMBN4\Desktop\fluent_add_on\fluent_gui'


def convert(py_name, gui_name):
    os.system(r'cd %s && pyuic5 -o %s %s' %(ui_path, py_name, gui_name))


gui_name = 'K_cal.ui'
py_name = gui_name.replace('.ui', '.py')

py_path = '%s\%s'%(py_folder, py_name)

convert(py_name, gui_name)
if os.path.exists(py_path) == True:
    os.remove(py_path)

shutil.move('%s\%s' %(ui_path, py_name), py_path)