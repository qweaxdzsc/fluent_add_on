import pandas as pd
import numpy as np


class PostProcess(object):
    def __init__(self, csv_path, number=21):
        self.csv_path = csv_path
        self.number = number
        # extract data
        self.read_velocity_data()
        self.get_avg_velocity()
        self.get_uniformity(self.total_avg_velocity)

    def read_velocity_data(self):
        self.df = pd.read_csv(self.csv_path, header=None, skiprows=1)
        print(self.df.head())
        print(self.df.columns)

    def get_avg_velocity(self):
        self.total_avg_velocity = self.df[4].mean()
        print('total_avg_velocity', self.total_avg_velocity)

        return self.total_avg_velocity

    def get_target_velocity(self, target_airflow, effective_area):
        # calculate min velocity through evaporator to satisfy target airflow(m3/s)
        tolerance = 1.07
        v = (target_airflow/effective_area) * tolerance
        print('target velocity', v)
        return v

    def get_uniformity(self, total_avg_velocity):
        # Uniformity
        rows = self.df.shape[0]
        tav_list = np.ones(rows) * total_avg_velocity
        diff_list = self.df[4] - tav_list
        uniformity = 1 - (diff_list.abs().sum() / (2 * total_avg_velocity * rows))

        print('uniformity: ', uniformity)
        return uniformity

    def sort_by(self, df, direction):
        # sort by direction
        # eg, df[[2], [3], [4]].sort_values([2], ascending=True), sort by Y direction
        mesh_grid = df.sort_values(direction, ascending=True)
        return mesh_grid

    def divide_sections(self, mesh_grid):
        # divide into parts based on point numbers
        # mesh_grid = self.sort_by(self.df[[2], [3], [4]], [2])
        section_number = (self.number - 2) * 2 + 2     # divide it into small sections

        rows = mesh_grid.shape[0]
        section_length = int(rows/section_number)
        print('section number: %s ; total rows: %s ; section_length: %s' % (section_number, rows, section_length))

        return section_number, section_length

    def section_avg_velocity(self, mesh_grid, section_number, section_length):
        # calculate average velocity of all sections
        section_list = []
        avg_velocity_list = np.zeros(self.number)

        for i in range(0, section_number + 2, 2):
            # not zero
            if not i:
                section_list.append(mesh_grid[i*section_length: (i+1)*section_length])
            elif i == section_number + 1:
                section_list.append(mesh_grid[(i + 1)*section_length:])
            else:
                section_list.append(mesh_grid[(i-1) * section_length: (i + 1) * section_length])

        for i, element in enumerate(section_list):
            avg_velocity_list[i] = element[4].mean()

        print(avg_velocity_list, len(avg_velocity_list))
        return avg_velocity_list

    def calculate_thickness(self, avg_velocity_list, boundary_list, thickness_list, target_velocity):
        # last time thickness
        # thickness_list = np.ones(self.number) * 54
        # variation
        alpha = 1.1
        evap_ly = 262
        avg_list = np.ones(self.number) * target_velocity
        distance_list = np.linspace(evap_ly, 0, self.number)

        # new_thickness = np.zeros(self.number)
        # for i in distance_list:
        new_thickness = thickness_list - \
                        (alpha * ((avg_velocity_list - avg_list) / avg_velocity_list) * \
                        thickness_list * (evap_ly + distance_list) / evap_ly)
        # define boundary
        up_boundary = np.ones(self.number) * 3  # thickness no less than 3mm
        lower_boundary = boundary_list
        thickness_copy = np.append(new_thickness[1:], (new_thickness[-1]))
        # make sure new thickness did not exceed boundary
        for i, element in enumerate(new_thickness):
            # front thickness should not be smaller than later one
            if new_thickness[i] > thickness_copy[i]:
                new_thickness[i] = thickness_copy[i]
            if element < up_boundary[i]:
                new_thickness[i] = up_boundary[i]
            elif element > lower_boundary[i]:
                new_thickness[i] = lower_boundary[i]
        # second point should have no more than 55% than the first
        if new_thickness[1] > new_thickness[0] * 1.55:
            new_thickness[1] = new_thickness[0] * 1.55

        print('original thickness list', thickness_list)
        print('new thickness list', new_thickness)
        return new_thickness

    def single_thickness(self, boundary_list, thickness_list, target_velocity, np_file):
        """
        calculate new thickness list based on the velocity on each sections of data,
        its for the single thickness list
        1. let data sort by Y direction
        2. confirm how many sections and section size
        3. get average velocity of each section
        4. calculate new thickness list
        :param boundary_list: up and lower boundary defined by user
        :param thickness_list: last thickness list
        :param target_velocity:
        :param np_file: .npy file path
        :return: new thickness list
        """
        mesh_grid = self.sort_by(self.df[[2, 3, 4]], [2])
        section_number, section_length = self.divide_sections(mesh_grid)
        avg_velocity_list = self.section_avg_velocity(mesh_grid, section_number, section_length)
        new_thickness = self.calculate_thickness(avg_velocity_list, boundary_list, thickness_list, target_velocity)
        np.save(np_file, new_thickness)

        return new_thickness

    def three_thickness(self, boundary_list, thickness_list, target_velocity, np_file):
        """
        same principle with single thickness, but now it return 3 thickness lists in Z direction
        :param boundary_list:
        :param thickness_list:
        :param target_velocity:
        :param np_file:
        :return: new_thickness: a list of three thickness lists
        """
        mesh_grid = self.sort_by(self.df[[2, 3, 4]], [3])   # from small to large
        # divide it into three sections 0.15: 0.7: 0.15
        part_ratio = [0.15, 0.7, 0.15]
        new_thickness = []
        rows = mesh_grid.shape[0]
        place_ratio = [0, 0.15, 0.85, 1]
        for i in range(3):
            new_mesh_grid = mesh_grid[int(place_ratio[i]*rows): int(place_ratio[i+1]*rows)]
            new_mesh_grid = self.sort_by(new_mesh_grid, [2])
            section_number, section_length = self.divide_sections(new_mesh_grid)
            avg_velocity_list = self.section_avg_velocity(new_mesh_grid, section_number, section_length)
            new_thickness.append(self.calculate_thickness(avg_velocity_list, boundary_list, thickness_list[i],
                                                      target_velocity))
        # the outside must not larger than inside
        new_thickness[0] = np.where(new_thickness[0] > new_thickness[1], new_thickness[1], new_thickness[0])
        new_thickness[2] = np.where(new_thickness[2] > new_thickness[1], new_thickness[1], new_thickness[2])
        # save
        np.save(np_file, new_thickness)
        return new_thickness


if __name__ == '__main__':
    csv_path = r'G:\test\auto_diffuser\ad_v2\ad_V6\result_ad_V6\ad_V6_data.csv'
    number = 21
    # thickness_list = np.ones(number) * 54
    file_name = r'G:\test\auto_diffuser\ad_v2\ad_V6\ad_V6_thickness_3.npy'
    thickness_list = np.load(file_name)
    boundary_list = np.ones(number) * 54
    np_file = r'G:\test\auto_diffuser\ad_v2\ad_V6\test1.npy'
    process = PostProcess(csv_path, number)
    target_velocity = process.get_target_velocity(0.15, 0.05502)
    # process.section_avg_velocity()
    # process.single_thickness(boundary_list, thickness_list, target_velocity, np_file)
    process.three_thickness(boundary_list, thickness_list, target_velocity, np_file)