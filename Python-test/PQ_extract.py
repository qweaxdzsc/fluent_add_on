
def txt_file_list(version_name, RPM_start, RPM_end, RPM_add, K_start, K_end, K_add):
    RPM_list = [RPM for RPM in range(RPM_start, RPM_end+RPM_add, RPM_add)]
    K_list = [K for K in range(K_start, K_end+K_add, K_add)]
    result_file_list = []

    for RPM in RPM_list:
        for K in K_list:
            result_file_list.append('%s_%srpm_K%s_totalresult.txt' % (version_name, RPM, K))

    return result_file_list


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
                data_dict['moment'] = i[3]

        return data_dict


if __name__ == '__main__':

    # Project_name = 'D2UX_PQ'
    version_name = 'D2UX_PQ'
    result_folder = r'\\192.168.1.101\works\motor'

    RPM_start = 2000
    RPM_end = 2600
    RPM_add = 200
    K_start = 1
    K_end = 9
    K_add = 2

    result_file_list = txt_file_list(version_name, RPM_start, RPM_end, RPM_add, K_start, K_end, K_add)    # form result file list

    result_dict = {}                                                                                        # form result dict
    for i in result_file_list:
        txt_path = result_folder + '\\' + i
        volume_dict = extract_data('Volumetric Flow Rate', txt_path)
        sp_dict = extract_data('Static Pressure', txt_path)
        moment = extract_data_moment('asmo_fan', txt_path)

        result_dict[i[:-4]] = {'volume': volume_dict['inlet_asmo'], 'static pressure': sp_dict['outlet_asmo'], 'moment': moment['moment']}

    print(result_dict)


