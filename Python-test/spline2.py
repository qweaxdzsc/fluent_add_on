import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# --------input data-------------------
# x = [1, 2, 3, 5]
# y = [1, 0, 2, 2]

f = pd.read_csv(r"C:\Users\BZMBN4\Desktop\db_dba2.csv", header=None)
x = np.array(f[0])
y = np.array(f[1])

# ---------construct matrix--------------
nx = len(x)  # how many points does data have
curv_number = nx - 1  # number of governing curvatures

lines = 3 * (nx - 1)  # lines for matrix
col = lines

# build shape of matrix
matrix_x = np.zeros([lines, col])
matrix_b = np.zeros([col])

# first line
matrix_x[0][0] = 1
matrix_b[0] = 0  # make a1 = 0

# following line
for i in range(nx - 1):
    matrix_x[2 * i + 1][3 * i: 3 * i + 3] = [x[i] ** 2, x[i], 1]
    matrix_x[2 * i + 2][3 * i: 3 * i + 3] = [x[i + 1] ** 2, x[i + 1], 1]

    matrix_b[2 * i + 1: 2 * i + 3] = [y[i], y[i + 1]]

next_line = 1 + 2 * (nx - 1)
for i in range(nx - 2):
    matrix_x[next_line + i][3 * i: 3 * i + 2] = [2 * x[i + 1], 1]
    matrix_x[next_line + i][3 * i + 3: 3 * i + 5] = [-2 * x[i + 1], -1]
    # matrix_x[i + 2][i + 4: i + 6] = [-2 * x[i + 1], -1]

print(matrix_x)
print(matrix_b)
# matrix_x = np.array([[1, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0], [4, 2, 1, 0, 0, 0], [0, 0, 0, 4, 2, 1], [0, 0, 0, 9, 3, 1],
#                      [0, -1, 0, 4, 1, 0]])
# matrix_c = np.zeros(6)
# matrix_b = np.array([[0], [1], [1], [1], [2], [0]])

# ----------get all function coefficient---------
# print(matrix_c)
matrix_c = np.linalg.solve(matrix_x, matrix_b)

print(matrix_c)

# -----------expand x-------------
n = 10

expand_x = []
spline_x = np.zeros([nx + (nx - 1) * n, col])
print(spline_x.shape)
for i in range(len(x) - 1):
    new_points = np.linspace(x[i], x[i + 1], n + 1, endpoint=False)
    expand_x.extend(new_points)
    for j in range(n + 1):
        spline_x[(n + 1) * i + j][3 * i: 3 * i + 3] = [new_points[j] ** 2, new_points[j], 1]

expand_x.append(x[-1])
spline_x[-1][-3:] = [x[-1] ** 2, x[-1], 1]

print(spline_x)

# ------------get spline y-coordinates---------------
spline_y = np.dot(spline_x, matrix_c)
print(spline_y)

# ---------------plot spline from functions above------------
plt.plot(x, y, 'o')
plt.plot(expand_x, spline_y)
plt.show()
