import struct
import chardet


file = r'G:\test\test2.msh'
with open(file, 'rb') as f:
    data = f.read()
    result = chardet.detect(data)

print(result)