import numpy as np
import os

# p1 = np.array([586
#                ])
# p2 = np.array([40])
# p8 = np.array([40])
#
# p3 = 100 **2 * p1 / 70**2
# p4 = 100 **2 * p2 / 125**2
# p9 = 105.555 **2 * p8 / 125**2
#
# print(p3, p4, p9)

import math

a = list()

r = [72.3, 80.6, 90.3, 100]
r2 = [93, 104.5, 116.8, 129.6]


for i in range(3):
    a.append(math.log(r[i + 1]/r[i])/90)

print(a)