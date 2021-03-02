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

class Thread1(QtCore.QObject):
    def __init__(self, parent=None):
        super(Thread1, self).__init__(parent)

    def run(self):
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
        QtCore.QTimer.singleShot(25, loop.quit)  # 25 ms
        loop.exec_()
        print("O")




class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.time_left_int = DURATION_INT
        self.myTimer = QtCore.QTimer(self)
        self.setWindowTitle("진힐라 패턴 체크")
        self.setGeometry(100, 100, 600, 280)


        layout = QVBoxLayout()

        self.lcd = QLCDNumber()
        self.lcd.display('')
        self.lcd.setDigitCount(5)

        self.lcd1 = QLCDNumber()
        self.lcd1.display('')
        self.lcd1.setDigitCount(5)

        self.lcd2 = QLCDNumber()
        self.lcd2.display('')
        self.lcd2.setDigitCount(5)

        self.lcd3 = QLCDNumber()
        self.lcd3.display('')
        self.lcd3.setDigitCount(5)



        layout = QGridLayout()

        self.lcd.setMaximumWidth(10000)
        layout.addWidget(self.lcd,0,0,1,0)
        layout.addWidget(self.lcd1,1,0)
        layout.addWidget(self.lcd2,1,1)
        layout.addWidget(self.lcd3,1,2)



        layout.addLayout(subLayout,2,1)

        self.setLayout(layout)

        self.update_gui()

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
            self.threadwait()



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
        print(minsec)
        self.lcd.display(minsec)

    def startintro(self):
            print("입장 화면 찾기")
            img_piece = cv.imread('start.png', cv.IMREAD_COLOR)
            h, w = img_piece.shape[:2]
            hwnd = win32gui.FindWindow(None, "MapleStory")
            tup = win32gui.GetWindowRect(hwnd)
            ew = int(((tup[2] - tup[0]) / 2) + tup[0] - 120)
            eh = int(((tup[3] - tup[1]) / 2) + tup[1] - 250)
            def threadintro():
                global max_val
                while max_val > 200:
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
            thread1 = threading.Thread(target=threadintro)
            thread1.daemon = True
            print("thread 시작")
            thread1.start()
            if max_val > 200:
                thread1.cancel()
                print("thread 종료")





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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    thread = QtCore.QThread()
    thread.start()
    scan = Thread1()
    scan.moveToThread(thread)

    push_button1 = QtWidgets.QPushButton("시작")
    push_button2 = QtWidgets.QPushButton("초기화")
    push_button2.clicked.connect(scan.run)

    subLayout = QHBoxLayout()
    subLayout.addWidget(push_button1)
    subLayout.addWidget(push_button2)

    push_button2.setEnabled(False)

    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())