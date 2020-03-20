# def view_path_init(self):
#     self.view_path_db = {}
#     view_path_file = r'C:\Users\BZMBN4\Desktop\fluent-command\view_path.csv'
# 
#     with open(view_path_file, 'r', newline='') as f:
#         view_path_csv = csv.DictReader(f)
#         for row in view_path_csv:
#             self.view_path_db[row['project_name']] = row['view_path']
#         self.view_path_combox.clear()
#         self.view_path_combox.addItems(self.view_path_db.keys())
# 
#     self.view_path_choose()
#     self.view_path_combox.activated.connect(self.view_path_choose)
# 
# 
# def view_path_choose(self):
#     view_file_name = self.view_path_combox.currentText()
#     self.view_path = self.view_path_db[view_file_name]

# def show_snip_setting(self):
#     if self.ui.actionsnip.isChecked():
#         self.ui.snip_on = True
#     else:
#         self.ui.snip_on = False
# 
#     self.snip_switch()
# 
# 
# def snip_switch(self):
#     if self.ui.snip_on and self.ui.show_c_on:
#         self.ui.snip_c.show()
#     else:
#         self.ui.snip_c.hide()
