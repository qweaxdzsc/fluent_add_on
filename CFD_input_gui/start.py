from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QSlider, QLineEdit, QTableWidgetItem, QFileDialog, QItemDelegate
)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, QTranslator, QFileInfo
from ui_input import Ui_MainWindow
from porous_model import Ui_porous
from k_cal import Ui_k_cal
from project_name import Ui_project_name
from output_html import output_web
from output_csv import OutputCsv
from html_parser import HtmlParser
import cgitb
import sys


class MyMainWindow(QMainWindow, Ui_MainWindow, QItemDelegate):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.signal_slot()
        self.porous_db_init()
        self.porous_item_update()
        self.set_number_validate()
        self.init_validator()
        # --------init variable------------
        self.project_name = ''
        self.input_d = {}              # initialize all data dict, include father(input_d), and 5 child dict.
        self.RPM_d = {}
        self.porous_d = {}
        self.outlet_k_dict = {}
        self.valve_d = {}
        self.comment_d = {}

    def signal_slot(self):
        self.actionexport.triggered.connect(self.export_cfd_parameter)
        self.actionimport.triggered.connect(self.import_cfd_parameter)
        self.mode_slider.valueChanged.connect(self.mode_choose)
        self.valve_slider.valueChanged.connect(self.valve_number)
        self.RPM_slider_signal()
        self.evap_combox.activated.connect(lambda: self.porous_choose(self.evap_combox.currentIndex(), 'evap'))
        self.hc_combox.activated.connect(lambda: self.porous_choose(self.hc_combox.currentIndex(), 'hc'))
        self.filter_combox.activated.connect(lambda: self.porous_choose(self.filter_combox.currentIndex(), 'filter'))
        self.outlet_btn.clicked.connect(self.outlet_ui_show)

    def set_number_validate(self):
        re = QRegExp("[0-9]+")
        self.int_validator = QRegExpValidator(re)
        re2 = QRegExp("[0-9]+\.[0-9]+")
        self.float_validator = QRegExpValidator(re2)

    def init_validator(self):
        modes = ['vent', 'foot', 'bil', 'defrost', 'defog', 'trl', 'hil']
        for i in modes:
            edit = self.RPM_tab.findChild(QLineEdit, i + '_edit')
            edit.setValidator(self.int_validator)
            edit.setMaxLength(4)

        value_delegate = QItemDelegate(self)
        value_delegate.createEditor = self.createEditor
        self.valve_table.setItemDelegateForColumn(1, value_delegate)

    def _translate(self, language):
        self.language = language
        self.trans = QTranslator()
        self.trans.load("ui_input_%s" % language)
        _app = QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)
        self.label.setWordWrap(True)

    def RPM_slider_signal(self):
        modes = ['vent', 'foot', 'bil', 'defrost', 'defog', 'trl', 'hil']
        for i in modes:
            slider = self.RPM_tab.findChild(QSlider, i+'_slider')
            slider.valueChanged.connect(lambda: self.RPM_slider_value(self.sender()))

    def RPM_slider_value(self, slider):
        value = slider.value()*50 + 2500
        edit = self.RPM_tab.findChild(QLineEdit, slider.objectName()[:-7]+'_edit')
        edit.setText('%s' % value)

    def porous_db_init(self):
        self.porous_model = Ui_porous()
        self.porous_index_dict = {'evap': 0, 'hc': 0, 'filter': 0}
        self.porous_model.db_change.connect(self.porous_item_update)

    def porous_item_update(self):
        porous_dict = self.porous_model.db_dict
        self.evap_combox.clear()
        self.evap_combox.addItem('add')
        self.evap_combox.addItems(porous_dict.keys())
        self.evap_combox.setCurrentIndex(self.porous_index_dict['evap'])
        self.evap_combox.addItem('none')
        self.hc_combox.clear()
        self.hc_combox.addItem('add')
        self.hc_combox.addItems(porous_dict.keys())
        self.hc_combox.setCurrentIndex(self.porous_index_dict['hc'])
        self.hc_combox.addItem('none')
        self.filter_combox.clear()
        self.filter_combox.addItem('add')
        self.filter_combox.addItems(porous_dict.keys())
        self.filter_combox.setCurrentIndex(self.porous_index_dict['filter'])
        self.filter_combox.addItem('none')

    def mode_choose(self):
        value = self.mode_slider.value()
        self.mode_dict = {
                            2: ['foot_label', 'foot_slider', 'foot_edit'],
                            3: ['bil_label', 'bil_slider', 'bil_edit'],
                            4: ['defrost_label', 'defrost_slider', 'defrost_edit'],
                            5: ['defog_label', 'defog_slider', 'defog_edit'],
                            6: ['trl_label', 'trl_slider', 'trl_edit'],
                            7: ['hil_label', 'hil_slider', 'hil_edit']
                            }
        for key in self.mode_dict.keys():
            label = self.RPM_tab.findChild(QLabel, self.mode_dict[key][0])
            slider = self.RPM_tab.findChild(QSlider, self.mode_dict[key][1])
            edit = self.RPM_tab.findChild(QLineEdit, self.mode_dict[key][2])
            if key > value:
                label.setDisabled(True)
                slider.setDisabled(True)
                edit.setDisabled(True)
            else:
                label.setEnabled(True)
                slider.setEnabled(True)
                edit.setEnabled(True)

    def porous_choose(self, i, porous_type):
        if i == self.evap_combox.count() - 1:
            pass
        elif i == 0:
            self.porous_model.show()
            self.porous_model.add_mode()
            self.porous_model.model_combox.setCurrentIndex(0)
        else:
            self.porous_model.show()
            self.porous_model.read_mode(i)
            self.porous_model.model_combox.setCurrentIndex(i)
            self.porous_index_dict[porous_type] = i

    def outlet_ui_show(self):
        self.outlet_ui = Ui_k_cal()
        self.outlet_ui.show()
        self.outlet_ui.outlet_K_signal.connect(self.outlet_k_show)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        re2 = QRegExp("[0-9]{1,3}[.]{0,1}[0-9]{0,1}")
        valve_validator = QRegExpValidator(re2)
        editor = QLineEdit(QWidget)
        editor.setValidator(valve_validator)

        return editor

    def valve_number(self):
        former_value = self.valve_table.rowCount()
        value = self.valve_slider.value()

        if former_value < value:
            for i in range(value - former_value):
                self.valve_table.insertRow(former_value+i)
                name_item = QTableWidgetItem('temp_valve%s' % (value+i))
                self.valve_table.setItem(former_value+i, 0, name_item)
                data_item = QTableWidgetItem('0')
                self.valve_table.setItem(former_value+i, 1, data_item)
        else:
            for i in range(former_value - value):
                self.valve_table.removeRow(value)

    def outlet_k_show(self, dict):
        self.outlet_k_dict = dict
        row_count = self.formLayout.rowCount()
        for i in range(row_count):
            self.formLayout.removeRow(0)

        for outlet in dict.keys():
            outlet_label = QLabel(outlet)
            k_edit = QLineEdit()
            k_edit.setMaximumWidth(100)
            k_edit.setText(str(dict[outlet]))
            k_edit.setObjectName(outlet+'_edit')
            k_edit.setValidator(self.float_validator)
            k_edit.setMaxLength(8)
            self.formLayout.addRow(outlet_label, k_edit)

    def data_dict(self):
        self.input_d = {}
        self.RPM_d = {}
        self.porous_d = {}
        self.valve_d = {}
        self.comment_d = {}

        # form RPM_dict
        mode_value = self.mode_slider.value()
        modes = ['vent', 'foot', 'bil', 'defrost', 'defog', 'trl', 'hil']
        for i in range(mode_value):
            edit = self.RPM_tab.findChild(QLineEdit, modes[i] + '_edit')
            self.RPM_d[modes[i]] = edit.text()

        # form porous_dict
        self.porous_coefficient(self.evap_combox)
        self.porous_coefficient(self.hc_combox)
        self.porous_coefficient(self.filter_combox)

        # form outlet_k_dict
        for outlet in self.outlet_k_dict.keys():
            k = self.outlet_scrollarea.findChild(QLineEdit, outlet+'_edit').text()
            self.outlet_k_dict[outlet] = k

        # form valve_dict
        valve_count = self.valve_slider.value()
        for i in range(valve_count):
            if not self.valve_table.item(i, 1):
                pass
            else:
                valve_name = self.valve_table.item(i, 0).text()
                valve_travel = self.valve_table.item(i, 1).text()
                self.valve_d[valve_name] = valve_travel

        # form comment_dict
        self.comment_d['comment'] = self.comment_edit.toPlainText()

        # form all to input_dict
        self.input_d['project_name'] = self.project_name
        self.input_d['RPM'] = self.RPM_d
        self.input_d['porous'] = self.porous_d
        self.input_d['outlet_k'] = self.outlet_k_dict
        self.input_d['valve'] = self.valve_d
        self.input_d['comment'] = self.comment_d

    def porous_coefficient(self, combox):
        model = combox.currentText()
        model_type = combox.objectName()[:-7]
        model_c1 = model_type + '_c1'
        model_c2 = model_type + '_c2'
        if model == 'none':
            self.porous_d[model_type] = 'none'
            self.porous_d[model_c1] = 'none'
            self.porous_d[model_c2] = 'none'
        elif model == 'add':
            self.porous_d[model_type] = 'none'
            self.porous_d[model_c1] = 'none'
            self.porous_d[model_c2] = 'none'
        else:
            self.porous_d[model_type] = model
            self.porous_d[model_c1] = self.porous_model.db_dict[model]['c1']
            self.porous_d[model_c2] = self.porous_model.db_dict[model]['c2']

    def export_cfd_parameter(self):
        self.data_dict()
        print(self.input_d)
        # output = output_web(r'C:/Users/BZMBN4/Desktop/123.html', self.input_d)
        path = QFileDialog.getSaveFileName(self, filter='html, *.html')
        try:
            save_path = QFileInfo(path[0])
            html_save_path = save_path.filePath()
            csv_save_path = save_path.absolutePath() + '\\' + save_path.baseName() + '.csv'
            output_html = output_web(html_save_path, self.input_d)
            output_csv = OutputCsv(csv_save_path, self.input_d)

        except Exception as e:
            print(e)

    def import_cfd_parameter(self):
        path = QFileDialog.getOpenFileName(self, '选择要输入的参数模板', filter='html, *.html')
        if path[0] != '':
            html_path = path[0]
            self.input_d = {}
            parameter_file = HtmlParser(html_path)
            self.input_d = parameter_file.data_dict
            self.import_show_data()
        #     with open(csv_path, 'r', newline='') as csvfile:
        #         reader = csv.reader(csvfile)
        #         for row in reader:
        #             self.input_d[row[0]] = row[1]

    def import_show_data(self):
        # ----------show project name---------
        project_name = self.input_d['project_name']
        self.setWindowTitle(project_name)
        self.project_name = project_name
        # ----------show RPM data-------------
        rpm_d = self.input_d['RPM']
        mode_count = len(rpm_d)
        self.mode_slider.setValue(mode_count)

        for mode in rpm_d.keys():
            edit = self.RPM_tab.findChild(QLineEdit, mode + '_edit')
            slider = self.RPM_tab.findChild(QSlider, mode + '_slider')
            rpm = rpm_d[mode]
            edit.setText(rpm)
            slider_value = (int(rpm)-2500)/50
            slider.setValue(slider_value)
        # --------show porous choice---------
        porous_d = self.input_d['porous']
        self.evap_combox.setCurrentText(porous_d['evap'])
        self.hc_combox.setCurrentText(porous_d['hc'])
        self.filter_combox.setCurrentText(porous_d['filter'])
        # --------show outlet_k data---------
        self.outlet_k_show(self.input_d['outlet_k'])
        # --------show valve data------------
        valve_d = self.input_d['valve']
        valve_count = len(valve_d)
        self.valve_slider.setValue(valve_count)
        valve_list = list(valve_d.keys())
        for i in range(valve_count):
            self.valve_table.item(i, 0).setText(valve_list[i])
            self.valve_table.item(i, 1).setText(valve_d[valve_list[i]])
        # --------show comment --------------
        self.comment_edit.setText(self.input_d['comment'])


if __name__ == "__main__":
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    intro_window = Ui_project_name(MyMainWindow)
    intro_window.show()
    # myMain = MyMainWindow()
    # myMain.show()
    sys.exit(app.exec_())


