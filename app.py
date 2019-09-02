# -*- coding:utf-8 -*-
import sys
import time
import pyautogui as pag
from random import randrange
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Helper(QWidget):
    dirty = True
    drag = False
    title = '明日方舟护肝助手V0.1'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.screen_ref = min(screen_height, screen_width)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.resize(1280, 720)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('img/images.jpg'))
        self.setMouseTracking(True)

        self.setupUI()
        self.functionConnector()

    ##############
    # GUI Design #
    ##############
    def setupUI(self):
        self.mainlayout = QVBoxLayout(self)
        self.setLayout(self.mainlayout)
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)

        # ======= remake window title========
        self.winTitle = QHBoxLayout(self)

        self.iconLabel = QLabel(self)
        self.titleLabel = QLabel(self)
        self.minButton = QPushButton(self)
        self.closeButton = QPushButton(self)

        self.iconLabel.setAlignment(Qt.AlignLeft)
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.iconLabel.setPixmap(QPixmap("img/images.jpg").scaled(self.screen_ref*0.03, self.screen_ref*0.03))
        self.titleLabel.setText(self.title)
        self.titleLabel.setFont(QFont('Microsoft YaHei UI', 15))
        self.minButton.setIcon(QIcon("img/minimize.png"))
        self.minButton.setIconSize(QSize(self.screen_ref*0.03, self.screen_ref*0.03))
        self.minButton.setStyleSheet("QPushButton{border:none};")
        self.closeButton.setIcon(QIcon("img/cancel.png"))
        self.closeButton.setIconSize(QSize(self.screen_ref * 0.03, self.screen_ref * 0.03))
        self.closeButton.setStyleSheet("QPushButton{border:none};")

        # screen info on wintitle
        self.infoLayout = QVBoxLayout()

        self.frameInfoLayout = QHBoxLayout()
        self.frameHtLabel = QLabel('高[720]像素')
        self.frameWdLabel = QLabel('宽[1280]像素')
        self.frameInfoLayout.addWidget(self.frameWdLabel)
        self.frameInfoLayout.addWidget(self.frameHtLabel)
        self.infoLayout.addLayout(self.frameInfoLayout)

        self.mouseInfoLayout = QHBoxLayout()
        self.mouseRefPos = QLabel('(0.50, 0.50)')
        self.mouseInfoLayout.addWidget(QLabel('鼠标相对坐标:'))
        self.mouseInfoLayout.addWidget(self.mouseRefPos)
        self.infoLayout.addLayout(self.mouseInfoLayout)

        # combine widgets
        self.winTitle.addWidget(self.iconLabel)
        self.winTitle.addWidget(self.titleLabel)
        self.winTitle.addLayout(self.infoLayout)
        self.winTitle.addStretch()
        self.winTitle.addWidget(self.minButton)
        self.winTitle.addWidget(self.closeButton)

        self.mainlayout.addLayout(self.winTitle)

        # ======== set transparent simulator control ==========
        self.simulatorWidget = QWidget()
        self.simulatorWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mainlayout.addWidget(self.simulatorWidget)

        # ======== set bottom tools ===========
        self.toolLayout = QHBoxLayout()
        #self.toolLayout.setContentsMargins(5, 5, 5, 5)

        # Script Choice
        self.scriptChoiceLayout = QVBoxLayout()
        self.scriptChoice = QComboBox()
        # Todo: Load Configure to items
        self.scriptChoice.addItems(['OF_7', 'OF_F4'])
        self.scriptChoice.setFixedHeight(int(self.screen_ref*0.02))

        self.scriptChoiceLayout.addWidget(QLabel('选择辅助脚本：'))
        self.scriptChoiceLayout.addWidget(self.scriptChoice)

        self.toolLayout.addLayout(self.scriptChoiceLayout)
        self.toolLayout.addWidget(VLine())

        # Time Input
        self.loopTimeLayout = QVBoxLayout()
        self.loopTime = QSpinBox()
        self.loopTime.setRange(0, 30)
        self.loopTime.setValue(0)
        self.loopTime.setFixedHeight(int(self.screen_ref * 0.02))

        self.loopTimeLayout.addWidget(QLabel('执行次数：'))
        self.loopTimeLayout.addWidget(self.loopTime)

        self.toolLayout.addLayout(self.loopTimeLayout)

        # Start Btn
        self.startButton = QPushButton('开始')
        self.startButton.setFixedHeight(int(self.screen_ref*0.04))

        self.toolLayout.addWidget(self.startButton)

        self.toolLayout.addStretch()

        self.sizegrip = QSizeGrip(self)
        self.toolLayout.addWidget(self.sizegrip, 0, Qt.AlignBottom | Qt.AlignRight)

        self.mainlayout.addLayout(self.toolLayout)

    def functionConnector(self):
        self.minButton.clicked.connect(self.showMininizedWindow)
        self.closeButton.clicked.connect(self.closeWindow)
        self.scriptChoice.currentIndexChanged.connect(self.scriptChanges)

    def showMininizedWindow(self):
        self.setWindowState(Qt.WindowMinimized)

    def closeWindow(self):
        sys.exit()

    def updateMask(self):
        frameRect = self.frameGeometry()
        frame_width = frameRect.width()
        frame_height = frameRect.height()
        titleRect = self.winTitle.geometry()
        title_height = titleRect.height()
        toolRect = self.toolLayout.geometry()
        tool_height = toolRect.height()

        trans_height = frame_height-title_height-tool_height
        trans_width = frame_width-2

        region = QRegion(QRect(0, 0, frameRect.right(), frameRect.bottom()))
        # "subtract" the grabWidget rectangle to get a mask that only contains
        # the window titlebar, margins and panel
        region -= QRegion(QRect(1, titleRect.bottom(), trans_width, trans_height))
        self.setMask(region)

        self.frameHtLabel.setText(f'高[{trans_height}]像素')
        self.frameWdLabel.setText(f'宽[{trans_width}]像素')

    def resizeEvent(self, event):
        super(Helper, self).resizeEvent(event)
        # the first resizeEvent is called *before* any first-time showEvent and
        # paintEvent, there's no need to update the mask until then; see below
        if not self.dirty:
            self.updateMask()

    def paintEvent(self, event):
        super(Helper, self).paintEvent(event)
        # on Linux the frameGeometry is actually updated "sometime" after show()
        # is called; on Windows and MacOS it *should* happen as soon as the first
        # non-spontaneous showEvent is called (programmatically called: showEvent
        # is also called whenever a window is restored after it has been
        # minimized); we can assume that all that has already happened as soon as
        # the first paintEvent is called; before then the window is flagged as
        # "dirty", meaning that there's no need to update its mask yet.
        # Once paintEvent has been called the first time, the geometries should
        # have been already updated, we can mark the geometries "clean" and then
        # actually apply the mask.
        if self.dirty:
            self.updateMask()
            self.dirty = False

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.drag = True

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.NoButton:
            pass
        elif event.buttons() == Qt.LeftButton and self.drag:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.drag = False

    def scriptChanges(self):
        print(self.scriptChoice.currentText())

    #####################
    #  Mouse Controller #
    #####################
    def updateMouseRelativePos(self):
        # need to add asyn here
        x, y = pag.position()
        time.sleep(0.2)



class VLine(QFrame):
    # a simple VLine, like the one you get from designer
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine | self.Sunken)
        self.setLineWidth(3)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_height = app.primaryScreen().size().height()
    screen_width = app.primaryScreen().size().width()
    helper = Helper()
    helper.show()
    sys.exit(app.exec_())