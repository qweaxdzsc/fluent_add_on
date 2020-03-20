import qdarkstyle


class advanced_func(object):
    """here are the advanced function of main ui, in other word not commonly used function,
        which include in menu bar'高级' """
    def __init__(self, ui, app):
        self.ui = ui
        self.app = app
        
    def direct_solve(self):
        """skip mesh mode, directly go to solver,
            used when having mesh already"""
        confirm_info = self.ui.project_info_check()
    
        if confirm_info:
            self.ui.check_part()
            self.ui.pamt_GUI()
            self.ui.start_btn.setText('网   格')
            self.ui.start_btn.setEnabled(True)
            self.ui.solver_btn.show()
            self.ui.solver_btn.setEnabled(True)
            self.ui.append_text('警告：进入补算模式，请先确认正确的模型或网格')
    
    def force_stop(self):
        """future function, not useful today. it is mean to stop fluent"""
        try:
            if self.ui.mesh_thread.isRunning():
                self.ui.mesh_thread.stop_mesh()
                self.ui.mesh_clock.stop()
                self.ui.append_text('网格划分已经被终止')
    
            if self.ui.solver_thread.isRunning():
                self.ui.solver_thread.stop_solver()
                self.ui.append_text('计算已经被终止')
        except Exception as e:
            print('not yet being running')

    def darkstyle(self):
        """change the theme of ui into dark style"""
        self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.ui.actiondarkstyle.setDisabled(True)
        self.ui.append_text('进入暗色主题')

