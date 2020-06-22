import os
import re
import mmap
# import contextlib
import time


class MeshInfoParser(object):
    # 文本格式的.msh文件或者.cas文件，不支持二进制格式, 暂不支持.h5
    def __init__(self, file_name):
        self.file = file_name
        # os.chdir(os.path.abspath((os.path.dirname(__file__))))
        # -------------init parameter-----------------------------
        self.fsize_show = float()                           # the shown file size
        self.fsize_unit = str()                             # the unit of shown file size
        self.file_info = b''                                # file read by mmap(bytes)
        self.boundary = dict()                              # 用于保存边界名称，边界ID，边界类型的字典
        self.zone = {'0': {'name': 'Total', 'type': 'Total', 'cell_number': 0}}               # 用于保存计算域名称，计算域ID，计算域类型的字典
        self.dim = str()                                    # 用于保存模型的维度数
        self.node_number = 0                                # 用于保存模型的节点数
        self.nodes_show = str()                             # edited nodes number for shown purpose
        self.cell_number = 0                                # 用于保存模型的网格数
        self.element_type = {                               # 用与保存模型中各种网格类型的数目
            '0': {'name': '混合网格', 'number': 0},
            '1': {'name': '三角形网格', 'number': 0},
            '2': {'name': '四面体网格', 'number': 0},
            '3': {'name': '四边形网格', 'number': 0},
            '4': {'name': '六面体网格', 'number': 0},
            '5': {'name': '棱形网格', 'number': 0},
            '6': {'name': '锥形网格', 'number': 0},
            '7': {'name': '多面体网格', 'number': 0},
        }
        # ----------------Reg Pattern-----------------------
        self.pattern_zone_bc = re.compile(b'\(39\s\(([0-9]+\s.+)\)')         # 边界或者计算域, 以(39开头
        self.pattern_dim = re.compile(b'\(2\s([2-3])\)')                     # 模型维数, 以(2开头
        self.pattern_node = re.compile(b'\(10\s\(0\s[0-9]\s([0-9a-f]+)')     # 模型的节点描述信息, 以(10开头
        self.pattern_cell = re.compile(b'\([0-9]*12\s\(([0-9a-f\s]+)\)')     # 模型的网格描述信息, 以(12开头

    def get_file_size(self):
        if os.path.exists(self.file):
            fsize = os.path.getsize(file_name)
            self.fsize_show = fsize / 1024 / 1024
            self.fsize_unit = 'MB'
            if self.fsize_show > 1024:
                self.fsize_show = self.fsize_show / 1024
                self.fsize_unit = 'GB'
        else:
            print('file do not exist')

    def read_file(self):
        """
        contextlib.closing will auto close reading after 'with' structure
        :return:
        """
        with open(self.file, 'rb') as f:
            # self.file_info = f.read()
            # print(self.pattern_dim.findall(f))
            self.file_info = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            # with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as self.file_info:   # 内存映射
            #     self.parse_dimension()
            #     self.parse_nodes()
            #     self.parse_zone()
            #     self.parse_cell()

    def parse_dimension(self):
        self.dim = self.pattern_dim.findall(self.file_info)[0].decode()
        # print(dim)

    def parse_nodes(self):
        # print(pattern_node.findall(m))
        self.node_number = int(self.pattern_node.findall(self.file_info)[0].decode(), 16)
        self.nodes_show = '%.1f万' % (self.node_number/10000)

    def parse_zone(self):
        for i in self.pattern_zone_bc.findall(self.file_info):
            zone_info = i.decode()

            zone_bc_result = zone_info.split(' ')
            if zone_bc_result[1] in ['solid', 'fluid']:
                self.zone[zone_bc_result[0]] = {'name': zone_bc_result[2],
                                           'type': zone_bc_result[1],
                                           'cell_number': 0}
            else:
                self.boundary[zone_bc_result[0]] = {'name': zone_bc_result[2],
                                               'type': zone_bc_result[1],
                                               'cell_number': 0}

    def parse_cell(self):
        for i in self.pattern_cell.findall(self.file_info):
            cell_info = i.decode()
            cell_result = cell_info.split(' ')
            zone_id = str(int(cell_result[0], 16))
            self.zone[zone_id]['cell_number'] = '%.1f万' % ((int(cell_result[2], 16) - int(cell_result[1], 16))/10000)
            if len(cell_result) > 4:
                self.element_type[cell_result[4]]['number'] += (int(cell_result[2], 16) - int(cell_result[1], 16))

    def parse_all(self):
        self.read_file()
        self.get_file_size()
        self.parse_dimension()
        self.parse_nodes()
        self.parse_zone()
        self.parse_cell()

    def print_file_size(self):
        print('----------------------------------')
        print('文件大小: %.2f%s' % (self.fsize_show, self.fsize_unit))

    def print_nodes_number(self):
        print('----------------------------------')
        print('模型的总结点数: %s' % self.nodes_show)

    def print_dimension(self):
        print('----------------------------------')
        print('模型的维数为: %s维' % self.dim)

    def print_zone_info(self):
        print('----------------------------------')
        print('共有%s个计算域' % len(self.zone))
        for key, value in self.zone.items():
            print('计算域名称：%-18s' % value['name'],
                  '计算域ID：%-6s' % key,
                  '计算域类型：%-18s' % value['type'],
                  '网格数量:%-10s' % value['cell_number'])

    def print_boundary_info(self):
        print('----------------------------------')
        print('共有%s个边界' % len(self.boundary))
        for key, value in self.boundary.items():
            print('边界名称：%-18s' % value['name'],
                  '边界ID：%-6s' % key,
                  '边界类型：%-10s' % value['type'])

    def print_element_info(self):
        print('----------------------------------')
        for key, value in self.element_type.items():
            print('模型中%s的网格数：%.1f万' % (value['name'], value['number'] / 10000))

    def print_info(self):
        self.print_file_size()
        self.print_dimension()
        self.print_nodes_number()
        self.print_zone_info()
        self.print_boundary_info()
        self.print_element_info()


if __name__ == "__main__":
    start_time = time.time()
    # file_name = r'C:\Users\BZMBN4\Desktop\1234.cas'
    file_name = r'G:\_HAVC_Project\GE2_REAR\GE2-rear-round3\GE2-rear-ppc-FC\GE2-rear3-ppc-FC-mesh.cas'
    mesh_info = MeshInfoParser(file_name)
    mesh_info.get_file_size()
    mesh_info.read_file()
    mesh_info.parse_all()
    mesh_info.print_info()
    end_time = time.time()
    print('程序运行时间：', end_time - start_time)
    pass