# -*- coding:utf-8 -*-
import os
import sys
import time
import pyautogui as pag
from datetime import datetime
from random import randrange
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Helper(QWidget):
    dirty = True
    drag = False
    title = '明日方舟护肝助手V0.1'
    simulator = {'Left': 0, 'Top': 0, 'Width': 1280, 'Height': 720}
    script_list = []
    run_times = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.screen_ref = min(screen_height, screen_width)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.resize(1600+2, 900+126)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('img/images.jpg'))
        self.setMouseTracking(True)

        self.mouseTimer = QTimer(self)
        self.mouseTimer.start(200)
        self.runner = Runner(self)

        self.setupUI()
        self.functionConnector()

        self.loadScriptList()

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

        # Script Choice
        self.scriptChoiceLayout = QVBoxLayout()
        self.scriptChoice = QComboBox()
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
        self.mouseTimer.timeout.connect(self.updateMouseRelativePos)
        self.scriptChoice.currentIndexChanged.connect(self.scriptChanges)
        self.startButton.clicked.connect(self.runScript)
        self.runner.sigOut.connect(self.finish_once)

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

        self.simulator['Height'] = trans_height
        self.simulator['Width'] = trans_width
        self.simulator['Left'] = frameRect.left() + 1
        self.simulator['Top'] = frameRect.top() + title_height

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
            self.updateMask()

    def mouseReleaseEvent(self, event):
        self.drag = False

    def updateMouseRelativePos(self):
        # need to add asyn here
        x, y = pag.position()
        rel_x, rel_y = self.abslute2relative(x, y)
        self.mouseRefPos.setText(f"({format(rel_x, '.3f')}, {format(rel_y, '.3f')})")

    def abslute2relative(self, x, y):
        rel_x = (x - self.simulator['Left']) / self.simulator['Width']
        rel_y = (y - self.simulator['Top']) / self.simulator['Height']
        return rel_x, rel_y

    def relative2abslute(self, rel_x, rel_y):
        x = rel_x * self.simulator['Width'] + self.simulator['Left']
        y = rel_y * self.simulator['Height'] + self.simulator['Top']
        return x, y

    ##################
    #  Script Loader #
    ##################
    def loadScriptList(self):
        if not os.path.exists('Scripts/'):
            os.mkdir('Scripts')
        files = os.listdir('Scripts/')
        for f in files:
            if '.ark' in f:
                if 'run.ash' in os.listdir(f'Scripts/{f}/'):
                    self.script_list.append(f[:-4])

        if len(self.script_list) > 0:
            self.scriptChoice.addItems(self.script_list)
            self.startButton.setEnabled(True)
        else:
            QMessageBox.about(self, '警告', '未发现脚本，请将脚本文件复制到创建的Scripts文件夹内')
            self.startButton.setEnabled(False)

    def scriptChanges(self):
        print(self.scriptChoice.currentText())

    def runScript(self):
        if self.startButton.text() == '开始':
            self.run_times = self.loopTime.value()
            if self.run_times > 0:
                self.script_name = self.scriptChoice.currentText()
                self.current_dir = f'Scripts/{self.script_name}.ark/'
                script = ''
                with open(self.current_dir + 'run.ash') as f:
                    for row in f.readlines():
                        row = row.replace('click(', 'self.click(')
                        row = row.replace('set_skip_img(', 'self.set_skip_img(')
                        script += row
                # print(script)
                self.runner.set_params(script, current_dir=self.current_dir, simulator=self.simulator)
                self.runner.start()
                self.startButton.setText('结束')
                self.sizegrip.setEnabled(False)
            else:
                print('[Warning]: 执行次数请>1!')
        else:
            self.runner.terminate()
            self.runner.wait()
            self.startButton.setText('开始')
            self.sizegrip.setEnabled(True)
            self.loopTime.setValue(0)

    def finish_once(self):
        self.run_times -= 1
        print(f'[ Info {datetime.now().strftime("%H:%M:%S")}] 剩余{self.run_times}次')
        self.loopTime.setValue(self.run_times)
        if self.run_times > 0:
            self.runner.start()
        else:
            print(f'[ Info {datetime.now().strftime("%H:%M:%S")}] “{self.script_name}” 执行完毕')


class VLine(QFrame):
    # a simple VLine, like the one you get from designer
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine | self.Sunken)
        self.setLineWidth(3)

class Runner(QThread):
    sigOut = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.run_code = ''
        self.current_dir = ''
        self.simulator = {}
        self.skip_img_list = []
        self.stop_img_list = []

    def set_params(self, code, current_dir, simulator):
        self.run_code = code
        self.current_dir = current_dir
        self.simulator = simulator

    def run(self):
        exec(self.run_code)
        self.sigOut.emit(True)

    #####################
    #  Mouse Controller #
    #####################
    def _getImgAbsPos(self, img_name, confidence=0.90):
        img_list = img_name.split(' | ')
        click_pos = None
        for img in img_list:
            try:
                absLocation = pag.locateOnScreen(self.current_dir + 'img/' + img,
                                                 region=(self.simulator['Left'], self.simulator['Top'],
                                                         self.simulator['Width'], self.simulator['Height']),
                                                 confidence=confidence)
            except ValueError:
                absLocation = None
                print('[Warning]: 当前窗口大小比img中图片要小，请设置正确的分辨率！')

            if absLocation is not None:
                w = absLocation.width
                h = absLocation.height
                absCenter = pag.center(absLocation)
                center_x = absCenter.x
                center_y = absCenter.y
                click_x = randrange(int(center_x - 0.3 * w), int(center_x + 0.3 * w), 1)
                click_y = randrange(int(center_y - 0.3 * h), int(center_y + 0.3 * h), 1)
                click_pos = (click_x, click_y)
                return click_pos

        return click_pos

    def click(self, img_name, frequency=2):
        # check whether exist, not -> wait until exist
        # if exist, click, mark as found.
        # check if exist, still exist -> reclick, not exist -> next click command
        loop = True
        found = False
        while loop:
            self._check_stop_img()
            self._check_skip_img()
            abspos = self._getImgAbsPos(img_name)
            if abspos is None and not found:
                # check whether exist, not -> keep checking until exist
                print(
                    f'{datetime.now().strftime("%H:%M:%S")}[Warning] Picture "{img_name}" not found, wait for {frequency}s',
                    end='\r')
                time.sleep(frequency)

            if abspos is not None and not found:
                # the first time to find a position
                found = True
                print(
                    f'{datetime.now().strftime("%H:%M:%S")}[ info ] Picture "{img_name}" position {abspos} found, trying to click')
                pag.moveTo(*abspos, duration=0.5)
                pag.click()

            if abspos is not None and found:
                # still find the image after clicking -> click fail -> reclick
                print(f'{datetime.now().strftime("%H:%M:%S")}[Warning] Click "{img_name}" fail, trying to reclick',
                      end='\r')
                pag.click()

            if abspos is None and found:
                loop = False

    def click_pos(self, x, y, sleep_time=2):
        # this can operate directly
        pag.click(helper.relative2abslute(x, y))

    def img_exist(self, img_name):
        abspos = self._getImgAbsPos(img_name)
        if abspos is not None:
            return True
        else:
            return False

    def set_skip_img(self, img_name):
        self.skip_img_list = img_name.split(' | ')

    def set_stop_img(self, img_name):
        self.stop_img_list = img_name.split(' | ')

    def _check_skip_img(self):
        for skip in self.skip_img_list:
            if self.img_exist(skip):
                self.click_pos(0.5, 0.5)
                print(f'{datetime.now().strftime("%H:%M:%S")}[ Info] Skip "{skip}" ')

    def _check_stop_img(self):
        for stop in self.stop_img_list:
            if self.img_exist(stop):
                # do something here
                helper.loopTime.setValue(0)
                print(f'{datetime.now().strftime("%H:%M:%S")}[ Info] Catch stop image "{stop}", stop running')
                self.terminate()
                self.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_height = app.primaryScreen().size().height()
    screen_width = app.primaryScreen().size().width()
    helper = Helper()
    helper.show()
    sys.exit(app.exec_())