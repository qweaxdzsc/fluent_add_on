import time

start_time = time.time()

file_path = r'C:\Users\BZMBN4\Desktop\1.txt'
with open(file_path, 'r+') as f:
    new_content = ''
    n = 0
    for line in f:
        n += 1
        print(f"line {n}: {line}")
        if ('[' or ']')in line:
            print('find it')
            line = line.replace('[', '(')
            line = line.replace(']', ')')
        new_content += line
    f.seek(0)
    f.write(new_content)
    print(n)

end_time = time.time()

print("time cost: %s" % (end_time - start_time))