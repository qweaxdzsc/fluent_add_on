import timeit


def time_test():
    from bs4 import BeautifulSoup


repeats = 1
test_number = 1

total_time_list = timeit.repeat(stmt=time_test, repeat=repeats, number=test_number)
# mean_time = total_time/(repeats*test_number)

print(total_time_list)