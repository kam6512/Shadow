import os
from enum import Enum
import cv2 as cv
import numpy as np
# from matplotlib import pyplot as plt
import pyautogui

from . import AssetPath


def original(self):
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
        cv.rectangle(img_rgb, start, end, self.lineColor, self.thickness)
        break
    cv.imwrite('.\\samples\\res.png', img_rgb)


def originalWithScreenShot(self):
    pyautogui.screenshot('.\\samples\\main.png')
    img_rgb = cv.imread('.\\samples\\main.png')
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('.\samples\Handle\distance_label.png', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.95
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        start = pt
        end = (pt[0] + w, pt[1] + h)
        cv.rectangle(img_rgb, start, end, self.lineColor, self.thickness)
        break
    cv.imwrite('.\\samples\\res.png', img_rgb)
    print(start)
    print(end)


class Direction(Enum):
    NW = 0
    N = 1
    NE = 2
    W = 3
    CENTER = 4
    E = 5
    SW = 6
    S = 7
    SE = 8


class MatchTemplate:
    lineColor = (0, 0, 255)
    thickness = 1

    def __init__(self):
        self.asset = AssetPath.ImageAsset()

    def calcMatchingPoint(self, handle):
        path = self.asset.createPath(handle)
        handlePath = path[0]
        parentScreenShot = path[1]
        pyautogui.screenshot(parentScreenShot)

        img_rgb = cv.imread(parentScreenShot)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        template = cv.imread(handlePath, 0)
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.95
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            start = pt
            end = (pt[0] + w, pt[1] + h)
            # cv.rectangle(img_rgb, start, end, self.lineColor, self.thickness)
            break
        os.remove(parentScreenShot)
        # return (start, end, img_rgb)
        return start, end

    def clacPointWithDirection(self, handle, direction=Direction.CENTER):
        try:
            # (start, end, img_rgb) = self.calcMatchingPoint(handle)
            (start, end) = self.calcMatchingPoint(handle)
            return self.getPoint(direction, start, end)
        except:
            return []

    def clickNow(self, handle, direction=Direction.CENTER, appendPoint=[0, 0]):
        point = self.clacPointWithDirection(handle, direction)
        if len(point) == 0:
            raise RuntimeError
        pyautogui.moveTo(point[0] + appendPoint[0], point[1] + appendPoint[1])
        pyautogui.click()
        return True

    def dragTest(self, handle):
        point = self.clacPointWithDirection(handle, Direction.E)
        if len(point) == 0:
            return
        pyautogui.moveTo(point[0], point[1])
        pyautogui.dragRel(50, 0, 0.5)

    def getPoint(self, direction, start, end):
        return {
            Direction.NW: [start[0], start[1]],
            Direction.N: [((start[0] + end[0]) / 2), start[1]],
            Direction.NE: [end[0], start[1]],
            Direction.W: [start[0], ((start[1] + end[1]) / 2)],
            Direction.CENTER: [((start[0] + end[0]) / 2), ((start[1] + end[1]) / 2)],
            Direction.E: [end[0], ((start[1] + end[1]) / 2)],
            Direction.SW: [start[0], end[1]],
            Direction.S: [((start[0] + end[0]) / 2), end[1]],
            Direction.SE: [end[0], end[1]]
        }[direction]
