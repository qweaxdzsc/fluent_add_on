import os

# command = "-F"               # create one file
command = "-D -w"               # create one directory
package_path = r"C:\Users\BZMBN4\Desktop\fluent_add_on\CFD_input_gui"
package_name = "start.py"
package = package_path + "\\" + package_name
out_path = r"C:\Users\BZMBN4\Desktop"

os.system("pyinstaller %s %s --distpath %s" % (command, package, out_path))