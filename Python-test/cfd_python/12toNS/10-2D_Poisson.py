from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm


# plot function
def plot_contour(x, y, variable):
    fig = plt.figure(figsize=(7, 7), dpi=100)
    ax = fig.gca()
    X, Y = np.meshgrid(x, y)
    plt.xlabel('x', fontsize=16)
    plt.ylabel('y', fontsize=16)
    contf = ax.contourf(X, Y, variable, extend='both', cmap='jet')
    cbar = plt.colorbar(contf, orientation='horizontal', shrink=0.5, pad=0.1, ticks=np.linspace(0, 1, 10))
    cbar.set_label('Velocity', fontsize=16)
    plt.xlim(0, 2)
    plt.ylim(0, 2)
    plt.title('Contour of Pressure field', fontsize=16)


def plot_3d(x, y, variable):
    fig = plt.figure(figsize=(11, 7), dpi=100)
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(x, y)
    surf = ax.plot_surface(X, Y, variable, rstride=1, cstride=1, cmap=cm.viridis,
                           linewidth=0, antialiased=False)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1)
    ax.view_init(30, 225)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')


# Iteration Function
def poisson_2D(x, y, p, nt):
    for i in range(nt):
        p[1:-1, 1:-1] = (dy**2*(p[1:-1, 2:] + p[1:-1, :-2]) + dx**2*(p[2:, 1:-1] + p[:-2, 1:-1])
                         - b[1:-1, 1:-1]*dx**2*dy**2) \
                        / (2*(dx**2+dy**2))
        p[:, 0] = p[:, -1] = p[0, :] = p[-1, :] = 0


# predefine
nx = 101
ny = 101
nt = 100
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)


# Grid
x = np.linspace(0, 2, nx)
y = np.linspace(0, 1, ny)
print(x, y)

# Initial conditions
p = np.zeros((ny, nx))
b = np.zeros((ny, nx))
print(p.shape)

b[int(ny/4), int(nx/4)] = 100
b[int(3*ny/4), int(3*nx/4)] = -100
print(p)

# Plot Initial Condition
# plot_contour(x, y, p)
# plot_3d(x, y, p)


# Iterations
poisson_2D(x, y, p, nt)
plot_contour(x, y, p)
plot_3d(x, y, p)

plt.show()