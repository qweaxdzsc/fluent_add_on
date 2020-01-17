# import os
#
#
# def make_batch_folder(path, version_count, mode='VENT'):
#     for i in range(1, version_count):
#         os.makedirs(r'%s\V%s_%s' % (path, i, mode))
#
#
# def make_class_folder(path):
#     os.makedirs(r'%s\00_Inputs'% (path))
#     os.makedirs(r'%s\01_Airflow' % (path))
#     os.makedirs(r'%s\02_Linearity' % (path))
#
#
# if __name__ == '__main__':
#     path = r'S:\PE\Engineering database\CFD\02_Projects\SGM_458_Rear_HVAC\458_Rear_Round2\01_Airflow'
#     version_count = 4
#     # make_class_folder(path)
#     make_batch_folder(path, version_count, mode='FOOT')


class test():
    def orgi(self):
        print('我是原始函数！')

    def new(self):
        print('我是重写后的新函数!')


a = test() # 实例化
a.orgi()

# 用新函数代替原始函数，也就是【重写类方法】
a.orgi = a.new

# 现在原始函数已经被替换了
a.orgi()