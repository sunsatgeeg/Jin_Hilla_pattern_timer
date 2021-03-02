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
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

cv.namedWindow("result");
cv.moveWindow("result", 0, 500);

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
    print(max_val, top_left)

    cv.imshow('result', img_frame)

    key = cv.waitKey(1)
    if max_val > 7000000:
        icon1 = ew + top_left[0]
        icon2 = eh + top_left[1]
        break

print("AAAAA", icon1, icon2)


for i in range(1):
    pic = pg.screenshot(region=(icon1+187, icon2, 1, 8))
    img_frame = np.array(pic)
    img_frame = cv.cvtColor(img_frame, cv.COLOR_BGR2RGB)

    image = img_frame.reshape((img_frame.shape[0] * img_frame.shape[1], 3))  # height, width 통합

    k = 1  # 예제는 5개로 나누겠습니다
    clt = KMeans(n_clusters=k)
    clt.fit(image)

    for center in clt.cluster_centers_:
        break

    if center[2] < 57 or 70 < center[2] < 90:
        print("3페이즈 패턴")
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
            print("2페이즈 패턴")
        else:
            print("1페이즈 패턴")




#    cv.imshow('result', img_frame)

#    key = cv.waitKey(1)
#    if key == 27:
#        break