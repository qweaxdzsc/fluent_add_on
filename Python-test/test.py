import numpy as np
from matplotlib import pyplot as plt

# loop = np.linspace(1.0, 2, 11)
plt.figure(figsize=(12, 8))

# for i in loop:
b = np.linspace(0, 10, 21)
plot_signal = False
n = 2
a = [round(1 + j**n, 2) for j in b]

plt.plot(b, a)


print(a)

plt.show()
