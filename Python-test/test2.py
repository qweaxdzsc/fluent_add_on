import numpy as np
import matplotlib.pyplot as plt
import math

# == parameters ===
nx = 10  # 网格单元数
Nnodes = nx + 1  # 节点数，含左边界点
L = 1  # 长度，m
n2 = 25  # /m2, hP/kA
Tb = 100  # 边界B的温度值 ,℃
q = 0  # 自由端截面的热流密度值, W/m2
Tc = 20  # 环境温度，℃

# ==  x grid ==
dx = L / nx  # 网格间距
print('dx = ', dx)
x = np.zeros(Nnodes)  # x网格
x[1:] = np.linspace(dx / 2, L - dx / 2, nx)  # 以边界A为原点创建网格点的坐标值
print('x grid = ', x, '\n')

# ==  solution array ==
tt = np.zeros(Nnodes)  # 解向量
tt[0] = Tb  # 边界值

# == matrix ==
A = np.zeros((nx, nx))
b = np.zeros(nx)

su = n2 * dx * Tc
sp = -n2 * dx
for i in range(1, nx - 1):  # 内部节点
    A[i][i - 1] = -1 / dx
    A[i][i + 1] = -1 / dx
    A[i][i] = -(A[i][i - 1] + A[i][i + 1]) - sp
    b[i] = su

# for B boundary
i = 0
A[i][i + 1] = -1 / dx
su = 2 * Tb / dx + n2 * dx * Tc
sp = -2 / dx - n2 * dx
A[i][i] = -A[i][i + 1] - sp
b[i] = su

# for insulated boundary
i = nx - 1
A[i][i - 1] = -1 / dx
su = n2 * dx * Tc
sp = -n2 * dx
A[i][i] = -A[i][i - 1] - sp
b[i] = su

print('A = \n', A, '\n')
print('b = \n', np.matrix(b).T, '\n')

t_temp = np.linalg.solve(A, b)
print('solution = \n', np.matrix(t_temp).T, '\n')
tt[1:] = t_temp

xx = np.linspace(0, L, 50, endpoint=True)
exact_tt = np.zeros(50)
n = math.sqrt(n2)
for i in range(50):
    exact_tt[i] = Tc + (Tb - Tc) * (math.cosh(n * (L - xx[i]))) / math.cosh(n * L)

plt.xlabel('DisTbnce (m)')
plt.ylabel('Temperature (C)')
plt.plot(x, tt, 'bs', label='Numerical')
plt.plot(xx, exact_tt, 'k', label='Exct')
plt.legend()
plt.show()
