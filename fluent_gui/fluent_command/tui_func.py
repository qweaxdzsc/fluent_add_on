class tui(object):
    def __init__(self, whole_jou, project_title, version_name, case_path, cad_name):
        result_path = case_path + '\\' + 'result_' + project_title + '_' +version_name

        self.whole_jou = whole_jou
        self.project_title = project_title
        self.version_name = version_name
        self.case_out_path = case_path
        self.cad_path = case_path + '\\' + cad_name
        txt_out = result_path + '\\' + 'total_result.txt'
        self.txt_out = txt_out
        self.result_path = result_path
        self.size_field = self.case_out_path + '\\' + self.version_name + '.sf'

        self.mesh = Mesh(self)
        self.setup = Setup(self)
        self.post = Post(self)

    def read_journal(self, jou_path):
        text = """
/file/read-journal %s yes""" % jou_path
        self.whole_jou += text
        return self.whole_jou

    def close_fluent(self):
        text = """
/exit yes"""
        self.whole_jou += text
        return self.whole_jou


class Mesh(object):
    def __init__(self, tui):
        self.tui = tui
        print('create_object_mesh')

    def start_transcript(self, mode='mesh'):
        text = """
/file/start-transcript %s\\%s_%s_%s_transcript.txt ok
""" % (self.tui.case_out_path, self.tui.project_title, self.tui.version_name, mode)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def simple_import(self, specified_zone, porous_list, boi=False):
        self.import_CAD()
        self.size_scope_global()
        self.size_scope_curv('distrib_curv', 'distrib', 0.7, 5.5, 1.2, 16)
        self.size_scope_prox('distrib_prox', 'distrib', 0.8, 5.5, 1.2, 2)
        self.size_scope_curv('fan_blade_curv', 'fan_blade', 0.35, 1.5, 1.2, 16)
        self.size_scope_prox('fan_blade_prox', 'fan_blade', 0.8, 4, 1.2, 2)
        self.size_scope_prox('cutoff_curv', '*cutoff*', 0.5, 1, 1.2, 2)
        for i in specified_zone:
            self.size_scope_curv(i + '_curv', i, 0.8, 4.5, 1.2, 16)
            self.size_scope_prox(i + '_prox', i, 0.8, 4.5, 1.2, 2)
        self.size_scope_curv('fan_out_curv', 'fan_out', 1, 4, 1.2, 18)
        self.size_scope_prox('global_prox', '', 0.8, 5.5, 1.2, 1)
        self.size_scope_soft('inlet', '*inlet*', 14)
        for i in porous_list:
            self.size_scope_soft(i, '*'+i+'*', 4)
        # self.size_scope_curv('refine', 'fan_in', 1, 2.5, 1.2, 18)
        if boi:
            self.size_scope_boi('boi', '*boi*', 1.5)
        self.compute_size_field()
        self.write_size_field()
        self.import_surface_mesh()

    def import_CAD(self, cad_path='', tolerance=0.01, maxsize=8):
        if cad_path == '':
            cad_path = self.tui.cad_path
        text = """
/file/import/cad-options/save-PMDB yes
/file/import/cad-options/extract-features yes 0
/file/import/cad-geometry yes %s.scdoc mm cad-faceting yes
%s %s
""" % (cad_path, tolerance, maxsize)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def size_scope_global(self, min=0.3, max=14):
        text = """
/size-functions/set-global-controls {min} {max} 1.2
""".format(min=min, max=max)
        self.tui.whole_jou += text

    def size_scope_curv(self, scope_name, scope_zone, min_size, max_size, grow_rate, normal_angle):
        text = """
/scoped-sizing/create {scope_name} curvature face-zone yes yes *{scope_zone}* {min_size} {max_size} {grow_rate} {normal_angle}
""".format(scope_name=scope_name, scope_zone=scope_zone, min_size=min_size, max_size=max_size,
           grow_rate=grow_rate, normal_angle=normal_angle)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def size_scope_prox(self, scope_name, scope_zone, min_size, max_size, grow_rate, gap_cells):
        text = """
/scoped-sizing/create {scope_name} proximity edge-zone yes yes *{scope_zone}* {min_size} {max_size} {grow_rate} {gap_cells}
""".format(scope_name=scope_name, scope_zone=scope_zone, min_size=min_size, max_size=max_size,
           grow_rate=grow_rate, gap_cells=gap_cells)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def size_scope_soft(self, scope_name, scope_zone, max_size, grow_rate=1.2):
        text = """
/scoped-sizing/create {scope_name} soft face-zone yes yes "{scope_zone}" {max_size} {grow_rate}
""".format(scope_name=scope_name, scope_zone=scope_zone, max_size=max_size,
           grow_rate=grow_rate)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def size_scope_boi(self, scope_name, scope_zone, max_size, grow_rate=1.2):
        text = """
/scoped-sizing/create {scope_name} boi face-zone yes yes "{scope_zone}" {max_size} {grow_rate}
""".format(scope_name=scope_name, scope_zone=scope_zone, max_size=max_size,
           grow_rate=grow_rate)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def compute_size_field(self):
        text = """
/scoped-sizing/compute
"""
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def write_size_field(self, size_field_path=''):
        if not size_field_path == '':
            self.tui.size_field = size_field_path
        text = """
/file/write-size-field %s yes
""" % self.tui.size_field
        self.tui.whole_jou += text

        return self.tui.whole_jou

    def import_surface_mesh(self, cad_path=''):
        if cad_path == "":
            cad_path = self.tui.cad_path
        text = """
/file/import/cad-options/save-PMDB no
/file/import/cad-options/extract-features yes 10
/file/import/cad-geometry yes %s.scdoc.pmdb no mm cfd-surface-mesh yes %s yes
""" % (cad_path, self.tui.size_field)

        self.tui.whole_jou += text
        return self.tui.whole_jou

    def import_distrib(self, cad_name='', min_size=0.7, max_size=5, grow_rate=1.2, normal_angle=16, gap_cell=2):
        if cad_name == '':
            cad_path = self.tui.cad_path
        else:
            cad_path = self.tui.case_out_path + '\\' + cad_name
        text = """
/file/import/cad-options/extract-features yes 10
/file/import/cad-geometry yes {cad_path}.scdoc no 
mm cfd-surface-mesh no {min_size} {max_size} {grow_rate} yes yes 
{normal_angle} {gap_cell} edges yes no yes
/objects/merge *() {project_title}
""".format(cad_path=cad_path, min_size=min_size, max_size=max_size, grow_rate=grow_rate,
           normal_angle=normal_angle, gap_cell=gap_cell, project_title=self.tui.project_title)

        self.tui.whole_jou += text
        return self.tui.whole_jou

    def import_lin_cad(self, cad_name, specified_zone, porous_list, boi=False):
        cad_path = self.tui.case_out_path + '\\' + cad_name
        self.import_CAD(cad_path)
        self.size_scope_global()
        self.size_scope_curv('distrib_curv', 'distrib', 1, 5.5, 1.2, 20)
        self.size_scope_prox('distrib_prox', 'distrib', 1, 5.5, 1.2, 2)
        self.size_scope_curv('valve_curv', 'valve', 0.3, 4, 1.2, 14)
        self.size_scope_prox('valve_prox', 'valve', 0.4, 4, 1.2, 2)
        for i in specified_zone:
            self.size_scope_curv(i + '_curv', i, 1, 4.5, 1.2, 20)
            self.size_scope_prox(i + '_prox', i, 1, 4.5, 1.2, 2)
        self.size_scope_prox('global_prox', '', 1, 5.5, 1.2, 1)
        self.size_scope_soft('inlet', '*inlet*', 12)
        for i in porous_list:
            self.size_scope_soft(i, '*' + i + '*', 3)
        if boi:
            self.size_scope_boi('boi', '*boi*', 1.5)
        self.compute_size_field()
        self.write_size_field()
        self.import_surface_mesh(cad_path)

    def delete_boundary(self, boundary_name):
        text = """
/boundary/manage/delete %s() yes q q q
""" % boundary_name
        self.tui.whole_jou += text

    def stitch_free_face(self, tolerance=0.2):
        text = """
/diagnostics/face-connectivity/fix-free-faces objects *() stitch %s 3
""" % tolerance
        self.tui.whole_jou += text

    def general_improve(self, quality=0.75, feature_angle=30, iterations=10):
        text = """
/diagnostics/quality/general-improve objects *() skewness %s %s %s yes
""" % (quality, feature_angle, iterations)
        self.tui.whole_jou += text

    def collapse_area(self, area_size=0.015, relative_max=0.1, iterations=5, preserve_boundary='yes'):
        text = """
/diagnostics/quality/collapse objects *() area %s %s %s %s q
""" % (area_size, relative_max, iterations, preserve_boundary)
        self.tui.whole_jou += text

    def fix_slivers(self, skewness=0.8):
        text = """
/diagnostics/face-connectivity/fix-slivers objects *() 0 {skewness}
/diagnostics/face-connectivity/fix-slivers objects *() 0 {skewness}
/diagnostics/face-connectivity/fix-slivers objects *() 0 {skewness}
/diagnostics/face-connectivity/fix-slivers objects *() 0 {skewness}
""".format(skewness=skewness)
        self.tui.whole_jou += text

    def fix_steps(self, angle=30, step_width=0.05):
        text = """
/diagnostics/face-connectivity/fix-steps objects *() {critical_angle} {step_width} smooth q
/diagnostics/face-connectivity/fix-steps objects *() {critical_angle} {step_width} smooth q
/diagnostics/face-connectivity/fix-steps objects *() {critical_angle} {step_width} smooth q
/diagnostics/face-connectivity/fix-steps objects *() {critical_angle} {step_width} smooth q
""".format(critical_angle=angle, step_width=step_width)
        self.tui.whole_jou += text

    def fix_combo(self):
        self.stitch_free_face()
        self.general_improve()
        self.fix_slivers()
        self.fix_steps(20, 0.1)
        self.collapse_area()
        self.fix_slivers()
        self.fix_steps(20, 0.1)
        self.fix_slivers()
        return self.tui.whole_jou

    def valve_rotate(self, rotate_angle, valve_dir, valve_origin):
        text = """
boundary/manage/rotate valve*()
{rotate_angle} {valve_dx} {valve_dy} {valve_dz}() {valve_origin_x} {valve_origin_y} {valve_origin_z}() no
""".format(rotate_angle=rotate_angle, valve_dx=valve_dir[0], valve_dy=valve_dir[1], valve_dz=valve_dir[2],
           valve_origin_x=valve_origin[0], valve_origin_y=valve_origin[1], valve_origin_z=valve_origin[2])
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def compute_volume_region(self):
        text = """
/objects/volumetric-regions/compute * no
"""
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def volume_mesh_change_type(self, dead_zone_list=[]):
        text = """
/objects/volumetric-regions/change-type * *() fluid
"""
        self.tui.whole_jou += text
        if not dead_zone_list:
            pass
        else:
            for i in dead_zone_list:
                dead_zone = '/objects/volumetric-regions/change-type * *%s*() dead' % (i)
                self.tui.whole_jou += dead_zone
        return self.tui.whole_jou

    def auto_mesh_volume(self, grow_rate=1.22, mesh_type='tet'):
        text = """
/parallel/auto-partition yes q q
/mesh/tet/controls/cell-sizing size-field
/mesh/poly/controls/cell-sizing size-field
/mesh/auto-mesh * yes pyramids {mesh_type} no
""".format(rate=grow_rate, mesh_type=mesh_type)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def auto_node_move(self, skewness=0.8, preserve_boundary='yes', iterations=5, quality_method="inverse-ortho-quality"):
        text = """
/report/quality-method/%s
/mesh/modify/auto-node-move *() *() %s 50 120 %s %s
""" % (quality_method, skewness, preserve_boundary, iterations)
        self.tui.whole_jou += text

    def rename_cell(self, zone_list):
        for i in range(len(zone_list)):
            text = """
/mesh/manage/name *{zone}* {zone}
""".format(zone=zone_list[i])
            self.tui.whole_jou += text
        return self.tui.whole_jou

    def retype_face(self, face_list, face_type):
        text1 = """
/boundary/manage/type"""
        for i in face_list:
            text1 += " %s" % (i)
        text2="""() %s
        """ % (face_type)
        self.tui.whole_jou += text1 + text2
        return self.tui.whole_jou

    def delete_cell(self):
        text = """
/objects/volumetric-regions/delete-cells * *() q
"""
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def check_quality(self):
        text = """
/mesh/check-quality"""
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def write_case(self):
        text = """
/file/write-case %s\\%s_%s_mesh.cas yes
""" % (self.tui.case_out_path, self.tui.project_title, self.tui.version_name)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def write_mesh(self):
        text = """
/file/write-mesh %s\\%s_%s_mesh.msh yes
""" % (self.tui.case_out_path, self.tui.project_title, self.tui.version_name)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def write_lin_mesh(self, valve_angle):
        mesh_path = self.tui.case_out_path + '\\lin_mesh'
        import os
        if os.path.exists(mesh_path) == True:
            print('The mesh directory already exist, please check the path')
        else:
            os.makedirs(mesh_path)
        text = """
/file/write-mesh {mesh_path}\\{project_name}_{version}_{valve_angle}_mesh.msh yes
""".format(mesh_path=mesh_path, project_name=self.tui.project_title, version=self.tui.version_name,
           valve_angle=valve_angle)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def prepare_for_solve(self):
        text = """
/mesh/prepare-for-solve yes
"""
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def switch_to_solver(self):
        text = """
/switch-to-solution-mode yes
"""
        self.tui.whole_jou += text
        return self.tui.whole_jou


class Setup(object):
    def __init__(self, tui):
        self.tui = tui
        print('create_object_setup')

    def start_transcript(self, mode='solve'):
        text = """
/file/start-transcript %s\\%s_%s_%s_transcript.txt ok
""" % (self.tui.case_out_path, self.tui.project_title, self.tui.version_name, mode)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def set_timeout(self, minutes=5):
        text = """
/file/set-idle-timeout yes {time_out} no
""".format(time_out=minutes)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def read_mesh(self):
        text = """
/file/read %s\\%s_%s_mesh.msh yes
""" % (self.tui.case_out_path, self.tui.project_title, self.tui.version_name)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def read_case_data(self, plus=''):
        text = """
/file/read-case-data %s\\%s_%s_%s.cas yes
""" % (self.tui.case_out_path, self.tui.project_title, self.tui.version_name, plus)
        self.tui.whole_jou += text

    def read_lin_mesh(self, valve_angle):
        mesh_path = self.tui.case_out_path + '\\lin_mesh'
        text = """
/file/read {mesh_path}\\{project_name}_{version}_{valve_angle}_mesh.msh yes
""".format(mesh_path=mesh_path, project_name=self.tui.project_title, version=self.tui.version_name,
           valve_angle=valve_angle)

        self.tui.whole_jou += text
        return self.tui.whole_jou

    def replace_lin_mesh(self, valve_angle):
        mesh_path = self.tui.case_out_path + '\\lin_mesh'
        text = """
/file/replace-mesh {mesh_path}\\{project_name}_{version}_{valve_angle}_mesh.msh yes
""".format(mesh_path=mesh_path, project_name=self.tui.project_title, version=self.tui.version_name,
           valve_angle=valve_angle)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def rescale(self, scale_factor=0.001):
        text = """
/mesh/scale {0} {0} {0}
""".format(scale_factor)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def convert_polymesh(self):
        text = """
/mesh/polyhedra/convert q
"""
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def turb_models(self, model='ke-standard'):
        text = """
/define/models/viscous/%s yes q
""" % (model)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def energy_eqt(self, switch):
        text = """
/define/models/energy %s no no no yes q
""" % (switch)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def wall_treatment(self, treatment):
        text = """
/define/models/viscous/near-wall-treatment %s yes
""" % (treatment)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def expression(self, name, definition):
        text = """
/define/named-expressions/add %s definition "%s" q q q
""" % (name, definition)
        self.tui.whole_jou += text

    def rotation_volume(self, rpm, origin_xyz, axis_xyz, rotating_part='fan'):
        text = """
/define/units angular-velocity rpm
define/boundary-conditions/fluid {part_name} no no no
yes -1 no {fan_speed}
no 0 no 0 no 0
no {origin_x} no {origin_y} no {origin_z}
no {axis_x} no {axis_y} no {axis_z}
none no no no no no
""".format(fan_speed=rpm, origin_x=origin_xyz[0], origin_y=origin_xyz[1], origin_z=origin_xyz[2],
            axis_x=axis_xyz[0], axis_y=axis_xyz[1], axis_z=axis_xyz[2], part_name=rotating_part)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def porous_zone(self, porous_name, Direction1, Direction2, C1, C2):
        text = """
/define/boundary-conditions/fluid {part_name} no no no no 
no 0 no 0 no 0 no 0 no 1 no 0 
no no no 
yes no no {D1_x} no {D1_y} no {D1_z} no {D2_x} no {D2_y} no {D2_z}
yes no {Viscous_Resistance} no 1e10 no 1e10 yes no {Inertial_Resistence} no 1e5 no 1e5
0 0 no 1 constant 1 no
""".format(part_name=porous_name, D1_x=Direction1[0], D1_y=Direction1[1], D1_z=Direction1[2],
           D2_x=Direction2[0], D2_y=Direction2[1], D2_z=Direction2[2], Viscous_Resistance=C1,
           Inertial_Resistence=C2)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def BC_type(self, face_name, face_type):
        text = """
/define/boundary-conditions/zone-type %s %s
""" % (face_name, face_type)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def BC_pressure_inlet(self, face_name, initial_pressure=0, turb_intensity=5, turb_length_scale=0.005):
        text = """
/define/boundary-conditions/set/pressure-inlet %s() 
p0 no %s
ke-spec no yes turb-intensity %s turb-length-scale %s q
""" % (face_name, initial_pressure, turb_intensity, turb_length_scale)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def BC_mass_flow_inlet(self, face_name, mass_flow, turb_intensity=5, turb_length_scale=0.005):
        text = """
/define/boundary-conditions/set/mass-flow-inlet %s() 
mass-flow no %s
direction-spec no yes
ke-spec no yes turb-intensity %s turb-length-scale %s q
""" % (face_name, mass_flow, turb_intensity, turb_length_scale)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def BC_pressure_outlet(self, face_list, pressure=0, turb_intensity=5, turb_length_scale=0.005):
        face_name = ''
        for i in face_list:
            face_name += ' ' + i
        text = """
/define/boundary-conditions/set/pressure-outlet%s() 
gauge-pressure no %s
ke-spec no yes turb-intensity %s turb-length-scale %s q
""" % (face_name, pressure, turb_intensity, turb_length_scale)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def BC_inlet_vent(self, face_name, loss_coefficient=0, initial_pressure=0, turb_intensity=5,
                      turb_length_scale=0.005):
        text = """
/define/boundary-conditions/set/inlet-vent %s()
loss-coefficient constant %s
p0 no %s
ke-spec no yes turb-intensity %s turb-length-scale %s q
""" % (face_name, loss_coefficient, initial_pressure, turb_intensity, turb_length_scale)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def BC_outlet_vent(self, loss_coefficient=0.0, outlet_name='outlet*', initial_pressure=0, turb_intensity=5,
                       turb_length_scale=0.005):
        text = """
/define/boundary-conditions/set/outlet-vent %s()
loss-coefficient constant %s
p0 no %s
ke-spec no yes turb-intensity %s turb-length-scale %s q
""" % (outlet_name, loss_coefficient, initial_pressure, turb_intensity, turb_length_scale)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def init_temperature(self, inlet_type, outlet_type, init_temperature):
        text = """
/define/boundary-conditions/set/{inlet_type} inlet*() t0 no {init_temp} q
/define/boundary-conditions/set/{outlet_type} outlet*() t0 no {init_temp} q
""".format(inlet_type=inlet_type, outlet_type=outlet_type, init_temp=init_temperature)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def heat_flux(self, face_name, temperature, heat_transfer_coefficient=1000000, heat_flux=0):
        text = """
/define/boundary-conditions/set/radiator %s() temperature %s hc constant %s heat-flux %s q
""" % (face_name, temperature, heat_transfer_coefficient, heat_flux)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def solution_method(self):
        text = """
/solve/set/p-v-coupling 24
/solve/set/discretization-scheme/k 1
/solve/set/discretization-scheme/epsilon 1
/solve/set/pseudo-transient yes yes 1 1 0
/solve/set/warped-face-gradient-correction/enable yes no q
"""
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def switch_equations(self, equation_name, switch=True):
        """
        :param equation_name: flow, ke, temperature
        :param switch: True, false
        :return:
        """
        if switch:
            state = 'yes'
        else:
            state = 'no'
        text = """
/solve/set/equations/%s %s
""" % (equation_name, state)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def report_definition(self, report_name, report_type, surface_list, per_surface='yes', field='pressure'):
        surface_name = ''
        for i in surface_list:
            surface_name += ' ' + i
        text = """
/solve/report-definitions/add {report_name} {report_type}
field {field}
per-surface {per_surface}
surface-names{surface_name}()
average-over 1
q

/solve/report-files/add {report_name}
report-defs {report_name}() 
file-name .\\{report_name}.out
print yes
q

/solve/report-plots/add {report_name}
report-defs {report_name}()
q
""".format(report_name=report_name, report_type=report_type, surface_name=surface_name,
           per_surface=per_surface, field=field)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def convergence_criterion(self, type=None, switch=3, frequency=10):
        if type == 'pressure' or type == 'temperature':
            text = """
solve/monitors/residual/criterion-type %s
/solve/convergence-conditions/frequency %s
/conv-reports add %s-stable
report-defs %s initial-values-to-ignore 250 previous-values-to-consider 20 
stop-criterion 0.0002 print yes active yes
q q q
""" % (switch, frequency, type, type)
        elif type == 'volume':
            text = """
/solve/monitors/residual/criterion-type %s
/solve/convergence-conditions/frequency %s
conv-reports add %s-stable
report-defs volume initial-values-to-ignore 1000 previous-values-to-consider 20 
stop-criterion 0.0001 print yes active yes
q q q
""" % (switch, frequency, type)
        else:
            text = """
solve/monitors/residual/criterion-type %s
""" % (switch)

        self.tui.whole_jou += text
        return self.tui.whole_jou

    def input_summary(self):
        text = """
/report/summary yes %s/input.txt yes
""" % self.tui.case_out_path
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def hyb_initialize(self):
        text = """
/solve/initialize/hyb-initialization yes
"""
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def std_initialize(self):
        text = """
/solve/initialize/initialize-flow yes
"""
        self.tui.whole_jou += text

    def start_calculate(self, iterations=1000):
        text = """
/solve/iterate/%s yes
""" % iterations
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def write_case_data(self):
        text = """
/file/write-case-data/ %s\\%s_%s yes
""" % (self.tui.case_out_path, self.tui.project_title, self.tui.version_name)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def write_lin_case_data(self, valve_angle):
        text = """
/file/write-case-data/ {case_path}\\lin_case\\{project_name}_{version}_{valve_angle}\\{project_name}_{version}_{valve_angle} yes
""".format(case_path=self.tui.case_out_path, project_name=self.tui.project_title, version=self.tui.version_name,
           valve_angle=valve_angle)
        self.tui.whole_jou += text
        return self.tui.whole_jou


class Post(object):
    def __init__(self, tui):
        self.tui = tui
        print('create_object_post')

    def create_result_file(self):
        import os
        if os.path.exists(self.tui.result_path) == True:
            print('The result path already exist, please check the path')
        else:
            os.makedirs(self.tui.result_path)

    def simple_lin_post(self, valve_angle, field='temperature'):
        self.tui.result_path = self.tui.case_out_path + \
                           '\\lin_case\\{project_name}_{version}_{valve_angle}\\result'.format(
                               project_name=self.tui.project_title, version=self.tui.version_name, valve_angle=valve_angle)
        self.create_result_file()
        self.tui.txt_out = self.tui.result_path + '\\%s_%s.txt' % (self.tui.project_title, valve_angle)
        self.txt_surface_integrals('area-weighted-avg', ['outlet*'], 'temperature')
        self.txt_surface_integrals('volume-flow-rate', ['inlet*', 'outlet*'])
        self.txt_mass_flux()
        pressure_face_list = ['inlet*', 'evap_in', 'evap_out', 'hc*', 'outlet*']
        self.txt_surface_integrals('area-weighted-avg', pressure_face_list, 'total-pressure')
        self.txt_surface_integrals('area-weighted-avg', pressure_face_list, 'pressure')

        self.set_background()
        self.delete_display_object('view_model')
        self.delete_display_object('whole_pathline_scene')
        self.create_viewing_model()
        self.create_streamline('whole_pathline', 'inlet*', field_type=field, skip='2')
        self.create_scene('whole_pathline')
        self.snip_avz('whole_pathline_scene')

    def txt_surface_integrals(self, report_type, face_list, field=''):
        if field == '':
            pass
        else:
            field = field + ' '
        face_name = ''
        for i in face_list:
            face_name += ' ' + i
        text = """
/report/surface-integrals/%s%s() %syes %s yes q
""" % (report_type, face_name, field, self.tui.txt_out)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def txt_mass_flux(self):
        text = """
/report/fluxes/mass-flow no inlet* outlet*()
yes %s yes q
""" % self.tui.txt_out
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def txt_moment(self, origin_xyz, axis_xyz, fan_name='fan_blade'):

        text = """
/report/forces/wall-moments no 
{fan_name}() {origin_x} {origin_y} {origin_z} {axis_x} {axis_y} {axis_z} yes {out_path} yes
""".format(fan_name=fan_name, origin_x=origin_xyz[0], origin_y=origin_xyz[1], origin_z=origin_xyz[2],
            axis_x=axis_xyz[0], axis_y=axis_xyz[1], axis_z=axis_xyz[2], out_path=self.tui.txt_out)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def delete_display_object(self, display_object='view_model'):
        text = """
/display/objects/delete %s
""" % display_object
        self.tui.whole_jou += text

    def create_viewing_model(self):
        text = """
/display/objects/create mesh view_model options edges no q 
surfaces-list *%s*() q
""" % self.tui.project_title
        self.tui.whole_jou += text

    def create_contour(self, contour_name, contour_face, range='auto-range-on', field='velocity-magnitude',
                       level=10):
        if range == 'auto-range-on':
            pass
        else:
            range = 'auto-range-off clip-to-range yes maximum %s minimum %s' % (range[-1], range[0])
        text = """
/display/objects/creat contour %s
surfaces-list %s()    
field %s
filled yes
range-option %s 
global-range no
q
color-map size %s format %%0.1f
q q
""" % (contour_name, contour_face, field, range, level)
        self.tui.whole_jou += text

    def create_vector(self, vector_name, vector_face, range='auto-range-on', field='velocity', vector_scale=5,
                      level=25):
        if range == 'auto-range-on':
            pass
        else:
            range = 'auto-range-off clip-to-range yes maximum %s minimum %s' % (range[-1], range[0])
        text = """
/display/objects/creat vector %s
surfaces-list %s()    
vector-field %s
range-option %s 
global-range no
q
scale scale-f %s
q
color-map size %s format %%0.1f
q q
""" % (vector_name, vector_face, field, range, vector_scale, level)
        self.tui.whole_jou += text

    def create_iso_surface(self, surface_name, value_type, iso_value, from_surface='', from_zone='*'):
        text = """
/surface/iso-surface %s %s %s() %s() %s()
""" % (value_type, surface_name, from_surface, from_zone, iso_value)
        self.tui.whole_jou += text

    def create_streamline(self, line_name, surface_name, range='', field_type='velocity-magnitude', line_size='10', line_step='2000', skip='5'):
        if range == '':
            pass
        else:
            range = 'range clip-to-range max-value %s min-value %s q' % (range[-1], range[0])
        text = """
/display/objects/create pathlines {line_name} field {field_type} {range} 
color-map format %0.1f size {line_size} q step {line_step} skip {line_skip} surfaces-list {surface_name}() q
""".format(line_name=line_name, field_type=field_type, range=range, line_size=line_size, line_step=line_step,
            line_skip=skip, surface_name=surface_name)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def create_scene(self, graphic_object):
        text = """
/display/objects/create scene %s_scene graphics-objects 
add "view_model" transparency 75 q
add "%s" 
q q q
""" % (graphic_object, graphic_object)
        self.tui.whole_jou += text

    def create_view(self, dir_dict):
        view_file = self.tui.case_out_path + '\\' + self.tui.version_name + '.vw'
        view_setting = '(whole ((0 -1 0) (0 0 0) (0 0 1) 0.5 0.5 "orthographic") #(1. 0. 0. 0. 0. 1. 0. 0. 0. 0. 1. 0. 0. 0. 0. 1.))' \
                       '(distrib ((0 -1 0) (0 0 0) (0 0 1) 0.5 0.5 "orthographic") #(1. 0. 0. 0. 0. 1. 0. 0. 0. 0. 1. 0. 0. 0. 0. 1.))'
        for view in dir_dict.keys():
            x = float(dir_dict[view][0])
            y = float(dir_dict[view][1])
            z = float(dir_dict[view][2])
            if x < 0:
                position = '(%s %s %s)' % (-x, -y, -z)
            elif z < 0:
                position = '(%s %s %s)' % (-x, -y, -z)
            else:
                position = '(%s %s %s)' % (x, y, z)
            view_setting += """(%s (%s (0 0 0) (0 0 1) 0.5 0.5 "orthographic") #(1. 0. 0. 0. 0. 1. 0. 0. 0. 0. 1. 0. 0. 0. 0. 1.))""" \
                            % (view, position)
        code = """
(38 ((
(view-list (
%s
)))))
""" % view_setting
        with open(view_file, 'w') as f:
            f.write(code)

    def read_view(self):
        view_file = self.tui.case_out_path + '\\' + self.tui.version_name + '.vw'
        text = """
/views/read-views %s ok
""" % view_file
        self.tui.whole_jou += text

    def set_background(self):
        text = """
/views/camera/projection orthographic
/display/set/colors/color-by-type yes
;/display/set/filled-mesh no
;/display/set/rendering-options/surface-edge-visibility yes no yes no
/display/set/colors/inlet-faces "foreground"
/display/set/colors/outlet-faces "foreground" q
"""
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def snip_residual(self, window_number=1):
        text = """
/display/set-window {window_number}
/display/set/picture/driver/jpeg
/display/set/picture/use-window-resolution no
/display/set/picture/x-resolution 4096
/display/set/picture/y-resolution 2160
/display/save-picture {out_path}\\residual.jpg yes
""".format(window_number=window_number, out_path=self.tui.result_path)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def snip_picture(self, graphic_name, lights_on='no', window_number=9):
        end_index = graphic_name.index('_')
        view_name = graphic_name[:end_index]
        text = """
/display/open-window {window_number}
/display/set-window {window_number}
/display/set/lights/lights-on {light}
/display/set/lights/headlight-on {light}
/display/objects/display/{graphic_name}
/views/restore-view {view_name}
/views/auto-scale
/display/set/lights/lights-on {light}
/display/set/lights/headlight-on {light}
/display/set/picture/driver/jpeg
/display/set/picture/use-window-resolution no
/display/set/picture/x-resolution 4096
/display/set/picture/y-resolution 2160
/display/save-picture {out_path}\\{graphic_name}.jpg yes
/display/close-window {window_number}
""".format(window_number=window_number, graphic_name=graphic_name,
           out_path=self.tui.result_path, view_name=view_name, light=lights_on)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def snip_avz(self, graphic_name, window_number=10):
        text = """
/display/open-window {window_number}
/display/objects/display/{graphic_name}
/display/set/picture/driver/avz
/display/save-picture {out_path}\\{graphic_name}.avz yes
/display/close-window {window_number}
""".format(window_number=window_number, graphic_name=graphic_name,
           out_path=self.tui.result_path)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def snip_model(self, picture_name, window_number=11):
        text = """
;model view
/display/open-window %s
/display/set/colors/color-by-type no
/display/set/filled-mesh yes
/display/set/rendering-options/surface-edge-visibility no
/display/set/mesh-display-configuration/meshing 
/display/mesh-outline
/display/set/picture/driver/avz
/display/save-picture %s\\%s.avz yes
""" % (window_number, self.tui.result_path, picture_name)
        self.tui.whole_jou += text
        return self.tui.whole_jou

    def snip_mode_off(self):
        self.tui.whole_jou += """
/display/set/overlays no
/display/set/mesh-display-configuration solution
q
"""
