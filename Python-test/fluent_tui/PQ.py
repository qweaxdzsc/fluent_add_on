import os

import fluent_tui

project_title = 'PQ_APE4'
version_name = 'V1'
cad_name = 'PQ_APE4_V1'
project_path = r"G:\_validation\PQ\PQ_APE_4\PQ_APE4_V1"

# RPM_list = [2600]
RPM_list = [2992.38,
            3030.52,
            3075.84,
            3114.06,
            3159.52,
            3210.94,
            3256.40,
            3340.00
            ]
print('used RPM list', RPM_list)


# K_formal = np.linspace(1, 1.02, 20)
P_list = [-300,
          -350,
          -400,
          -450,
          -500,
          -550,
          -600,
          -650,
          ]
# K_list = [25, 44]
K_list = P_list
print('used K_list', P_list)

mesh_jou_name = f'{project_path}\\{project_title}_{version_name}_mesh.jou'          # txt final path
print('output journal in:', mesh_jou_name)
mesh_jou = open(mesh_jou_name, 'w')
whole_jou = ''

CFD = fluent_tui.tui(whole_jou, project_title, version_name, project_path, cad_name)

CFD.mesh.start_transcript()
CFD.mesh.import_CAD()
CFD.mesh.size_scope_global(0.3, 10)
CFD.mesh.size_scope_curv('fan_blade_curv', '*fan_blade*', 0.35, 1.5, 1.2, 16)
CFD.mesh.size_scope_prox('fan_blade_prox', '*fan_blade*', 0.8, 4, 1.2, 2)
CFD.mesh.size_scope_curv('fan_out_curv', '*fan_out*', 1, 4, 1.2, 18)
CFD.mesh.size_scope_curv('volute_curv', '*volute*', 0.8, 4.5, 1.2, 16)
CFD.mesh.size_scope_prox('volute_prox', '*volute*', 0.8, 4.5, 1.2, 2)
CFD.mesh.size_scope_curv('cutoff_curv', '*cutoff*', 0.5, 1, 1.2, 12)
# CFD.mesh.size_scope_curv('box_curv', '*box*', 1, 10, 1.25, 16)
# CFD.mesh.size_scope_prox('box_prox', '*box*', 1, 10, 1.25, 2)
CFD.mesh.size_scope_curv('extend_curv', '*extend*', 1, 8, 1.25, 16)
CFD.mesh.size_scope_prox('extend_prox', '*extend*', 1, 8, 1.25, 2)
# CFD.mesh.size_scope_curv('point_curv', '*pressure_points*', 0.5, 1, 1.2, 16)
# CFD.mesh.size_scope_prox('point_prox', '*pressure_points*', 0.5, 1, 1.2, 2)
CFD.mesh.size_scope_prox('global_prox', '', 0.8, 10, 1.2, 1)
CFD.mesh.size_scope_soft('inlet', '*inlet*', 10)

CFD.mesh.compute_size_field()
CFD.mesh.write_size_field()
CFD.mesh.import_surface_mesh()

CFD.mesh.fix_combo()
CFD.mesh.compute_volume_region()
CFD.mesh.volume_mesh_change_type(dead_zone_list=['fan_blade'])
CFD.mesh.auto_mesh_volume(1.23, 'poly')
CFD.mesh.auto_node_move(0.85)
CFD.mesh.auto_node_move(0.9, preserve_boundary='no', iterations=3)
CFD.mesh.auto_node_move(50, iterations=3, quality_method="aspect-ratio")
CFD.mesh.auto_node_move(0.85)
CFD.mesh.rename_cell(zone_list=['inlet_sphere', 'fan', 'volute', 'extend', 'cone'])
# CFD.mesh.rename_cell(zone_list=['cone', 'fan', 'volute', 'extend', 'box'])
CFD.mesh.retype_face(face_list=['inlet'], face_type='pressure-inlet')
CFD.mesh.retype_face(face_list=['filter_out', 'fan_in', 'volute_out'], face_type='internal')
# CFD.mesh.retype_face(face_list=['fan_in', 'volute_out'], face_type='internal')
# CFD.mesh.retype_face(face_list=['fan_out*'], face_type='interface')
CFD.mesh.retype_face(face_list=['outlet*'], face_type='pressure-outlet')
CFD.mesh.prepare_for_solve()
CFD.mesh.write_mesh()
# CFD.mesh.switch_to_solver()
CFD.close_fluent()
mesh_jou.write(CFD.whole_jou)
mesh_jou.close()


solve_jou_name = f'{project_path}\\{project_title}_{version_name}_solve.jou'          # txt final path
print('output journal in:', solve_jou_name)
solve_jou = open(solve_jou_name, 'w')
whole_jou = ''

CFD = fluent_tui.tui(whole_jou, project_title, version_name, project_path, cad_name)
# fan_origin = [0, 0, 0]
fan_origin = (0.4183, 0.37337, -0.32398)
# fan_origin = [0.32514, 0.393, 0.4276]
fan_axis = (0, 0, 1)
# fan_axis = [0, 0, -1]
CFD.setup.start_transcript()
CFD.setup.read_mesh()
CFD.setup.rescale()
CFD.setup.turb_models()
# CFD.setup.wall_treatment()
CFD.setup.rotation_volume(RPM_list[0], fan_origin, fan_axis, 'fan')
CFD.setup.BC_pressure_inlet('inlet')
# CFD.setup.BC_type('outlet', 'outlet-vent')


def set_outlet_expression(pressure):
    CFD.setup.expression('Pstat', '%s[Pa]' % pressure)
    CFD.setup.expression('Pcurrent', "Average(StaticPressure, ['outlet'], Weight='Area')")
    CFD.setup.expression('Pmeasure', "Average(StaticPressure, ['pressure_points'], Weight='Area')")
    CFD.setup.expression('Ptarget', '%s[Pa]' % pressure)
    CFD.setup.expression('Padjust', 'IF(abs(Ptarget - Pmeasure)/Pmeasure<0.005, '
                                    'Pcurrent, Pcurrent+(Ptarget - Pmeasure)*0.5)')
    CFD.setup.expression('outlet_pressure', 'IF(iter<1000, Pstat, IF(mod(iter, 20)==0, Padjust, Pcurrent))')

    CFD.setup.BC_pressure_outlet(['outlet'], '"outlet_pressure"')


# set_outlet_expression(P_list[0])
# CFD.setup.BC_outlet_vent(K_list[0], 'outlet')
CFD.setup.BC_pressure_inlet('inlet', K_list[0])
# CFD.setup.BC_pressure_outlet(['outlet'], P_list[0])


# CFD.setup.std_initialize()
CFD.setup.solution_method()
CFD.setup.input_summary()
CFD.setup.hyb_initialize()
CFD.setup.start_calculate(800)
CFD.setup.write_case_data()
CFD.setup.report_definition('volume', 'surface-volumeflowrate', ['outlet*'])
CFD.setup.report_definition('mass-flux', 'surface-massflowrate', ['inlet*', 'outlet*'], 'no')
CFD.setup.report_definition('pressure', 'surface-areaavg', ['pressure_points', 'outlet'])
CFD.setup.convergence_criterion('volume')
CFD.setup.start_calculate(1200)
CFD.setup.write_case_data()

CFD.post.create_result_file()
CFD.post.txt_surface_integrals('volume-flow-rate', ['inlet', 'outlet'])
CFD.post.txt_surface_integrals('uniformity-index-area-weighted', ['outlet', 'volute_out'], 'velocity-magnitude')
CFD.post.txt_mass_flux()
CFD.post.txt_surface_integrals('area-weighted-avg', ['inlet*', 'outlet*', 'fan*', 'volute_out', 'filter_out'], 'pressure')
CFD.post.txt_surface_integrals('area-weighted-avg', ['inlet*', 'outlet*', 'fan*', 'volute_out', 'filter_out'], 'total-pressure')
CFD.post.txt_moment(fan_origin, fan_axis)


def post_picture():
    CFD.post.set_background()
    # CFD.post.create_viewing_model()

    # naming
    view_file = CFD.post.tui.case_out_path + '\\' + CFD.post.tui.version_name + '.vw'
    # create txt, for loop to include all views
    code = """
    (38 ((
    (view-list (
    (z ((0 0 1) (0 0 0) (0 -1 0) 0.5 0.5 "orthographic") #(1. 0. 0. 0. 0. 1. 0. 0. 0. 0. 1. 0. 0. 0. 0. 1.))
    (x0 ((1 0 0) (0 0 0) (0 0 1) 0.5 0.5 "orthographic") #(1. 0. 0. 0. 0. 1. 0. 0. 0. 0. 1. 0. 0. 0. 0. 1.))
    )))))
    """
    with open(view_file, 'w') as f:
        f.write(code)
    CFD.post.read_view()
    CFD.post.snip_residual()

    CFD.post.create_iso_surface('zmid_plane_volute', 'z-coordinate', 0.035, from_zone='fan volute')
    CFD.post.create_iso_surface('zup_plane_volute', 'z-coordinate', 0.012, from_zone='fan volute')
    CFD.post.create_iso_surface('zbottom_plane_volute', 'z-coordinate', 0.06, from_zone='fan volute')
    CFD.post.create_iso_surface('zmid_plane_all', 'z-coordinate', 0.035)
    CFD.post.create_iso_surface('x0_plane', 'x-coordinate', 0)

    CFD.post.create_contour('z_mid_velocity', 'zmid_plane_volute', level=25)
    CFD.post.create_contour('z_mid_pressure', 'zmid_plane_volute', field='pressure', level=25)
    CFD.post.create_vector('z_mid_vector', 'zmid_plane_volute')
    CFD.post.snip_picture('z_mid_velocity')
    CFD.post.snip_picture('z_mid_pressure')
    CFD.post.snip_picture('z_mid_vector')

    CFD.post.create_contour('z_all_velocity', 'zmid_plane_all', level=25)
    CFD.post.create_contour('z_all_pressure', 'zmid_plane_all', field='pressure', level=25)
    CFD.post.snip_picture('z_all_velocity')
    CFD.post.snip_picture('z_all_pressure')

    CFD.post.create_contour('z_up_velocity', 'zmid_plane_volute', level=25)
    CFD.post.create_contour('z_up_pressure', 'zmid_plane_volute', field='pressure', level=25)
    CFD.post.create_vector('z_up_vector', 'zmid_plane_volute')
    CFD.post.snip_picture('z_up_velocity')
    CFD.post.snip_picture('z_up_pressure')
    CFD.post.snip_picture('z_up_vector')

    CFD.post.create_contour('z_bottom_velocity', 'zmid_plane_volute', level=25)
    CFD.post.create_contour('z_bottom_pressure', 'zmid_plane_volute', field='pressure', level=25)
    CFD.post.create_vector('z_bottom_vector', 'zmid_plane_volute')
    CFD.post.snip_picture('z_bottom_velocity')
    CFD.post.snip_picture('z_bottom_pressure')
    CFD.post.snip_picture('z_bottom_vector')

    CFD.post.create_contour('x0_velocity', 'x0_plane', level=25)
    CFD.post.create_contour('x0_pressure', 'x0_plane', field='pressure', level=25)
    CFD.post.create_vector('x0_vector', 'x0_plane', vector_scale=10)
    CFD.post.snip_picture('x0_velocity')
    CFD.post.snip_picture('x0_pressure')
    CFD.post.snip_picture('x0_vector')


# post_picture()
K_reverse_list = K_list[::-1]
combox_list = []

# for RPM in RPM_list:
#     if RPM_list.index(RPM) % 2 == 0:
#         for P in K_list:
#             combox_list.append([RPM, P])
#     else:
#         for P in K_reverse_list:
#             combox_list.append([RPM, P])
for i in range(len(RPM_list)):
    combox_list.append([RPM_list[i], K_list[i]])


print(combox_list)
for i in combox_list[1:]:
    CFD.setup.rotation_volume(i[0], fan_origin, fan_axis, 'fan')
    # CFD.setup.BC_pressure_outlet(['outlet'], i[1])
    # set_outlet_expression(i[1])
    # CFD.setup.BC_outlet_vent(i[1], 'outlet')
    CFD.setup.BC_pressure_inlet('inlet', i[1])
    # CFD.setup.std_initialize()
    # CFD.setup.hyb_initialize()
    CFD.setup.start_calculate(2000)
    CFD.version_name = '%s_%s' % (i[0], i[1])
    CFD.setup.write_case_data()

    CFD.txt_out = CFD.result_path + '\\' + CFD.version_name + '.txt'
    CFD.post.create_result_file()
    CFD.post.txt_surface_integrals('volume-flow-rate', ['inlet', 'outlet'])
    CFD.post.txt_surface_integrals('uniformity-index-area-weighted', ['outlet', 'volute_out'], 'velocity-magnitude')
    CFD.post.txt_mass_flux()
    CFD.post.txt_surface_integrals('area-weighted-avg', ['inlet*', 'outlet*', 'fan*', 'volute_out', 'filter_out'],
                                   'pressure')
    CFD.post.txt_surface_integrals('area-weighted-avg', ['inlet*', 'outlet*', 'fan*', 'volute_out', 'filter_out'],
                                   'total-pressure')
    CFD.post.txt_moment(fan_origin, fan_axis)

CFD.close_fluent()
solve_jou.write(CFD.whole_jou)
solve_jou.close()
os.system(mesh_jou_name)
os.system(solve_jou_name)