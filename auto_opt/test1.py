import os
import subprocess
import time
import numpy as np

from post_algorithm import PostProcess
from tui_run import CreateTUI
from report.get_report import GetReport


class EvapShape(object):
    def __init__(self, original_point, effective_shape):
        self.original_point = original_point
        self.effective_shape = effective_shape
        self.effective_area = effective_shape[1] * effective_shape[2] / 1e+6
        self.ox = original_point[0]
        self.oy = original_point[1]
        self.oz = original_point[2]
        self.lx = effective_shape[0]
        self.ly = effective_shape[1]
        self.lz = effective_shape[2]


class ShapeLine(object):
    def __init__(self, evap_shape):
        self.evap_shape = evap_shape
        self.start_point = list(evap_shape.original_point)
        self.end_point = list(evap_shape.original_point)
        self.end_point[1] += evap_shape.ly

    def get_points(self, x_list, number=21):
        y_list = np.linspace(self.evap_shape.oy, self.evap_shape.oy + self.evap_shape.ly, number, endpoint=True)
        z_list = np.ones(number) * self.evap_shape.oz
        points = np.column_stack((x_list, y_list, z_list))
        points = np.row_stack((self.start_point, points, self.end_point))

        points = [list(i) for i in points]  # change array to list
        print('generate points', points)
        return points

    def get_default_x(self, thickness, number=21):
        x_list = np.ones(number) * (self.evap_shape.ox - thickness)
        return x_list

    def get_x(self, thickness_list, number=21):
        x_list = np.ones(number) * self.evap_shape.ox - thickness_list
        return x_list

    def get_points_dict(self, thickness_list, number=21):
        points_dict = {}
        place_ratio = [0, 0.15, 0.85]
        part_ratio = [0.15, 0.7, 0.15]
        for i, element in enumerate(thickness_list):
            x_list = np.ones(number) * self.evap_shape.ox - element
            y_list = np.linspace(self.evap_shape.oy, self.evap_shape.oy + self.evap_shape.ly, number, endpoint=True)
            z_list = np.ones(number) * self.evap_shape.oz + self.evap_shape.lz * place_ratio[i]
            points = np.column_stack((x_list, y_list, z_list))
            points = np.row_stack((self.start_point, points, self.end_point))
            points = [list(i) for i in points]  # change array to list
            # form dict
            new_dict = {
                'place_ratio': place_ratio[i],
                'part_ratio': part_ratio[i],
                'point_list': points,
            }
            points_dict[i+1] = new_dict

        print('generate points', points_dict)
        return points_dict


def write_script(base_file, origin_z, z_length, points_dict, script_path, save_path):
    text = """
print('start script')
DocumentOpen.Execute(r"{base_file}.scdoc")

# 3 parts
points_dict = {points_dict}

for key, value in points_dict.items():
    # create datum plane
    point = Point.Create(MM(0), MM(0), MM({origin_z} + {z_length}*value['place_ratio']))
    direction = Direction.Create(0, 0, 1)
    result = DatumPlaneCreator.Create(point, direction)
    selection = Selection.CreateByNames('Plane')
    RenameObject.Execute(selection,'Plane%s' % key)
    
    # set plane as sketch
    selection = Selection.CreateByNames('Plane%s' % key)
    ViewHelper.SetSketchPlane(selection)
    
    # draw first vertical line
    start = Point2D.Create(MM(value['point_list'][0][0]), MM(value['point_list'][0][1]))
    end = Point2D.Create(MM(value['point_list'][1][0]), MM(value['point_list'][1][1]))
    result = SketchLine.Create(start, end)
    
    # draw second vertical line
    start = Point2D.Create(MM(value['point_list'][-1][0]), MM(value['point_list'][-1][1]))
    end = Point2D.Create(MM(value['point_list'][-2][0]), MM(value['point_list'][-2][1]))
    result = SketchLine.Create(start, end)
    
    # draw up line
    start = Point2D.Create(MM(value['point_list'][0][0]), MM(value['point_list'][0][1]))
    end = Point2D.Create(MM(value['point_list'][-1][0]), MM(value['point_list'][-1][1]))
    result = SketchLine.Create(start, end)
    
    # draw middle spline
    points = List[Point2D]()
    point_list = value['point_list'][1:-1]
    for i in point_list:
        # print(i)
        points.Add(Point2D.Create(MM(i[0]), MM(i[1])))
    result = SketchNurbs.CreateFrom2DPoints(False, points)
    
    # Solidify Sketch
    mode = InteractionMode.Solid
    result = ViewHelper.SetViewMode(mode)
    
    # Extrude 1 Face
    selection = Selection.Create(GetRootPart().Bodies[0].Faces[0])
    options = ExtrudeFaceOptions()
    options.ExtrudeType = ExtrudeType.Add
    Body1 = ExtrudeFaces.Execute(selection, MM({z_length}*value['part_ratio']), options)
    selection = Selection.Create(GetRootPart().Bodies[0])
    RenameObject.Execute(selection,"shape%s" % key)
    
    # Make Components
    selection =Selection.CreateByNames("shape%s" % key)
    component= Selection.CreateByNames("volute")
    result = ComponentHelper.MoveBodiesToComponent(selection, component, False, None)

# Merge Bodies
targets = Selection.Create(GetRootPart().GetComponents('volute')[0].GetAllBodies())
result = Combine.Merge(targets)

# Share Topology
options = ShareTopologyOptions()
options.Tolerance = MM(0.2)
result = ShareTopology.FindAndFix(options)

# save file
options = ExportOptions.Create()
DocumentSave.Execute(r"{save_path}.scdoc", options)
print('script finished')
""" .format(origin_z=origin_z, z_length=z_length, points_dict=points_dict,
            save_path=save_path, base_file=base_file)
    with open(script_path, 'w') as f:
        f.write(text)


def call_SCDM(py_script):
    p = subprocess.Popen(r'cd C:\Program Files\ANSYS Inc\v201\scdm && SpaceClaim.exe /RunScript="%s" /ExitAfterScript=True' % py_script,
                         shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    print('SCDM finished')
    # out = out.decode()


def call_mesh(mesh_journal):
    p = subprocess.Popen(r'cd C:\\Program Files\\ANSYS Inc\\v201\\fluent\\ntbin\\win64 && '
                              r'fluent 3d -meshing -t4 -i %s' % mesh_journal, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    print('mesh finished')


def call_solver(cwd, solve_journal, cores=12):
    disk = cwd[:2]
    software_path = r'C:\\Program Files\\ANSYS Inc\\v191\\fluent\\ntbin\\win64'
    exe_name = 'fluent'
    command = '3d -t%s -i %s' % (cores, solve_journal)
    p = subprocess.Popen(r'%s &&'
                         r'cd %s &&'
                         r'"%s\%s" %s' %
                         (disk, cwd, software_path, exe_name, command),
                         shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE, universal_newlines=True)

    out, err = p.communicate()
    print('mesh finished')


total_begin_time = time.time()
# input
original_point = (262, -87.4, 272.4)   # unit mm
evap_shape = (40, 262, 210)
target_airflow = 0.15                  # m3/s

opt_iter = 1
for i in range(1, opt_iter+1):
    print('==========================================')
    print('The %s optimized iteration start' % i)
    start_time = time.time()
    project_address = r'G:\test\auto_diffuser\ad_v3'
    project_title = 'ad'
    version_name = 'V%s' % i
    line_number = 21
    boundary_list = np.ones(line_number) * 54

    # file, path info based on inputs
    base_cad_name = '%s_base_whole' % project_title                 # whole module as base
    new_cad_name = '%s_%s' % (project_title, version_name)
    new_script_name = 'script_%s.py' % version_name
    base_file_path = f'{project_address}\\ad_base\\{base_cad_name}'
    cwd = f'{project_address}\\{project_title}_{version_name}'
    print('current work directory: %s' % cwd)
    if not os.path.exists(cwd):
        os.mkdir(cwd)
    save_path = f'{cwd}\\{new_cad_name}'
    script_path = f'{cwd}\\{new_script_name}'
    result_path = f'{cwd}\\result_{project_title}_{version_name}'

    # calculate points line
    evap = EvapShape(original_point, evap_shape)
    shape_line = ShapeLine(evap)

    # calculate X_list
    if i == 1:
        csv_path = r'G:\test\auto_diffuser\return_test\result_MQBA0_new_V10.2_VENT\MQBA0_new_V10.2_VENT_data.csv'
        number = 21
        file_name = r'G:\test\auto_diffuser\return_test\MQBA0_new_V10.2_VENT_thickness_3.npy'
        thickness_list = np.load(file_name)
        boundary_list = np.ones(number) * 54
        np_file = f'{cwd}\\{project_title}_{version_name}_thickness'
        process = PostProcess(csv_path, number)
        target_velocity = process.get_target_velocity(0.15, 0.05502)
        new_thickness = process.three_thickness(boundary_list, thickness_list, target_velocity, np_file)
        points_dict = shape_line.get_points_dict(new_thickness)
    else:
        pass
        last_version = 'V%s' % (i - 1)
        last_dir = f'{project_address}\\{project_title}_{last_version}'
        last_file = f'{last_dir}\\{project_title}_{last_version}_thickness.npy'
        original_thickness_list = np.load(last_file)
        np_file = f'{cwd}\\{project_title}_{version_name}_thickness'
        csv_path = f'{last_dir}\\result_{project_title}_{last_version}\\{project_title}_{last_version}_data.csv'
        process = PostProcess(csv_path)
        target_velocity = process.get_target_velocity(target_airflow, evap.effective_area)
        new_thickness = process.three_thickness(boundary_list, original_thickness_list, target_velocity, np_file)
        points_dict = shape_line.get_points_dict(new_thickness)

    # write SCDM script
    write_script(base_file_path, evap.oz, shape_line.evap_shape.lz, points_dict, script_path, save_path)

    # # make new journal
    journal = CreateTUI(cwd, project_title, version_name, new_cad_name)
    mesh_jou_path = journal.get_mesh_jou(whole_model=True)
    solve_jou_path = journal.get_solve_jou(whole_model=True)

    # launch scdm to do the CAD modify
    # call_SCDM(script_path)

    # launch fluent meshing to do mesh
    # call_mesh(mesh_jou_path)

    # # launch fluent solver to do calculation
    # call_solver(cwd, solve_jou_path, 12)
    #
    # # get report
    # report = GetReport(result_path)
    # report.get_html()
    # report.get_excel()
    end_time = time.time()
    print('==========================================')
    print('The %s optimized iteration finished' % i)
    print('using time %s minutes' % ((end_time - start_time)/60))
    print('==========================================')


total_final_time = time.time()
print('===============================================')
print('Finished all %s optimize iterations' % opt_iter)
print('total using time: %s hours' % ((total_final_time - total_begin_time)/3600))
print('===============================================')