from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.optimize import curve_fit
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# from PyQt5.QtWidgets import QVBoxLayout, QFrame


class MyMplCanvas(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        from matplotlib.figure import Figure
        import matplotlib.pyplot as plt
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        self.fig = Figure(figsize=(width, height), dpi=dpi)  # 新建一个figure

        self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改

        # 配置中文显示
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def start_static_plot(self, x, y):
        self.fig.suptitle('V-P拟合图')

        def func(x, a, b):
            return a * x ** 2 + b * x

        popt, pcov = curve_fit(func, x, y)
        # 获取popt里面是拟合系数
        a = popt[0]
        b = popt[1]
        yvals = func(x, a, b)  # 拟合y值
        self.a = a
        self.b = b
        # print('系数pcov:', pcov)
        # print('系数yvals:', yvals)
        self.axes.cla()
        self.axes.plot(x, y, 's', label='原值')
        self.axes.plot(x, yvals, 'r', label='拟合曲线')
        for a, b in zip(x, y):
            self.axes.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=13)
        self.axes.set_ylabel('P(Pa)')
        self.axes.set_xlabel('V(m/s)')
        self.axes.legend(loc=4)
        self.axes.grid(True)
        self.draw()


# class MatplotlibWidget(QFrame):
#     def __init__(self, parent=None):
#         super(MatplotlibWidget, self).__init__(parent)
#
#
#     def initUi(self):
#         self.layout = QVBoxLayout(self)
#         # from MatplotlibWidget import MyMplCanvas
#         self.mpl = MyMplCanvas(self, width=4, height=2, dpi=70)
#         # self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar
#
#         self.layout.addWidget(self.mpl)
#         # self.layout.addWidget(self.mpl_ntb)


