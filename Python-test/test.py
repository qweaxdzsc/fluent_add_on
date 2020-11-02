import requests
import time
import hashlib

start_time = time.time()


def get_md5(file):
    with open(file, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        value = md5obj.hexdigest()
        return value


file1 = r'G:\test\queue_test2\queue_test2_mesh.msh'
file2 = r'G:\test\queue_test2\queue_test2_solve.jou'

file_list = [file1, file2]
files = []
file_md5 = []

for file in file_list:
    files.append(("file_list", open(file, "rb")))
    md5 = get_md5(file)
    file_md5.append(md5)

request_data = {
    'exec_file_name':  r'queue_test2_solve.jou',
    'user_name':  r'zonghui.jin',
    'file_md5': file_md5
}
print(request_data)
# MyLogger().getlogger().info('url:%s' % (request_url))
resp = requests.post(url='http://localhost:80/api/upload/', data=request_data, files=files)
# resp = requests.post(url='http://localhost:80/api/upload/', files=files)

end_time = time.time()


print('use time', end_time - start_time)