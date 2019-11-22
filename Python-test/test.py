# import timeit
# import numpy as np
#
# # 待测试的函数
# def add():
#     import openpyxl
#     wb = openpyxl.Workbook()
#     worksheet = wb['Sheet']
#
#     worksheet.cell(1, 1, 2)
#
#     wb.save(filename=r'C:\Users\BZMBN4\Desktop\test.xlsx')
#
# # stmt 需要测试的函数或语句，字符串形式
# # setup 运行的环境，本例子中表示 if __name__ == '__main__':
# # number 被测试的函数或语句，执行的次数，本例表示执行100000次add()。省缺则默认是10000次
# # repeat 测试做100次
# # 综上：此函数表示 测试 在if __name__ == '__main__'的条件下，执行100000次add()消耗的时间，并把这个测试做100次,并求出平均值
#
# t = timeit.repeat(stmt="add()", setup="from __main__ import add", number=1, repeat=1)
#
# print(t)
# print(sum(t) / len(t))
b = 2.25335
number = 1
factor = 10**(number+1)
#
# b = int(b*factor)/factor

# a = '%.1f' % (b)



print(a)


