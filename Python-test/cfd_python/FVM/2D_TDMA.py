import numpy as np

# ========== Problem coefficient ===============
Lx = 0.3
Ly = 0.4
Lz = 0.01
nx = 3
ny = 4
k = 1000
iterations = 100
converge_criteria = 1e-4

dx = Lx / nx
dy = Ly / ny
# ============ Grid points =====================
x = np.linspace(0, Lx, nx, endpoint=False)
y = np.linspace(0, Ly, ny, endpoint=False)

x += 0.5 * dx
y += 0.5 * dy

X, Y = np.meshgrid(x, y)
# print(X, Y)

# ============= Init Setting ==================
T = np.zeros((ny + 2, nx + 2))
Tn = 100
qw = 500 * 1e3
hw = qw * (dx * Lz)
# print(qw)
Su = np.zeros_like(T)
Sp = np.zeros_like(T)

Su[:, 1] += hw
Su[-2, :] += 2 * k / dy * (Lz * dx) * Tn
Sp[-2, :] += - 2 * k / dy * (Lz * dx)
# print(Su)
# print(Sp)
Aj = np.zeros_like(T)
Cdj = np.zeros_like(T)
# Because aw=ae=as=an, and dx=dy, use a to replace them
a = np.zeros_like(T)
a[1:-1, 1:-1] = k / dx * Lz * dx
# print(a)

# =================== Solver ==========================
n = 0
residual = 1
while (n < iterations) and (residual > converge_criteria):
    n += 1

    T_last = T.copy()
    for j in range(1, nx + 1):
        for i in range(1, ny + 1):
            alpha = a[i + 1, j]
            beta = a[i - 1, j]
            D = a[i - 1, j] + a[i + 1, j] + a[i, j - 1] + a[i, j + 1] - Sp[i, j]
            C = a[i, j - 1] * T[i, j - 1] + a[i, j + 1] * T[i, j + 1] + Su[i, j]
            Aj[i, j] = alpha / (D - beta * Aj[i - 1, j])
            Cdj[i, j] = (beta * Cdj[i - 1, j] + C) / (D - beta * Aj[i - 1, j])
            # print(beta, D, alpha, C)

        for i in range(ny, 0, -1):
            T[i, j] = Aj[i, j] * T[i + 1, j] + Cdj[i, j]

    residual = abs(np.sum(T - T_last))
    print('Iteration %s: residual %s' % (n, residual))
        # print(T)

# print(Aj)
# print(Cdj)
print(T)
