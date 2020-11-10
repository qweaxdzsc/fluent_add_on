import numpy as np


file_name = r'G:\test\auto_diffuser\ad_v1\ad_v9_thickness.npy'
original_thickness_list = np.load(file_name)

print(original_thickness_list)

file_name = r'G:\test\auto_diffuser\ad_v1\ad_v10_thickness.npy'
original_thickness_list = np.load(file_name)

print(original_thickness_list)

file_name = r'G:\test\auto_diffuser\ad_v1\ad_v11_thickness.npy'
original_thickness_list = np.load(file_name)

print(original_thickness_list)



# new_thickness = 10.16619333 - 0.5 * ((3.6370963 - 2.72943074) / 3.6370963) * 10.16619333 * (262 + 262) / 262
# print(new_thickness)
#
# new_thickness = 54. - 0.5 * ((1.04536248 - 2.72943074) / 1.04536248) * 54. * (262 + 0) / 262
# print(new_thickness)