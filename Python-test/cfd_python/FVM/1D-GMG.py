import numpy as np

# =============Basic Info================
# model definition
L = 1
nx = 20
Area = 0.01
dx = L / nx
# coefficients
k = 5
g = 20e3
# boundary condition
Ta = 100
Tb = 500

# iterations = 100
# converge_criteria = 1e-4
# ================Grid======================
# Fine Grid 1
x = np.linspace(0, L, nx, endpoint=False)
x += 0.5*dx
print(x)

# ===============Solver====================
# =========================================
# init setting
T = np.zeros(nx + 2)

a = np.zeros_like(T)
a[1: -1] = k * Area / dx

Su = np.zeros_like(T)
Su[1: -1] = g * Area * dx
Su[1] = g * Area * dx + 2 * k * Area * Ta / dx
Su[-2] = g * Area * dx + 2 * k * Area * Tb / dx

Sp = np.zeros_like(T)
Sp[1] = -2 * k * Area / dx
Sp[-2] = -2 * k * Area / dx

Aj = np.zeros_like(T)
Cdj = np.zeros_like(T)
# print(a)
# print(Su)
# print(Sp)

# ============= TDMA for Grid 1 ==============
# for later verifications
T_last = T.copy()
for i in range(1, nx + 1):
    alpha = a[i + 1]
    beta = a[i - 1]
    D = a[i - 1] + a[i + 1] - Sp[i]
    C = Su[i]
    Aj[i] = alpha / (D - beta * Aj[i - 1])
    Cdj[i] = (beta * Cdj[i - 1] + C) / (D - beta * Aj[i - 1])
    # print(beta, D, alpha, C)
for i in range(nx, 0, -1):
    T[i] = Aj[i] * T[i + 1] + Cdj[i]

residual = abs(np.sum(T - T_last))
print('The result of TDMA: %s' % T)

# ========= Multi Grid Acceleration ==============
# Step 1: Gauss-Seidel iteration for Fine Grid 1
T = np.zeros(nx + 2)
T[1: -1] = 150
# steps = 800
# for n in range(steps):
#     for i in range(1, nx + 1):
#         alpha = a[i + 1]
#         beta = a[i - 1]
#         D = a[i - 1] + a[i + 1] - Sp[i]
#         C = Su[i]
#         T[i] = (alpha * T[i + 1] + beta * T[i - 1] + C) / D
#     residual = np.zeros_like(T)
#     residual[1: -1] = Su[1:nx + 1] + a[2:nx + 2] * T[2:nx + 2] - (a[:nx] + a[2:nx + 2] - Sp[1:nx + 1]) * T[1:nx + 1] + a[:nx] * T[:nx]
#     print('Step %s, RMS residual %s' % (n, np.sqrt(np.sum(residual ** 2 / len(residual)))))

for step in range(23):
    steps = 5
    for n in range(steps):
        for i in range(1, nx + 1):
            alpha = a[i + 1]
            beta = a[i - 1]
            D = a[i - 1] + a[i + 1] - Sp[i]
            C = Su[i]
            T[i] = (alpha * T[i + 1] + beta * T[i - 1] + C) / D

        # T[1:nx+1] = (a[2:nx+2] * T[2:nx+2] + a[:nx] * T[:nx] + Su[1:nx+1]) / (a[:nx] + a[2:nx+2] - Sp[1:nx+1])
    # print(T)

    residual = np.zeros_like(T)
    residual[1: -1] = Su[1:nx + 1] + a[2:nx + 2] * T[2:nx + 2] - (a[:nx] + a[2:nx + 2] - Sp[1:nx + 1]) * T[1:nx + 1] + a[:nx] * T[:nx]
    # print('residual is: %s, total RMS residual %s' % (residual, np.sqrt(np.sum(residual**2 / len(residual)))))

    # Step 2: Restriction(construct coarse grid and iterate error)
    # Coarser Grid 2 (2h)
    nx2 = int(nx/2)
    dx2 = L/nx2
    residual2 = np.zeros(nx2 + 2)

    residual_part1 = residual[1:-1:2]
    residual_part2 = residual[2::2]

    residual2[1:-1] += residual_part1
    residual2[1:-1] += residual_part2
    residual2[1:-1] /= 2
    # print(residual2)

    # recalculate coefficients for Grid2
    E2 = np.zeros_like(residual2)

    a2 = np.zeros_like(residual2)
    a2[1: -1] = k * Area / dx2

    Sp2 = np.zeros_like(residual2)
    Sp2[1] = -2 * k * Area / dx2
    Sp2[-2] = -2 * k * Area / dx2
    steps = 10
    # Gauss-Seidel Iterations for Grid2
    for n in range(steps):
        for i in range(1, nx2 + 1):
            alpha = a2[i + 1]
            beta = a2[i - 1]
            D = a2[i - 1] + a2[i + 1] - Sp2[i]
            C = residual2[i]
            # print(beta, D, alpha, C)
            E2[i] = (alpha * E2[i + 1] + beta * E2[i - 1] + C) / D

    # print(E2)

    residual22 = np.zeros_like(residual2)
    residual22[1: -1] = residual2[1: -1] - \
                        (-a2[2: nx2 + 2] * E2[2: nx2 + 2]
                         + (a2[2: nx2 + 2] + a2[: nx2] - Sp2[1: nx2 + 1]) * E2[1: nx2 + 1]
                         - a2[: nx2] * E2[: nx2])
    # print('residual22 is: %s, total RMS residual22 %s' % (residual22, np.sqrt(np.sum(residual22**2 / len(residual)))))

    # Coarser Grid 3
    nx3 = int(nx2 / 2)
    dx3 = L / nx3

    residual3 = np.zeros(nx3 + 2)

    residual_part1 = residual22[1:-1:2]
    residual_part2 = residual22[2::2]

    residual3[1:-1] += residual_part1
    residual3[1:-1] += residual_part2
    residual3[1:-1] /= 2
    # print(residual3)

    # recalculate coefficients for Grid3
    E3 = np.zeros_like(residual3)

    a3 = np.zeros_like(residual3)
    a3[1: -1] = k * Area / dx3

    Sp3 = np.zeros_like(residual3)
    Sp3[1] = -2 * k * Area / dx3
    Sp3[-2] = -2 * k * Area / dx3
    steps = 10

    # Gauss-Seidel Iterations for Grid3
    for n in range(steps):
        for i in range(1, nx3 + 1):
            alpha = a3[i + 1]
            beta = a3[i - 1]
            D = a3[i - 1] + a3[i + 1] - Sp3[i]
            C = residual3[i]
            # print(beta, D, alpha, C)
            E3[i] = (alpha * E3[i + 1] + beta * E3[i - 1] + C) / D

    # print('The error calculated by Grid 3 is', E3)

    # Step3: prolongation
    # linear interpolation E3 to E2
    E22 = np.zeros_like(E2)
    for i in range(1, nx2 + 1):
        i_y0 = int(i/2)
        i_y1 = int(i/2) + 1
        x = (i/2 - int(i/2)) + 1/2/2
        x0 = 0
        x1 = 1
        # print(E3[i_y1], E3[i_y0], x, x0, x1)
        E22[i] = E3[i_y0] + (x - x0)*((E3[i_y1] - E3[i_y0])/(x1 - x0))

    # print(E22)

    # Correct E2 by adding E22
    E2_corrected = E2 + E22
    # print(E2_corrected)

    steps = 2
    # Gauss-Seidel Iterations for Grid2
    for n in range(steps):
        for i in range(1, nx2 + 1):
            alpha = a2[i + 1]
            beta = a2[i - 1]
            D = a2[i - 1] + a2[i + 1] - Sp2[i]
            C = residual2[i]
            # print(beta, D, alpha, C)
            E2_corrected[i] = (alpha * E2_corrected[i + 1] + beta * E2_corrected[i - 1] + C) / D

    # print(E2_corrected)

    # linear interpolation E2 to E1
    E12 = np.zeros_like(T)
    for i in range(1, nx + 1):
        i_y0 = int(i/2)
        i_y1 = int(i/2) + 1
        x = (i/2 - int(i/2)) + 1/2/2
        x0 = 0
        x1 = 1
        # print(E3[i_y1], E3[i_y0], x, x0, x1)
        E12[i] = E2_corrected[i_y0] + (x - x0)*((E2_corrected[i_y1] - E2_corrected[i_y0])/(x1 - x0))

    # print(E12)

    # Step 4: Correction and final iterations
    T = T + E12
    steps = 2
    for n in range(steps):
        for i in range(1, nx + 1):
            alpha = a[i + 1]
            beta = a[i - 1]
            D = a[i - 1] + a[i + 1] - Sp[i]
            C = Su[i]
            T[i] = (alpha * T[i + 1] + beta * T[i - 1] + C) / D
    residual = np.zeros_like(T)
    residual[1: -1] = Su[1:nx + 1] + \
                      a[2:nx + 2] * T[2:nx + 2] \
                      - (a[:nx] + a[2:nx + 2] - Sp[1:nx + 1]) * T[1:nx + 1] + \
                      a[:nx] * T[:nx]
    print('Step %s, RMS residual %s' % (step, np.sqrt(np.sum(residual**2 / len(residual)))))

print(T)
