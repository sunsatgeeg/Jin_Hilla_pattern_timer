import win32gui
import pyautogui as pg
from time import sleep
import numpy as np
import cv2 as cv
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from sklearn.cluster import KMeans
from PyQt5 import QtCore, QtGui
import ctypes


DURATION_INT = 1798

def secs_to_minsec(secs: int):
    mins = secs // 60
    secs = secs % 60
    minsec = f'{mins:02}:{secs:02}'
    return minsec

#쓰레드 선언
class Introscreen(QThread):
    def run(self):
        print("입장 화면 찾기")
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
            print("입장", max_val, top_left)
            if max_val > 200:
                break

class hillaicon(QThread):
    def run(self):
        print("힐라 아이콘 감지")
        img_piece = cv.imread('hilla.png', cv.IMREAD_COLOR)
        h, w = img_piece.shape[:2]
        hwnd = win32gui.FindWindow(None, "MapleStory")
        tup = win32gui.GetWindowRect(hwnd)
        ew = int(((tup[2] - tup[0]) / 2) + tup[0] - 405)
        eh = int(((tup[3] - tup[1]) / 2) + tup[1] - 535)
        global icon1
        global icon2
        while 1:
            pic = pg.screenshot(region=(ew, eh, 50, 50))
            img_frame = np.array(pic)
            img_frame = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)
            meth = 'cv.TM_CCOEFF'
            method = eval(meth)
            res = cv.matchTemplate(img_piece, img_frame, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv.rectangle(img_frame, top_left, bottom_right, (0, 255, 0), 2)
            print("아이콘",max_val, top_left)
            if max_val > 7000000:
                icon1 = ew + top_left[0]
                icon2 = eh + top_left[1]
                break

class Sickle(QThread):
    def run(self):
        sleep(3)
        print("패턴 감지")
        img_piece = cv.imread('sickle.png', cv.IMREAD_COLOR)
        h, w = img_piece.shape[:2]
        hwnd = win32gui.FindWindow(None, "MapleStory")
        tup = win32gui.GetWindowRect(hwnd)
        ew = int(((tup[2] - tup[0])/2)+tup[0]-120)
        eh = int(((tup[3] - tup[1])/2)+tup[1]-110)
        while 1:
            pic = pg.screenshot(region=(ew, eh, 240, 240))
            img_frame = np.array(pic)
            img_frame = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)
            meth = 'cv.TM_CCOEFF'
            method = eval(meth)
            res = cv.matchTemplate(img_piece, img_frame, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv.rectangle(img_frame, top_left, bottom_right, (0, 255, 0), 2)
            print("패턴",max_val, top_left)
            if max_val > 300000000:
                break

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.time_left_int = DURATION_INT
        self.myTimer = QtCore.QTimer(self)
        self.myTimer.timeout.connect(self.timerTimeout)

        self.introscreen = Introscreen(self)
        self.hillaicon = hillaicon(self)
        self.sickle = Sickle(self)
        self.introscreen.finished.connect(self.introscreenthreadStop)  # 종료 이벤트 연결
        self.hillaicon.finished.connect(self.hillaiconstop)  # 종료 이벤트 연결
        self.sickle.finished.connect(self.sicklethreadStop)  # 종료 이벤트 연결

        self.setWindowTitle("진힐라 패턴 체크")
        self.setGeometry(100, 100, 300, 280)

        self.lcd = QLCDNumber()
        self.lcd.display('')
        self.lcd.setDigitCount(5)
        subLayout = QHBoxLayout()

        self.label1 = QLabel('<b>패턴 오는 시간<b>')
        self.label1.setAlignment(Qt.AlignCenter)

        self.label1.setFont(QtGui.QFont("맑은 고딕", 15))  # 폰트,크기 조절

        self.lcd1 = QLCDNumber()
        self.lcd1.display('')
        self.lcd1.setDigitCount(5)

        self.btnStart = QPushButton("시작")
        self.btnStart.clicked.connect(self.maplewindowsstatecheck)
        self.btnReset = QPushButton("사용법")
        self.btnReset.clicked.connect(self.help)

        layout = QGridLayout()

        self.lcd.setMaximumWidth(10000)
        self.lcd1.setMaximumWidth(10000)
        self.label1.setMaximumHeight(30)
        layout.addWidget(self.lcd,0,0,1,0)
        layout.addWidget(self.lcd1,2,0,1,0)
        layout.addWidget(self.label1,1,0,1,0)
        subLayout.addWidget(self.btnStart)
        subLayout.addWidget(self.btnReset)

        layout.addLayout(subLayout,3,0)

        self.setLayout(layout)

        self.update_gui()

    def help(self):
        self.btnStart.setEnabled(False)
        self.btnReset.setEnabled(False)
        msg1 = ctypes.windll.user32.MessageBoxW(None, "진 힐라 입장 전에 시작 버튼 누르시면 됩니다.", "", 0)
        if msg1 == 1:
            self.btnStart.setEnabled(True)
            self.btnReset.setEnabled(True)


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
            self.introscreen.start()

    def introscreenthreadStop(self):
        print("Thread stopped!")
        self.startTimer()

    def startTimer(self):
        print("카운트 시작")
        self.time_left_int = DURATION_INT
        self.myTimer.start(1000)
        self.hillaicon.start()

    def timerTimeout(self):
        self.time_left_int -= 1
        if self.time_left_int == 0:
            self.time_left_int = DURATION_INT
        self.update_gui()

    def update_gui(self):
        minsec = secs_to_minsec(self.time_left_int)
        self.lcd.display(minsec)

    def hillaiconstop(self):
        self.sickle.start()

    def sicklethreadStop(self):
        for i in range(1):
            pic = pg.screenshot(region=(icon1 + 187, icon2, 1, 8))
            img_frame = np.array(pic)
            img_frame = cv.cvtColor(img_frame, cv.COLOR_BGR2RGB)

            image = img_frame.reshape((img_frame.shape[0] * img_frame.shape[1], 3))  # height, width 통합

            k = 1  # 예제는 5개로 나누겠습니다
            clt = KMeans(n_clusters=k)
            clt.fit(image)

            for center in clt.cluster_centers_:
                break

            if center[2] < 57 or 70 < center[2] < 90:
                minsec = secs_to_minsec(self.time_left_int - 150)
                self.lcd1.display(minsec)
                self.label1 = QLabel('1페이즈 패턴')
            else:
                pic = pg.screenshot(region=(icon1 + 338, icon2, 1, 8))
                img_frame = np.array(pic)
                img_frame = cv.cvtColor(img_frame, cv.COLOR_BGR2RGB)

                image = img_frame.reshape((img_frame.shape[0] * img_frame.shape[1], 3))  # height, width 통합

                k = 1  # 예제는 5개로 나누겠습니다
                clt = KMeans(n_clusters=k)
                clt.fit(image)

                for center in clt.cluster_centers_:
                    break

                print(center)

                if 150 < center[2] < 170 or 70 < center[2] < 90:
                    minsec = secs_to_minsec(self.time_left_int - 125)
                    self.lcd1.display(minsec)
                    self.label1 = QLabel('2페이즈 패턴')
                else:
                    minsec = secs_to_minsec(self.time_left_int - 100)
                    self.lcd1.display(minsec)
                    self.label1 = QLabel('3페이즈 패턴')
        self.sickle.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())