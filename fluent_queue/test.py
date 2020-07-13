import configparser
import os
import sys

config = configparser.ConfigParser()
config.read(r'.\config\config.ini')   # TODO path might change when pack exe
software_path = config['Software']['Software_path']
exe_name = config['Software']['exe_name']
main_path = os.path.abspath(sys.path[0])
print(main_path)
script = 'txt.jou'
cores = 4
command = eval(config['Software']['command']).replace(".\\", main_path + '\\')
print(command)