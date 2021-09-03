import numpy as np
from matplotlib import pyplot as plt
from matplotlib import collections
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

        result_file = r'{project_address}\lin_case\{project_name}_{version_name}_{angle}\result\{project_name}_{angle}.txt' \
            .format(project_address=self.project_address, project_name=self.project_name,
                    version_name=self.version_name, angle=self.angle_array[0])

        temp_dict_total = self.txt_to_dict(result_file)

        for i in self.angle_array[1:]:                      # extract data from all result file
            result_file = r'{project_address}\lin_case\{project_name}_{version_name}_{angle}\result\{project_name}_{angle}.txt' \
                .format(project_address=self.project_address, project_name=self.project_name,
                        version_name=self.version_name, angle=i)

            temp_dict = self.txt_to_dict(result_file)
            for item in temp_dict_total.keys():
                temp_dict_total[item].append(temp_dict[item][0])

        self.outlet_list = list(temp_dict_total.keys())
        print(temp_dict_total)
        print(self.outlet_list)
        self.data_matrix = np.array(list(temp_dict_total.values()))
        self.angle_array = np.insert(self.angle_array, 0, 0)
        self.angle_array = np.append(self.angle_array, 100)

        first_col = np.zeros([len(self.outlet_list), 1])
        last_col = np.ones([len(self.outlet_list), 1])*75
        self.data_matrix = np.hstack((first_col, self.data_matrix, last_col))


        self.get_diff_matrix()
        self.get_avg_matrix()
        self.get_avg_diff_matrix()
        self.get_side_diff_matrix()
        self.get_vent_diff_matrix()
        self.get_fr_diff_matrix()

    def txt_to_dict(self, txt_path):
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

            temp_dict = {}
            for i in lines[first_row_number:last_row_number]:       # form dict
                i = i.split()
                outlet_name = i[0]
                temp = round(float(i[1])-273.15, 1)
                temp_dict[outlet_name] = [temp]

            return temp_dict

    def get_diff_matrix(self):
        np_matrix = np.zeros(np.shape(self.data_matrix))
        np_matrix[:] = self.data_matrix[:]
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
        # classify exist outlets into designate list
        for i in self.outlet_list:
            if 'v' in i:
                # if 'r' is i[-2]:                                  # isolate rear_vent
                #     rear_vent.append(self.outlet_list.index(i))
                # else:
                vent.append(self.outlet_list.index(i))
            elif 'f' in i:
                if 'r' is i[-3]:
                    rear_foot.append(self.outlet_list.index(i))
                else:
                    foot.append(self.outlet_list.index(i))
            elif 'd' in i:
                defrost.append(self.outlet_list.index(i))

        # remove empty class
        for i in list(clasif_outlet_dict.keys()):
            if not clasif_outlet_dict[i]:
                clasif_outlet_dict.pop(i)
        avg_diff_dict = clasif_outlet_dict.copy()

        for i in avg_diff_dict.keys():                                      # each class
            avg_temp = np.zeros(np.shape(self.angle_array[1:]))             # create empty average temperature array
            for j in avg_diff_dict[i]:                                      # each outlet in one class
                avg_temp += self.diff_matrix[j]
            avg_temp = np.around(avg_temp/len(avg_diff_dict[i]), 1)         # mean value of temperature for each class
            avg_diff_dict[i] = avg_temp[:]

        self.avg_diff_dict = avg_diff_dict

    def get_avg_matrix(self):
        vent = []
        rear_vent = []
        foot = []
        rear_foot = []
        defrost = []
        clasif_outlet_dict = {'vent': vent, 'rear_vent': rear_vent, 'foot': foot, 'rear_foot': rear_foot,
                              'defrost': defrost}
        # classify exist outlets into designate list
        for i in self.outlet_list:
            if 'v' in i:
                # if 'r' is i[-2]:                                  # isolate rear_vent
                #     rear_vent.append(self.outlet_list.index(i))
                # else:
                vent.append(self.outlet_list.index(i))
            elif 'f' in i:
                if 'r' is i[-3]:
                    rear_foot.append(self.outlet_list.index(i))
                else:
                    foot.append(self.outlet_list.index(i))
            elif 'd' in i:
                defrost.append(self.outlet_list.index(i))

        # remove empty class
        for i in list(clasif_outlet_dict.keys()):
            if not clasif_outlet_dict[i]:
                clasif_outlet_dict.pop(i)
        avg_dict = clasif_outlet_dict.copy()
        for i in avg_dict.keys():                                      # each class
            avg_temp = np.zeros(np.shape(self.angle_array[:]))        # create empty average temperature array
            for j in avg_dict[i]:                                      # each outlet in one class
                avg_temp += self.data_matrix[j]
            avg_temp = np.around(avg_temp/len(avg_dict[i]), 1)         # mean value of temperature for each class
            avg_dict[i] = avg_temp[:]

        self.avg_dict = avg_dict

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
                    # if i[-3] is 'c':
                    #     center_vent.append(self.outlet_list.index(i))
                    # else:
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
            side_diff_dict[i] = self.np_matrix[first_index]-self.np_matrix[last_index]

        self.side_diff_dict = side_diff_dict

    def get_vent_diff_matrix(self):
        vent = []
        rear_vent = []
        foot = []
        rear_foot = []
        defrost = []
        clasif_outlet_dict = {'vent': vent, 'rear_vent': rear_vent, 'foot': foot, 'rear_foot': rear_foot,
                              'defrost': defrost}
        # classify exist outlets into designate list
        for i in self.outlet_list:
            if 'v' in i:
                if 'r' is i[-2]:                                  # isolate rear_vent
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

        vent_diff_dict = clasif_outlet_dict.copy()
        for i in vent_diff_dict.keys():
            matrix = self.np_matrix[[vent_diff_dict[i]], :]      # extract rows belongs to i class
            vent_diff_dict[i] = np.squeeze(matrix.max(axis=1) - matrix.min(axis=1))

        self.vent_diff_dict = vent_diff_dict

    def get_fr_diff_matrix(self):
        vent = []
        rear_vent = []
        foot = []
        rear_foot = []
        defrost = []
        clasif_outlet_dict = {'vent': vent, 'rear_vent': rear_vent, 'foot': foot, 'rear_foot': rear_foot,
                              'defrost': defrost}
        # classify exist outlets into designate list
        for i in self.outlet_list:
            if 'v' in i:
                if 'r' is i[-2]:  # isolate rear_vent
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

        diff_dict = clasif_outlet_dict.copy()
        front_matrix = self.np_matrix[[diff_dict['foot']], :]
        front_matrix = front_matrix.mean(axis=1)
        rear_matrix = self.np_matrix[[diff_dict['rear_foot']], :]
        rear_matrix = rear_matrix.mean(axis=1)
        self.fr_diff = np.squeeze(front_matrix - rear_matrix)
        print(self.fr_diff)

    def plot_temp(self):
        ax = self.temp_chart_setting('temperature', 'Temperature(°C)', 5, 0, 80)
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
            ax.plot(x, y, marker_type, markersize=marker_size, label=self.outlet_list[i])

        plt.legend()
        plt.show()

    def plot_temp_diff(self, low_limit, up_limit):
        self.temp_chart_setting('every-10%-temperature-difference', 'Temperature Difference(°C)', 5, -5, 35)
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
        ax = self.temp_chart_setting('outlet-average-every-10%-difference', 'Temperature Difference(°C)', 3, -4, 24)
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
                ax.plot(x, y, marker_type, markersize=marker_size, label=i)

        y = [low_limit for i in self.angle_array[1:]]
        ax.plot(x, y, '--', color='black', label='low_limit')

        y = [up_limit for i in self.angle_array[1:]]
        ax.plot(x, y, '--', color='black', label='up_limit')

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

    def plot_vent_temp_diff(self, low_limit, up_limit):
        self.temp_chart_setting('outlet-average-every-10%-difference', 'Temperature Difference(°C)', 2, -8, 8)
        for i in self.vent_diff_dict.keys():
                x = self.angle_array
                y = self.vent_diff_dict[i]
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

    def plot_fr_temp_diff(self, low_limit, up_limit):
        self.temp_chart_setting('every-10%-temperature-difference', 'Temperature Difference(°C)', 5, -5, 35)
        x = self.angle_array[:]
        y = self.fr_diff
        marker_size = 6
        marker_type = 'o-'
        plt.plot(x, y, marker_type, markersize=marker_size, label='front_rear_vent_diff')

        y = [low_limit for i in self.angle_array[:]]
        plt.plot(x, y, '--', color='black', label='low_limit')

        y = [up_limit for i in self.angle_array[:]]
        plt.plot(x, y, '--', color='black', label='up_limiit')

        plt.legend()
        plt.show()

    def plot_effective_area(self, mode, xmin, xmax):
        ax = self.temp_chart_setting('outlet-average-every-10%-difference', 'Temperature Difference(°C)', 3, -4, 24)
        x = self.angle_array
        y = self.avg_dict[mode]
        marker_size = 6
        marker_type = '-'
        if 'v' in mode:
            marker_type = 'o-'
        elif 'f' in mode:
            marker_type = '^-'
        elif 'd' in mode:
            marker_type = 's-'
        ax.plot(x, y, marker_type, markersize=marker_size, label=mode)
        # collection = collections.BrokenBarHCollection.span_where(x, ymin=-100, ymax=100,
        #                                                          where=5, facecolor='green', alpha=0.4)

        plt.axvspan(xmin=xmin, xmax=xmax, facecolor="g", alpha=0.4)

        # ax.add_collection(collection)
        plt.legend()
        plt.show()

    def temp_chart_setting(self, title_plus, ylabel_name, y_major, y_low_limit, y_up_limit):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title("%s-%s-%s" % (self.project_name, self.version_name, title_plus), fontsize=20)
        ax.set_xlabel("open valve percentage(%)")
        ax.set_ylabel("%s"%(ylabel_name))
        x_major_locator = plt.MultipleLocator(10)
        y_major_locator = plt.MultipleLocator(y_major)
        ax.xaxis.set_major_locator(x_major_locator)
        ax.yaxis.set_major_locator(y_major_locator)

        x_major_formatter = PercentFormatter(100)
        ax.xaxis.set_major_formatter(x_major_formatter)

        # plt.xlim(0, 100)
        # plt.ylim(y_low_limit, y_up_limit)
        ax.grid()

        return ax


if __name__ == "__main__":
    project_address = r"G:\_HAVC_Project\HA2HG\HA2HG_13_lin_tri_level\HA2HG_V6_lin_trl"
    project_name = 'HA2HG'
    version_name = 'V6_lin_trl'

    whole_name = project_name + '-' + version_name
    Linearity_report = LinReport(project_address, project_name, version_name, 10, 90, 9)
    # Linearity_report.plot_temp()
    # Linearity_report.plot_effective_area('foot', (np.where(Linearity_report.avg_dict['foot'] > 25))[0][0]*10, 100)
    # Linearity_report.plot_temp_diff(-10, 10)
    # Linearity_report.plot_avg_temp_diff(0, 5)
    # Linearity_report.plot_side_temp_diff(-5, 5)
    # Linearity_report.plot_vent_temp_diff(-5, 5)
    # Linearity_report.plot_fr_temp_diff(-12, 12)
    # fig, ax = plt.subplots(figsize=(10, 6))

