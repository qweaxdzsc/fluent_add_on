import numpy as np

# def batch_plane(dx1, dx2, dy1, dy2, dz1, dz2, direction, col_number):
#     dx1, dx2 = scaling(dx1, dx2)
#     dy1, dy2 = scaling(dy1, dy2)
#     dz1, dz2 = scaling(dz1, dz2)
#     if direction == 'z':
#         tui = ''
#         batch_list = np.linspace(dz1, dz2, col_number + 1)
#         print(batch_list)
#         for index, value in enumerate(batch_list):
#             plane_name = 'plane_%s' % (index + 1)
#             tui += create_plane(plane_name, dx1, )
#
#
# def scaling(d1, d2):
#     d1 = d1 + (d1 - d2)*0.05
#     d2 = d2 - (d1 - d2)*0.05
#     return d1, d2
#
#
# def create_plane(name, dx1, dy1, dz1, dx2, dy2, dz2, dx3, dy3, dz3):
#     tui = """
# surface/plane-surface/{plane_name} three-points {dx1} {dy1} {dz1} {dx2} {dy2} {dz2} {dx3} {dy3} {dz3}yes no
# """.format(plane_name=name, dx1=dx1, dy1=dy1, dz1=dz1, dx2=dx2, dy2=dy2, dz2=dz2, dx3=dx3, dy3=dy3, dz3=dz3)
#     return tui

import numpy as np
import os


def iso_surface(direction, location, surface_name='section'):
    tui = """
/surface/iso-surface/{direction}-coordinate {surface_name} () *() {value}()
""".format(direction=direction, surface_name=surface_name, value=location)
    return tui


def clip_plane(direction, clip_face, new_face_name, min, max):
    tui = """
/surface/iso-clip/{direction}-coordinate {new_surface_name} {from_surface} {min} {max}
""".format(direction=direction, new_surface_name=new_face_name, from_surface=clip_face, min=min, max=max)
    return tui


def batch_clip(direction, clip_face, total_min, total_max, column_number):
    tui = ''
    location_list = np.linspace(total_min, total_max, column_number + 1)
    print(location_list)
    for index, value in enumerate(location_list[:-1]):
        new_face_name = 'clip_%s' % (index + 1)
        tui += clip_plane(direction, clip_face, new_face_name, value, location_list[index + 1])
    print(tui)
    return tui


def get_mass_flow(plane_name, file_path):
    tui = """
report/surface-integrals/mass-flow-rate {plane_name}() yes {file_path}
""".format(plane_name=plane_name, file_path=file_path)
    return tui


if __name__ == "__main__":
    tui = batch_clip('z', 'section', 0.3214, 0.4245, 8)
    journal_address =  r'C:\Users\BZMBN4\Desktop\clip_journal.jou'
    with open(journal_address, 'w') as f:
        f.write(tui)
    os.system(journal_address)
    # dx1 = -0.7277
    # dx2 = -0.7571
    # dy1 = -0.2061
    # dy2 = -0.2055
    # dz1 = 0.4245
    # dz2 = 0.3214
    # col_number = 8
    # batch_plane(dx1, dx2, dy1, dy2, dz1, dz2, 'z', 8)
