from fluent_command import tui_func
import os
import cgitb


class get_tui():
    def __init__(self, pamt, body_list, energy_check, K_dict, porous_list, up_list, dead_zone_list, internal_list):
        print(pamt, body_list, energy_check, K_dict, porous_list, up_list, dead_zone_list, internal_list)
        self.d = pamt
        self.body_list = body_list
        self.energy_check = energy_check
        self.K_dict = K_dict
        self.porous_list = porous_list
        self.up_list = up_list
        self.dead_zone_list = dead_zone_list
        self.internal_list = internal_list


        self.prepare_info()
        self.assemble_tui()
        self.open_tui()

    def assemble_tui(self):
        if 'valve' in self.body_list:
            self.angle_array()
            self.lin_mesh()
            self.lin_solver()
        else:
            self.meshing()
            self.solver()

    def prepare_info(self):
        whole_jou = ''
        project_title = self.d['project_name']
        version_name = self.d['version']
        whole_name = project_title + '-' + version_name
        cad_name = self.d['cad_name']
        case_out = self.d['file_path']

        self.CFD = tui_func.tui(whole_jou, project_title, version_name, case_out, cad_name)
        self.jou_mesh_path = case_out + '/' + whole_name + '-mesh-TUI.jou'
        self.jou_solve_path = case_out + '/' + whole_name + '-solve-TUI.jou'
        self.uni_face_list = self.porous_list.copy()

        for i in self.porous_list:
            self.uni_face_list[self.porous_list.index(i)] = i + '*'

        self.pressure_face_list = ['inlet*', 'outlet*'] + self.internal_list.copy()

    def meshing(self):
        mesh = self.CFD.mesh
        jou_mesh = open(self.jou_mesh_path, 'w')

        mesh_zone_list = self.body_list.copy()
        if 'fan' in self.body_list:
            mesh.simple_import(self.up_list, self.porous_list)
        else:
            mesh.import_distrib()
        mesh.stitch_free_face()
        mesh.general_improve()
        mesh.fix_slivers()
        mesh.compute_volume_region()
        mesh.volume_mesh_change_type(self.dead_zone_list)
        mesh.retype_face(face_list=['inlet*'], face_type='pressure-inlet')
        mesh.retype_face(face_list=self.internal_list, face_type='internal')
        mesh.retype_face(face_list=['outlet*'], face_type='outlet-vent')
        if self.energy_check is True:
            mesh.retype_face(face_list=['hc*'], face_type='radiator')
            mesh.auto_mesh_volume(1.25, 'poly')
        else:
            mesh.auto_mesh_volume()
        mesh.auto_node_move(0.85)
        mesh.rename_cell(zone_list=mesh_zone_list)
        mesh.check_quality()
        mesh.prepare_for_solve()
        mesh.write_mesh()
        self.CFD.close_fluent()

        jou_mesh.write(self.CFD.whole_jou)
        jou_mesh.close()

    def solver(self):
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

        if 'fan' in self.body_list:
            setup.BC_pressure_inlet('inlet')
            origin_xyz = [d['fan_ox'], d['fan_oy'], d['fan_oz']]
            axis_xyz = [d['fan_dx'], d['fan_dy'], d['fan_dz']]
            setup.rotation_volume(d['RPM'], origin_xyz, axis_xyz)
        else:
            setup.BC_type('inlet', 'mass-flow-inlet')
            setup.BC_mass_flow_inlet('inlet', d['mass_inlet'])
        setup.BC_type('outlet*()', 'outlet-vent')
        for i in self.K_dict:
            setup.BC_outlet_vent(self.K_dict[i], i)
        setup.solution_method()

        setup.report_definition('volume', 'surface-volumeflowrate', ['inlet*'])
        setup.report_definition('mass-flux', 'surface-massflowrate', mass_flux_list, 'no')
        setup.report_definition('pressure', 'surface-areaavg', self.pressure_face_list)

        if self.energy_check is True:
            inlet_temp = float(d['temp_inlet']) + 273.15
            hc_temp = float(d['temp_hc']) + 273.15
            setup.energy_eqt('yes')
            setup.init_temperature('mass-flow-inlet', 'outlet-vent', inlet_temp)
            setup.heat_flux('hc_in', hc_temp)
            setup.heat_flux('hc_out', hc_temp)
            setup.report_definition('temperature', 'surface-areaavg', ['outlet*'], 'yes', 'temperature')
            setup.convergence_criterion('temperature')
        else:
            setup.convergence_criterion('volume')
        setup.start_transcript()
        setup.set_timeout(60)
        setup.hyb_initialize()
        if 'fan' in self.body_list:
            setup.start_calculate(800)
        else:
            setup.start_calculate(260)
        setup.write_case_data()

        volume_face_list = ['inlet*', 'outlet*']
        post.create_result_file()
        post.set_background()
        porous_dir = {}
        for i in self.porous_list:
            d1 = [d[i + '_x1'], d[i + '_y1'], d[i + '_z1']]
            porous_dir[i] = d1
        post.create_view(porous_dir)
        if self.energy_check is True:
            post.txt_surface_integrals('area-weighted-avg', ['outlet*'], 'temperature')
            post.create_streamline('temp_pathline', 'inlet', '', 'temperature')
            post.snip_avz('temp_pathline')
        else:
            post.read_view()
            for i in self.porous_list:
                post.create_contour(i+'_out', i+'_out')
                post.snip_picture(i+'_out')
                # post.snip_avz(i + '_out')
            post.create_streamline('whole_pathline', 'inlet')
            # post.create_streamline('distrib_pathline', 'evap_in', [0, 12])
            post.snip_avz('whole_pathline')
            post.snip_picture('whole_pathline', 'yes')
            # post.snip_avz('distrib_pathline')
            post.snip_model('model')

        post.txt_surface_integrals('volume-flow-rate', volume_face_list)
        post.txt_mass_flux()
        post.txt_surface_integrals('uniformity-index-area-weighted', self.uni_face_list, 'velocity-magnitude')
        post.txt_surface_integrals('area-weighted-avg', self.pressure_face_list, 'total-pressure')
        post.txt_surface_integrals('area-weighted-avg', self.pressure_face_list, 'pressure')
        if 'fan' in self.body_list:
            post.txt_moment(origin_xyz, axis_xyz)
        post.snip_mode_off()
        self.CFD.close_fluent()

        jou_solve.write(self.CFD.whole_jou)
        jou_solve.close()

    def angle_array(self):
        d = self.d
        rotate_percente = float(d['valve_rp'])
        points = int(100/rotate_percente) - 1
        import numpy as np
        angle_array = np.linspace(rotate_percente, 100-rotate_percente, points, endpoint=True)  # define your angle range and points
        self.lin_array = [int(i) for i in angle_array]
        print(self.lin_array)

    def lin_mesh(self):
        mesh = self.CFD.mesh
        mesh_zone_list = self.body_list.copy()
        for i in mesh_zone_list:
            if 'valve' in i:
                mesh_zone_list.remove(i)

        jou_mesh = open(self.jou_mesh_path, 'w')
        for i in self.lin_array:
            cad_lin_name = '%s_%s' % (self.d['cad_name'], i)
            mesh.import_distrib(cad_name=cad_lin_name)
            mesh.general_improve(0.75)
            mesh.fix_slivers()
            mesh.compute_volume_region()
            mesh.volume_mesh_change_type(self.dead_zone_list)
            mesh.auto_mesh_volume(mesh_type='poly')
            mesh.auto_node_move(0.85, 6)
            mesh.rename_cell(zone_list=mesh_zone_list)
            mesh.retype_face(face_list=['inlet'], face_type='mass-flow-inlet')
            mesh.retype_face(face_list=self.internal_list, face_type='internal')
            mesh.retype_face(face_list=['hc*'], face_type='radiator')
            mesh.retype_face(face_list=['outlet*'], face_type='outlet-vent')
            mesh.prepare_for_solve()
            mesh.write_lin_mesh(i)

        mesh.switch_to_solver()

        jou_mesh.write(self.CFD.whole_jou)
        jou_mesh.close()

    def lin_solver(self):
        d = self.d
        self.CFD.whole_jou = ''
        setup = self.CFD.setup
        post = self.CFD.post
        print('output journal in:', d['file_path'])

        mass_flux_list = ['inlet*', 'outlet*']
        inlet_temp = float(d['temp_inlet'])+273.15
        hc_temp = float(d['temp_hc']) + 273.15

        jou_solve = open(self.jou_solve_path, 'w')

        setup.replace_lin_mesh(self.lin_array[0])
        # setup.read_lin_mesh(start_angle)
        setup.rescale()
        setup.turb_models()

        for i in self.porous_list:
            d1 = [d[i+'_x1'], d[i+'_y1'], d[i+'_z1']]
            d2 = [d[i+'_x2'], d[i+'_y2'], d[i+'_z2']]
            setup.porous_zone(i, d1, d2, d[i+'_c1'], d[i+'_c2'])

        if 'fan' in self.body_list:
            setup.BC_pressure_inlet('inlet')
            origin_xyz = [d['fan_ox'], d['fan_oy'], d['fan_oz']]
            axis_xyz = [d['fan_dx'], d['fan_dy'], d['fan_dz']]
            setup.rotation_volume(d['RPM'], origin_xyz, axis_xyz)
        else:
            setup.BC_type('inlet', 'mass-flow-inlet')
            setup.BC_mass_flow_inlet('inlet', d['mass_inlet'])

        setup.BC_type('outlet*()', 'outlet-vent')
        setup.solution_method()
        setup.energy_eqt('yes')
        # setup.BC_pressure_inlet('inlet')
        if 'fan' in self.body_list:
            setup.init_temperature('pressure-inlet', 'outlet-vent', inlet_temp)
        else:
            setup.init_temperature('mass-flow-inlet', 'outlet-vent', inlet_temp)

        for i in self.K_dict:
            setup.BC_outlet_vent(self.K_dict[i], i)
        setup.heat_flux('hc_in', hc_temp)
        setup.heat_flux('hc_out', hc_temp)
        setup.report_definition('temperature', 'surface-areaavg', ['outlet*'], 'yes', 'temperature')
        setup.report_definition('mass-flux', 'surface-massflowrate', mass_flux_list, 'no')
        setup.convergence_criterion('temperature')
        setup.hyb_initialize()
        setup.start_calculate(350)
        setup.write_lin_case_data(self.lin_array[0])
        post.simple_lin_post(self.lin_array[0])

        for i in self.lin_array[1:]:
            setup.replace_lin_mesh(i)
            setup.rescale()
            setup.init_temperature('mass-flow-inlet', 'outlet-vent', inlet_temp)
            setup.BC_mass_flow_inlet('inlet', d['mass_inlet'])
            setup.heat_flux('hc_in', hc_temp)
            setup.heat_flux('hc_out', hc_temp)
            setup.hyb_initialize()
            setup.start_calculate(350)
            setup.write_lin_case_data(i)
            post.simple_lin_post(i)

        jou_solve.write(self.CFD.whole_jou)
        jou_solve.close()

    def open_tui(self):
        os.system(self.jou_mesh_path)
        os.system(self.jou_solve_path)


if __name__ == "__main__":
    cgitb.enable(format='text')