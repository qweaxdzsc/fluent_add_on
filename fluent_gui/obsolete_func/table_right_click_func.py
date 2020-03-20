
# def show_outlet_name(self):
#     # if self.import_outlet:
#     #     self.outlet_name_and_K()
#     # else:
#     #     self.outlet_rename = subUI_outlet_choose()
#     #     self.outlet_rename.show()
#     #     self.outlet_rename.chosed_btn.clicked.connect(self.receive_outlet_name)
#     #     self.outlet_rename.chosed_btn.clicked.connect(self.outlet_name_and_K)
#
#     self.outlet_assign = subUI_outlet_assign()
#     self.outlet_assign.show()
#     self.outlet_assign.outlet_K_signal.connect(self.receive_outlet_name)
#
# def receive_outlet_name(self, outlet_dict):
#     # self.outlet_list = self.outlet_rename.outlet_list
#     # self.outlet_K = [0 for i in self.outlet_list]
#     self.K_dict = outlet_dict
#     self.outlet_list = list(outlet_dict.keys())
#     self.outlet_K = list(outlet_dict.values())
#     self.face_list.extend(self.outlet_list)
#     self.update_project_info()
#     if self.need_launch_CAD:
#         self.launchCAD()
#
# # def outlet_name_and_K(self):
#     # self.dialog_tip = subUI_outlet_assign()
#     # self.dialog_tip.show()
#
#     # self.dialog_tip.rename_btn.clicked.connect(self.dialog_tip.close)
#     # self.dialog_tip.rename_btn.clicked.connect(self.update_project_info)
#
# #     self.inlet_n = self.inlet_number.value()
# #     self.outlet_n = len(self.outlet_list)
# #
# #     self.dialog_tip.rename_table.setRowCount(max(self.inlet_n, self.outlet_n))
# #     self.dialog_tip.rename_table.setFixedHeight(max(self.inlet_n, self.outlet_n)*35+35)
# #
# #     for i in range(self.inlet_n):
# #         new_item = QTableWidgetItem("%s" % (self.face_list[i]))
# #         self.dialog_tip.rename_table.setItem(i, 0, new_item)
# #
# #     for i in range(len(self.outlet_list)):
# #         new_item = QTableWidgetItem("%s" % (self.outlet_list[i]))
# #         self.dialog_tip.rename_table.setItem(i, 1, new_item)
# #
# #         new_item = QTableWidgetItem("%s" % (self.outlet_K[i]))
# #         self.dialog_tip.rename_table.setItem(i, 2, new_item)
# #
# #     self.dialog_tip.rename_table.customContextMenuRequested.connect(self.generate_cal_menu)
# #
# # def generate_cal_menu(self, pos):
# #     column_num = -1
# #     for i in self.dialog_tip.rename_table.selectionModel().selection().indexes():
# #         column_num = i.column()
# #         self.K_row = i.row()
# #
# #     if column_num == 2:
# #         cal_menu = QMenu()
# #         cal_action = cal_menu.addAction(u"计算K值")
# #         action = cal_menu.exec_(self.dialog_tip.rename_table.mapToGlobal(pos))
# #         if action == cal_action:
# #             self.K_cal = subUI_cal_K()
# #             self.K_cal.show()
# #             self.K_cal.K_result.connect(self.K_result)
#
# # def K_result(self, K):
# #     modify_item = QTableWidgetItem(K)
# #     self.dialog_tip.rename_table.setItem(self.K_row, 2, modify_item)
# #     self.K_cal.close()
#
# def update_project_info(self):
#     # self.outlet_list, self.K_list = [], []
#     #
#     # for i in range(self.inlet_n):
#     #     self.face_list[i] = self.dialog_tip.rename_table.item(i, 0).text()
#     #
#     # for i in range(self.dialog_tip.rename_table.rowCount()):
#     #     try:
#     #         self.outlet_list.append(self.dialog_tip.rename_table.item(i, 1).text())
#     #         self.K_list.append(self.dialog_tip.rename_table.item(i, 2).text())
#     #     except Exception as e:
#     #         continue
#     # self.K_dict = dict(zip(self.outlet_list, self.K_list))
#     self.f = open('%s/project_info.py' % (self.pamt['file_path']), 'w')
#     message = """
# print('start script')
# body_list = %s
# body_number = len(body_list)
#
# selection = Selection.Create(GetRootPart().GetAllBodies())
# result = RenameObject.Execute(selection,"solid")
#
# result = Copy.ToClipboard(Selection.Create(GetRootPart().GetAllBodies()))
# result = Paste.FromClipboard()
#
# # Delete Selection
# selection = Selection.Create(GetRootPart().Components[:])
# result = Delete.Execute(selection)
#
# for i in range(body_number):
#     result = Copy.ToClipboard(Selection.Create(GetRootPart().Bodies[0]))
#     result = Paste.FromClipboard()
#
# for i in range(body_number):
#     selection = Selection.Create(GetRootPart().Bodies[-1-i])
#     result = RenameObject.Execute(selection, body_list[i])
#
# selection = Selection.Create(GetRootPart().Bodies[-body_number:])
# result = ComponentHelper.CreateSeparateComponents(selection, None)
#
# for i in range(body_number):
#     selection = Selection.CreateByNames(body_list[i])
#     result = Delete.Execute(selection)
#
# # face rename
# face_list = %s
# for i in range(len(face_list)):
#     primarySelection = Selection.Create(GetRootPart())
#     secondarySelection = Selection()
#     result = NamedSelection.Create(primarySelection, secondarySelection)
#
# for i in range(len(face_list)):
#     result = NamedSelection.Rename("Group%%s"%%(i+1), face_list[i])
#
# # options = ShareTopologyOptions()
# # options.Tolerance = MM(0.01)
# # result = ShareTopology.FindAndFix(options)
#
# # save file
# options = ExportOptions.Create()
# DocumentSave.Execute(r"%s", options)
# print('script finished')
# """ % (self.body_list, self.face_list, self.pamt['cad_save_path'])
#     self.f.write(message)
#     self.f.close()