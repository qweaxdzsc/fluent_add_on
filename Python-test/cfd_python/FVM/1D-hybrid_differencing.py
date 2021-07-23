

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
nx = 25
dx = L/nx

D = k/dx
print(D)
Pe = F / D
print(Pe)

x = np.zeros(nx + 2)
x[1:-1] = np.linspace(0 + 0.5 * dx, L - 0.5 * dx, nx)
x[-1] = L
print('mesh points', x)


# Initial condition


# # Boundary condition
# T[0] = Ta
# T[-1] = Tb
# print('', T)


# Solver
# analytical solution
xx = np.linspace(0, L, 50, endpoint=True)
exact_solution = np.zeros(50)
for i in range(50):
    exact_solution[i] = (math.exp(rho*u*xx[i] / k) -1) / (math.exp(rho*u*L / k) -1) * (phi_b - phi_a) + phi_a


# construct A matrix
def matrix_A(nx, D, F):
    A = np.zeros((nx, nx))
    # boundary A
    A[0][1] = -max(-F, 2 * D - 0.5 * F, 0)
    sp = -(F + 2 * D)
    A[0][0] = -A[0][1] - sp

    # boundary B
    A[-1][-2] = -max(F, D + 0.5 * F, 0)
    if Pe >= 2:
        sp = - 2 * D
    else:
        sp = F - 2 * D
    A[-1][-1] = -A[-1][-2] - sp

    for i in range(len(A[1:-1, :])):
        a1 = -max(F, D + F / 2, 0)
        a3 = -max(-F, D - F / 2, 0)
        a2 = -(a1 + a3)
        A[1 + i, i:i + 3] = [a1, a2, a3]

    print(A)
    return A


def matrix_b(nx, D, F):
    b = np.zeros(nx)
    b[0] = (2 * D + F) * phi_a
    if Pe >= 2:
        b[-1] = 2 * D * phi_b
    else:
        b[-1] = (2 * D - F) * phi_b

    print(b)
    return b


A = matrix_A(nx, D, F)
b = matrix_b(nx, D, F)
new_phi = np.linalg.solve(A, b)
new_phi = np.insert(new_phi, 0, phi_a)
new_phi = np.append(new_phi, phi_b)
print(new_phi)

fig = plt.figure()
plt.plot(xx, exact_solution)
plt.plot(x, new_phi, 'bs')

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
