zones = ['hc', 'valve1', 'valve2', 'valve3', 'valve4', 'outlet']


for i in zones[::-1]:
    print(i)
    if 'valve' in i:
        zones.remove(i)
        print(zones)

print(zones)