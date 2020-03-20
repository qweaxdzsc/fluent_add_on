def create_scdm_script(file_path, body_list, face_list, cad_save_path):
        f = open('%s/project_info.py' % file_path, 'w')
        message = """
print('start script')
body_list = %s
body_number = len(body_list)

selection = Selection.Create(GetRootPart().GetAllBodies())
result = RenameObject.Execute(selection,"solid")

result = Copy.ToClipboard(Selection.Create(GetRootPart().GetAllBodies()))
result = Paste.FromClipboard()

# Delete Selection
selection = Selection.Create(GetRootPart().Components[:])
result = Delete.Execute(selection)

for i in range(body_number):
    result = Copy.ToClipboard(Selection.Create(GetRootPart().Bodies[0]))
    result = Paste.FromClipboard()

for i in range(body_number):
    selection = Selection.Create(GetRootPart().Bodies[-1-i])
    result = RenameObject.Execute(selection, body_list[i])

selection = Selection.Create(GetRootPart().Bodies[-body_number:])
result = ComponentHelper.CreateSeparateComponents(selection, None)

for i in range(body_number):
    selection = Selection.CreateByNames(body_list[i])
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
""" % (body_list, face_list, cad_save_path)
        f.write(message)
        f.close()