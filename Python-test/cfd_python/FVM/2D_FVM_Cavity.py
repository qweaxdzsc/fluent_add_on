import numpy as np
import sys
from matplotlib import pyplot as plt
from numba import jit
from matplotlib import animation
from matplotlib.lines import Line2D
import math
import time

# ======Predefined Coefficient=========
nx = 50
ny = 50
mu = 0.01  # dynamic viscosity
Lx = 1
Ly = 1
dx = Lx / nx
dy = Ly / ny
n_steps = 600
rho = 1

factor_v = 0.1
factor_p = 0.05
# =========Grid define============
xc = np.zeros(nx + 2)
yc = np.zeros(nx + 2)
xc[1:-1] = np.linspace(dx / 2, Lx - dx / 2, nx)
yc[1:-1] = np.linspace(dy / 2, Ly - dy / 2, ny)
xc[-1] = Lx
yc[-1] = Ly
print('Cell center coordinates in X-direction: %s' % xc)
print('Cell center coordinates in Y-direction: %s' % yc)
xu = np.linspace(0, Lx - dx, nx)
yv = np.linspace(0, Ly - dy, ny)
print('u-velocity coordinates in X-direction: %s' % xu)
print('v-velocity coordinates in Y-direction: %s' % yv)

XC, YC = np.meshgrid(xc, yc)
XU, YU = np.meshgrid(xu, yc)
XV, YV = np.meshgrid(xc, yv)

# ==========Initial Setting==============
# velocity in boundary
Ut = 5.0
Ub = 0.0
Vl = 0.0
Vr = 0.0
print('Reynolds Number:', Ut * Lx * rho / mu)
# time
dt = min(0.25 * dx * dx / mu, 4.0 * mu / Ut / Ut)
print('dt=', dt)

# initialize velocities - we stagger everything in the negative direction
u = np.zeros([ny + 2, nx + 2])  # include 2 ghost cells
v = np.zeros([ny + 2, nx + 2])  # include 2 ghost cells

ut = np.zeros_like(u)
vt = np.zeros_like(v)

# initialize pressure
p = np.zeros([ny + 2, nx + 2])  # include 2 ghost cells

# intermediate coefficient
ddu = np.zeros_like(u)
ddv = np.zeros_like(v)


p_correction = np.zeros_like(p)
# p_correction[0, :] = 1
# p_correction[-1, :] = 1
# p_correction[:, 0] = 1
# p_correction[:, -1] = 1

# a bunch of lists for animation purposes
# usol = list()
# vsol = list()
# psol = list()
# usol.append(u)
# vsol.append(v)
# psol.append(p)


# ============== Solver =======================
# @jit(nopython=True)
def iteration(n_steps, u, v, p):
    for n in range(n_steps):
        # ========= Step 1 : define boundary condition =========
        # left wall
        u[1: -1, 1] = 0
        # right wall
        u[1: -1, -1] = 0
        # top wall
        u[-1, 1:] = 2 * Ut - u[-2, 1:]
        # bottom wall
        u[0, 1:] = 2 * Ub - u[1, 1:]

        # left wall
        v[1:, 0] = 2 * Vl - v[1:, 1]
        # right wall
        v[1:, -1] = 2 * Vr - v[1:, -2]
        # top wall
        v[-1, 1: -1] = 0
        # bottom wall
        v[1, 1: -1] = 0

        Un = u.copy()
        Vn = v.copy()
        Pn = p.copy()
        # ========= Step 2 : Discrete Momentum Equations ==================
        # ==== Discrete u-momentum equation, only for interior nodes ====
        # range control
        ia = 2
        ib = nx + 1
        ja = 1
        jb = ny + 1
        # reshape F, D for U-control volume
        De = np.ones([ny, nx - 1])
        Dw = np.ones([ny, nx - 1])
        Dn = np.ones([ny, nx - 1])
        Ds = np.ones([ny, nx - 1])
        # Convection coefficient rho * u * Area
        Fe = 0.5 * rho * dy * (Un[ja:jb, ia + 1: ib + 1] + Un[ja:jb, ia:ib])
        Fw = 0.5 * rho * dy * (Un[ja:jb, ia - 1: ib - 1] + Un[ja:jb, ia:ib])
        Fn = 0.5 * rho * dx * (Vn[ja + 1:jb + 1, ia:ib] + Vn[ja + 1:jb + 1, ia - 1: ib - 1])
        Fs = 0.5 * rho * dx * (Vn[ja:jb, ia:ib] + Vn[ja:jb, ia - 1: ib - 1])

        # Diffusion coefficient mu * Area / distance
        De *= mu / dx * dy
        Dw *= mu / dx * dy
        Dn *= 4 * mu / (4 * dy) * dx
        Ds *= 4 * mu / (4 * dy) * dx
        # U* coefficient
        Ae = De - 0.5 * Fe
        Aw = Dw + 0.5 * Fw
        An = Dn - 0.5 * Fn
        As = Ds + 0.5 * Fs
        Ap = Ae + Aw + An + As + Fe - Fw + Fn - Fs
        # Source term, Pressure gradient
        Su = (p[ja:jb, ia - 1:ib - 1] - p[ja:jb, ia:ib]) * dy
        u[ja:jb, ia:ib] = (Aw * Un[ja:jb, ia - 1:ib - 1] + Ae * Un[ja:jb, ia + 1:ib + 1]
                           + An * Un[ja + 1:jb + 1, ia:ib] + As * Un[ja - 1:jb - 1, ia:ib] + Su) / Ap
        ddu[ja:jb, ia:ib] = dy / Ap

        # ==== Discrete v-momentum equation, only for interior nodes ====
        # range control
        ia = 1
        ib = nx + 1
        ja = 2
        jb = ny + 1
        # reshape D for V-control volume
        De = np.ones([ny - 1, nx])
        Dw = np.ones([ny - 1, nx])
        Dn = np.ones([ny - 1, nx])
        Ds = np.ones([ny - 1, nx])
        # Convection coefficient rho * u * Area
        Fe = 0.5 * rho * dy * (Un[ja:jb, ia + 1: ib + 1] + Un[ja - 1:jb - 1, ia + 1:ib + 1])
        Fw = 0.5 * rho * dy * (Un[ja:jb, ia: ib] + Un[ja - 1:jb - 1, ia:ib])
        Fn = 0.5 * rho * dx * (Vn[ja:jb, ia:ib] + Vn[ja + 1:jb + 1, ia: ib])
        Fs = 0.5 * rho * dx * (Vn[ja - 1:jb - 1, ia:ib] + Vn[ja:jb, ia: ib])

        # Diffusion coefficient mu * Area / distance
        De *= 4 * mu / (4 * dx) * dy
        Dw *= 4 * mu / (4 * dx) * dy
        Dn *= mu / dy * dx
        Ds *= mu / dy * dx
        # U* coefficient
        Ae = De - 0.5 * Fe
        Aw = Dw + 0.5 * Fw
        An = Dn - 0.5 * Fn
        As = Ds + 0.5 * Fs
        Ap = Ae + Aw + An + As + Fe - Fw + Fn - Fs
        # Source term, Pressure gradient
        Su = (p[ja - 1:jb - 1, ia:ib] - p[ja:jb, ia:ib]) * dx
        v[ja:jb, ia:ib] = (Aw * Vn[ja:jb, ia - 1:ib - 1] + Ae * Vn[ja:jb, ia + 1:ib + 1]
                           + An * Vn[ja + 1:jb + 1, ia:ib] + As * Vn[ja - 1:jb - 1, ia:ib] + Su) / Ap
        ddv[ja:jb, ia:ib] = dx / Ap
        # print(u, v)
        # ==== STEP 3: solving pressure correction equation ====
        # range control
        ia = 1
        ib = nx + 1
        ja = 1
        jb = ny + 1
        # create iterative method for solve
        print('=========P calculation========')
        p_norm = 1
        # for i in range(500):
        #     last_correction = p_correction.copy()
        #     print(np.around(last_correction, 2))
        #     Ae = rho * ddu[ja:jb, ia + 1: ib + 1] * dy
        #     Aw = rho * ddu[ja:jb, ia: ib] * dy
        #     An = rho * ddv[ja + 1:jb + 1, ia: ib] * dx
        #     As = rho * ddv[ja:jb, ia: ib] * dx
        #     Ap = Ae + Aw + An + As
        #     b = rho * dy * u[ja:jb, ia: ib] - rho * dy * u[ja:jb, ia + 1: ib + 1] + \
        #         rho * dx * v[ja:jb, ia: ib] - rho * dx * v[ja + 1:jb + 1, ia: ib]
        #     p_correction[ja:jb, ia: ib] = p_correction[ja:jb, ia: ib] + 0.8 * ((Ae * p_correction[ja:jb, ia + 1: ib + 1] +
        #                                    Aw * p_correction[ja:jb, ia - 1: ib - 1] +
        #                                    An * p_correction[ja + 1:jb + 1, ia: ib] +
        #                                    As * p_correction[ja - 1:jb - 1, ia: ib] + b) / Ap - p_correction[ja:jb, ia: ib])
        #     print(np.around(p_correction, 2))
        #     p_norm = np.sum(np.abs(p_correction - last_correction))
        #     print('residual of p_correction: ', p_norm)
        if n < 50:
            p_criteria = 1e-2
        else:
            p_criteria = 1e-4
        while p_norm > p_criteria:
            last_correction = p_correction.copy()
            # print(last_correction)
            Ae = rho * ddu[ja:jb, ia + 1: ib + 1] * dy
            Aw = rho * ddu[ja:jb, ia: ib] * dy
            An = rho * ddv[ja + 1:jb + 1, ia: ib] * dx
            As = rho * ddv[ja:jb, ia: ib] * dx
            Ap = Ae + Aw + An + As
            b = rho * dy * u[ja:jb, ia: ib] - rho * dy * u[ja:jb, ia + 1: ib + 1] + \
                rho * dx * v[ja:jb, ia: ib] - rho * dx * v[ja + 1:jb + 1, ia: ib]
            # add relaxation factor
            p_correction[ja:jb, ia: ib] = p_correction[ja:jb, ia: ib] + 0.7 * ((Ae * p_correction[ja:jb, ia + 1: ib + 1] +
                                           Aw * p_correction[ja:jb, ia - 1: ib - 1] +
                                           An * p_correction[ja + 1:jb + 1, ia: ib] +
                                           As * p_correction[ja - 1:jb - 1, ia: ib] + b) / Ap - p_correction[ja:jb, ia: ib])
            # print(p_correction)
            p_norm = np.sum(np.abs(p_correction - last_correction))
            if p_norm > 100:
                print("p_correction is divergence")
                sys.exit()
            # print('use matrix iteration, P_correction: ', p_correction)
        print('residual of p_correction: ', p_norm)
        # print('p_correction: ', np.around(p_correction, 2))
        print('===========End of P calculation============')

        # == STEP 4: correct pressure and velocity ==
        p = p + factor_p * p_correction
        # correct boundary of p
        p[:, 0] = p[:, 1]
        p[:, -1] = p[:, -2]
        p[0, :] = p[1, :]
        p[-1, :] = p[-2, :]
        # correct momentum
        # print(u[2:nx + 1, 1:ny + 1])
        # print(ddu[2:nx + 1, 1:ny + 1])
        u[1:ny + 1, 2:nx + 1] = u[1:ny + 1, 2:nx + 1] + \
                                ddu[1:ny + 1, 2:nx + 1] * \
                                (p_correction[1:ny + 1, 1:nx] - p_correction[1:ny + 1, 2:nx + 1])
        v[2:ny + 1, 1:nx + 1] = v[2:ny + 1, 1:nx + 1] + \
                                ddv[2:ny + 1, 1:nx + 1] * \
                                (p_correction[1:ny, 1:nx + 1] - p_correction[2:ny + 1, 1:nx + 1])
        # relaxation
        u[1:ny+1, 2: nx+1] = (1 - factor_v) * Un[1:ny+1, 2: nx+1] + factor_v * u[1:ny+1, 2: nx+1]
        v[2:ny+1, 1:nx+1] = (1 - factor_v) * Vn[2:ny+1, 1:nx+1] + factor_v * v[2:ny+1, 1:nx+1]

        mass_flow = rho * np.sqrt(u**2 + v**2)

        uu_residual = np.sum(np.abs(u - Un))
        P_residual = np.sum(np.abs(p - Pn))
        print('=============')
        print(uu_residual)
        print('=============')
        print(P_residual)
        # mass_residual = np.abs(mass_flow - mass_flow_old)
        # div_u = (u[:ny, 2:nx + 1] - u[1:ny + 1, 2:nx + 1])/dx
        # div_v = (v[2:ny + 1, :nx] - v[2:ny + 1, 1:nx + 1])/dy
        # print(np.sum(div_u))
        # print(np.sum(div_v))
    return u, v, p


u, v, p = iteration(n_steps, u, v, p)
print('=============')
print('u', np.around(u, 2))
print('=============')
print('v', np.around(v, 2))
print('=============')
print('p', np.around(p, 2))
# print('=============')
# print(np.around(mass_flow, 2))
# print('=============')
# print(np.around(uu_residual, 2))
# print('=============')
# print(np.around(P_residual, 2))

# fig = plt.figure(figsize=(11, 7), dpi=100)
# # plotting the pressure field as a contour
# plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)
# plt.colorbar()
# # plotting the pressure field outlines
# plt.contour(X, Y, p, cmap=cm.viridis)
# # plotting velocity field
# plt.quiver(X[::2, ::2], Y[::2, ::2], u[::2, ::2], v[::2, ::2])
# plt.xlabel('X')
# plt.ylabel('Y')

fig = plt.figure(figsize=(7, 7), dpi=100)
ax = fig.gca()
plt.xlabel('x', fontsize=16)
plt.ylabel('y', fontsize=16)
contf = ax.contourf(XC, YC, p, extend='both', cmap='jet', levels=20)
cont = ax.contour(XC, YC, p, extend='both', colors='black', levels=20, linestyles='solid', linewidths=1.5)
cbar = plt.colorbar(contf, orientation='horizontal', shrink=0.5, pad=0.1)
cbar.set_label('Velocity', fontsize=16)
# plt.xlim(0, 2)
# plt.ylim(0, 2)
plt.title('Contour of Pressure field', fontsize=16)
plt.quiver(XC, YC, u, v)
plt.xlabel('X')
plt.ylabel('Y')

plt.show()