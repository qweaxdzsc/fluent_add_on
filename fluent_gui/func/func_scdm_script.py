def create_import_script(file_path, original_cad_name, body_list, face_list, cad_save_path):
        cad_open_path = file_path + '/' + original_cad_name
        script_path = '%s/project_info.py' % file_path
        f = open(script_path, 'w')
        message = """
print('start script')
body_list = %s
body_number = len(body_list)

for i in range(body_number):
    # Create Sphere
    SphereBody.Create(Point.Create(MM(0), MM(0), MM(0)), Point.Create(MM(1), MM(1), MM(1)), ExtrudeType.None, None)
    # Rename 'Solid' to 'body name'
    selection = Selection.Create(GetRootPart().Bodies[0])
    result = RenameObject.Execute(selection,body_list[i])
    # Make Components
    selection = Selection.Create(GetRootPart().Bodies[0])
    result = ComponentHelper.MoveBodiesToComponent(selection, None)

# Delete sphere
selection = Selection.Create(GetRootPart().GetAllBodies())
result = Delete.Execute(selection)

# Insert From File
importOptions = ImportOptions.Create()
DocumentInsert.Execute(r"%s")

# Take out bodies
selections = Selection.Create(GetRootPart().GetAllBodies())
component = Selection.Create(GetRootPart())
result = ComponentHelper.MoveBodiesToComponent(selections, component, False, None)

# Delete old empty component
selection = Selection.Create(GetRootPart().Components[-1])
result = Delete.Execute(selection)

# face rename
face_list = %s
for i in range(len(face_list)):
    primarySelection = Selection.Create(GetRootPart())
    secondarySelection = Selection()
    result = NamedSelection.Create(primarySelection, secondarySelection)

for i in range(len(face_list)):
    result = NamedSelection.Rename("Group%%s"%%(i+1), face_list[i])

# options = ShareTopologyOptions()
# options.Tolerance = MM(0.01)
# result = ShareTopology.FindAndFix(options)

# save file
options = ExportOptions.Create()
DocumentSave.Execute(r"%s", options)
print('script finished')
""" % (body_list, cad_open_path, face_list, cad_save_path)
        f.write(message)
        f.close()

        return script_path


def create_rotate_script(pamt_dict, valve_number):
        file_path = pamt_dict['file_path']
        valve_percentage = pamt_dict['valve_rp']
        original_cad_name = pamt_dict['open_cad_name']
        valve_list = list(pamt_dict.keys())
        valve_list.sort()
        rotate_list = list()
        for i in valve_list:
            if '_td' in i and 'valve' in i:
                total_degree = pamt_dict[i]
                every_rotate = int(total_degree) / (100 / int(valve_percentage))
                rotate_list.append(every_rotate)
        script_path = '%s/rotate_valve.py' % file_path
        f = open(script_path, 'w')
        message = """        
save_path = r"%s"
file_name = r'%s'
rotate_angle = %s
valve_number = %s 

save_file = save_path + '\\\\' + file_name

options = ExportOptions.Create()
DocumentSave.Execute(r"%%s/%%s.scdoc" %%(save_path, file_name), options)

cnumber = len(GetRootPart().Components)

valve_name_list = ['valve%%s' %% (i+1) for i in range(valve_number)] 
valve_name_index = [0 for i in range(valve_number)]

for i in range(cnumber):
    for j in range(len(valve_name_list)):
        if valve_name_list[j] == GetRootPart().Components[i].GetName():
            valve_name_index[j] = i

print(valve_name_index)

for j in range(%s, 100, %s):
    for i in range(len(valve_name_index)):
        selection = Selection.Create(GetRootPart().Components[valve_name_index[i]])
        # Rotate About Z Handle
        anchor = Selection.CreateByNames('Axis%%s'%%(i+1))
        axis = Move.GetAxis(anchor)
        options = MoveOptions()
        result = Move.Rotate(selection, axis, DEG(rotate_angle[i]), options, Info1)
        # EndBlock

    # Save File
    options = ExportOptions.Create()
    DocumentSave.Execute(r"%%s_%%s.scdoc" %%(save_file, j), options)

""" % (file_path, original_cad_name, rotate_list, valve_number, valve_percentage, valve_percentage)
        f.write(message)
        f.close()

        return script_path