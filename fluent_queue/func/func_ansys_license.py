import os


class LicenseUsage(object):
    def __init__(self):
        # -------------init variable-------------------------
        self.license_list = ["10.243.75.38", "10.243.75.40", "10.243.75.67"]
        self.application = r'C:\Program Files\ANSYS Inc\Shared Files\Licensing\winx64\lmutil'
        self.license_command = r'lmstat -a -c 1055@'
        self.module_dict = {'spaceclaim': ["Users of a_spaceclaim_dirmod", 'Users of acfd_preppost'],
                            'hpc': ['Users of anshpc_pack'],
                            'pre_post': ['Users of acfd_preppost', 'Users of acfdsol2', 'Users of cfd_base'],
                            'solver': ['Users of cfd_base', 'Users of acfdsol2']
                            }
        self.license_dict = dict()
        # -------------init function-------------------------
        self.license_info = self.get_license_info()
        self.license_usage_dict(self.module_dict)

    def get_license_info(self):
        info = ''
        for i in self.license_list:
            command = self.license_command + i
            info += os.popen('"%s" %s' % (self.application, command)).read()
        info = info.split("\n")

        return info

    def print_license_info(self):
        print(self.license_info)

    def license_usage_dict(self, module_dict):
        self.license_dict = dict()
        for item in module_dict.keys():
            self.license_dict[item] = [0, 0]
        for row in self.license_info:
            for k, v in module_dict.items():
                for i in v:
                    self.check_usage(row, i, self.license_dict[k])
        print(self.license_dict)

    def check_usage(self, info, flag, reserv_list):
        if flag in info:
            total_lic = int(info.split("of")[2][1])
            used_lic = int(info.split("of")[3][1])
            reserv_list[0] += total_lic
            reserv_list[1] += total_lic - used_lic

    def is_license(self, license_name):
        usable_license = self.license_dict[license_name][1]
        print('license left:', usable_license)
        if usable_license:
            return True
        else:
            return False

    def is_enough(self, required_cores):
        solver_left = self.license_dict['solver'][1]
        if not solver_left:
            print('not enough solver')
            return False
        hpc_left = self.license_dict['hpc'][1]
        if hpc_left:
            core_left = 4 + 8 * 4 ** (hpc_left - 1)
        else:
            core_left = 4

        if required_cores > core_left:
            print('not enough HPC')
            return False
        else:
            return True


if __name__ == '__main__':
    ansys_license = LicenseUsage()
    ansys_license.print_license_info()