import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import win32gui
import pyautogui as pg
import threading
from time import sleep
import ctypes
import numpy as np
import cv2 as cv
import sys
from PyQt5.QtWidgets import *

import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

DURATION_INT = 1799
max_val = 0

def secs_to_minsec(secs: int):
    mins = secs // 60
    secs = secs % 60
    minsec = f'{mins:02}:{secs:02}'
    return minsec

class ShowVideo(QtCore.QObject):
    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startVideo(self):
        print("입장 화면 찾기")
        img_piece = cv.imread('start.png', cv.IMREAD_COLOR)
        h, w = img_piece.shape[:2]
        hwnd = win32gui.FindWindow(None, "MapleStory")
        tup = win32gui.GetWindowRect(hwnd)
        ew = int(((tup[2] - tup[0]) / 2) + tup[0] - 240)
        eh = int(((tup[3] - tup[1]) / 2) + tup[1] - 240)
        global max_val
        while max_val < 200:
            pic = pg.screenshot(region=(ew, eh, 120, 120))
            img_frame = np.array(pic)
            img_frame = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)
            meth = 'cv.TM_CCOEFF'
            method = eval(meth)
            res = cv.matchTemplate(img_piece, img_frame, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv.rectangle(img_frame, top_left, bottom_right, (0, 255, 0), 2)
            print(max_val, top_left)

        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(25, loop.quit) #25 ms
        loop.exec_()

    @QtCore.pyqtSlot()
    def canny(self):
        self.flag = 1 - self.flag


class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.time_left_int = DURATION_INT
        self.myTimer = QtCore.QTimer(self)

    def initUI(self):
        self.setWindowTitle('Test')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)


    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)

    push_button1 = QtWidgets.QPushButton('Start')
    push_button2 = QtWidgets.QPushButton('Canny')
    push_button1.clicked.connect(vid.startVideo)
    push_button2.clicked.connect(vid.canny)

    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout = QtWidgets.QHBoxLayout()
    vertical_layout.addLayout(horizontal_layout)
    vertical_layout.addWidget(push_button1)
    vertical_layout.addWidget(push_button2)

    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())