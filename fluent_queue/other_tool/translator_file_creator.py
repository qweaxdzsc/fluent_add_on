import os


py_path = r'../ui_py'
py_file_name = 'ui_login.py'
out_path = r'../ui_translate'


def create_ts_file(path, py_file_name, out_path):
    language_file_name = '%s/%s_CN.ts' % (out_path, py_file_name[:-3])
    os.system(r'cd %s && pylupdate5 %s -ts %s' %(path, py_file_name, language_file_name))


if __name__ == '__main__':
    # file_list = os.listdir(py_path)
    # for file in file_list:
    #     if file.endswith('.py'):
    #         print(file)
    #         create_ts_file(py_path, file, out_path)
    create_ts_file(r'../func', 'func_setting.py', out_path)