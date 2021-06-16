#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import pylab as pl
from scipy import interpolate


def generate_data(x, ppl):
    """ 产生x点集 """
    b = []
    for i in range(len(x) - 1):
        new_array = np.linspace(x[i], x[i + 1], ppl, endpoint=False)
        b.extend(new_array)

    b.append(x[-1])
    b = np.array(b)

    return b


def generate_sin(x):
    """ 得到 sin 函数的x,对应的y点 """
    y = np.sin(x)
    return y


def interpolate_linear(x, y):
    """ 线性插值"""
    f_linear = interpolate.interp1d(x, y)
    return f_linear


def interpolate_b_spline(x, y, x_new, der=0):
    """ B 样条曲线插值 或者导数. 默认der = 0"""
    tck = interpolate.splrep(x, y)
    y_bspline = interpolate.splev(x_new, tck, der=der)
    return y_bspline


def test_interpolate():
    import pandas

    # # pt_x = generate_data(begin=begin, end=end, num=10)
    # # pt_y = generate_sin(pt_x)
    f = pandas.read_csv(r"C:\Users\BZMBN4\Desktop\db_dba2.csv", header=None)
    pt_x = np.array(f[0])
    pt_y = np.array(f[1])
    begin = pt_x[0]
    end = pt_x[-1]

    interpolate_x = generate_data(pt_x, 4)
    # f_linear = interpolate_linear(pt_x, pt_y)

    y_bspline = interpolate_b_spline(pt_x, pt_y, interpolate_x, der=0)
    print(len(pt_x))
    print(pt_x)
    print(interpolate_x)
    print(y_bspline)
    # y_bspine_derivative = interpolate_b_spline(pt_x, pt_y, interpolate_x, der=1) # 一阶导数

    pl.plot(pt_x, pt_y, "o", label=u"origin data")
    # pl.plot(interpolate_x, f_linear(interpolate_x), label=u"linear")
    pl.plot(interpolate_x, y_bspline, label=u"B-spline")
    # pl.plot(interpolate_x, y_bspine_derivative, label=u"B-spline-der")
    pl.legend()
    pl.show()


if __name__ == '__main__':
    test_interpolate()

