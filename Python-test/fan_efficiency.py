# root = r"G:\GE2_REAR\GE2-rear-vent\GE2-rear-v9.2-FC\result"
# path = root + '\\'


class fan(object):
    def __init__(self, path, fan_speed, pressure_type='s'):
        import numpy as np
        self.path = path
        self.fan_speed = fan_speed
        self.pressure_type = pressure_type
        data_matrix = np.load(path + 'data_matrix.npy', allow_pickle=True)
        self.data_matrix = data_matrix
        if self.pressure_type[0] == 't':
            up_dp_index = self.data_matrix[5].index('fan_in')
            down_dp_index = self.data_matrix[5].index('evap_in')

            whole_dp = float(self.data_matrix[6][down_dp_index]) - float(self.data_matrix[6][up_dp_index])
        elif self.pressure_type[0] == 's':
            up_dp = 0
            for i in self.data_matrix[3]:
                if 'filter' in i:
                    up_dp_index = self.data_matrix[3].index('fan_in')
                    up_dp = -float(self.data_matrix[4][up_dp_index])
                    break
            down_dp_index = self.data_matrix[3].index('evap_in')
            down_dp = float(self.data_matrix[4][down_dp_index])
            whole_dp = up_dp + down_dp
        else:
            pass
        self.whole_dp = whole_dp

    def fan_ef(self):
        import numpy as np
        total_volume = float(self.data_matrix[1][-1])
        air_watts = self.whole_dp * total_volume / 1000
        fan_torque = float(self.data_matrix[-1][-1])
        shaft_power = fan_torque * self.fan_speed * 2.0 * np.pi / 60
        fan_ef = air_watts / shaft_power
        fan_ef_pc = '%.1f %%' % (fan_ef * 100)
        print('Whole dp is:', self.whole_dp)
        print('air_watt is:', air_watts)
        print('shaft power is:', shaft_power)
        print('fan efficiency is:', fan_ef_pc)

        self.fan_ef = fan_ef
        self.fan_ef_pc = fan_ef_pc

        return fan_ef

    def fan_ef_pc(self):
        import numpy as np
        total_volume = float(self.data_matrix[1][-1])
        air_watts = self.whole_dp * total_volume / 1000
        fan_torque = float(self.data_matrix[-1][-1])
        shaft_power = fan_torque * self.fan_speed * 2.0 * np.pi / 60
        fan_ef = air_watts / shaft_power
        fan_ef_pc = '%.1f %%' % (fan_ef * 100)
        print('Whole dp is:', self.whole_dp)
        print('air_watt is:', air_watts)
        print('shaft power is:', shaft_power)
        print('fan efficiency is:', fan_ef_pc)

        self.fan_ef = fan_ef
        self.fan_ef_pc = fan_ef_pc

        return fan_ef_pc

# ge2 = fan(path, 2850)
# whole_dp = ge2.whole_dp()
# fan_ef = ge2.fan_ef()
# fan_ef_pc = ge2.fan_ef_pc()

