from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

# predefine
nx = 401
ny = 401
nt = 250

dx = 2 / (nx - 1)
dy = 2 / (ny - 1)
sigma = 0.2
c = 1
dt = sigma * dx / c

# Grid
x = np.linspace(0, 2, nx)
y = np.linspace(0, 2, ny)

print(x, y)

# Initial conditions
u = np.ones((ny, nx))
print(u.shape)

u[np.min(np.where((y >= 0.5))):np.max(np.where((y <= 1))), np.min(np.where((x >= 0.5))):np.max(np.where((x <= 1)))] = 2
print(u)

# Plot Initial Condition
# the figure size parameter can be used to produce different sized images
fig = plt.figure(figsize=(7, 7), dpi=100)
# ax = fig.gca(projection='3d')
ax = fig.gca()
X, Y = np.meshgrid(x, y)
# surf = ax.plot_surface(X, Y, u[:])
# width = 10
plt.xlabel('x', fontsize=16)
plt.ylabel('y', fontsize=16)
contf = ax.contourf(X, Y, u, extend='both', cmap='jet')
cbar = plt.colorbar(contf, orientation='horizontal', shrink=0.5, pad=0.1, ticks=np.linspace(0, 3, 15))
cbar.set_label('Velocity', fontsize=16)
# plt.fill([], [], color='k', linestyle='solid', linewidth=2, zorder=2)
# plt.axis('scaled', adjustable='box')
plt.xlim(0, 2)
plt.ylim(0, 2)
plt.title('Contour of Velocity field', fontsize=16)

# Iterations
for i in range(nt):
    u[1:, 1:] = u[1:, 1:] - c * dt * (u[1:, 1:] - u[1:, :-1]) / dx - c * dt * (u[1:, 1:] - u[:-1, 1:]) / dy
    u[:, 0] = u[:, -1] = u[0, :] = u[-1, :] = 1


fig = plt.figure(figsize=(7, 7), dpi=100)
# ax = fig.gca(projection='3d')
# surf2 = ax.plot_surface(X, Y, u[:], cmap=cm.viridis)

ax = fig.gca()
X, Y = np.meshgrid(x, y)
# surf = ax.plot_surface(X, Y, u[:])
# width = 10
plt.xlabel('x', fontsize=16)
plt.ylabel('y', fontsize=16)
contf = ax.contourf(X, Y, u, extend='both', cmap='jet')
cbar = plt.colorbar(contf, orientation='horizontal', shrink=0.5, pad=0.1, ticks=np.linspace(0, 3, 15))
cbar.set_label('Velocity', fontsize=16)
# plt.fill([], [], color='k', linestyle='solid', linewidth=2, zorder=2)
# plt.axis('scaled', adjustable='box')
plt.xlim(0, 2)
plt.ylim(0, 2)
plt.title('Contour of Velocity field', fontsize=16)

plt.show()
