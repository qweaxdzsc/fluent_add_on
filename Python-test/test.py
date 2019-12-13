import numpy as np

ab = ['outlet_rfr', 'outlet_rfl', 'outlet_ffr', 'outlet_ffl', 'outlet_vc', 'outlet_vr', 'outlet_vl']
side_vent = []
center_vent = []
foot = []
rear_foot = []
side_defrost = []
clasif_outlet_dict = {'side_vent': side_vent, 'center_vent':center_vent, 'foot': foot, 'rear_foot': rear_foot,
                       'side_defrost': side_defrost}

for i in ab:
    if i[-1] is 'r' or i[-1] is 'l':
        if 'v' in i:
            if i[-3] is 'c':
                center_vent.append(ab.index(i))
            else:
                side_vent.append(ab.index(i))
        elif 'f' in i:
            if i[-3] is 'f':
                foot.append(ab.index(i))
            elif i[-3] is 'r':
                rear_foot.append(ab.index(i))
        elif 'd' in i:
            side_defrost.append(ab.index(i))

for i in list(clasif_outlet_dict.keys()):
    if not clasif_outlet_dict[i]:
        clasif_outlet_dict.pop(i)

print(clasif_outlet_dict)



