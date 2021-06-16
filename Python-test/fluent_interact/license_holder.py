from fluent_interact import license_checker
import threading
import subprocess
import time

# basic global config
import os
ansys_root = os.environ.get('AWP_ROOT191')
disk = 'F'
project_address = 'F:\luo'
app_path = r'%s\fluent\ntbin\win64\fluent' % ansys_root


# function and class
class FluentThread(threading.Thread):
    def __init__(self, cores):
        super().__init__()
        self.cores = cores

    def run(self):
        command = f'3d -t{self.cores}'
        p = subprocess.Popen(r'%s &&'
                             r'cd %s &&'
                             r'"%s" %s' %
                             (disk, project_address, app_path, command),
                             shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True)


# requirement
user_list = ['bzmbn4', 'HZ4EYB']
license_require = {
    'solver': 2,
    'hpc': 2,
}

# check license and hold license if not satisfied


while True:
    time.sleep(5)
    license_hold = license_require.copy()
    cur_license = license_checker.LicenseUsage()

    for key, value in license_require.items():
        used = cur_license.user_usage(key, user_list)
        license_hold[key] -= used
    print(license_hold)
    launch = False
    threads_list = []
    if license_hold['solver'] > 0:
        required_cores = 4 + 8 * 4 ** (license_hold['hpc'] - 1)
        launch = cur_license.is_enough(required_cores)
        if launch:
            fluent_thread = FluentThread(required_cores)
            fluent_thread.start()
            threads_list.append(fluent_thread)


