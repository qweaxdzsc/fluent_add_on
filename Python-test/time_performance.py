import timeit


def time_test():
    from python_to_pptx import get_ppt
    project_name = 'GE2-rear3'
    version = 'ppd-V1-FH'
    Rotation_speed = 3000
    get_ppt(project_name, version)



repeats = 1
test_number = 1

total_time_list = timeit.repeat(stmt=time_test, repeat=repeats, number=test_number)
# mean_time = total_time/(repeats*test_number)

print(total_time_list)