import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pyautogui

lineColor = (0, 0, 255)
thickness = 1


def calcMatchingPoint(parent, child):
    print(parent)
    print(child)
    img_rgb = cv.imread(parent)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread(child, 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.95
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        start = pt
        end = (pt[0] + w, pt[1] + h)
        cv.rectangle(img_rgb, start, end, lineColor, thickness)
        break
    return (start, end, img_rgb)


def calcCenterPoint(parent, child, result=None):
    (start, end, img_rgb) = calcMatchingPoint(parent, child)
    pointX = ((start[0]+end[0])/2)
    pointY = ((start[1]+end[1])/2)
    if result is not None:
        cv.imwrite(result, img_rgb)
    return [pointX, pointY]

def original():
    img_rgb = cv.imread('.\\samples\\main.png')
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('.\samples\Handle\chrome.png', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.95
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        start = pt
        end = (pt[0] + w, pt[1] + h)
        cv.rectangle(img_rgb, start, end, lineColor, thickness)
        break
    cv.imwrite('.\\samples\\res.png', img_rgb)

def originalWithScreenShot():
    pyautogui.screenshot('.\\samples\\main.png')
    img_rgb = cv.imread('.\\samples\\main.png')
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('.\samples\Handle\caption.png', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.95
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        start = pt
        end = (pt[0] + w, pt[1] + h)
        cv.rectangle(img_rgb, start, end, lineColor, thickness)
        break
    cv.imwrite('.\\samples\\res.png', img_rgb)

originalWithScreenShot()