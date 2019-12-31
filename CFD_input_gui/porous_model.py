from ui_porous_model import Ui_porous_model_form
from PyQt5.QtWidgets import QWidget, QLineEdit, QMenu, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal
import csv


class Ui_porous(Ui_porous_model_form, QWidget):
    db_change = pyqtSignal()

    def __init__(self):
        super(Ui_porous_model_form, self).__init__()
        self.setupUi(self)
        self.default_ui()
        self.default_btn()
        self.init_db()

    def default_ui(self):
        self.load_btn.hide()
        self.operate_frame.hide()
        self.resize(220, 135)
        self.unit_choose = 'kg/h'
        self.db_dict = {}
        self.db_path = r'C:\Users\BZMBN4\Desktop\fluent-command\porous_db.csv'

    def default_btn(self):
        self.model_combox.activated.connect(self.choose)
        self.QP_table.customContextMenuRequested.connect(self.generate_unit_menu)
        self.cal_btn.clicked.connect(self.cal_C1C2)
        self.del_btn.clicked.connect(self.delete_warning)
        self.modify_ui_btn.clicked.connect(self.modify_mode)
        self.modify_btn.clicked.connect(self.modify)
        self.add_btn.clicked.connect(self.add)

    def init_db(self):
        self.porous_info_dict()
        self.db_header = self.pd.keys()
        try:
            with open(self.db_path, 'r', newline='') as f:
                self.init_read = csv.DictReader(f)
                for row in self.init_read:
                    self.db_dict[row['model_name']] = row
            self.model_combox.addItems(self.db_dict.keys())
        except Exception as e:
            print(e)

    def choose(self, i):
        if i == 0:
            self.add_mode()
        else:
            self.read_mode(i)

    def default_show(self):
        self.operate_frame.show()
        self.resize(670, 670)
        self.load_btn.show()
        self.modify_ui_btn.hide()
        self.modify_btn.hide()
        self.add_btn.hide()
        self.del_btn.hide()

        self.model_name_edit.setEnabled(True)
        self.cal_btn.setEnabled(True)
        self.QP_table.setEnabled(True)
        self.effective_dimension_box.setEnabled(True)
        self.c1_edit.setEnabled(True)
        self.c2_edit.setEnabled(True)

    def add_mode(self):
        self.default_show()
        self.add_btn.show()
        self.load_btn.hide()
        self.clear_edit_data(self.operate_frame,
                             'model_name', 'length', 'width', 'height', 'c1', 'c2')

    def clear_edit_data(self, container, *args):
        for edit in args:
            wigdet = container.findChild(QLineEdit, edit+'_edit')
            wigdet.setText('')

    def read_mode(self, combox_index):
        self.default_show()

        self.model_name_edit.setEnabled(False)
        self.cal_btn.setEnabled(False)
        self.QP_table.setEnabled(False)
        self.effective_dimension_box.setEnabled(False)
        self.c1_edit.setEnabled(False)
        self.c2_edit.setEnabled(False)

        self.modify_ui_btn.show()
        self.del_btn.show()

        choose_model = self.model_combox.itemText(combox_index)
        model_info = self.db_dict[choose_model]

        for i in model_info:
            name = i + '_edit'
            widget = self.findChild(QLineEdit, name)
            if widget != None:
                widget.setText(str(model_info[i]))
            if "volume" in i:
                self.QP_table.item(int(i[-1]), 0).setText(model_info[i])
            if "pressure" in i:
                self.QP_table.item(int(i[-1]), 1).setText(model_info[i])

    def modify_mode(self):
        self.default_show()
        self.modify_btn.show()

    def modify(self):
        choosed_model_index = self.model_combox.currentIndex()
        modify_model_name = self.model_combox.itemText(choosed_model_index)
        self.db_dict.pop(modify_model_name)

        self.porous_info_dict()
        self.db_dict[self.pd['model_name']] = self.pd
        self.model_combox.removeItem(choosed_model_index)
        self.model_combox.addItem(self.pd['model_name'])
        self.write_db()

    def delete_warning(self):
        reply = QMessageBox.warning(self, "删除警告", "删除模型后无法恢复，确认要删除吗?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            reply2 = QMessageBox.warning(self, "删除再次警告", "真的要删除吗???", QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
            if reply2 == QMessageBox.Yes:
                self.delete_model()

    def delete_model(self):
        choosed_model_index = self.model_combox.currentIndex()
        delete_model_name = self.model_combox.itemText(choosed_model_index)
        self.db_dict.pop(delete_model_name)
        self.model_combox.removeItem(choosed_model_index)
        self.write_db()

    def generate_unit_menu(self, pos):
        column_num = -1
        for i in self.QP_table.selectionModel().selection().indexes():
            column_num = i.column()

        if column_num == 0:
            unit_menu = QMenu()
            unit_ls = unit_menu.addAction(u"l/s")
            unit_mh = unit_menu.addAction(u"m3/h")
            unit_kgm = unit_menu.addAction(u"kg/min")
            unit_kgh = unit_menu.addAction(u"kg/h")
            action = unit_menu.exec_(self.QP_table.mapToGlobal(pos))
            try:
                self.unit_choose = action.text()
                unit_item = QTableWidgetItem("流量(%s)" % action.text())
                self.QP_table.setHorizontalHeaderItem(0, unit_item)
            except:
                pass

    def cal_C1C2(self):
        l_raw = self.length_edit.text()
        w_raw = self.width_edit.text()
        h_raw = self.height_edit.text()
        rho = 1.225                                 # density
        mu = 0.000017894                            # dynamic viscosity
        self.Q_unit = {'l/s': 1000, 'm3/h': 1 / 3600, 'kg/min': 1 / rho / 60, 'kg/h': 1 / rho / 3600}

        if l_raw and w_raw and h_raw != '':
            l = float(l_raw)/1000
            w = float(w_raw)/1000
            h = float(h_raw)/1000
            eff_area = l*w                          # effective area size

            import numpy as np
            row_num = self.QP_table.rowCount()
            Q = np.zeros(row_num + 1)
            P = np.zeros(row_num + 1)
            for i in range(row_num):
                q = self.QP_table.item(i, 0).text()
                p = self.QP_table.item(i, 1).text()
                try:
                    q = float(q)
                    Q[i + 1] = q
                except:
                    continue
                try:
                    p = float(p)
                    P[i + 1] = p
                except:
                    continue

            Q = set(Q)
            Q = np.array(list(Q))
            Q.sort()

            P = set(P)
            P = np.array(list(P))
            P.sort()
            v = Q*self.Q_unit[self.unit_choose]/eff_area

            self.plot_frame.setVisible(True)
            self.plot_frame.mpl.start_static_plot(v, P)

            a = self.plot_frame.mpl.a
            b = self.plot_frame.mpl.b
            C1 = b/h/mu
            C2 = 2*a/rho/h

            self.c1_edit.setText(str('%.2e'%C1))
            self.c2_edit.setText(str('%.2f'%C2))
        else:
            print('please complete all blank edit')

    def porous_info_dict(self):
        self.pd = {}

        self.pd['model_name'] = self.model_name_edit.text()
        self.pd['c1'] = self.c1_edit.text()
        self.pd['c2'] = self.c2_edit.text()
        self.pd['length'] = self.length_edit.text()
        self.pd['width'] = self.width_edit.text()
        self.pd['height'] = self.height_edit.text()
        self.pd['unit_choose'] = self.unit_choose
        for i in range(5):
            self.pd['volume%s' % i] = self.QP_table.item(i, 0).text()
            self.pd['pressure%s' % i] = self.QP_table.item(i, 1).text()

    def add(self):
        self.porous_info_dict()

        if self.pd['model_name'] in self.db_dict.keys():
            print(self.pd['model_name'], self.db_dict.keys())
            reply = QMessageBox.warning(self, "警告", "数据库中已拥有此模型，请重新核对", QMessageBox.Yes, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                pass
        else:
            print('start add')
            self.db_dict[self.pd['model_name']] = self.pd
            self.model_combox.addItem(self.pd['model_name'])
            self.write_db()

    def write_db(self):
        with open(self.db_path, 'w', newline='') as f:
            dwriter = csv.DictWriter(f, fieldnames=self.db_header)
            dwriter.writeheader()
            for i in self.db_dict:
                dwriter.writerow(self.db_dict[i])

            self.db_change.emit()
