from fluent_tui_V2 import tui


class CreateTUI(object):
    def __init__(self, project_addres, project_title, version_name, cad_name):
        self.project_addres = project_addres
        self.project_title = project_title
        self.version_name = version_name
        self.cad_name = cad_name

    def get_mesh_jou(self, whole_model=False):
        mesh_jou_path = f'{self.project_addres}\\{self.project_title}_{self.version_name}_mesh.jou'          # txt final path
        print('output journal in:', mesh_jou_path)
        mesh_jou = open(mesh_jou_path, 'w')
        whole_jou = ''

        CFD = tui(whole_jou, self.project_title, self.version_name, self.project_addres, self.cad_name)

        if whole_model:
            CFD.mesh.simple_import(['ai', 'filter', 'cone'], ['filter', 'evap'])
            CFD.mesh.stitch_free_face()
            CFD.mesh.general_improve()
            CFD.mesh.fix_slivers()
            CFD.mesh.fix_steps(20, 0.1)
            CFD.mesh.collapse_area()
            CFD.mesh.fix_slivers()
            CFD.mesh.fix_steps(20, 0.1)
            CFD.mesh.fix_slivers()
            CFD.mesh.compute_volume_region()
            CFD.mesh.volume_mesh_change_type(dead_zone_list=['fan_blade'])
            CFD.mesh.retype_face(face_list=['inlet*'], face_type='pressure-inlet')
            CFD.mesh.retype_face(face_list=['filter*', 'fan_in', 'fan_out', 'evap*'], face_type='internal')
            CFD.mesh.retype_face(face_list=['outlet*'], face_type='outlet-vent')
            CFD.mesh.auto_mesh_volume(mesh_type='tet')
            CFD.mesh.auto_node_move(0.85)
            CFD.mesh.auto_node_move(0.9, 'no')
            CFD.mesh.rename_cell(zone_list=['ai', 'filter', 'cone', 'fan', 'volute', 'evap', 'distrib'])
        else:
            CFD.mesh.import_distrib()
            CFD.mesh.stitch_free_face()
            CFD.mesh.general_improve()
            CFD.mesh.fix_slivers()
            CFD.mesh.fix_steps(20, 0.1)
            CFD.mesh.collapse_area()
            CFD.mesh.fix_slivers()
            CFD.mesh.compute_volume_region()
            CFD.mesh.volume_mesh_change_type()
            CFD.mesh.retype_face(face_list=['inlet*'], face_type='mass-flow-inlet')
            CFD.mesh.retype_face(face_list=['evap*'], face_type='internal')
            CFD.mesh.retype_face(face_list=['outlet*'], face_type='pressure-outlet')
            CFD.mesh.auto_mesh_volume(mesh_type='tet')
            CFD.mesh.auto_node_move(0.85)
            CFD.mesh.auto_node_move(0.9, 'no')
            CFD.mesh.rename_cell(zone_list=['diffuser', 'evap', 'distrib'])
            CFD.mesh.check_quality()
        CFD.mesh.prepare_for_solve()
        CFD.mesh.write_mesh()
        CFD.close_fluent()

        mesh_jou.write(CFD.whole_jou)
        mesh_jou.close()

        return mesh_jou_path

    def get_solve_jou(self, whole_model=False):
        solve_jou_path = f'{self.project_addres}\\{self.project_title}_{self.version_name}_solve.jou'          # txt final path
        print('output journal in:', solve_jou_path)
        solve_jou = open(solve_jou_path, 'w')
        whole_jou = ''

        CFD = tui(whole_jou, self.project_title, self.version_name, self.project_addres, self.cad_name)

        CFD.setup.start_transcript()
        CFD.setup.set_timeout(60)
        CFD.setup.read_mesh()
        CFD.setup.rescale()
        CFD.setup.turb_models()
        evap_d1 = [1, 0, 0]
        evap_d2 = [0, 1, 0]
        CFD.setup.porous_zone('evap', evap_d1, evap_d2, 3.07e+07, 523)
        if whole_model:
            CFD.setup.BC_pressure_inlet('inlet', -295)
            filter_d1 = [0, 0, 1]
            filter_d2 = [0, 1, 0]
            CFD.setup.porous_zone('filter', filter_d1, filter_d2, 5.23e+07, 250.69)
            fan_origin = [0.34693, 0.38973, 0.38921]
            fan_axis = [0, 0, 1]
            rpm = 3800
            CFD.setup.rotation_volume(rpm, fan_origin, fan_axis, 'fan')
        else:
            CFD.setup.BC_type('inlet', 'mass-flow-inlet')
            CFD.setup.BC_mass_flow_inlet('inlet', '0.18375')
        CFD.setup.BC_pressure_outlet(['outlet'])
        CFD.setup.solution_method()
        mass_flux_list = ['inlet*', 'outlet*']
        pressure_face_list = ['inlet', 'outlet*', 'evap*']
        CFD.setup.report_definition('volume', 'surface-volumeflowrate', ['inlet*'])
        CFD.setup.report_definition('mass-flux', 'surface-massflowrate', mass_flux_list, 'no')
        CFD.setup.report_definition('pressure', 'surface-areaavg', pressure_face_list)
        CFD.setup.input_summary()
        CFD.setup.hyb_initialize()
        if whole_model:
            CFD.setup.convergence_criterion('volume')
            CFD.setup.start_calculate(1000)
        else:
            CFD.setup.convergence_criterion('pressure')
            CFD.setup.start_calculate(260)
        CFD.setup.write_case_data()

        volume_face_list = ['inlet*', 'outlet*']
        CFD.post.create_result_file()
        CFD.post.set_background()
        CFD.post.create_viewing_model()
        CFD.post.create_view(evap_d1)
        CFD.post.read_view()
        CFD.post.create_streamline('whole_pathline', 'inlet*', skip='2')
        CFD.post.create_streamline('distrib_pathline', 'evap_in', [0, 15], skip='2')
        CFD.post.create_scene('distrib_pathline')
        CFD.post.snip_picture('distrib_pathline_scene', 'yes')
        CFD.post.create_scene('whole_pathline')
        CFD.post.snip_residual()
        CFD.post.snip_avz('whole_pathline_scene')
        # CFD.post.snip_avz('distrib_pathline')
        CFD.post.snip_model('model')
        CFD.post.create_contour('evap_out', 'evap_out')
        CFD.post.snip_picture('evap_out')

        CFD.post.txt_surface_integrals('volume-flow-rate', volume_face_list)
        CFD.post.txt_mass_flux()
        CFD.post.txt_surface_integrals('uniformity-index-area-weighted', pressure_face_list, 'velocity-magnitude')
        CFD.post.txt_surface_integrals('area-weighted-avg', pressure_face_list, 'total-pressure')
        CFD.post.txt_surface_integrals('area-weighted-avg', pressure_face_list, 'pressure')
        CFD.post.export_solution_data(['evap_out'], ['velocity-magnitude'])
        CFD.post.snip_mode_off()
        CFD.close_fluent()

        solve_jou.write(CFD.whole_jou)
        solve_jou.close()

        return solve_jou_path
