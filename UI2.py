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
from PyQt5.QtCore import *


DURATION_INT = 1799

def secs_to_minsec(secs: int):
    mins = secs // 60
    secs = secs % 60
    minsec = f'{mins:02}:{secs:02}'
    return minsec

class ThreadClass(QtCore.QThread):
    def __init__(self, parent = None):
        super(ThreadClass,self).__init__(parent)
    def run(self):
        self.time_left_int = DURATION_INT
        self.myTimer = QtCore.QTimer(self)
        self.setWindowTitle("진힐라 패턴 체크")
        self.setGeometry(100, 100, 600, 280)

        layout = QVBoxLayout()

        self.lcd = QLCDNumber()
        self.lcd.display('')
        self.lcd.setDigitCount(5)
        subLayout = QHBoxLayout()

        self.lcd1 = QLCDNumber()
        self.lcd1.display('')
        self.lcd1.setDigitCount(5)

        self.lcd2 = QLCDNumber()
        self.lcd2.display('')
        self.lcd2.setDigitCount(5)

        self.lcd3 = QLCDNumber()
        self.lcd3.display('')
        self.lcd3.setDigitCount(5)

        self.btnStart = QPushButton("시작")
        self.btnStart.clicked.connect(self.maplewindowsstatecheck)
        self.btnReset = QPushButton("초기화")

        layout = QGridLayout()

        self.lcd.setMaximumWidth(10000)
        layout.addWidget(self.lcd,0,0,1,0)
        layout.addWidget(self.lcd1,1,0)
        layout.addWidget(self.lcd2,1,1)
        layout.addWidget(self.lcd3,1,2)

        subLayout.addWidget(self.btnStart)
        subLayout.addWidget(self.btnReset)

        layout.addLayout(subLayout,2,1)

        self.setLayout(layout)

        self.btnReset.setEnabled(False)

        self.update_gui()

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.threadclass = ThreadClass()
        self.threadclass.start()

    def maplewindowsstatecheck(self):
        hwnd = win32gui.FindWindow(None, "MapleStory")
        rect = win32gui.GetWindowRect(hwnd)
        ex = rect[0]
        if ex == (-32000):
            msg = ctypes.windll.user32.MessageBoxW(None, "메이플 최소화 상태", "", 0)
            if msg == 1:
                print("OK")
        else:
            print("힐라 입장 대기")
            self.btnStart.setEnabled(False)
            self.btnReset.setEnabled(True)
            self.threadclass.start()

    def start(self):
        img_piece = cv.imread('start.png', cv.IMREAD_COLOR)
        h, w = img_piece.shape[:2]
        hwnd = win32gui.FindWindow(None, "MapleStory")
        tup = win32gui.GetWindowRect(hwnd)
        ew = int(((tup[2] - tup[0]) / 2) + tup[0] - 120)
        eh = int(((tup[3] - tup[1]) / 2) + tup[1] - 250)
        while 1:
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
            if max_val > 200:
                self.threadclass.join()
                self.MyWindow()
                break


#    def start(self):
#        img_piece = cv.imread('start.png', cv.IMREAD_COLOR)
#        h, w = img_piece.shape[:2]
#        hwnd = win32gui.FindWindow(None, "MapleStory")
#        tup = win32gui.GetWindowRect(hwnd)
#        ew = int(((tup[2] - tup[0]) / 2) + tup[0] - 120)
#        eh = int(((tup[3] - tup[1]) / 2) + tup[1] - 250)
#        while 1:
#            pic = pg.screenshot(region=(ew, eh, 120, 120))
#            img_frame = np.array(pic)
#            img_frame = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)
#            meth = 'cv.TM_CCOEFF'
#            method = eval(meth)
#            res = cv.matchTemplate(img_piece, img_frame, method)
#            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
#            top_left = max_loc
#            bottom_right = (top_left[0] + w, top_left[1] + h)
#            cv.rectangle(img_frame, top_left, bottom_right, (0, 255, 0), 2)
#            print(max_val, top_left)
#            if max_val > 200:
#                break

#    def thread(self):
#        thread = self.threadclass
#        thread.daemon = True  # 프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
#        print("thread 시작")
#        thread.start()
#        thread.join()
#        print("thread 종료")
#        self.startTimer()
#



    def startTimer(self):
        print("카운트 시작")
        self.time_left_int = DURATION_INT

        self.myTimer.timeout.connect(self.timerTimeout)
        self.myTimer.start(1000)

    def timerTimeout(self):
        self.time_left_int -= 1

        if self.time_left_int == 0:
            self.time_left_int = DURATION_INT

        self.update_gui()

    def update_gui(self):
        minsec = secs_to_minsec(self.time_left_int)
        self.lcd.display(minsec)

#    def patterncheck(self):
#        print("패턴 체크 시작")
#        img_piece = cv.imread('sickle.png', cv.IMREAD_COLOR)
#        h, w = img_piece.shape[:2]
#
#        hwnd = win32gui.FindWindow(None, "MapleStory")
#        tup = win32gui.GetWindowRect(hwnd)
#
#        ew = int(((tup[2] - tup[0])/2)+tup[0]-120)
#        eh = int(((tup[3] - tup[1])/2)+tup[1]-120)
#
#        while 1:
#            pic = pg.screenshot(region=(ew, eh, 240, 240))
#            img_frame = np.array(pic)
#            img_frame = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)
#            meth = 'cv.TM_CCOEFF'
#            method = eval(meth)
#
#            res = cv.matchTemplate(img_piece, img_frame, method)
#            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
#            top_left = max_loc
#            bottom_right = (top_left[0] + w, top_left[1] + h)
#
#            cv.rectangle(img_frame, top_left, bottom_right, (0, 255, 0), 2)
##            print(max_val, top_left)
#            if max_val>400000000:
#                msg = ctypes.windll.user32.MessageBoxW(None, "패턴", "", 0)
#                if msg == 1:
#                    print("OK")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    ThreadClass = ThreadClass()
    ThreadClass.show()
    sys.exit(app.exec_())
