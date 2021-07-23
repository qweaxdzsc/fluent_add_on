import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.lines import Line2D


# predefine
Ta = 100
Tb = 500
k = 1000
L = 0.5
a = 1

# define mesh
nx = 5
dx = L/nx
x = np.zeros(nx+2)
x[1:-1] = np.linspace(0+0.5*dx, L-0.5*dx, nx)
print('mesh points', x)


# Initial condition
T = np.zeros(nx)

# # Boundary condition
# T[0] = Ta
# T[-1] = Tb
# print('', T)

# Solver
# construct A matrix


def matrix_A(nx, dx, k, a):
    A = np.zeros((nx, nx))
    print(A)
    A[0, :2] = [3 * k * a / dx, -k * a / dx]
    A[-1, -2:] = [-k * a / dx, 3 * k * a / dx]

    for i in range(len(A[1:-1, :])):
        a1 = - k * a / dx
        a2 = 2 * k * a / dx
        a3 = - k * a / dx
        A[1 + i, i:i+3] = [a1, a2, a3]

    print(A)
    return A


def matrix_b(nx, k, a, dx, Ta, Tb):
    b = np.zeros(nx)
    b[0] = 2*k*a*Ta/dx
    b[-1] = 2*k*a*Tb/dx

    print(b)
    return b


# A = matrix_A(nx, dx, k, a)
# b = matrix_b(nx, k, a, dx, Ta, Tb)
# new_T = np.linalg.solve(A, b)


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


ani = animation.FuncAnimation(fig, update_iter, np.arange(1, 10), interval=100)
plt.show()

print(T)
