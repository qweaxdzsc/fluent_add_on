import sympy
import numpy
from sympy.utilities.lambdify import lambdify
from sympy import init_printing
from matplotlib import pyplot as plt   # and our 2D plotting library


init_printing(use_latex=True)

# form function for u
x, nu, t = sympy.symbols('x nu t')
phi = (sympy.exp(-(x - 4 * t)**2 / (4 * nu * (t + 1))) +
       sympy.exp(-(x - 4 * t - 2 * sympy.pi)**2 / (4 * nu * (t + 1))))

phiprime = phi.diff(x)
print(phiprime)

u = -2 * nu * (phiprime / phi) + 4
print(u)

ufunc = lambdify((t, x, nu), u)

# predefine
nx = 1501
nt = 100
dx = 2 * numpy.pi / (nx - 1)
nu = .07
dt = 0.3 *dx * nu

# grid define
x = numpy.linspace(0, 2 * numpy.pi, nx)
un = numpy.empty(nx)
t = 0

u = numpy.asarray([ufunc(t, x0, nu) for x0 in x])
print(u)

# plt.figure(figsize=(11, 7), dpi=100)
# plt.plot(x, u, marker='o', lw=2)
# plt.xlim([0, 2 * numpy.pi])
# plt.ylim([0, 10])
# plt.show()


for i in range(nt):
    u[0] = u[0] - u[0] * dt * (u[0] - u[-2])/dx + nu * dt * (u[1] + u[-2] - 2 * u[0]) / dx ** 2
    u[1:-1] = u[1:-1] - u[1:-1] * dt * (u[1:-1] - u[:-2])/dx + nu * dt * (u[2:] + u[:-2] - 2 * u[1:-1]) / dx ** 2
    u[-1] = u[0]

u_analytical = numpy.asarray([ufunc(nt * dt, xi, nu) for xi in x])

plt.figure(figsize=(11, 7), dpi=100)
plt.plot(x, u, marker='o', lw=2, label='Computational')
plt.plot(x, u_analytical, label='Analytical')
plt.xlim([0, 2 * numpy.pi])
plt.ylim([0, 10])
plt.legend()
plt.show()
