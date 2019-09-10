import os


def convert(py_name, gui_name):
    os.system(r'cd C:\Users\BZMBN4\Desktop && pyuic5 -o %s %s' %(py_name, gui_name))


gui_name = 'easy_test.ui'
py_name = gui_name.replace('.ui', '.py')


convert(py_name, gui_name)
os.system(r'cd C:\Users\BZMBN4\Desktop && %s' %(py_name))