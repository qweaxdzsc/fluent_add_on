import fluent_tui
import os


class get_tui():
    def __init__(self, pamt, body_list, energy_check, K_dict, porous_list):
        self.d = pamt
        self.body_list = body_list
        self.energy_check = energy_check
        self.K_dict = K_dict
        self.porous_list = porous_list

        self.pre_info()
        self.get_mesh()
        self.get_solver()
        self.open_tui()

    def pre_info(self):
        whole_jou = ''
        project_title = self.d['project_name']
        version_name = self.d['version']
        whole_name = project_title + '-' + version_name
        cad_name = self.d['cad_name']
        case_out = self.d['file_path']

        self.CFD = fluent_tui.tui(whole_jou, project_title, version_name, case_out, cad_name)
        self.jou_mesh_path = case_out + '/' + whole_name + '-mesh-TUI.jou'
        self.jou_solve_path = case_out + '/' + whole_name + '-solve-TUI.jou'
        self.internal_list = self.porous_list.copy()

        for i in self.porous_list:
            self.internal_list[self.porous_list.index(i)] = i + '*'

        self.uni_face_list = self.internal_list
        self.pressure_face_list = (['inlet*', 'outlet*'] + self.internal_list).copy()

        print('pre info', self.jou_mesh_path)

    def get_mesh(self):
        mesh = self.CFD.mesh
        print('output journal in:', self.d['file_path'])
        jou_mesh = open(self.jou_mesh_path, 'w')

        dead_zone_list = []
        if 'valve' in self.body_list:
            dead_zone_list.append('valve')
            self.body_list.remove('valve')
        mesh_zone_list = self.body_list

        mesh.import_distrib()
        mesh.general_improve()
        mesh.fix_slivers()
        mesh.compute_volume_region()
        mesh.volume_mesh_change_type(dead_zone_list)
        if self.energy_check is True:
            mesh.retype_face(face_list=['hc*'], face_type='radiator')
            self.internal_list.remove('hc*')
            mesh.auto_mesh_volume(1.25, 'poly')
        else:
            mesh.auto_mesh_volume()
        mesh.auto_node_move()
        mesh.rename_cell(zone_list=mesh_zone_list)
        mesh.retype_face(face_list=['inlet*'], face_type='pressure-inlet')
        mesh.retype_face(face_list=self.internal_list, face_type='internal')
        mesh.retype_face(face_list=['outlet*'], face_type='outlet-vent')
        mesh.check_quality()
        mesh.prepare_for_solve()
        mesh.write_mesh()
        self.CFD.close_fluent()

        jou_mesh.write(self.CFD.whole_jou)
        jou_mesh.close()
        print('mesh_jou success')

    def get_solver(self):
        d = self.d
        self.CFD.whole_jou = ''
        setup = self.CFD.setup
        post = self.CFD.post
        print('output journal in:', d['file_path'])
        jou_solve = open(self.jou_solve_path, 'w')

        mass_flux_list = ['inlet*', 'outlet*']
        setup.read_mesh()
        setup.rescale()
        setup.turb_models()

        for i in self.porous_list:
            d1 = [d[i+'_x1'], d[i+'_y1'], d[i+'_z1']]
            d2 = [d[i+'_x2'], d[i+'_y2'], d[i+'_z2']]
            setup.porous_zone(i, d1, d2, d[i+'_c1'], d[i+'_c2'])

        setup.BC_type('inlet', 'mass-flow-inlet')
        setup.BC_type('outlet*()', 'outlet-vent')
        setup.BC_mass_flow_inlet('inlet', d['mass_inlet'])
        for i in self.K_dict:
            setup.BC_outlet_vent(self.K_dict[i], i)
        setup.solution_method()
        if self.energy_check is True:
            inlet_temp = float(d['temp_inlet']) + 273.15
            hc_temp = float(d['temp_hc']) + 273.15
            setup.energy_eqt('yes')
            setup.init_temperature('mass-flow-inlet', 'outlet-vent', inlet_temp)
            setup.heat_flux('hc_in', hc_temp)
            setup.heat_flux('hc_out', hc_temp)
            setup.report_definition('temperature', 'surface-areaavg', ['outlet*'], 'yes', 'temperature')
        setup.report_definition('volume', 'surface-volumeflowrate', ['inlet*'])
        setup.report_definition('mass-flux', 'surface-massflowrate', mass_flux_list, 'no')
        setup.report_definition('pressure', 'surface-areaavg', ['evap_in'])
        setup.convergence_criterion()
        setup.hyb_initialize()
        setup.start_calculate(260)
        setup.write_case_data()

        volume_face_list = ['inlet*', 'outlet*']

        post.create_result_file()
        post.set_background()
        if self.energy_check is True:
            post.txt_surface_integrals('area-weighted-avg', ['outlet*'], 'temperature')
            post.create_streamline('temp_pathline', 'inlet', '', 'temperature')
            post.snip_avz(8, 'temp_pathline')
        else:
            for i in self.porous_list:
                post.create_contour(i+'_out', i+'_out')
                post.snip_avz(7, i +'_out')
            post.create_streamline('whole_pathline', 'inlet')
            post.create_streamline('distrib_pathline', 'evap_out', [0, 15])
            post.snip_avz(5, 'whole_pathline')
            post.snip_avz(6, 'distrib_pathline')
            post.snip_model(10, 'model')

        post.txt_surface_integrals('volume-flow-rate', volume_face_list)
        post.txt_mass_flux()
        post.txt_surface_integrals('uniformity-index-area-weighted', self.uni_face_list, 'velocity-magnitude')
        post.txt_surface_integrals('area-weighted-avg', self.pressure_face_list, 'total-pressure')
        post.txt_surface_integrals('area-weighted-avg', self.pressure_face_list, 'pressure')
        post.snip_mode_off()
        self.CFD.close_fluent()

        jou_solve.write(self.CFD.whole_jou)
        jou_solve.close()

    def open_tui(self):
        os.system(self.jou_mesh_path)
        os.system(self.jou_solve_path)