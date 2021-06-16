import numpy as np            # we're importing numpy
from matplotlib import pyplot as plt   # and our 2D plotting library

# predefine
nx = 101
dx = 5 / (nx - 1)
nt = 2000
sigma = 0.2
nu = 0.3
dt = sigma * dx**2 / nu


# grid define
x = np.linspace(0, (nx - 1)*dx, nx, endpoint=True)

# initial condition
u = np.ones(nx)
u[np.where((x >= 0.5) & (x <= 1))] = 2

print(u)

# Iterations
for i in range(nt):
    u[1:-1] = u[1:-1] + nu * u[1:-1] * dt * (u[2:] + u[:-2] - 2 * u[1:-1]) / dx**2

print(u)
plt.plot(x, u)
plt.show()


