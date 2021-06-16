import numpy as np            # we're importing numpy
from matplotlib import pyplot as plt   # and our 2D plotting library

# predefine
nx = 101
dx = 2 / (nx - 1)
nt = 200
dt = 0.005


# grid define
x = np.linspace(0, (nx - 1)*dx, nx, endpoint=True)

# initial condition
u = np.ones(nx)
u[np.where((x >= 0.5) & (x <= 1))] = 2

print(u)

# Iterations
for i in range(nt):
    u[1:] = u[1:] - u[1:] * dt * (u[1:] - u[:-1]) / dx

print(u)
plt.plot(x, u)
plt.show()


