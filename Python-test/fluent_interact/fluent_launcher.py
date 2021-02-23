# fluent launcher with last time memory

import os
from fluent_interact.txt_repository import default, write

# default value
default_value = default()
model_default = default_value[0]
cores_default = default_value[1]

# new input
model_input = input("Please choose mesh or solver[%s]:" % model_default)            # choose fluent model, mesh or fluent solver
cores_input = input("Please enter Parallel threads number[%s]: " % cores_default)   # number of threads

journal = 'start_mesh.jou'


# find wanted model and cores

if model_input == '':
    model = model_default
else:
    model = model_input
if cores_input == '':
    cores = cores_default
else:
    cores = cores_input

# record model and cores
write(model, cores)

# realize open fluent with specific model and threads
if model.strip()[0] == 's':
    os.system('cd C:\\Program Files\\ANSYS Inc\\v191\\fluent\\ntbin\\win64 '
              '&& fluent 3d -t%s' % cores)
elif model.strip()[0] == 'm':
    os.system('cd C:\\Program Files\\ANSYS Inc\\v191\\fluent\\ntbin\\win64 '
              '&& fluent 3d -t%s -i C:\\Users\\BZMBN4\\Desktop\\fluent-command\\%s' % (cores, journal))
else:
    pass
