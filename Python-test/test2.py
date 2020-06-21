import struct
import chardet


file = r'C:\Users\BZMBN4\Desktop\123.msh'
with open(file, 'r') as f:
    data = f.readlines()
    for i in data:
        # print(i)
        # print(list(i))
        print(type(i))
    # result = chardet.detect(data)

# print(result)

