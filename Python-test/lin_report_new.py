import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter


class LinReport(object):
    def __init__(self, project_address, project_name, version_name, start_percent=10, end_percent=90, process_point=9):
        self.project_address = project_address
        self.project_name = project_name
        self.version_name = version_name
        self.start_percent = start_percent
        self.end_percent = end_percent
        self.process_point = process_point
        self.whole_name = project_name + version_name

        self.form_data_list()

    def form_data_list(self):
        # create valve open angle array
        self.angle_array = np.linspace(self.start_percent, self.end_percent, self.process_point, dtype=int)
        self.data_matrix = []

        for i in self.angle_array:          # extract data from all result file
            result_file = r'{project_address}\lin_case\{project_name}-{version_name}-{angle}\result\{project_name}_{angle}.txt' \
                .format(project_address=self.project_address, project_name=self.project_name,
                        version_name=self.version_name, angle=i)

            outlet_list, temp_list = self.txt_to_list(result_file)
            # temp_list = np.array(temp_list)
            self.data_matrix.append(temp_list)

        self.outlet_list = outlet_list
        self.angle_array = np.insert(self.angle_array, 0, 0)
        self.angle_array = np.append(self.angle_array, 100)
        self.data_matrix.insert(0, [0 for i in outlet_list])
        self.data_matrix.append([75 for i in outlet_list])
        self.data_matrix = list(zip(*self.data_matrix))

        self.get_diff_matrix()
        self.get_avg_diff_matrix()
        self.get_side_diff_matrix()

    def txt_to_list(self, txt_path):
        with open(txt_path, 'r') as f:
            lines = f.readlines()
            line_number = 0

            while 'Static Temperature' not in lines[line_number]:   # find temperature area and first temperature row
                lines[line_number] = lines[line_number].strip()
                line_number += 1
            line_number += 2
            first_row_number = line_number

            while '-----' not in lines[line_number]:                # last temperature row
                lines[line_number] = lines[line_number].strip()
                if not lines[line_number]:
                    break
                line_number += 1
            last_row_number = line_number

            outlet_list = []
            temp_list = []
            for i in lines[first_row_number:last_row_number]:       # form list
                i = i.split()
                outlet_name = i[0]
                temp = round(float(i[1])-273.15, 1)
                outlet_list.append(outlet_name)
                temp_list.append(temp)

            return outlet_list, temp_list

    def get_diff_matrix(self):
        np_matrix = np.zeros(np.shape(self.data_matrix))
        np_matrix[:] = np.array(self.data_matrix[:])
        self.np_matrix = np_matrix

        self.diff_matrix = np_matrix[:, 1:]-np_matrix[:, :-1]

    def get_avg_diff_matrix(self):
        vent = []
        rear_vent = []
        foot = []
        rear_foot = []
        defrost = []
        clasif_outlet_dict = {'vent': vent, 'rear_vent': rear_vent, 'foot': foot, 'rear_foot': rear_foot,
                              'defrost': defrost}
        for i in self.outlet_list:
            if 'v' in i:
                if 'r' is i[-3]:
                    rear_vent.append(self.outlet_list.index(i))
                else:
                    vent.append(self.outlet_list.index(i))
            elif 'f' in i:
                if 'r' is i[-3]:
                    rear_foot.append(self.outlet_list.index(i))
                else:
                    foot.append(self.outlet_list.index(i))
            elif 'd' in i:
                defrost.append(self.outlet_list.index(i))

        for i in list(clasif_outlet_dict.keys()):
            if not clasif_outlet_dict[i]:
                clasif_outlet_dict.pop(i)

        avg_diff_dict = clasif_outlet_dict.copy()
        for i in avg_diff_dict.keys():
            avg_temp = np.zeros(np.shape(self.angle_array[1:]))
            for j in avg_diff_dict[i]:
                avg_temp += self.diff_matrix[j]
            avg_temp = np.around(avg_temp/len(avg_diff_dict[i]), 1)
            avg_diff_dict[i] = avg_temp[:]

        self.avg_diff_dict = avg_diff_dict

    def get_side_diff_matrix(self):
        side_vent = []
        center_vent = []
        foot = []
        rear_foot = []
        side_defrost = []
        clasif_outlet_dict = {'side_vent': side_vent, 'center_vent': center_vent, 'foot': foot, 'rear_foot': rear_foot,
                              'side_defrost': side_defrost}
        for i in self.outlet_list:
            if i[-1] is 'r' or i[-1] is 'l':
                if 'v' in i:
                    if i[-3] is 'c':
                        center_vent.append(self.outlet_list.index(i))
                    else:
                        side_vent.append(self.outlet_list.index(i))
                elif 'f' in i:
                    if i[-3] is 'f':
                        foot.append(self.outlet_list.index(i))
                    elif i[-3] is 'r':
                        rear_foot.append(self.outlet_list.index(i))
                elif 'd' in i:
                    side_defrost.append(self.outlet_list.index(i))

        for i in list(clasif_outlet_dict.keys()):
            if not clasif_outlet_dict[i]:
                clasif_outlet_dict.pop(i)

        side_diff_dict = clasif_outlet_dict.copy()
        for i in side_diff_dict.keys():
            first_index = side_diff_dict[i][0]
            last_index = side_diff_dict[i][-1]
            print(first_index, last_index)
            side_diff_dict[i] = self.np_matrix[first_index]-self.np_matrix[last_index]

        self.side_diff_dict = side_diff_dict

    def plot_temp(self):
        self.temp_chart_setting('temperature', 'Temperature(°C)', 5, 0, 80)
        for i in range(len(self.data_matrix)):
            x = self.angle_array
            y = self.data_matrix[i]
            marker_size = 6
            marker_type = '-'
            if 'v' in self.outlet_list[i]:
                marker_type = 'o-'
            elif 'f' in self.outlet_list[i]:
                marker_type = '^-'
            elif 'd' in self.outlet_list[i]:
                marker_type = 's-'
            plt.plot(x, y, marker_type, markersize=marker_size, label=self.outlet_list[i])

        plt.legend()
        plt.show()

    def plot_temp_diff(self, low_limit, up_limit):
        self.temp_chart_setting('every-10%-temperature-difference', 'Temperature Difference(°C)', 3, -5, 35)
        for i in range(len(self.diff_matrix)):
                x = self.angle_array[1:]
                y = self.diff_matrix[i]
                marker_size = 6
                marker_type = '-'
                if 'v' in self.outlet_list[i]:
                    marker_type = 'o-'
                elif 'f' in self.outlet_list[i]:
                    marker_type = '^-'
                elif 'd' in self.outlet_list[i]:
                    marker_type = 's-'
                plt.plot(x, y, marker_type, markersize=marker_size, label=self.outlet_list[i])

        y = [low_limit for i in self.angle_array[1:]]
        plt.plot(x, y, '--', color='black', label='low_limit')

        y = [up_limit for i in self.angle_array[1:]]
        plt.plot(x, y, '--', color='black', label='up_limiit')

        plt.legend()
        plt.show()

    def plot_avg_temp_diff(self, low_limit, up_limit):
        self.temp_chart_setting('outlet-average-every-10%-difference', 'Temperature Difference(°C)', 3, -4, 24)
        for i in self.avg_diff_dict.keys():
                x = self.angle_array[1:]
                y = self.avg_diff_dict[i]
                marker_size = 6
                marker_type = '-'
                if 'v' in i:
                    marker_type = 'o-'
                elif 'f' in i:
                    marker_type = '^-'
                elif 'd' in i:
                    marker_type = 's-'
                plt.plot(x, y, marker_type, markersize=marker_size, label=i)

        y = [low_limit for i in self.angle_array[1:]]
        plt.plot(x, y, '--', color='black', label='low_limit')

        y = [up_limit for i in self.angle_array[1:]]
        plt.plot(x, y, '--', color='black', label='up_limiit')

        plt.legend()
        plt.show()

    def plot_side_temp_diff(self, low_limit, up_limit):
        self.temp_chart_setting('outlet-average-every-10%-difference', 'Temperature Difference(°C)', 2, -8, 8)
        for i in self.side_diff_dict.keys():
                x = self.angle_array
                y = self.side_diff_dict[i]
                marker_size = 6
                marker_type = '-'
                if 'v' in i:
                    marker_type = 'o-'
                elif 'f' in i:
                    marker_type = '^-'
                elif 'd' in i:
                    marker_type = 's-'
                plt.plot(x, y, marker_type, markersize=marker_size, label=i)

        y = [low_limit for i in self.angle_array]
        plt.plot(x, y, '--', color='black', label='low_limit')

        y = [up_limit for i in self.angle_array]
        plt.plot(x, y, '--', color='black', label='up_limiit')

        plt.legend()
        plt.show()

    def temp_chart_setting(self, title_plus, ylabel_name, y_major, y_low_limit, y_up_limit):
        plt.figure(figsize=(10, 6))
        plt.title("%s-%s-%s" % (self.project_name, self.version_name, title_plus), fontsize=20)
        plt.xlabel("open valve percentage(%)")
        plt.ylabel("%s"%(ylabel_name))
        ax = plt.gca()
        x_major_locator = plt.MultipleLocator(10)
        y_major_locator = plt.MultipleLocator(y_major)
        ax.xaxis.set_major_locator(x_major_locator)
        ax.yaxis.set_major_locator(y_major_locator)

        x_major_formatter = PercentFormatter(100)
        ax.xaxis.set_major_formatter(x_major_formatter)

        # plt.xlim(0, 100)
        # plt.ylim(y_low_limit, y_up_limit)
        plt.grid()


if __name__ == "__main__":

    project_address = r"G:\458-rear\458-rear-lin14"
    project_name = '458-rear'
    version_name = 'lin14-vent'

    whole_name = project_name + '-' + version_name
    Linearity_report = LinReport(project_address, project_name, version_name)
    Linearity_report.plot_temp()
    Linearity_report.plot_temp_diff(2, 15)
    Linearity_report.plot_avg_temp_diff(4, 12)
    # Linearity_report.plot_side_temp_diff(-2, 2)
