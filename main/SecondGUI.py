import matplotlib
# from PyQt5.QtCore.Qt import ToolButtonTextBesideIcon
from PyQt5 import QtCore
from PyQt5 import QtWidgets, Qt
from PyQt5.QtGui import *
# from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *

matplotlib.use("Qt5Agg")  # 声明使用pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg  # pyqt5的画布
import matplotlib.pyplot as plt
# matplotlib.figure 模块提供了顶层的Artist(图中的所有可见元素都是Artist的子类)，它包含了所有的plot元素
from matplotlib.figure import Figure
import designer
import global_var
class MyMatplotlibFigure(FigureCanvasQTAgg):
    """
    创建一个画布类，并把画布放到FigureCanvasQTAgg
    """
    def __init__(self, width=10, heigh=10, dpi=100):
        plt.rcParams['figure.facecolor'] = 'r'  # 设置窗体颜色
        plt.rcParams['axes.facecolor'] = 'b'  # 设置绘图区颜色
        self.width = width
        self.heigh = heigh
        self.dpi = dpi
        self.figs = Figure(figsize=(self.width, self.heigh), dpi=self.dpi)
        super(MyMatplotlibFigure, self).__init__(self.figs)  # 在父类种激活self.fig， 否则不能显示图像
        self.axes = self.figs.add_subplot(111)
class SecondUI(QWidget):

    def __init__(self):
        super(SecondUI, self).__init__()
        layout = QVBoxLayout()
        self.resize(1000, 600)
        self.setWindowTitle("Wrong  PICTURE  INPUT")
        # self.LabelX=LabelX
        # self.LabelY=LabelY

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(30, 200, 381, 91))
        self.label.setText("请输入错误描述,请注意格式")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 80, 281, 91))
        self.label.setText("错误类型")
        # 实例化QComBox对象
        self.cb = QComboBox(self)
        # 单个添加条目
        self.cb.addItem('坐标失真')
        self.cb.addItem('坐标系出错')
        self.cb.addItem('失去基准')
        # 多个添加条目
        self.cb.addItems(['点类型错误', '点数值出错', '失去焦点'])
        # self.cb.setGeometry(QtCore.QRect(10, 50, 1, 91))
        self.cb.resize(200, 50)
        self.cb.move(100, 100)
        # 当下拉索引发生改变时发射信号触发绑定的事件
        # self.cb.currentIndexChanged.connect(self.selectionchange)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 30, 281, 91))
        self.label.setText("错误描述")
        self.textbox = Qt.QLineEdit(self)
        self.textbox.resize(200, 50)
        self.textbox.move(100, 50)

        self.content = QTextEdit()
        self.btn = QtWidgets.QPushButton("set", self)
        self.btn.resize(100, 80)
        # self.btn_1.setText("从文件中获取照片")
        self.btn.setToolTip('按钮提示')
        self.btn.move(250, 200)
        self.content = QTextEdit()
        self.textEdit = QTextEdit()
        # self.btn.clicked.connect(self.Textvalue)
        # self.btn.clicked.connect(designer.gui.Textvalue)
        self.btn.clicked.connect(self.Textvalue)
        window_pale = Qt.QPalette()
        window_pale.setBrush(self.backgroundRole(), Qt.QBrush(Qt.QPixmap("one.png").scaled(self.width(), self.height())))
        self.setPalette(window_pale)
        self.show()

        # 设置输入框提示

    def Textvalue(self):
        i=1
        # f.close()  # 将文件关闭
        self.textboxvalue = self.textbox.text()

        if self.textboxvalue == '':
            # return
            pass
        reply=QMessageBox.information(self, "导入提示",
                                    "该点{0},{1}出现的{2}错误为{3}".format(str(global_var.labelX),str(global_var.labelY),self.cb.currentText(),self.textboxvalue),
                                    QMessageBox.Yes)
        # strtest: tuple[str, Union[str, Any]]=("导入提示", '该地图出现的{0}错误为'.format('坐标失真') + textboxvalue)
        if reply==QMessageBox.Yes:
            pass
        open(".\wrong.txt", "a+")
        with open(".\wrong.txt", "r+") as f:  # 设置文件对象
            count = len(f.readlines())
            f.write(str(count+1) + ',' + '图像点类型错误:' + 'X:,' + str(global_var.labelX) + 'Y:' + str(
                global_var.labelY) + ',' +
                    self.cb.currentText() + ',' + self.textboxvalue + '\n')
            QMessageBox.information(self, "导入提示","已导入",QMessageBox.Yes)
            self.textbox.clear()
            f.close()  # 将文件关
            i = i + 1
            # self.truepointX.append(int(designer.gui.LabelX))
            # self.truepointY.append(int(designer.gui.LabelY))
            return




