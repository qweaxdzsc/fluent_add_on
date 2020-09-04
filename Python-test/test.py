"""
Example of simple TUI script generation
"""


def read_case(case_path, case_name):
    text = """
/file/read-case {case_path}/{case_name} yes
""".format(case_path=case_path, case_name=case_name)
    return text


def initialization():
    text = """
/solve/initialize/hyb-initialization yes
"""
    return text


def start_calculation(iterations):
    text = """
/solve/iterate/{iteration} yes
""".format(iteration=iterations)
    return text


def write_case_data(case_path, case_name):
    text = """
/file/write-case-data {{case_path}}/{{case_name}} yes
""".format(case_path=case_path, case_name=case_name)
    return text


def exit_fluent():
    text = """
/exit yes
"""
    return text


def read_journal(journal_file):
    text = """
/file/read-journal {jou}
""".format(jou=journal_file)
    return text


def BC_mass_flow_inlet(face_name, mass_flow, turb_intensity=5, turb_length_scale=0.005):
    text = """
/define/boundary-conditions/set/mass-flow-inlet %s() 
mass-flow no %s
direction-spec no yes
ke-spec no yes turb-intensity %s turb-length-scale %s q
""" % (face_name, mass_flow, turb_intensity, turb_length_scale)
    return text


if __name__ == '__main__':
    # 定义变量
    journal_path = r"C:\Users\BZMBN4\Desktop\test.jou"
    case_path = r'C:\Users\BZMBN4\Desktop'
    case_name = r'demo.cas'
    # 打开空白新文件
    jou_file = open(journal_path, 'w')
    # 通过应用函数构造内容
    content = ''
    content += read_case(case_path, case_name)
    content += initialization()
    content += start_calculation(200)
    content += write_case_data(case_path, case_name)
    for i in range(1, 10):
        content += BC_mass_flow_inlet('inlet', 0.1*i)
        content += start_calculation(200)
        content += write_case_data(case_path, case_name)
    content += exit_fluent()
    # content += read_journal(journal_path)
    # 写入构造好的内容
    jou_file.write(content)
    # 关闭新文件写入
    jou_file.close()
    # 调用os模块，打开刚写好的文件
    import os
    os.system(journal_path)