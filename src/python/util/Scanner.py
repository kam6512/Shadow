import os
from enum import Enum
import cv2 as cv
import numpy as np
# from matplotlib import pyplot as plt
import pyautogui

# from . import AssetPath
import AssetPath


def original():
    
    lineColor = (0, 0, 255)
    thickness = 2
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
    cv.imwrite('.\\samples\\Temp\\res.png', img_rgb)


def originalWithScreenShot():
    pyautogui.screenshot('..\\samples\\Temp\\main.png')
    img_rgb = cv.imread('..\\samples\\Temp\\main.png')
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('..\\samples\\Handle\\trans_test_new.png', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.96
    loc = np.where(res >= threshold)

    startList = []
    endList = []
    for pt in zip(*loc[::-1]):
        startList.append(pt)
        endList.append((pt[0] + w, pt[1] + h))

    points = mergePorintValue(startList, endList)

    lineColor = (0, 0, 255)
    thickness = 2
    for point in points:
        print(point)
        cv.rectangle(img_rgb, point[0], point[1], lineColor, thickness)

    cv.imwrite('..\\samples\\Temp\\res.png', img_rgb)


def mergePorintValue(startList, endList):
    startList = mergeSimilarValue(startList)
    endList = mergeSimilarValue(endList)
    length = 0
    if len(startList) == len(endList):
        length = len(startList)

    points = []
    for idx in range(length):
        point = [(startList[idx]), (endList[idx])]
        points.append(point)
    return points

def mergeSimilarValue(valueList):
    for idx, value in enumerate(valueList):
        length = len(valueList)
        if idx+1 == length:
            break
        currentVal = value[0]+value[1]
        for nextIdx in range(idx+1, length):
            nextValue = valueList[nextIdx]
            nextVal = nextValue[0]+nextValue[1]
            if abs(currentVal-nextVal) < 10:
                valueList[nextIdx] = (int((value[0]+nextValue[0])/2),
                                    int((value[1]+nextValue[1])/2))
                valueList[idx] = 0

    return list(filter(lambda x: x != 0, valueList))

originalWithScreenShot()


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
