from root_transfer import add_slash

angle = [20, 40, 60, 80]

raw_path = r'G:\GE2_REAR\GE2-rear-vent\GE2-rear-linearty\GE2-rear-linearity-case-v2\result'


def mkdir(path):

    import os
    path = path.strip()
    path = path.rstrip("\\")

    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)

        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


for i in angle:
    out_path = add_slash(raw_path)
    final_path = out_path + 'GE2-%s' % (i)
    mkdir(final_path)