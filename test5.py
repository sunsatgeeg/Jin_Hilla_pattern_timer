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