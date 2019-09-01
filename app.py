# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Helper(QMainWindow):

    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle('明日方舟护肝小助手')
        self.resize(1280, 720)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setStyleSheet("background:transparent;")
        #self.setStyleSheet("background-color: rgba(100,0,0,0);")
        self.setWindowOpacity(0.5)
        #self.setAttribute(Qt.WA_TransparentForMouseEvents)
        #self.setFocusPolicy(Qt.NoFocus)
        #self.setWindowFlags(Qt.WindowTransparentForInput | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        self.mainWidget = QWidget()
        self.mainWidget.setWindowFlags(Qt.WindowTransparentForInput | Qt.WindowStaysOnTopHint)
        self.mainWidget.setStyleSheet("background:transparent;")
        self.setCentralWidget(self.mainWidget)
    '''
    def __init__(self, parent=None):
        
        super().__init__(parent)
        
        self.setWindowTitle('明日方舟护肝小助手')
        self.resize(1280, 720)
        
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.setStyleSheet("border: 1px solid rgba(0, 0, 0, 0.15);")
        self.setSizeGripEnabled(True);
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    helper = Helper()
    helper.show()
    sys.exit(app.exec_())