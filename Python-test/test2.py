import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


class PostProcess(object):
    def __init__(self, csv_path, number=11):
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

    def get_uniformity(self, total_avg_velocity):
        # Uniformity
        rows = self.df.shape[0]
        tav_list = np.ones(rows) * total_avg_velocity
        diff_list = self.df[4] - tav_list
        uniformity = 1 - (diff_list.abs().sum() / (2 * total_avg_velocity * rows))

        print('uniformity: ', uniformity)
        return uniformity

    def sort_by_Y(self):
        # take Y,Z PLANE and its velocity, sort by Y
        mesh_grid = self.df[[2, 3, 4]].sort_values([2], ascending=True)
        return mesh_grid

    def sort_by_Z(self):
        # take Y,Z PLANE and its velocity, sort by Z
        mesh_grid = self.df[[2, 3, 4]].sort_values([3], ascending=True)
        return mesh_grid

    def divide_sections(self):
        # divide into parts based on point numbers
        mesh_grid = self.sort_by_Y()
        sections = (self.number - 2) * 2 + 2     # divide it into small sections

        rows = mesh_grid.shape[0]
        section_length = int(rows/sections)
        print('section number: %s ; total rows: %s ; section_length: %s' % (sections, rows, section_length))

        return sections, section_length

    def section_avg_velocity(self):
        mesh_grid = self.sort_by_Y()
        sections, section_length = self.divide_sections()
        # calculate average velocity of all sections
        section_list = []
        avg_velocity_list = np.zeros(self.number)

        for i in range(0, sections + 2, 2):
            # not zero
            if not i:
                section_list.append(mesh_grid[i*section_length: (i+1)*section_length])
            elif i == sections + 1:
                section_list.append(mesh_grid[(i + 1)*section_length:])
            else:
                section_list.append(mesh_grid[(i-1) * section_length: (i + 1) * section_length])

        for i, element in enumerate(section_list):
            avg_velocity_list[i] = element[4].mean()

        print(avg_velocity_list, len(avg_velocity_list))
        return avg_velocity_list

    def calculate_thickness(self, thickness_list, np_file):
        avg_velocity_list = self.section_avg_velocity()
        # last time thickness
        # thickness_list = np.ones(self.number) * 54

        # variation
        alpha = 0.8
        evap_ly = 262
        avg_list = np.ones(self.number) * self.total_avg_velocity
        distance_list = np.linspace(evap_ly, 0, 11)

        # new_thickness = np.zeros(self.number)
        # for i in distance_list:
        new_thickness = thickness_list - \
                        (alpha * ((avg_velocity_list - avg_list) / avg_velocity_list) * \
                        thickness_list * (evap_ly + distance_list) / evap_ly)

        up_boundary = np.zeros(self.number)
        lower_boundary = thickness_list

        for i, element in enumerate(new_thickness):
            if element < up_boundary[i]:
                new_thickness[i] = 0
            elif element > lower_boundary[i]:
                new_thickness[i] = lower_boundary[i]
        np.save(np_file, new_thickness)
        print('new thickness list', new_thickness)
        return new_thickness


if __name__ == '__main__':
    csv_path = r'G:\test\auto_diffuser\ad_v1\result_ad_V4_201106\ad_V4_201106_data.csv'
    np_file = r'G:\test\auto_diffuser\ad_v1\ad_v5_thickness'
    number = 11
    # thickness_list = np.ones(number) * 54
    file_name = r'G:\test\auto_diffuser\ad_v1\ad_v4_thickness.npy'
    thickness_list = np.load(file_name)
    process = PostProcess(csv_path, number)
    process.calculate_thickness(thickness_list, np_file)