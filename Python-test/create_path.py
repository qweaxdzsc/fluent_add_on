import os


def mkdir(path):
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)

        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


if __name__ == "__main__":
    dir = r'S:\PE\Engineering database\CFD\02_Projects\SVW_MQB_A1_HVAC\02_Lineairty'
    for i in range(1, 11):
        address = "%s\\result_MQB_A1_V%s_lin_defrost" % (dir, i)
        mkdir(address)
