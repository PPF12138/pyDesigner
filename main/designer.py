import os
import sys
import webbrowser
import time
import re
import base64
import json

# 本打算画布调用，将matpoylib显示影像，但最后决定在界面显示，故没调用matplotlib
# import matplotlib
# matplotlib.use("Qt5Agg")  # 声明使用pyqt5
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg  # pyqt5的画布
import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
# 关于界面设计的模块接口库
# from PyQt5.QtCore.Qt import ToolButtonTextBesideIcon
from PyQt5 import QtCore
from PyQt5 import QtWidgets, QtGui, Qt
from PyQt5.QtGui import *
# from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from Jpeg import img as one
# matplotlib.figure 模块提供了顶层的Artist(图中的所有可见元素都是Artist的子类)，它包含了所有的plot元素


import SecondGUI
import global_var
# from QCandyUi.CandyWindow import colorful
# import FirstGUI
"""
ZetCode PyQt5 tutorial 

This program creates a mapGUI.

Author: pengfei pan
Website: https://github.com/PPF12138/mapdesigner.com 
Last edited: March 2022
"""
# @colorful('blue')
    # 点击鼠标触发函数
class GUI(QMainWindow):

    def __init__(self):
        # 初始化————init__

        super(GUI, self).__init__()
        global LabelX
        global LabelY
        self.initGUI()

    def initGUI(self):
        # 设置窗口大小
        self.resize(1600, 800)
        self.move(200, 100)
        # 设置整体布局字体
        font = QtGui.QFont()
        font.setFamily("华文行楷")
        font.setBold(True)
        font.setPointSize(13)
        font.setWeight(75)

        font1 = QtGui.QFont()
        font1.setFamily("仿宋")
        font1.setBold(True)
        font1.setPointSize(9)
        font1.setWeight(60)
        self.style = QApplication.style()
        self.truepointX = []
        self.truepointY = []
        self.fname = None
        self.PointBoolean = False
        self.picture_Boolean = False
        self.xxoo = False
        self.ttee=False
        layout = QVBoxLayout()
        self.setLayout(layout)
        # 设置窗口位置(下面配置的是居于屏幕中间)
        # self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        # self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        # self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        # 设置窗口标题和图标,菜单栏
        self.setWindowTitle('质检工具')
        menu = QMenu(self)
        self.bar = self.menuBar()
        fileMenu = self.bar.addMenu("File(&F)")
        editMenu = self.bar.addMenu("Edit(&E)")
        error_check = self.bar.addMenu("错误查询(&C)")
        helpMenu = self.bar.addMenu("帮助(&H)")
        # 菜单栏添加动作设置

        # 错误查询动作
        ################################################################
        error_Check = QAction('错误查询(&O)...', self)
        # error_Check.setIcon(self.style.standardIcon(QStyle.SP_DirLinkIcon))
        # error_Check.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        # # error_Check.triggered.connect(self.open_second_ui)
        # error_check.addAction(self.error_search)
        # aHelpCheck = QAction('查找操作(&C)...', self)
        # aHelpCheck.triggered.connect(self.SP_TitleBarUnshadeButton)
        error_Check.triggered.connect(self.error_search)
        error_check.addAction(error_Check)
        ###########################################################

        aHelpAbout = QAction('关于(&A)...', self)
        aHelpAbout.triggered.connect(self.onHelpAbout)
        aHelpAbout.setIcon(self.style.standardIcon(QStyle.SP_BrowserReload))
        helpMenu.addAction(aHelpAbout)

        aHelpCheck = QAction('查找操作(&C)...', self)
        # aHelpCheck.triggered.connect(self.SP_TitleBarUnshadeButton)
        helpMenu.addAction(aHelpCheck)
        #######################################################3#
        # ==== 文件操作部分 ==== #
        # 新建文件
        aFileNew = QAction('重新选择(&N)', self)
        # 添加一个图标
        aFileNew.setIcon(self.style.standardIcon(QStyle.SP_FileIcon))
        # 添加快捷键
        aFileNew.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_N)
        aFileNew.triggered.connect(self.onFileNew)
        fileMenu.addAction(aFileNew)
        # 打开文件
        aFileOpen = QAction('打开(&O)...', self)
        aFileOpen.setIcon(self.style.standardIcon(QStyle.SP_DialogOpenButton))
        aFileOpen.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        aFileOpen.triggered.connect(self.loadFile)
        fileMenu.addAction(aFileOpen)
        # 保存
        aFileSave = QAction('保存(&S)', self)
        aFileSave.setIcon(self.style.standardIcon(QStyle.SP_DialogSaveButton))
        aFileSave.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        aFileSave.triggered.connect(self.onFileSave)
        fileMenu.addAction(aFileSave)
        # 另存为
        aFileSaveAs = QAction('另存为(&A)...', self)
        aFileSaveAs.triggered.connect(self.onFileSaveAs)
        fileMenu.addAction(aFileSaveAs)
        # 间隔线
        fileMenu.addSeparator()
        # 退出菜单
        aFileExit = QAction('退出(&X)', self)
        aFileExit.triggered.connect(self.close)
        fileMenu.addAction(aFileExit)
        ##############################################################
        # self.setWindowIcon(QtGui.QIcon('2.png'))

        # 设置窗口提示
        self.setToolTip('窗口提示')
        self.statusBar().showMessage('Everything is ready')

        # 设置画布
        # self.canvas = MyMatplotlibFigure(width=5, heigh=4, dpi=100)
        # self.loadFile()
        # self.hboxlayout = QtWidgets.QHBoxLayout(self.label)
        # self.hboxlayout.addWidget(self.canvas)

        # 设置label信息
        self.label = QtWidgets.QLabel(self)
        # self.label.setText("   ")
        self.label.setFixedSize(700, 680)
        self.label.move(1, 100)
        # self.label.setGeometry(QtCore.QRect(500, 450, 500, 200))
        self.label.setObjectName('label')
        self.label.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )
        self.label.setMouseTracking(True)
        # 设置label提示
        self.label.setToolTip(' ')
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setText("first line\nsecond line")
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setStyleSheet(
            'border-width: 1px;border-style: solid;border-color: rgb(0, 0, 0);background-color: rgb(240, 240, 240);')

        self.label_1 = QtWidgets.QLabel(self)
        # self.label.setText("   ")
        self.label_1.setFixedSize(800, 400)
        self.label_1.move(800, 30)
        # self.label.setGeometry(QtCore.QRect(500, 450, 500, 200))
        self.label_1.setObjectName('label_1')
        self.label_1.setStyleSheet("QLabel{background:white;}"
                                   "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                   )
        self.label_1.setMouseTracking(True)
        # 设置label提示
        self.label_1.setToolTip('  ')
        self.label_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_1.setStyleSheet(
            'border-width: 1px;border-style: solid;border-color: rgb(0, 0, 0);background-color: rgb(240, 240, 240);')
        self.label_1.setFont(font)

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setFixedSize(300, 30)
        self.label_2.move(1, 60)
        # self.label.setGeometry(QtCore.QRect(500, 450, 500, 200))
        self.label_2.setObjectName('label_1')
        self.label_2.setStyleSheet("QLabel{background:white;}"
                                   # "QLabel{color:rgb(300,300,300,120);font-size:20px;font-weight:bold;font-family:宋体;}"
                                   )
        self.label_2.setMouseTracking(True)
        self.label_2.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.label_2.setAttribute(Qt.Qt.WA_TranslucentBackground)
        self.label_2.setText("影像图示")
        self.label_2.setFont(font)
        # 设置label提示
        self.label_2.setToolTip('  ')

        frame = QtWidgets.QSplitter(self)
        frame.resize(500, 800)
        frame.move(500, 25)
        frame.setFrameStyle(QFrame.VLine | QFrame.Raised)
        frame.setLineWidth(3)

        sub_menu = QMenu(menu)
        sub_menu.setTitle("文本类")
        sub_menu.setIcon(self.style.standardIcon(QStyle.SP_FileIcon))
        sub_menu_1 = QMenu(menu)
        sub_menu_1.setTitle("图像类")
        sub_menu_1.setIcon(self.style.standardIcon(QStyle.SP_TitleBarNormalButton))
        # 在菜单中添加子菜单
        menu.addMenu(sub_menu)
        menu.addMenu(sub_menu_1)

        # 设置按钮
        self.btn_1 = QtWidgets.QPushButton("清除文本", self)
        self.btn_1.resize(160, 50)
        # self.btn_1.setText("从文件中获取照片")
        self.btn_1.move(1400, 300)
        self.btn_1.setFont(font)

        self.btn_2 = QtWidgets.QPushButton("错误记录查询", self)
        self.btn_2.resize(160, 50)
        # self.btn_1.setText("从文件中获取照片")
        self.btn_2.move(900, 300)
        self.btn_2.setFont(font)

        self.btn_3 = QtWidgets.QPushButton("实时显示坐标", self)
        self.btn_3.resize(160, 50)
        self.btn_3.move(1150, 300)
        self.btn_3.setFont(font)

        self.content = QTextEdit()
        layout.addWidget(self.content)

        self.btn_4 = QtWidgets.QPushButton("影像错误标记", self)
        self.btn_4.resize(160, 50)
        self.btn_4.move(1400, 380)
        self.btn_4.setFont(font)

        self.btn_5 = QtWidgets.QPushButton("json类错误标记", self)
        self.btn_5.resize(160, 50)
        self.btn_5.move(900, 380)
        self.btn_5.setFont(font)

        self.btn_6 = QtWidgets.QPushButton("打开文件", self)
        self.btn_6.resize(160, 50)
        self.btn_6.move(400, 50)
        self.btn_6.setFont(font)

        self.btn_1.setToolTip('按钮提示')
        self.btn_2.setToolTip('错误查询')
        self.btn_3.setToolTip('按钮提示')
        self.btn_4.setToolTip('坐标选择')
        self.btn_5.setToolTip('坐标选择')

        # 点击鼠标触发事件
        self.textEdit = QTextEdit(self)
        self.textEdit.setFont(font)
        self.textEdit.setText("文件类")
        # self.textEdit.setStyleSheet("border:none;")
        self.textEdit.setEnabled(False)
        self.textEdit.resize(160, 35)
        self.textEdit.move(1150, 380)
        self.textEdit.setAlignment(QtCore.Qt.AlignHCenter)
        self.textEdit.setStyleSheet(
            'border-width: 1px;font-size:25px;border-style: solid;border-color: rgb(0, 0, 0);background-color: rgb(240, 240, 240);border:none')

        self.textEdit1 = QTextEdit(self)
        self.textEdit1.setFont(font1)
        self.textEdit1.setText("错误检索")
        # self.textEdit.setStyleSheet("border:none;")
        self.textEdit1.setEnabled(False)
        self.textEdit1.resize(50, 325)
        self.textEdit1.move(820, 70)
        self.textEdit1.setStyleSheet(
            'border-width: 8px;font-size:30px;vertical-align: baseline;border-style: solid;border-color: rgb(0, 0, 0);background-color: rgb(240, 240, 240);border:none')

        self.btn_1.clicked.connect(self.delete_File)
        self.btn_2.clicked.connect(self.error_search)
        self.btn_3.clicked.connect(self.Textvalue)
        self.btn_4.clicked.connect(self.access_Point)
        self.btn_5.clicked.connect(self.access_text)
        self.btn_6.clicked.connect(self.loadFile)

        # 点击菜单栏触发事件

        self.label.setMouseTracking(True)

        self.label_mouse_x = QLabel(self)
        self.label_mouse_x.setGeometry(230, 40, 80, 30)
        self.label_mouse_x.setText('x')
        self.label_mouse_x.setMouseTracking(True)

        self.label_mouse_y = QLabel(self)
        self.label_mouse_y.setText('y')
        self.label_mouse_y.setGeometry(300, 40, 80, 30)
        self.label_mouse_y.setMouseTracking(True)
        # self.
        self.text_browser = QTextEdit(self)  # 实例化一个QTextBrowser对象
        self.text_browser.setText("<h1>Hello World,this is JSON!</h1>")  # 设置编辑框初始化时显示的文本
        self.text_browser.resize(800, 340)
        self.text_browser.move(800, 450)
        self.text_browser.setReadOnly(True)
        self.textedit = QTextEdit(self)
        self.textedit.setText("<h1>请点击\'标记错误\'按钮输入搜索关键词!<h1>")
        self.textedit.resize(600, 210)
        self.textedit.move(900, 60)
        self.text_browser.setStyleSheet(
            'border-width: 1px;border-style: solid;border-color: rgb(0, 0, 0);background-color: rgb(220, 220, 220);')
        self.text_browser.setReadOnly(True)
        self.textedit.setFont(font1)
        self.show();
    def loadFile(self):
        print("load--file")
        # QFileDialog就是系统对话框的那个类第一个参数是上下文，第二个参数是弹框的名字，第三个参数是开始打开的路径，第四个参数是需要的格式
        # fname, _ = QFileDialog.getOpenFileName(self, '选择图片', 'c:\\', 'Image files(*.jpg *.gif *.png *.tif *.shp)')
        reply = QtWidgets.QMessageBox.question(self, '提示', "请确定文件类型",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            items = ('tif类', 'json类', 'shp类', 'jpeg类')
            # 返回两个值，第一个item代表用户选择的值，ok代表用户是否按下了取消
            inputdialog = QInputDialog()
            item, ok = inputdialog.getItem(self, "请选择文件类型", "类型列表", items)
            self.item = item
        if ok == True:
            if self.item == 'json类':
                self.fjsoname, _ = QFileDialog.getOpenFileName(self, '选择json类', 'C:\\',
                                                               'Json files(*.json)')
            else:
                self.fname, _ = QFileDialog.getOpenFileName(self, '选择影像', 'C:\\',
                                                            'Image files(*.tif *.jpg *.gif *.png *.shp)')
        else:
            return
        try:
            image = QtGui.QPixmap(self.fname).scaled(self.label.width(), self.label.height())
            self.label.setPixmap(image)
            self.picture_Boolean = True
            pfname = os.path.basename(self.fname)
            self.label_2.setText(pfname)
            print('good')
        except Exception as e:
            with open(self.fjsoname, 'r', encoding='utf8') as fp:
                json_data = json.load(fp)
                self.text_browser.setText(str(json_data))
                print('这是读取到文件数据的数据类型：', type(json_data))
        self.textEdit.setText(self.item)
        self.textEdit.setAlignment(QtCore.Qt.AlignHCenter)
        print('已显示')
        return


    def access_Point(self):
        self.PointBoolean = True
        if self.picture_Boolean==True:
            QtWidgets.QMessageBox.question(self, '提示', "请标记出图片的点",
                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                       QtWidgets.QMessageBox.No)
        else:
            QtWidgets.QMessageBox.question(self, '提示', "图片未加载",
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

    def access_text(self):
        textCursor = self.text_browser.textCursor()
        tc = textCursor
        if tc.selectedText() == '':
            QtWidgets.QMessageBox.question(self, '提示', "请选定内容",
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)
            return
            # print(tc.selectedText())  # 打印出所选择的文本
            # print(tc.selection().toPlainText())  # QDocumentFragment
            # print(tc.selectedTableCells())
            # print(tc.selectionStart())  # 所选中内容 的位置
            # print(tc.selectionEnd())
            # print(len(tc.selectedText()))
            # self.text_browser.cursorPositionChanged()
            # self.text_browser.mouseDoubleClickEvent()
            # if self.text_browser.mousePressEvent()==
            # textCursor.setPosition(3, QTextCursor.MoveAnchor)
            # textCursor.setPosition(9, QTextCursor.KeepAnchor)
            # print(tc.select(QTextCursor.LineUnderCursor))
        lengthwords=len(self.text_browser.toPlainText())
        # firrst=self.text_browser.toPlainText().find('[',int(lengthwords/2))
        # secrst = self.text_browser.toPlainText().find(']', int(lengthwords/2))
        firrst=self.text_browser.toPlainText().find('[',100)
        secrst = self.text_browser.toPlainText().find(']', 100)
        gap=secrst-firrst
        if len(tc.selectedText()) > gap+2 or (tc.selectedText()).count('[') != 1 or (tc.selectedText()).count(
                ']') != 1 :
            QMessageBox.question(self, "警告",
                                 "请选择一个正确的坐标点",
                                 QMessageBox.Yes)
            return
        if tc.selectedText().index('[') > tc.selectedText().index(']'):
            QMessageBox.question(self, "警告",
                                 "请按标准格式选择固定点",
                                 QMessageBox.Yes)
            return
        SelectedText = tc.selectedText()
        p1 = re.compile(r'[[](.*?)[]]', re.S)
        print(re.findall(p1, SelectedText))
        try:
            selectY = SelectedText.split(',')[-1]
            selectX = SelectedText.split(',')[-2]
        except Exception as e:
            QMessageBox.question(self, "警告",
                                 "请按标准格式选择固定点",
                                 QMessageBox.Yes)
            return
        error_type,OK=QInputDialog.getText(self,'错误类型','请输入错误类型:')
        text, ok = QInputDialog.getMultiLineText(self, '错误描述', '请输入错误描述:')
        if not ok:
            return
        if text =='' or error_type== '':
            return
        QMessageBox.information(self, "导入提示",
                                "该json点{0}出现的错误为".format(SelectedText) + text,
                                QMessageBox.Yes)
        self.fjsonrealname = self.fjsoname.split('.')[-2].split('/')[-1]
        # strtest: tuple[str, Union[str, Any]]=("导入提示", '该地图出现的{0}错误为'.format('坐标失真') + textboxvalue)
        open(".\{0}.txt".format(self.fjsonrealname), "a+")
        with open(".\{0}.txt".format(self.fjsonrealname), "r+") as f:  # 设置文件对象
            # f.write(('我爱Python' + os.linesep).encode('utf-8'))
            # sTr=str().format('2')
            count = len(f.readlines())
            f.write(str(count+1) + ',' + 'json点类型错误: ' + 'X:' + str(selectX) + ' ' + 'Y:' + str(
                selectY) + ',' +'错误类型'+' '+error_type+'错误描述: '+
                    text + '\n')
            QMessageBox.information(self, "导入提示",
                                    "成功导入一点",
                                    QMessageBox.Yes)
            f.close()  # 将文件关
            # self.tc.setFocus()
        print('good!')

    def closeEvent(self, QCloseEvent):
        reply = QtWidgets.QMessageBox.question(self, '警告', "确定关闭当前窗口?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:

            QCloseEvent.accept()

        else:

            QCloseEvent.ignore()


    def delete_File(self):
        items = ['错误文件', '文本框']
        inputdialog = QtWidgets.QInputDialog()
        item, ok = inputdialog.getItem(self, "清理错误文件还是应用文本框", "语言列表", items)
        self.item = item
        if item == '文本框':
            self.text_browser.clear()
            if self.textedit.toPlainText() == "请点击'标记错误'按钮输入搜索关键词!\n":
                return
            else:
                self.textedit.clear()
        elif item == '错误文件':
            reply = QtWidgets.QMessageBox.question(self, '警告', "确定删除错误列表文件？",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                open(".\{0}.txt".format(self.fjsonrealname), "a+")
                with open(".\{0}.txt".format(self.fjsonrealname), 'r+') as file:
                    file.truncate(0)
                    QtWidgets.QMessageBox.information(self, '提示', "文件内容已删除，可重新填充",
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                      QtWidgets.QMessageBox.No)
        else:
            pass

    def error_search(self):
        s = ''
        try:
            f1 = open(".\{0}.txt".format(self.fjsonrealname), "r")
            f = f1.readlines()
            text, ok = QInputDialog.getText(self, '错误检索', '请输入关键词：')
            if ok:
                s = text
            if s == '':
                return
        except Exception as e:
            QMessageBox.information(self, 'tips', '请先打开相应地图类型文件')
            return
        for i in range(len(f)):
            if s in f[i]:
                print('line:', i + 1)
                data = f[i].split(',')[-1]
                datawrong = f[i].split(',')[-2]
                print('错误类型:' + datawrong + '    ' + '错误描述:' + data)
                # self.textedit.append('line:'+str(i+1)+'\n'+'错误类型:'+datawrong+'    '+'错误描述:'+data)
                self.textedit.append(f[i])
                continue
            else:
                self.textedit.setText('无相关信息')
                QMessageBox.information(self, 'tips', '无相关信息')
                print('sorry!')
            # print(str)
        f1.close()  # 将文件关闭

    def onHelpAbout(self):
        try:
            webbrowser.open("https://github.com/PPF12138/mapdesigner", new=0, autoraise=True)
        except Exception as e:
            webbrowser.open("https://pypi.org/project/PyQt5/", new=0, autoraise=True)
        QMessageBox.information(self, '实战PyQt5', 'PyQt5实现的桌面地图质检演示版')

    def onHelpCheck(self):
        QMessageBox.information(self, '实战PyQt5', 'PyQt5实现的文本编辑器演示版')

    def onFileNew(self):
        self.close()
        app1 = QtWidgets.QApplication(sys.argv)
        gui1 = GUI()
        gui1.show()
        time.sleep(.5)
        self.close()
        self.label.setPixmap(QPixmap(""))


    def onFileOpen(self):
        path, _ = QFileDialog.getOpenFileName(self, '打开文件', '', '文本文件 (*.txt)')
        if path:
            try:
                with open(path, 'rU') as f:
                    text = f.read()
            except Exception as e:
                self.msgCritical(str(e))
            else:
                self.path = path
                self.txtEditor.setPlainText(text)

    def onFileSave(self):
        if self.PointBoolean:
            plt.savefig(self.fname)  # 保存图片 注意 在show()之前  不然show会重新创建新的 图片
            plt.show()
        else:
            QMessageBox.information(self, '提示', '当前无图')


    def onFileSaveAs(self):
        path, _ = QFileDialog.getSaveFileName(self, '保存文件', '', '文本文件 (*.txt)')
        if not path:
            return
        plt._saveToPath(path)

    def _saveToPath(self, path):
        text = self.txtEdit.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.msgCritical(str(e))
        else:
            self.path = path

    def mouseMoveEvent(self, event):
        s = event.windowPos()
        self.setMouseTracking(True)
        self.label_mouse_x.setText('X:' + str(s.x()))
        self.label_mouse_y.setText('Y:' + str(s.y()))



    def mousePressEvent(self, event):
        s = event.windowPos()
        i = 1
        if self.picture_Boolean == False:
            return
        self.setMouseTracking(True)
        if event.buttons() == QtCore.Qt.LeftButton:  # 左键按下
            if self.PointBoolean == True:
                self.LabelX = event.windowPos().x()
                self.LabelY = event.windowPos().y()
                if 0 < self.LabelX < 700 and 100 < self.LabelY < 700:
                    # self.label.setText("单击鼠标左键的事件: 自己定义")
                    Default = QtWidgets.QMessageBox.question(self, '提示', "确定选择该点?",
                                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                             QtWidgets.QMessageBox.No)

                    if Default == QtWidgets.QMessageBox.Yes:
                        if i > 1:
                            QtWidgets.QMessageBox.question(self, '提示', "确定继续添加点？",
                                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                           QtWidgets.QMessageBox.No)
                        print("X:{0},Y:{1}".format(self.LabelX, self.LabelY))  # 响应测试语句
                        QtWidgets.QMessageBox.question(self, '提示', '选中点坐标X:{0},Y:{1}'.format(self.LabelX,
                                                                                             self.LabelY) + '\n' + '确定选中?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)

                        self.second_ui = SecondGUI.SecondUI()
                        self.second_ui.show()
                        # error_type, OK = QInputDialog.getText(self, '错误类型', '请输入错误类型:')
                        # text, ok = QInputDialog.getMultiLineText(self, '错误描述', '请输入错误描述:')
                        # if not ok:
                        #     return
                        # if text =='' or error_type == '':
                        #     return
                        # reply = QMessageBox.information(self, "导入提示",
                        #                                 "该点{0},{1}出现的{2}错误为".format(str(self.LabelX),str(self.LabelY),
                        #                                     error_type) + text,
                        #                                 QMessageBox.Yes)
                        # # strtest: tuple[str, Union[str, Any]]=("导入提示", '该地图出现的{0}错误为'.format('坐标失真') + textboxvalue)
                        # if reply == QMessageBox.Yes:
                        #     # gui=designer.
                        #     pass
                        # with open("D:\Desktop\mapshp\wrong.txt", "r+") as f:  # 设置文件对象
                        #     # f.write(('我爱Python' + os.linesep).encode('utf-8'))
                        #     # sTr=str().format('2')
                        #     count = len(f.readlines())
                        #     f.write(str(count) + ',' + '图像点类型错误:' + 'X:,' + str(self.LabelX) + 'Y:' + str(
                        #         self.LabelY) + ',' +'错误类型:  '+
                        #             error_type + ',' +'错误描述： ' + text + '\n')
                        #     # self.textbox.clear()
                        #     f.close()  # 将文件关
                        #     QMessageBox.information(self, "导入提示","已导入",QMessageBox.Yes)
                        #     return
                        global_var.labelX = self.LabelX
                        global_var.labelY = self.LabelY
                else:
                    QtWidgets.QMessageBox.question(self, '警告', "请选择图片上的点",
                                                   QtWidgets.QMessageBox.Yes)
            else:
                return
    #
    def Textvalue(self):
        self.xxoo = True
        self.ttee=True
        QtWidgets.QMessageBox.information(self, '提示', "请点击左上角的x,y图标左侧实时显示影像点坐标便于选择",
                                       QtWidgets.QMessageBox.Yes)
    def Items_File(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.addLibraryPath(os.path.join(os.path.dirname(QtCore.__file__), "plugins"))
    tmp = open('one.png', 'wb')  # 创建临时的文件
    tmp.write(base64.b64decode(one))  ##把这个one图片解码出来，写入文件中去。
    tmp.close()
    gui = GUI()
    # fileload = filedialogdemo()
    gui.show()
    # os.remove('one.png')  # 用完可以删除这个临时图片
    # label.setScaledContents(True)
    sys.exit(app.exec_())

