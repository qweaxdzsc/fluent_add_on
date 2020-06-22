import os


path = r'/'


py_file_name = '../ui_py/ui_porous_model.py'
language_file_name = py_file_name[:-3] + '_EN' + '.ts'


os.system(r'cd %s && pylupdate5 %s -ts %s' %(path, py_file_name, language_file_name))