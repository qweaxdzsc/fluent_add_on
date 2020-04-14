def create_scdm_script(file_path, original_cad_name, body_list, face_list, cad_save_path):
        cad_open_path = file_path + '/' + original_cad_name
        py_path = '%s/project_info.py' % file_path
        f = open(py_path, 'w')
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
DocumentInsert.Execute(r"%s", importOptions, GetMaps("1cf69ef6"))

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

        return py_path