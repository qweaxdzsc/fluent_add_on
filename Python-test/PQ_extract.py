from matplotlib import pyplot as plt
import numpy as np


def list_RPM_K(RPM_start, RPM_end, RPM_add, K_number):
    RPM_list = [RPM for RPM in range(RPM_start, RPM_end+RPM_add, RPM_add)]

    K_formal = np.linspace(1, 6, K_number)
    K_list = [round(i ** 3, 2) for i in K_formal]

    return RPM_list, K_list


def extract_data(extract_class, txt_path):
    with open(txt_path, 'r') as f:
        lines = f.readlines()
        line_number = 0

        while extract_class not in lines[line_number]:   # find temperature area and first temperature row
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

        data_dict = {}
        for i in lines[first_row_number:last_row_number]:       # form dict
            i = i.split()
            data_dict[i[0]] = i[1]

        return data_dict


def extract_data_moment(measure_zone, txt_path):
    with open(txt_path, 'r') as f:
        lines = f.readlines()
        line_number = 0

        while 'Moment Axis' not in lines[line_number]:   # find temperature area and first temperature row
            lines[line_number] = lines[line_number].strip()
            line_number += 1
        line_number += 3
        first_row_number = line_number

        while '-----' not in lines[line_number]:                # last temperature row
            lines[line_number] = lines[line_number].strip()
            if not lines[line_number]:
                break
            line_number += 1
        last_row_number = line_number

        data_dict = {}
        for i in lines[first_row_number:last_row_number]:       # form dict
            if measure_zone in i:
                i = i.split()
                data_dict['moment'] = i[3]                      # form list

        return data_dict


def temp_chart_setting(title_plus, ylabel_name, y_major, y_low_limit, y_up_limit):
    plt.figure(figsize=(16, 10))
    plt.title("Volute-PQ-%s" % (title_plus), fontsize=20)
    plt.xlabel("volume")
    plt.ylabel("%s"%(ylabel_name))
    ax = plt.gca()
    x_major_locator = plt.MultipleLocator(5)
    y_major_locator = plt.MultipleLocator(y_major)
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)

    plt.xlim(0, 180)
    plt.ylim(y_low_limit, y_up_limit)

    plt.grid()


def plot_pq(project_name, plot_dict):
    temp_chart_setting(project_name, 'pressure', 10, 0, 600)
    for RPM in plot_dict.keys():
        x = plot_dict[RPM][0]
        y = plot_dict[RPM][1]
        plt.plot(x, y, 'o-', markersize=6, label=RPM)

    plt.legend()
    plt.show()


if __name__ == '__main__':
    project_name = '137DGR'
    version_name = 'V1'
    result_folder = r'G:\volute_PQ\137DGR\result_137DGR_V1'

    RPM_start = 1400
    RPM_end = 2800
    RPM_add = 200
    K_number = 20

    RPM_list, K_list = list_RPM_K(RPM_start, RPM_end, RPM_add, K_number)    # form result file list
    print(RPM_list)
    print(K_list)
    plot_dict = {}
    for RPM in RPM_list:
        volume_list = []
        pressure_list = []
        moment_list = []
        for K in K_list:
            txt_path = result_folder + '\\' + '%s-%s.txt' % (RPM, K)
            volume_dict = extract_data('Volumetric Flow Rate', txt_path)
            sp_dict = extract_data('Static Pressure', txt_path)
            moment = extract_data_moment('fan_blade', txt_path)
            volume = float(volume_dict['inlet'])*1000
            sp = float(sp_dict['outlet'])
            moment = float(moment['moment'])
            volume_list.append(volume)
            pressure_list.append(sp)
            moment_list.append(moment)

            # result_dict[i[:-4]] = {'volume': volume_dict['inlet'], 'static pressure': sp_dict['outlet'], 'moment': moment['moment']}
        plot_dict[RPM] = [volume_list, pressure_list, moment_list]

    plot_pq(project_name, plot_dict)
    print(plot_dict)


