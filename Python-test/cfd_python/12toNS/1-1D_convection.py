import numpy as np
from matplotlib import pyplot as plt


# -------------predefine-------------
grid_nx = 21
grid_dx = 0.1
nt = 12
dt = 0.05
c = 1
u0 = 1

# ------grid---------
x = np.linspace(0, grid_dx*(grid_nx-1), grid_nx, endpoint=True)
print('grid list:', x)

# ------initial condition-------
u = np.ones(grid_nx)


a = 88/(9e-7) - 9.7777777e+7
print(a)