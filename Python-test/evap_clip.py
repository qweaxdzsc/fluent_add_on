import os


def clip(file_path, y_min, y_max, z_min, z_max, cl_y=5, cl_z=5):
    import numpy as np

    txt_name = file_path + '\\' + 'evap_clip_tui' + '.jou'
    print('output journal in:', txt_name)
    grid = open(txt_name, 'w')

    y_divide = np.linspace(y_max, y_min, cl_y, endpoint=True)
    print(y_divide)
    z_divide = np.linspace(z_min, z_max, cl_z, endpoint=True)
    print(z_divide)
    whole_messege = """"""
    for i in range(len(z_divide)-1):

        # de_z = """/surface/delete-surface evap_z%s""" % i
        message_z = """
surface/iso-clip/z-coordinate evap_z%s evap_out() %s %s
""" % (i, z_divide[i], z_divide[i+1])
        whole_messege += message_z
        for j in range(len(y_divide)-1):

            # de_y = """/surface/delete-surface evap_y%sz%s""" % (j, i)
            message_y = """
surface/iso-clip/y-coordinate evap_y%sz%s evap_z%s() %s %s
""" % (j, i, i, y_divide[j], y_divide[j+1])
            whole_messege += message_y
    whole_messege += """report/surface-integrals/area-weighted-avg"""

    for j in range(len(y_divide) - 1):
        for i in range(len(z_divide) - 1):
            whole_messege += " evap_y%sz%s" % (j, i)
    whole_messege += """() velocity yes 
%s\clip_velocity.txt yes""" % file_path
    # print(whole_messege)
    print("文件已写入到 %s" % (file_path))
    grid.write(whole_messege)
    grid.close()
    os.system(txt_name)


# y_min = 0.6852
# y_max = 0.8352001
# z_min = 0.7771059
# z_max = 0.9467155
print('4X4 Grid velocity\nPlease follow instruction enter y_min, y_max, z_min, z_max'
      '(you could use fluent iso-clip to read these parametr)'
      '\nIt will generate a script, which you could copy to fluent console to run\n'
      'After done, fluent will create a velocity file under same output address')
# y_min = input('Please enter y_min of Evaporater:')
# y_max = input('Please enter y_max of Evaporater:')
# z_min = input('Please enter z_min of Evaporater:')
# z_max = input('Please enter z_max of Evaporater:')
y_min = -0.0874
y_max = 0.1746
z_min = 0.2724
z_max = 0.4824
# clip_path = r'C:\Users\BZMBN4\Desktop'
clip_path = input('Please give file output address:')
clip(clip_path, y_min, y_max, z_min, z_max, 21, 2)
print('Output file in:%s\n Please copy whole file to fluent console to run' % clip_path)


# def evap_range(file_path, evap_average):
#
#     grid = open(file_path +'\\uni_range.jou', 'w')
#     evap_amax = evap_average * 1.2
#     evap_amin = evap_average * 0.8
#     print(evap_amin, evap_amax)
#     message = """display/set/overlays no
# /views/read-views G:\GE2_REAR\GE2-rear-command\GE2.vw ok
# display/objects/delete evap_v20p
# surface/iso-clip/velocity-magnitude evap_v20p evap_out %s %s
# display/objects/delete evap_v20p
# display/objects/create contour evap_v20p filled yes range-option auto-range-on global-range no q
# color-map format %%0.8f size 10 q surfaces-list evap_v20p() field velocity q
# display/objects/display evap_v20p
# display/views/restore-view evap_out q
# display/views/auto-scale
# display/set/picture/driver/jpeg
# display/save-picture %s/evap_v20p.jpg ok
# report/surface-integrals/area evap_out evap_v20p() yes %s\evap_range.txt yes
# """ % (evap_amin, evap_amax, file_path, file_path)
#     grid.write(message)
#     grid.close()
# #
# # file_path = r'C:\Users\BZMBN4\Desktop'
# # evap_range(file_path, 2.7908)
#
#
# def get_surface_name():
#
#     surface_name = open(r'C:\Users\BZMBN4\Desktop\surface_name.jou', 'w')
#     message = """"""
#     for i in range(4):
#         for j in range(4):
#             message += """evap_y%sz%s """ % (i, j)
#     surface_name.write(message)
#     print('write success')
#     surface_name.close()

#
# get_surface_name()