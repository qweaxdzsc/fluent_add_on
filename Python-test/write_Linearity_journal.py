
import numpy as np
import os

out_path = 'C:\\Users\\BZMBN4\\Desktop\\'       # txt output root
title = 'solve'                                  # txt name

txt_name = out_path + title + '.jou'            # txt final path
print('output journal in:', txt_name)
report = open(txt_name, 'w')                    # create txt

# linearity angle setup
total_angle = 92.25
angle_array = np.linspace(9.225, total_angle, 10, endpoint=True)   # define your angle range and points
print('angle array:', angle_array)


# content for journal
def mesh_case(cad_path, min_size=0.8, max_size=5.5, grow_rate=1.2, normal_angle=16, gap_cell=2):
    mesh_case = """
/file/import/cad-options/save-PMDB yes
/file/import/cad-options/extract-features yes 10
/file/import/cad-geometry yes {cad_path}.scdoc mm cfd-surface-mesh no {min_size} {max_size} {grow_rate} yes yes 
{normal_angle} {gap_cell} edges yes no
""".format(cad_path=cad_path, min_size=min_size, max_size=max_size, grow_rate=grow_rate,
               normal_angle=normal_angle, gap_cell=gap_cell)

    return mesh_case


def lin_mesh(project_name, angle_array, mesh_path, valve_dir, valve_origin):
    message = """;0
;write mesh
file/write-mesh %s\\%s-%s 
""" % (mesh_path, project_name, angle_array[0])
    j = 0
    for i in angle_array[1:]:
        j = j + 1
        rotate = round(angle_array[j]-angle_array[j-1],2)
        mesh_part = """;{valve_angle}
;delet-cells \n
/objects/volumetric-regions/delete-cells * *()
q

;repair face mesh
/diagnostics/quality/general-improve objects *() skewness 0.5 30 5 yes

;rotate
boundary/manage/rotate valve*()
{rotate_angle} {valve_dx} {valve_dy} {valve_dz}() {valve_origin_x} {valve_origin_y} {valve_origin_z}() no


;compute volume region
/objects/volumetric-regions/compute * no yes

;volume region change type
/objects/volumetric-regions/change-type * *() fluid
/objects/volumetric-regions/change-type * valve*() dead

;Auto-mesh-volume
/mesh/tet/controls/cell-sizing geometric 1.25
/mesh/auto-mesh * yes pyramids tet no


;Auto-node-move
/mesh/modify/auto-node-move *() *() 0.7 50 120 yes 10

;rename cell zone
mesh/manage/name *ai* ai
mesh/manage/name *distrib* distrib
mesh/manage/name *evap* evap
mesh/manage/name *hc* hc

;retype face
/boundary/manage/type evap_in evap_out hc_out()
internal

/boundary/manage/type inlet*()
pressure-inlet

/boundary/manage/type outlet*()
outlet-vent

/boundary/manage/type hc_in()
radiator

;write mesh
file/write-mesh {mesh_path}\\{project_name}-{valve_angle} 

""".format(valve_angle=i, rotate_angle=rotate, valve_dx=valve_dir[0], valve_dy=valve_dir[1], valve_dz=valve_dir[2],
           valve_origin_x=valve_origin[0], valve_origin_y=valve_origin[1], valve_origin_z=valve_origin[2],
           mesh_path=mesh_path, project_name=project_name)
        message += mesh_part

    return message


def lin_solve(project_name, angle, mesh_path, case_path, result_path):
    import post_process
    message = ''
    for i in angle:
        solve_part = """
;replace mesh
file/replace-mesh {mesh_path}\\{project_name}-{angle}.msh yes

;re scale
mesh/scale 0.001 0.001 0.001


;modify heat flux
/define/boundary-conditions/set/pressure-inlet inlet*() t0 no 273.15 q q q
/define/boundary-conditions/set/outlet-vent outlet*() t0 no 273.15 q q q

/define/boundary-conditions/zone-type hc_in radiator
/define/boundary-conditions/set/radiator hc_in() temperature 348.15 hc constant 1000000 q 
/define/boundary-conditions/zone-type hc_out radiator
/define/boundary-conditions/set/radiator hc_out() temperature 348.15 hc constant 1000000
q

;initialize
/solve/initialize/hyb-initialization yes

;calculation
solve/iterate/210 yes

;write case and data
file/write-case-data/ {case_path}/{project_name}_{angle}\\{project_name}_{angle}
""".format(mesh_path=mesh_path, case_path= case_path, project_name=project_name, angle=i)
        message += solve_part
        message += post_process.post_process(i, result_path)

    return message


project_path = r"G:\458-rear\458-rear-lin\458-vent-lin"
cad_name = "458-vent-lin"
project_name = '458-rear'
valve_dir = [0, -1, 0]
valve_origin = [5407.69, 869.38, 1022.1]


cad_path = project_path + '\\' + cad_name
case_path = project_path + '\\lin_case'
mesh_out_path = project_path + '\\lin_mesh'
result_path = case_path

# mesh_case = mesh_case(cad_path)
# mesh_part = lin_mesh(project_name, angle_array, mesh_out_path, valve_dir, valve_origin)
# whole_message = mesh_case + mesh_part
solve_part = lin_solve(project_name, angle_array, mesh_out_path, case_path, result_path)
whole_message = solve_part

report.write(whole_message)
report.close()

os.system(txt_name)

