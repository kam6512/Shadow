import os
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pyautogui
from . import AssetPath


class MatchTemplate:
    lineColor = (0, 0, 255)
    thickness = 1

    def __init__(self):
        self.asset = AssetPath.ImageAsset()

    def calcMatchingPoint(self, parent, child):
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
            cv.rectangle(img_rgb, start, end, self.lineColor, self.thickness)
            break
        return (start, end, img_rgb)

    def calcCenterPoint(self, parent, child, result=None):
        try:
            (start, end, img_rgb) = self.calcMatchingPoint(parent, child)
            pointX = ((start[0]+end[0])/2)
            pointY = ((start[1]+end[1])/2)
            if result is not None:
                cv.imwrite(result, img_rgb)
            return [pointX, pointY]
        except:
            return []

    def clickNow(self, templateImage):
        path = self.asset.createPath(templateImage)
        handle = path[0]
        screenShot = path[1]
        pyautogui.screenshot(screenShot)
        point = self.calcCenterPoint(screenShot,  handle)
        os.remove(screenShot)
        if len(point) == 0:
            return
        pyautogui.moveTo(point[0], point[1])
        pyautogui.click()

    def calcEndPointTest(self, parent, child, result=None):
        try:
            (start, end, img_rgb) = self.calcMatchingPoint(parent, child)
            pointX = end[0]
            pointY = ((start[1]+end[1])/2)
            if result is not None:
                cv.imwrite(result, img_rgb)
            return [pointX, pointY]
        except:
            return []

    def dragTest(self, templateImage):
        path = self.asset.createPath(templateImage)
        handle = path[0]
        screenShot = path[1]
        pyautogui.screenshot(screenShot)
        point = self.calcEndPointTest(screenShot,  handle)
        os.remove(screenShot)
        if len(point) == 0:
            return
        pyautogui.moveTo(point[0], point[1])
        pyautogui.dragRel(50, 0, 0.5)
        # pyautogui.click()

    def clickRightTest(self, templateImage):
        path = self.asset.createPath(templateImage)
        handle = path[0]
        screenShot = path[1]
        pyautogui.screenshot(screenShot)
        point = self.calcCenterPoint(screenShot,  handle)
        os.remove(screenShot)
        if len(point) == 0:
            return
        pyautogui.moveTo(point[0]+50, point[1])
        pyautogui.click()
        pyautogui.click()

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


# lineColor = (0, 0, 255)
# thickness = 1
# def originalWithScreenShot():
#         pyautogui.screenshot('..\\samples\\main.png')
#         img_rgb = cv.imread('..\\samples\\main.png')
#         img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
#         template = cv.imread('..\samples\Handle\distance_label.png', 0)
#         w, h = template.shape[::-1]
#         res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
#         threshold = 0.95
#         loc = np.where(res >= threshold)
#         for pt in zip(*loc[::-1]):
#             start = pt
#             end = (pt[0] + w, pt[1] + h)
#             cv.rectangle(img_rgb, start, end, lineColor, thickness)
#             break
#         cv.imwrite('..\\samples\\res.png', img_rgb)
#         print(start)
#         print(end)

# originalWithScreenShot()
