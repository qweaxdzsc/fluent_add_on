import os

# command = "-F"               # create one file
command = "-D -w"               # create one directory
package_path = r"C:\Users\BZMBN4\Desktop"
package_name = "PDF_TO_PNG.py"
package = package_path + "\\" + package_name
out_path = r"C:\Users\BZMBN4\Desktop\PDF_TO_PNG_V1.1"

os.system("pyinstaller %s %s --distpath %s" % (command, package, out_path))