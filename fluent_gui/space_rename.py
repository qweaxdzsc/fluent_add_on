
f = open(r'C:\Users\BZMBN4\Desktop\project_info.txt', 'r')
lines = f.readlines()
face_list = lines[0].split("'")
face_list = face_list[1:-1:2]
print(face_list)

cad_save_path = lines[1]
print(cad_save_path)