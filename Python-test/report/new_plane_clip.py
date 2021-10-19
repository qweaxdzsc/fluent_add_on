import os
import numpy as np

class extractor(object):
    def __init__(self,  project_path, project_name):
        self.project_path = project_path
        self.project_name = project_name
        self.content = ''

    def read_case_data(self, case_name):
        text = """
/file/read-case-data %s\\lin_case\\%s\\%s.cas yes
""" % (self.project_path, case_name, case_name)
        self.content += text

    def create_three_point_plane(self, surface_name, three_points, bounded):
        first = three_points[0].copy()
        second = three_points[1].copy()
        third = three_points[2].copy()
        print(first)
        for i in range(3):
            first[i] = round(first[i]/1000, 4)
            second[i] = round(second[i]/1000, 4)
            third[i] = round(third[i]/1000, 4)

        text = f"""
/surface/plane-surface {surface_name} three-points {first[0]} {first[1]} {first[2]}
{second[0]} {second[1]} {second[2]} {third[0]} {third[1]} {third[2]} {bounded} no
"""
        self.content += text

    def txt_surface_integrals(self, face_list, txt_out, field='temperature'):
        if field == '':
            pass
        else:
            field = field + ' '
        face_name = ''
        for i in face_list:
            face_name += ' ' + i
        text = """
/report/surface-integrals/mass-weighted-avg%s() %syes %s yes q
""" % (face_name, field, txt_out)
        self.content += text

    def create_txt(self, txt_path):
        with open(txt_path, 'w') as f:
            f.write(self.content)
            f.close()
        os.system(txt_path)


if __name__ == '__main__':
    outlet_cvl = [[694.92, -208.05, 688.8], [655.04, -208.05, 670.21], [655.04, -102.69, 670.21]]
    outlet_cvr = [[697.64, 79.95, 690.07], [655.95, 79.95, 670.63], [655.92, 186.95, 670.63]]
    outlet_svr = [[444.02, 442.3, 813.8], [444.02, 442.3, 752.8], [383.02, 442.3, 752.8]]
    outlet_svl = [[441.85, -502.25, 792.5], [441.85, -502.25, 746.5], [510.85, -502.25, 746.5]]
    outlet_sdr = [[381.02, 442.3, 820.8], [381.02, 442.3, 794.8], [322.02, 442.3, 794.8]]
    outlet_sdl = [[352.85, -502.25, 823.5], [352.85, -502.25, 794.5], [420.85, -502.25, 794.5]]
    outlet_cd = [[91.59, 124.56, 842.93], [94.59, 124.56, 804.93], [91.59, -88.44, 804.93]]
    outlet_rfl = [[643.83, -137.4, 121.17], [531.83, -137.4, 121.17], [531.83, -103.4, 121.17]]
    outlet_rfr = [[643.83, 107.6, 121.17], [533.83, 107.6, 121.17], [533.83, 134.6, 121.17]]
    outlet_ffl = [[555.83, -265.4, 524.26], [454.83, -265.4, 524.26], [454.83, -190.4, 524.26]]
    outlet_ffr = [[621.45, 184.6, 524.26], [537.83, 184.6, 524.26], [537.83, 249.46, 524.26]]
    project_path = r'G:\_HAVC_Project\MRH_FRONT\MRH_FRONT_12_lin_defog\MRH_V47_lin_defog'
    project_name = 'MRH_V47_lin_defog'
    angle_array = np.linspace(10, 90, 9, dtype=int)
    print(angle_array)
    a = extractor(project_path, project_name)
    for i in angle_array:
        case_name = project_name + f'_{i}'
        result_path = project_path + f'\\lin_case\\{case_name}\\result\\total_result.txt'
        a.read_case_data(case_name)
        a.create_three_point_plane('middle_svr', outlet_svr, 'yes')
        a.create_three_point_plane('middle_svl', outlet_svl, 'yes')
        # a.create_three_point_plane('middle_cvl', outlet_cvl, 'yes')
        # a.create_three_point_plane('middle_cvr', outlet_cvr, 'yes')
        a.create_three_point_plane('middle_sdr', outlet_sdr, 'yes')
        a.create_three_point_plane('middle_sdl', outlet_sdl, 'yes')
        a.create_three_point_plane('middle_cd', outlet_cd, 'yes')
        a.create_three_point_plane('middle_rfl', outlet_rfl, 'yes')
        a.create_three_point_plane('middle_rfr', outlet_rfr, 'yes')
        a.create_three_point_plane('middle_ffl', outlet_ffl, 'yes')
        a.create_three_point_plane('middle_ffr', outlet_ffr, 'yes')
        a.txt_surface_integrals(['middle*'], result_path)

    a.create_txt(r'C:\Users\BZMBN4\Desktop\test.jou')
