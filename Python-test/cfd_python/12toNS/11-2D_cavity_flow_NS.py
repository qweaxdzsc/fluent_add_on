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


def plot_vector(x, y, u, v, variable):
    X, Y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(11, 7), dpi=100)
    # plotting the pressure field as a contour
    plt.contourf(X, Y, variable, alpha=0.5, cmap=cm.viridis)
    plt.colorbar()
    # plotting the pressure field outlines
    plt.contour(X, Y, p, cmap=cm.viridis)
    # plotting velocity field
    plt.quiver(X[::2, ::2], Y[::2, ::2], u[::2, ::2], v[::2, ::2])
    plt.xlabel('X')
    plt.ylabel('Y')


def plot_streamline(x, y, u, v, p):
    X, Y = np.meshgrid(x, y)
    fig = plt.figure(figsize=(11, 7), dpi=100)
    plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)
    plt.colorbar()
    plt.contour(X, Y, p, cmap=cm.viridis)
    plt.streamplot(X, Y, u, v)
    plt.xlabel('X')
    plt.ylabel('Y')


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


def poisson_b(b, rho, dt, u, v, dx, dy):
    # b[1:-1, 1:-1] = rho * ((u[1:-1, 2:] - u[1:-1, :-2])/(2*dx) + (v[2:, 1:-1] - v[:-2, 1:-1])/(2*dy))/dt \
    #     - ((u[1:-1, 2:] - u[1:-1, :-2]) / (2 * dx))**2 \
    #     - 2 * ((u[2:, 1:-1] - u[:-2, 1:-1])/(2 * dy)) * ((v[1:-1, 2:] - v[1:-1, :-2])/(2 * dx)) \
    #     - ((v[2:, 1:-1] - v[:-2, 1:-1])/(2 * dy)) * ((v[1:-1, 2:] - v[1:-1, :-2])/(2 * dy))

    b[1:-1, 1:-1] = (rho * (1 / dt *
                            ((u[1:-1, 2:] - u[1:-1, 0:-2]) /
                             (2 * dx) + (v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy)) -
                            ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx)) ** 2 -
                            2 * ((u[2:, 1:-1] - u[0:-2, 1:-1]) / (2 * dy) *
                                 (v[1:-1, 2:] - v[1:-1, 0:-2]) / (2 * dx)) -
                            ((v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy)) ** 2))
    return b


# Iteration Function
def pressure_poission(p, dx, dy, b, nit):
    for i in range(nit):
        # p[1:-1, 1:-1] = (dy**2*(p[1:-1, 2:] + p[1:-1, :-2]) + dx**2*(p[2:, 1:-1] + p[:-2, 1:-1])
        #                  - b[1:-1, 1:-1]*dx**2*dy**2) \
        #                 / (2*(dx**2 + dy**2)) - dx**2*dy**2 * b[1:-1, 1:-1] / (2*(dx**2 + dy**2))
        p[1:-1, 1:-1] = (((p[1:-1, 2:] + p[1:-1, 0:-2]) * dy ** 2 +
                          (p[2:, 1:-1] + p[0:-2, 1:-1]) * dx ** 2) /
                         (2 * (dx ** 2 + dy ** 2)) -
                         dx ** 2 * dy ** 2 / (2 * (dx ** 2 + dy ** 2)) *
                         b[1:-1, 1:-1])
        p[:, -1] = p[:, -2]
        p[:, 0] = p[:, 1]
        p[0, :] = p[1, :]
        p[-1, :] = 0

    return p


def cavity_flow(nt, u, v, dt, nit, dx, dy, p, b, rho, nu):
    n = 0
    for i in range(nt):
        n += 1
        print('step', n)
        b = poisson_b(b, rho, dt, u, v, dx, dy)
        p = pressure_poission(p, dx, dy, b, nit)

        u[1:-1, 1:-1] = u[1:-1, 1:-1] - u[1:-1, 1:-1] * dt * (u[1:-1, 1:-1] - u[1:-1, :-2]) / dx \
                        - v[1:-1, 1:-1] * dt * (u[1:-1, 1:-1] - u[:-2, 1:-1]) / dy \
                        - dt * (p[1:-1, 2:] - p[1:-1, :-2]) / (2 * rho * dx) \
                        + nu * (dt * (u[1:-1, 2:] - 2 * u[1:-1, 1:-1] + u[1:-1, :-2]) / dx ** 2
                                + dt * (u[2:, 1:-1] - 2 * u[1:-1, 1:-1] + u[:-2, 1:-1]) / dy ** 2)

        v[1:-1, 1:-1] = v[1:-1, 1:-1] - u[1:-1, 1:-1] * dt * (v[1:-1, 1:-1] - v[1:-1, :-2]) / dx \
                        - v[1:-1, 1:-1] * dt * (v[1:-1, 1:-1] - v[:-2, 1:-1]) / dy \
                        - dt * (p[2:, 1:-1] - p[0:-2, 1:-1]) / (2 * rho * dy) \
                        + nu * (dt * (v[1:-1, 2:] - 2 * v[1:-1, 1:-1] + v[1:-1, :-2]) / dx ** 2
                                + dt * (v[2:, 1:-1] - 2 * v[1:-1, 1:-1] + v[:-2, 1:-1]) / dy ** 2)

        u[0, :] = 0
        u[-1, :] = 1
        u[:, 0] = 0
        u[:, -1] = 0
        v[0, :] = 0
        v[-1, :] = 0
        v[:, 0] = 0
        v[:, -1] = 0

    return u, v, p


# predefine
nx = 41
ny = 41
nt = 100
nit = 50
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)

rho = 1
nu = 0.1
dt = 0.001

# Grid
x = np.linspace(0, 2, nx)
y = np.linspace(0, 2, ny)
print(x, y)

# Initial conditions
u = np.zeros((ny, nx))
v = np.zeros((ny, nx))
p = np.zeros((ny, nx))
b = np.zeros((ny, nx))
print(p.shape)

# Plot Initial Condition
# plot_vector(x, y, p)
# plot_contour(x, y, v)
# plot_contour(x, y, p)
# plot_3d(x, y, p)
nt = 2500
u, v, p = cavity_flow(nt, u, v, dt, nit, dx, dy, p, b, rho, nu)


# Iterations
# pressure_poission(x, y, p, nt)
plot_contour(x, y, p)
# plot_3d(x, y, p)
plot_vector(x, y, u, v, p)
plot_streamline(x, y, u, v, p)

plt.show()