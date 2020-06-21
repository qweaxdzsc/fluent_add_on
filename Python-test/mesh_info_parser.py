import os
import re
import mmap
import contextlib
import time

# os.chdir(os.path.abspath((os.path.dirname(__file__))))

# file_name = r'G:\_HAVC_Project\D2U-2\D2U-2_vent\D2U-2_vent_V24\D2U-2_V24_vent.cas'     # 文本格式的.msh文件或者.cas文件，不支持二进制格式, 暂不支持.h5
file_name = r'C:\Users\BZMBN4\Desktop\1234.cas'     # 文本格式的.msh文件或者.cas文件，不支持二进制格式, 暂不支持.h5
boundary = dict()           # 用于保存边界名称，边界ID，边界类型的字典
zone = {'0': {'name': 'Total', 'type': 'Total', 'cell_number': 0}}               # 用于保存计算域名称，计算域ID，计算域类型的字典
dim = str()                  # 用于保存模型的维度数
node_number = 0             # 用于保存模型的节点数
cell_number = 0             # 用于保存模型的网格数
element_type = {                                               # 用与保存模型中各种网格类型的数目
    '0': {'name': '混合网格', 'number': 0},
    '1': {'name': '三角形网格', 'number': 0},
    '2': {'name': '四面体网格', 'number': 0},
    '3': {'name': '四边形网格', 'number': 0},
    '4': {'name': '六面体网格', 'number': 0},
    '5': {'name': '棱形网格', 'number': 0},
    '6': {'name': '锥形网格', 'number': 0},
    '7': {'name': '多面体网格', 'number': 0},
}

pattern_zone_bc = re.compile(b'\(39\s\((.+)\)')                 # 边界或者计算域, 以(39开头
pattern_dim = re.compile(b'\(2\s([2-3])\)')                     # 模型维数, 以(2开头
pattern_node = re.compile(b'\(10\s\(0\s[0-9]\s([0-9a-f]+)')     # 模型的节点描述信息, 以(10开头
pattern_cell = re.compile(b'\([0-9]*12\s\(([0-9a-f\s]+)\)')     # 模型的网格描述信息, 以(12开头

# -------- start parse------------
start_time = time.time()
fsize = os.path.getsize(file_name)
fsize_show = fsize / 1024 / 1024
fsize_unit = 'MB'
if fsize_show > 1024:
    fsize_show = fsize_show / 1024
    fsize_unit = 'GB'
# --------read file---------------
with open(file_name, 'rb') as f:
    # print(pattern_dim.findall(f.read())[0])
    with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:    # 内存映射
        dim = pattern_dim.findall(m)[0].decode()
        # print(dim)
        # dim = re.split(b'[()]', pattern_dim.findall(m)[0])[2]

        # print(pattern_node.findall(m))
        nodes = int(pattern_node.findall(m)[0].decode(), 16)
        nodes_show = '%.1f万' % (nodes/10000)

        for i in pattern_zone_bc.findall(m):
            zone_info = i.decode()
            # print(zone_info)
            zone_bc_result = zone_info.split(' ')
            if zone_bc_result[1] in ['solid', 'fluid']:
                zone[zone_bc_result[0]] = {'name': zone_bc_result[2],
                                           'type': zone_bc_result[1],
                                           'cell_number': 0}
            else:
                boundary[zone_bc_result[0]] = {'name': zone_bc_result[2],
                                               'type': zone_bc_result[1],
                                               'cell_number': 0}

        for i in pattern_cell.findall(m):
            cell_info = i.decode()
            cell_result = cell_info.split(' ')
            zone_id = str(int(cell_result[0], 16))
            zone[zone_id]['cell_number'] = '%.1f万' % ((int(cell_result[2], 16) - int(cell_result[1], 16))/10000)
            if len(cell_result) > 4:
                element_type[cell_result[4]]['number'] += (int(cell_result[2], 16) - int(cell_result[1], 16))


end_time = time.time()
print('----------------------------------')
print('文件大小: %.2f%s' % (fsize_show, fsize_unit))
print('----------------------------------')
print('模型的总结点数: %s' % nodes_show)
print('----------------------------------')
print('模型的维数为: %s维' % dim)
print('----------------------------------')
print('共有%s个计算域' % len(zone))
for key, value in zone.items():
    print('计算域名称：%-18s' % value['name'],
          '计算域ID：%-6s' % key,
          '计算域类型：%-18s' % value['type'],
          '网格数量:%-10s' % value['cell_number'])
print('----------------------------------')
print('共有%s个计算域' % len(zone))
for key, value in boundary.items():
    print('计算域名称：%-18s' % value['name'],
          '计算域ID：%-6s' % key,
          '计算域类型：%-10s' % value['type'])
print('----------------------------------')
for key, value in element_type.items():
    print('模型中%s的网格数\t：%.1f万' % (value['name'], value['number']/10000))
print('----------------------------------')
print('程序运行时间：', end_time - start_time)