import struct
import chardet


file = r'G:\test\test.tgf'
with open(file, 'rb') as f:
    data = f.readlines()
    for i in data[:]:
        # print(i)
        # print(list(i))
        print(i.decode())
    # result = chardet.detect(data)

# print(result)

