import numpy as np

phi_init = np.array([0, 0, 0, 0])
phi = np.zeros_like(phi_init)
converge_criteria = 1e-6

A = np.array([[3, -1, 0, 0],
              [-2, 6, -1, 0],
              [0, -2, 6, -1],
              [0, 0, -2, 7]])
b = np.array([3, 4, 5, -3])


def get_residual(A, phi, b):
    residual = np.dot(A, phi) - b
    r_norm = np.linalg.norm(residual)

    return r_norm


# jacobi method
D = np.diag(np.diag(A, 0))         # extract diagonal matrix
D_inv = np.diag(1 / np.diag(A, 0))
# print(D_inv)
LU = A - D
#
# r_norm_init = get_residual(A, phi, b)
# r = 1 / r_norm_init
# n = 0
#
# while r > converge_criteria:
#     n += 1
#     phi_last = phi.copy()
#     phi = - np.dot(np.dot(D_inv, LU), phi_last) + np.dot(D_inv, b)
#     r_norm = get_residual(A, phi, b)
#     r = r_norm/r_norm_init
#     print("step %s, relative residual %s" % (n, r))
#
# print(phi)

# Gauss-Seidel method
DL = np.tril(A, k=0)            # extract lower tri of matrix including diagonal
U = np.triu(A, k=1)             # extract upper tri of matrix without diagonal
DL_inv = np.linalg.inv(DL)

r_norm_init = get_residual(A, phi, b)
r = 1 / r_norm_init
n = 0

while r > converge_criteria:
    n += 1
    phi_last = phi.copy()
    phi = - np.dot(np.dot(DL_inv, U), phi_last) + np.dot(DL_inv, b)
    r_norm = get_residual(A, phi, b)
    r = r_norm/r_norm_init
    print("step %s, relative residual %s" % (n, r))

print(phi)