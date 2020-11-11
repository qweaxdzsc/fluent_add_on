import numpy as np
import pandas as pd
#
# np_file = r'G:\test\auto_diffuser\ad_v2\ad_V6\ad_V6_thickness.npy'
# original_thickness = np.load(np_file)
# print(original_thickness)
#
# original_thickness[1] = 3.8
# original_thickness[2] = 4.6
# original_thickness[3] = 7.99
# original_thickness[4] = 7.99
# original_thickness[5] = 11.46
# original_thickness[6] = 14
#
# b = np.tile(original_thickness, (3, 1))
# print(b)
#
# new_np_file = r'G:\test\auto_diffuser\return_test\MQBA0_new_V10.2_VENT_thickness_3.npy'
# np.save(new_np_file, b)
file_path = r'C:\Users\BZMBN4\Desktop\test.csv'
df = pd.read_csv(file_path, header=None, skiprows=2)
df = df.applymap(lambda x: x.replace('*', ''))
df = df.applymap(lambda x: x.replace('\\', '0'))
new = np.array(df)[:, 1:].astype('int64')
print(new)
print(new.mean())


new_df = pd.DataFrame(data=new)
print(new_df.median())
print(new_df.describe())
# second = np.where('*' in new, 1641, new)
# print(second)

