def porous_d2( x, y, z):
    try:
        x = float(x)
        y = float(y)
        z = float(z)
        d1 = [x, y, z]
        d2 = [0, 0, 0]
        for i in d1:
            if i == 0:
                d2[d1.index(i)] = 1
                return d2
        d2[1] = round(-z / y, 4)
        d2[2] = 1
        return d2
    except Exception as e:
        print('porous_c contains zero')
        return [None, None, None]