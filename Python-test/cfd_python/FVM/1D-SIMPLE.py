import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.lines import Line2D
import math

# predefine
L = 2
rho = 1
A1 = 0.5
A2 = 0.1
P0 = 10

P_out = 0

mass_flow = 1
factor_p = 0.01
factor_u = 0.01
iterations_max = 20000
residual_criteria = 1e-5
# define mesh
nx = 50
dx = L / (nx - 1)

xp = np.linspace(0, L, nx)
xv = np.zeros(nx - 1)
xv = np.linspace(0 + 0.5 * dx, L - 0.5 * dx, nx - 1)
print('mesh points', xp, xv)

# coefficients
au = np.zeros(nx - 1)
dd = np.zeros(nx - 1)
bb = np.zeros(nx)
Aap = np.zeros((nx, nx))
Bap = np.zeros(nx)

# Initial condition
Ap = np.linspace(A1, A2, nx)
Av = np.linspace(A1 - (A1 - A2) / (nx - 1) / 2, A2 + (A1 - A2) / (nx - 1) / 2, nx - 1)

P = np.linspace(P0, 0, nx)
mass_flow = np.ones(nx - 1)
U = mass_flow / rho / Av
a = None

print('Area of pressure points with change of x: ', Ap)
print('Area of velocity points with change of x: ', Av)
print('initial U:', U)
print('initial P:', P)

uu_residual = np.zeros(nx - 1)  # residual of velcity

# Iterations
# SIMPLE Algorithm


def update_iter(n):
    steps.append(n)
    # == STEP 1 : solving momentum equations ==
    # == inlet(Left Boundary) ==
    global U, P, mass_flow
    Un = U.copy()
    Pn = P.copy()
    mass_flow_old = mass_flow.copy()

    i = 0
    ua = Un[0] * Av[0] / Ap[0]
    Fe = rho * Ap[i + 1] * (Un[i] + Un[i + 1]) / 2
    Fw = rho * Ap[i] * ua
    ae = 0
    aw = 0
    ap = Fe + 0.5 * Fw * (Av[0] / Ap[0]) ** 2
    Su = (P0 - P[i + 1]) * Av[i] + Fw * (Av[0] / Ap[0]) * Un[0]
    U[i] = (aw * ua + ae * U[i] + Su) / ap
    dd[i] = Av[i] / ap

    # == internal nodes ==
    for i in range(1, nx - 2):
        Fe = rho * Ap[i + 1] * (Un[i + 1] + Un[i]) / 2
        Fw = rho * Ap[i] * (Un[i] + Un[i - 1]) / 2
        ae = 0
        aw = Fw
        ap = ae + aw + Fe - Fw
        Su = (P[i] - P[i + 1]) * Av[i]
        # print(Fe)
        # print(aw)
        # print(ap)
        # print(Su)
        # print('============')
        U[i] = (aw * U[i - 1] + ae * U[i] + Su) / ap
        dd[i] = Av[i] / ap

    # == outlet nodes ==
    i = -1
    Fe = rho * Un[i] * Av[i]
    Fw = rho * Ap[i - 1] * (Un[i] + Un[i - 1]) / 2
    ae = 0
    aw = Fw
    ap = ae + aw + Fe - Fw
    Su = (P[i - 1] - P[i]) * Av[i]
    # print(Fe)
    # print(aw)
    # print(ap)
    # print(Su)
    U[i] = (aw * U[i - 1] + ae * U[i] + Su) / ap
    dd[i] = Av[i] / ap

    # print('U* :', U)
    # == STEP 2: solving pressure correction equation ==
    for i in range(1, nx - 1):
        Aap[i, i - 1] = - rho * dd[i - 1] * Av[i - 1]
        Aap[i, i + 1] = - rho * dd[i] * Av[i]
        Aap[i, i] = -(Aap[i, i - 1] + Aap[i, i + 1])
        Bap[i] = rho * Av[i - 1] * U[i - 1] - rho * Av[i] * U[i]

    Aap[0, 0] = Aap[-1, -1] = 1
    # print('Aap is:', Aap)
    # print('Bap is: ', Bap)
    P_correction = np.linalg.solve(Aap, Bap)
    # print('P_correction: ', P_correction)

    # == STEP 3: correct pressure and velocity ==
    P = P + factor_p * P_correction
    U = U + factor_u * dd * (P_correction[:-1] - P_correction[1:])
    P[0] = P0 - 0.5 * rho * U[0] ** 2 * (Av[0] / Ap[0]) ** 2
    mass_flow = rho * Av * U

    uu_residual = np.abs(U - Un)
    P_residual = np.abs(P - Pn)
    mass_residual = np.abs(mass_flow - mass_flow_old)

    u_norm.append(uu_residual.sum())
    residual_plot.set_data(steps[1:], u_norm[1:])
    plt.xlim(0, steps[-1] + 50)
    if u_norm[-1] > 1:
        plt.ylim(0, u_norm[1] + 1)
    elif u_norm[-1] > 0.1:
        plt.ylim(0, 0.1)
    elif u_norm[-1] > 0.01:
        plt.ylim(0, 0.05)
    elif u_norm[-1] > 0.001:
        plt.ylim(0, 0.005)
    else:
        plt.ylim(0, 0.0005)

    print('Iteration %s, U residual %.6f' % (n + 1, uu_residual.sum()))
    if uu_residual.sum() <= residual_criteria:
        print('result is converged. \n'
              'The velocity residual is: \t%s \n'
              'P residual is: \t%s \n'
              'mass flow residual is: \t%s' % (uu_residual.sum(), P_residual.sum(), mass_residual.sum()))
        return residual_plot,
    if uu_residual.sum() > 1e+4:
        print('result is divergence, please lower the under-relaxation factor or check the setting')
        return residual_plot,
    return residual_plot,


steps = [0]
u_norm = [1]

fig = plt.figure()

residual_plot, = plt.plot(steps[1:], u_norm[1:], 'k')
residual_plot.set_data(steps[1:], u_norm[1:])

plt.xlabel('Iterations')
plt.ylabel('Residual of velocity')

ani = animation.FuncAnimation(fig, update_iter, np.arange(1, iterations_max), interval=0)

plt.show()
print('============================================')
print('dd: ', dd)
print('U: ', U)
print('P: ', P)
print('mass_flow: ', mass_flow)
print('============================================')

# == exact solution ==
nodes_exact = 50
area_exact = np.linspace(A1, A2, nodes_exact, endpoint=True)
xe_grid = np.linspace(0, L, nodes_exact, endpoint=True)
pp_exact = np.zeros(nodes_exact)
uu_exact = np.zeros(nodes_exact)
for i in range(nodes_exact):
    pp_exact[i] = P0 - 0.5 * 0.44721 ** 2 / rho / area_exact[i] ** 2
    uu_exact[i] = math.sqrt((P0 - pp_exact[i]) * 2 / rho)

plt.xlabel('Distance (m)')
plt.ylabel('Velocity (m/s)')
plt.plot(xv, U, 'bs--', label='Numerical')
plt.plot(xe_grid, uu_exact, 'k', label='Exact')
plt.title('velocity')
plt.legend()

plt.figure(2)
plt.xlabel('Distance (m)')
plt.ylabel('Pressure (Pa)')
plt.plot(xp, P, 'bs--', label='Numerical')
plt.plot(xe_grid, pp_exact, 'k', label='Exact')
plt.title('Pressure')
plt.legend()

plt.show()
