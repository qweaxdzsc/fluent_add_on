from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

# predefine
nx = 101
ny = 101
nt = 10

dx = 2 / (nx - 1)
dy = 2 / (ny - 1)
sigma = 0.001
nu = 0.01
dt = sigma * dx * dy / nu

# Grid
x = np.linspace(0, 2, nx)
y = np.linspace(0, 2, ny)

print(x, y)

# Initial conditions
u = np.ones((ny, nx))
v = np.ones((ny, nx))
print(u.shape, v.shape)

u[np.min(np.where((y >= 0.5))):np.max(np.where((y <= 1))), np.min(np.where((x >= 0.5))):np.max(np.where((x <= 1)))] = 2
v[np.min(np.where((y >= 0.5))):np.max(np.where((y <= 1))), np.min(np.where((x >= 0.5))):np.max(np.where((x <= 1)))] = 2
print(u, v)

# Plot Initial Condition
# the figure size parameter can be used to produce different sized images
fig = plt.figure()
ax = fig.gca(projection='3d')
X, Y = np.meshgrid(x, y)
surf = ax.plot_surface(X, Y, u, rstride=1, cstride=1, cmap=cm.viridis,
        linewidth=0, antialiased=False)

ax.set_xlim(0, 2)
ax.set_ylim(0, 2)
ax.set_zlim(1, 2.5)

ax.set_xlabel('$x$')
ax.set_ylabel('$y$')

# fig = plt.figure(figsize=(7, 7), dpi=100)
# # ax = fig.gca(projection='3d')
# ax = fig.gca()
# X, Y = np.meshgrid(x, y)
# # surf = ax.plot_surface(X, Y, u[:])
# # width = 10
# plt.xlabel('x', fontsize=16)
# plt.ylabel('y', fontsize=16)
# contf = ax.contourf(X, Y, u, extend='both', cmap='jet')
# cbar = plt.colorbar(contf, orientation='horizontal', shrink=0.5, pad=0.1, ticks=np.linspace(0, 3, 15))
# cbar.set_label('Velocity', fontsize=16)
# # plt.fill([], [], color='k', linestyle='solid', linewidth=2, zorder=2)
# # plt.axis('scaled', adjustable='box')
# plt.xlim(0, 2)
# plt.ylim(0, 2)
# plt.title('Contour of Velocity field', fontsize=16)


# Iterations
def burger_iter(nt):
    for i in range(nt):
        u[1:-1, 1:-1] = u[1:-1, 1:-1] - dt * u[1:-1, 1:-1] * (u[1:-1, 1:-1] - u[1:-1, :-2]) / dx \
                        - dt * v[1:-1, 1:-1] * (u[1:-1, 1:-1] - u[:-2, 1:-1]) / dy\
                        + nu * dt * (u[1:-1, 2:] + u[1:-1, :-2] - 2*u[1:-1, 1:-1]) / dx**2\
                        + nu * dt * (u[2:, 1:-1] + u[:-2, 1:-1] - 2*u[1:-1, 1:-1]) / dy**2
        u[:, 0] = u[:, -1] = u[0, :] = u[-1, :] = 1

        v[1:-1, 1:-1] = v[1:-1, 1:-1] - dt * u[1:-1, 1:-1] * (v[1:-1, 1:-1] - v[1:-1, :-2]) / dx \
                        - dt * v[1:-1, 1:-1] * (v[1:-1, 1:-1] - v[:-2, 1:-1]) / dy \
                        + nu * dt * (v[1:-1, 2:] + v[1:-1, :-2] - 2 * v[1:-1, 1:-1]) / dx ** 2 \
                        + nu * dt * (v[2:, 1:-1] + v[:-2, 1:-1] - 2 * v[1:-1, 1:-1]) / dy ** 2
        v[:, 0] = v[:, -1] = v[0, :] = v[-1, :] = 1

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
    cbar = plt.colorbar(contf, orientation='horizontal', shrink=0.5, pad=0.1, ticks=np.linspace(0, 3, 10))
    cbar.set_label('Velocity', fontsize=16)
    # plt.fill([], [], color='k', linestyle='solid', linewidth=2, zorder=2)
    # plt.axis('scaled', adjustable='box')
    plt.xlim(0, 2)
    plt.ylim(0, 2)
    plt.title('Contour of Velocity field @ %s' % (nt*dt), fontsize=16)

    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # surf = ax.plot_surface(X, Y, u[:], rstride=1, cstride=1, cmap=cm.viridis,
    #                        linewidth=0, antialiased=True)
    # ax.set_zlim(1, 2.5)
    # ax.set_xlabel('$x$')
    # ax.set_ylabel('$y$')


burger_iter(6000)
plt.show()
