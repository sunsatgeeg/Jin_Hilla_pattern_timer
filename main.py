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
from PyQt5.QtGui import QIcon
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

global Cal
global kk
global minsec1
global minsec2
global interv
DURATION_INT = 1798
Cal = 0
kk = 0
minsec1 = 1634
minsec2 = 3
interv = 0
cv.namedWindow("result");
cv.moveWindow("result", 0, 500);


def secs_to_minsec(secs: int):
    mins = secs // 60
    secs = secs % 60
    minsec = f'{mins:02}:{secs:02}'
    return minsec

#쓰레드 선언
class Introscreen(QThread):
    def run(self):
        print("입장 화면 찾기 시작")
        img_piece = cv.imread(resource_path('img/start.png'), cv.IMREAD_COLOR)
        h, w = img_piece.shape[:2]
        hwnd = win32gui.FindWindow(None, "MapleStory")
        tup = win32gui.GetWindowRect(hwnd)
        ew = int(((tup[2] - tup[0]) / 2) + tup[0] - 120)
        eh = int(((tup[3] - tup[1]) / 2) + tup[1] - 250)
        while 1:
            sleep(0.1)
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
            if max_val > 200:
                print("입장")
                break

class Hillaicon(QThread):
    def run(self):
        print("시계 아이콘 감지 시작")
        img_piece = cv.imread(resource_path('img/time.png'), cv.IMREAD_COLOR)
        h, w = img_piece.shape[:2]
        hwnd = win32gui.FindWindow(None, "MapleStory")
        tup = win32gui.GetWindowRect(hwnd)
        ew = int((((tup[2] - tup[0]) / 2) + tup[0]) - 120)
        eh = int(tup[1])
        global icon1
        global icon2
        while 1:
            sleep(1)
            pic = pg.screenshot(region=(ew, eh, 60, 120))
            img_frame = np.array(pic)
            img_frame = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)
            meth = 'cv.TM_CCOEFF'
            method = eval(meth)
            res = cv.matchTemplate(img_piece, img_frame, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv.rectangle(img_frame, top_left, bottom_right, (0, 255, 0), 2)
            if 360000 <= max_val <= 370000:
                icon1 = ew + top_left[0]
                icon2 = eh + top_left[1]
                print("시계 아이콘 감지")
                break

class Sickle(QThread):
    def run(self):
        sleep(5)
        print("패턴 1차 감지 시작")
        while 1:
            sleep(0.1)
            pic = pg.screenshot(region=(icon1+118, icon2+280, 54, 17))
            img_frame = np.array(pic)
            img_frame = cv.cvtColor(img_frame, cv.COLOR_BGR2RGB)

            image = img_frame.reshape((img_frame.shape[0] * img_frame.shape[1], 3))

            k = 1
            clt = KMeans(n_clusters=k)
            clt.fit(image)

            self.kk = 1
            cv.imshow('result', img_frame)
            for center in clt.cluster_centers_:
                break

            print(center,"1")
            if int(center[0]) == 0 and int(center[1]) == 0 and int(center[2]) == 0:
                print("패턴 확인 1차")
                break

class Sickle2(QThread):
    def run(self):
        print("패턴 2차 감지 시작")
        self.interv = 0
        while 1:
            sleep(0.1)
            pic = pg.screenshot(region=(icon1 + 118, icon2 + 280, 54, 17))
            img_frame = np.array(pic)
            img_frame = cv.cvtColor(img_frame, cv.COLOR_BGR2RGB)

            image = img_frame.reshape((img_frame.shape[0] * img_frame.shape[1], 3))

            k = 1
            clt = KMeans(n_clusters=k)
            clt.fit(image)
            self.interv += 1
            self.kk = 1
            cv.imshow('result', img_frame)
            for center in clt.cluster_centers_:
                break

            print(center, "2")
            if int(center[0]) == 255 and int(center[1]) == 255 and int(center[2]) == 255:
                print("패턴 확인 2차")
                break

            if self.interv == 30:
                print("2차 패턴 확인 실패")
                break

class Sickle3(QThread):
    def run(self):
        print("패턴 3차 감지 시작")
        interv = 0
        while 1:
            sleep(0.1)
            pic = pg.screenshot(region=(icon1 + 118, icon2 + 280, 54, 17))
            img_frame = np.array(pic)
            img_frame = cv.cvtColor(img_frame, cv.COLOR_BGR2RGB)

            image = img_frame.reshape((img_frame.shape[0] * img_frame.shape[1], 3))

            k = 1
            clt = KMeans(n_clusters=k)
            clt.fit(image)

            self.kk = 1
            cv.imshow('result', img_frame)
            for center in clt.cluster_centers_:
                break

            print(center, "3")
            if int(center[0]) == 0 and int(center[1]) == 0 and int(center[2]) == 0:
                print("패턴 클리어")
                break

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.time_left_int = DURATION_INT
        self.Cal = Cal
        self.kk = kk
        self.minsec1 = minsec1
        self.minsec2 = minsec2
        self.interv = interv
        self.myTimer = QtCore.QTimer(self)
        self.myTimer.timeout.connect(self.timerTimeout)

        self.introscreen = Introscreen(self)
        self.hillaicon = Hillaicon(self)
        self.sickle = Sickle(self)
        self.sickle2 = Sickle2(self)
        self.sickle3 = Sickle3(self)
        self.introscreen.finished.connect(self.introscreenthreadStop)
        self.hillaicon.finished.connect(self.hillaiconstop)
        self.sickle.finished.connect(self.sicklethreadStop)
        self.sickle2.finished.connect(self.sicklethreadStop2)
        self.sickle3.finished.connect(self.sicklethreadStop3)

        self.setWindowTitle("Time")
        self.setGeometry(960, 540, 300, 280)

        self.lcd = QLCDNumber()
        self.lcd.display('')
        self.lcd.setDigitCount(5)
        subLayout = QHBoxLayout()


        self.label1 = QLabel('<b>패턴 오는 시간<b>')
        self.label1.setAlignment(Qt.AlignCenter)

        self.label1.setFont(QtGui.QFont("맑은 고딕", 15))

        self.lcd1 = QLCDNumber()
        self.lcd1.display('')
        self.lcd1.setDigitCount(5)
        self.lcd2 = QLCDNumber()
        self.lcd2.display('')
        self.lcd2.setStyleSheet("background-color: transparent")

        self.btnStart = QPushButton("시작")
        self.btnStart.clicked.connect(self.maplewindowsstatecheck)
        self.btnColor = QPushButton("색 알림")
        self.btnColor.clicked.connect(self.coloralram)
        self.btnReset = QPushButton("도움말")
        self.btnReset.clicked.connect(self.dialog_open)

        self.dialog = QDialog()
        self.dialog2 = QDialog()
        self.accept = QDialog()

        layout = QGridLayout()

        self.lcd.setMaximumWidth(10000)
        self.lcd1.setMaximumWidth(10000)
        self.lcd2.setMaximumWidth(10000)
        self.label1.setMaximumHeight(30)
        layout.addWidget(self.lcd,0,0,1,0)
        layout.addWidget(self.lcd1,2,0,1,0)
        layout.addWidget(self.lcd2,3,0,1,0)
        layout.addWidget(self.label1,1,0,1,0)
        subLayout.addWidget(self.btnStart)
        subLayout.addWidget(self.btnColor)
        subLayout.addWidget(self.btnReset)

        layout.addLayout(subLayout,4,0)

        self.setLayout(layout)

        self.update_gui()
        self.lcd2.setDigitCount(0)
        self.accept_open()

    def accept_open(self):
        btnDialog3 = QPushButton("동의", self.accept)
        btnDialog3.move(160, 50)
        btnDialog3.clicked.connect(self.accept_close)
        btnDialog4 = QPushButton("동의안함", self.accept)
        btnDialog4.move(245, 50)
        btnDialog4.clicked.connect(self.accept_no)

        self.accept.setWindowTitle(' ')
        self.label4 = QLabel('이 프로그램을 사용하였을 때 발생하는 문제에 대한 모든 책임은 사용자에게 있습니다.', self.accept)
        self.label4.setAlignment(Qt.AlignCenter)
        self.label4.move(10, 10)
        layout4 = QVBoxLayout()
        layout4.addWidget(self.label4)

        self.accept.setWindowModality(Qt.ApplicationModal)
        self.accept.resize(480, 90)
        self.accept.show()

    def accept_close(self):
        self.accept.close()

    def accept_no(self):
        self.accept.close()
        self.btnStart.setEnabled(False)
        self.btnReset.setEnabled(False)
        self.btnColor.setEnabled(False)

    def dialog_open(self):
        btnDialog = QPushButton("확인", self.dialog)
        btnDialog.move(165, 200)
        btnDialog.clicked.connect(self.dialog_close)

        self.dialog.setWindowTitle('도움말')
        self.label2 = QLabel('진 힐라 입장 전에 시작 버튼 누르시면 됩니다.\n\n색 알림\n60초 전 : 초록 \n40초 전 : 주황\n20초 전 : 빨강\n\n창 크기 조절 가능\n\nopencv 이용해서 이미지로 판단하는거라 가끔씩 정확하지 않을 수 있음\n\n타이머도 틀릴 수 있으니 너무 맹신하지 마시길', self.dialog)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.move(10, 10)
        self.label3 = QLabel('ㅁ\n크로아 무형\n젬 한개만 줍쇼', self.dialog)
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.move(162, 226)
        layout2 = QVBoxLayout()
        layout2.addWidget(self.label2)
        layout2.addWidget(self.label3)

        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(405, 230)
        self.dialog.show()

    def dialog_close(self):
        self.dialog.close()

    def initUI(self):
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon(resource_path('img/hilla.png')))
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def coloralram(self):
        self.Cal += 1
        self.btnColor.setEnabled(False)

    def help(self):
        self.btnStart.setEnabled(False)
        self.btnReset.setEnabled(False)
        self.btnColor.setEnabled(False)

    def maplewindowsstatecheck(self):
        hwnd = win32gui.FindWindow(None, "MapleStory")
        rect = win32gui.GetWindowRect(hwnd)
        ex = rect[0]
        if ex == (-32000):
            self.dialog2_open()
        else:
            print("힐라 입장 대기")
            self.btnColor.setEnabled(False)
            self.btnStart.setEnabled(False)
            self.introscreen.start()

    def dialog2_open(self):
        btnDialog2 = QPushButton("확인", self.dialog2)
        btnDialog2.move(20, 30)
        btnDialog2.clicked.connect(self.dialog2_close)

        self.dialog2.setWindowTitle(' ')
        self.label3 = QLabel('메이플 최소화 상태', self.dialog2)
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.move(10, 10)
        layout3 = QVBoxLayout()
        layout3.addWidget(self.label3)

        self.dialog2.setWindowModality(Qt.ApplicationModal)
        self.dialog2.resize(120, 60)
        self.dialog2.show()

    def dialog2_close(self):
        self.dialog2.close()

    def introscreenthreadStop(self):
        self.startTimer()

    def startTimer(self):
        print("카운트 시작")
        self.time_left_int = DURATION_INT
        self.myTimer.start(1000)
        self.hillaicon.start()
        self.lcd1.display(secs_to_minsec(self.time_left_int-164))

    def timerTimeout(self):
        self.time_left_int -= 1
        if self.time_left_int == 0:
            self.time_left_int = DURATION_INT
        self.update_gui()

    def update_gui(self):
        minsec = secs_to_minsec(self.time_left_int)
        self.lcd.display(minsec)
        self.lcd2.setDigitCount(3)

        if self.Cal == 0:
            if self.time_left_int - self.minsec1 <= 0:
                self.lcd2.setDigitCount(0)
            else:
                self.lcd2.display(self.time_left_int - self.minsec1)


        if self.Cal == 1:
            self.lcd2.display(self.time_left_int - self.minsec1)
            if self.time_left_int - self.minsec1 > 60:
                self.lcd2.setStyleSheet("color :black;"
                                       "background-color: transparent") #투명
            else:
                if 40 < self.time_left_int - self.minsec1 <= 60:
                    self.lcd2.setStyleSheet("color :white;"
                                           "background-color: #009900") #초록
                else:
                    if 20 < self.time_left_int - self.minsec1 <= 40:
                        self.lcd2.setStyleSheet("color :white;"
                                               "background-color: #cc6633") #주황
                    else:
                        if 0 < self.time_left_int - self.minsec1 <= 20:
                            self.lcd2.setStyleSheet("color :white;"
                                                   "background-color: #cc3333") #빨강
                        else:
                            if self.time_left_int - self.minsec1 <= 0:
                                self.lcd2.setDigitCount(0)



    def hillaiconstop(self):
        self.sickle.start()

    def sicklethreadStop(self):
        self.sickle2.start()

    def sicklethreadStop2(self):
        print(self.interv)
        if self.interv > 30:
            self.sickle3.start()
        else:
            self.sickle.start()

    def sicklethreadStop3(self):
        if self.interv > 30:
            for i in range(1):
                pic = pg.screenshot(region=(icon1 - 111, icon2 - 38, 1, 8))
                img_frame = np.array(pic)
                img_frame = cv.cvtColor(img_frame, cv.COLOR_BGR2RGB)

                image = img_frame.reshape((img_frame.shape[0] * img_frame.shape[1], 3))

                k = 1
                clt = KMeans(n_clusters=k)
                clt.fit(image)

                self.kk = 1

                for center in clt.cluster_centers_:
                    break

                if center[2] < 57 or 70 < center[2] < 90:
                    minsec = secs_to_minsec(self.time_left_int - 100)
                    self.minsec1 = self.time_left_int - 100
                    self.lcd1.display(minsec)
                    self.label1.setText('<b>3페이즈 패턴<b>')

                else:
                    pic = pg.screenshot(region=(icon1 + 41, icon2 - 38, 1, 8))
                    img_frame = np.array(pic)
                    img_frame = cv.cvtColor(img_frame, cv.COLOR_BGR2RGB)

                    image = img_frame.reshape((img_frame.shape[0] * img_frame.shape[1], 3))

                    k = 1
                    clt = KMeans(n_clusters=k)
                    clt.fit(image)

                    for center in clt.cluster_centers_:
                        break

                    if 150 < center[2] < 170 or 70 < center[2] < 90:
                        minsec = secs_to_minsec(self.time_left_int - 125)
                        self.minsec1 = self.time_left_int - 125
                        self.lcd1.display(minsec)
                        self.label1.setText('<b>2페이즈 패턴<b>')
                    else:
                        minsec = secs_to_minsec(self.time_left_int - 150)
                        self.minsec1 = self.time_left_int - 150
                        self.lcd1.display(minsec)
                        self.label1.setText('<b>1페이즈 패턴<b>')
            self.sickle.start()
        else:
            self.sickle.start()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())