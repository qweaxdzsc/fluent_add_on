
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.lines import Line2D
import math


# predefine
phi_a = 1
phi_b = 0
u = 2.5
L = 1
rho = 1
k = 0.1

F = rho * u
D = float()
# n = 25
# a = 1

# define mesh
nx = 35
dx = L/nx

D = k/dx

x = np.zeros(nx + 2)
x[1:-1] = np.linspace(0 + 0.5 * dx, L - 0.5 * dx, nx)
x[-1] = L
print('mesh points', x)


# Initial condition
T = np.zeros(nx)

# # Boundary condition
# T[0] = Ta
# T[-1] = Tb
# print('', T)


# Solver
# analytical solution



# construct A matrix
def matrix_A(nx, D, F):
    A = np.zeros((nx, nx))
    A[0, :2] = [D - F/2 + (2*D + F), -(D - F/2)]
    A[-1, -2:] = [-(D + F/2), D + F/2 + 2*D - F]

    for i in range(len(A[1:-1, :])):
        a1 = -(D + F/2)
        a2 = 2*D
        a3 = -(D - F/2)
        A[1 + i, i:i+3] = [a1, a2, a3]

    print(A)
    return A


def matrix_b(nx, D, F):
    b = np.zeros(nx)
    b[0] = (2*D + F) * phi_a
    b[-1] = (2*D - F) * phi_b

    print(b)
    return b


A = matrix_A(nx, D, F)
b = matrix_b(nx, D, F)
new_phi = np.linalg.solve(A, b)
new_phi = np.insert(new_phi, 0, phi_a)
new_phi = np.append(new_phi, phi_b)
print(new_phi)

fig = plt.figure()
# plt.plot(a_x, a_T)
plt.plot(x, new_phi, 'bs')
# plt.xlabel('Iterations')
# plt.ylabel('Residual of temperature')
plt.show()


# Iterations
def iterations(diff_target, T):

    T_norm = [1]
    n = 0
    steps = [0]

    while T_norm[-1] >= diff_target:
        n += 1
        steps.append(n)
        T_last = T.copy()

        T[0] = (T[1] + 2*Ta)/3
        T[1:-1] = 0.5*(T[:-2] + T[2:])
        T[-1] = (T[-2] + 2*Tb)/3

        T_norm.append(np.abs(np.sum(T - T_last)))
        print("step %s" % n)
        print(T_norm[-1])

    fig = plt.figure()
    residual_plot, = plt.plot(steps[1:], T_norm[1:], 'k')
    residual_plot.set_data(steps[1:], T_norm[1:])
    plt.xlabel('Iterations')
    plt.ylabel('Residual of temperature')


diff_target = 1e-4
# iterations(diff_target, T)

T_norm = [1]
n = 1
steps = [0]

fig = plt.figure()

residual_plot, = plt.plot(steps[1:], T_norm[1:], 'k')
residual_plot.set_data(steps[1:], T_norm[1:])
plt.xlim(0, 100)
plt.ylim(0, 500)
plt.xlabel('Iterations')
plt.ylabel('Residual of temperature')


def update_iter(n):
    steps.append(len(steps))
    print(steps)
    T_last = T.copy()

    T[0] = (T[1] + 2 * Ta) / 3
    T[1:-1] = 0.5 * (T[:-2] + T[2:])
    T[-1] = (T[-2] + 2 * Tb) / 3

    T_norm.append(np.abs(np.sum(T - T_last)))
    print(T_norm)
    residual_plot.set_data(steps[1:], T_norm[1:])

    return residual_plot,


# ani = animation.FuncAnimation(fig, update_iter, np.arange(1, 10), interval=100)
# plt.show()

# print(T)
