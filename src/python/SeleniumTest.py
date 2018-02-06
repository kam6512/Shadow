import os
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from extension import DaumMap

from util import Scanner
from util import ImagePath
from util import Language
from util import ClipBoard

POINT_START = 'A2'
POINT_ADDRESS = 'A6'
POINT_DISTANCE = ['D', '6']

def clickNow(matchImage):
    path = ImagePath.createPath(matchImage)
    handle = path[0]
    screenShot = path[1]
    pyautogui.screenshot(screenShot)
    point = Scanner.calcCenterPoint(screenShot,  handle)

    if len(point) == 0:
        return
    pyautogui.moveTo(point[0], point[1])
    pyautogui.click()


def test():
    openExcel()
    ADDRESS_START = getStartAddress()
    ADDRESS_END = getEndAddresses()

    daumMap = DaumMap.Extension("http://map.daum.net/")
    daumMap.changeModeToWalk()
    daumMap.setStartAddress(ADDRESS_START)
    for i in range(0, len(ADDRESS_END)):
        addressInfos = ADDRESS_END[i].split('\t')

        permission = addressInfos[2].strip()
        if permission == '제외':
            continue
        distance = daumMap.searchAndGetDistance(addressInfos)

        clickNow('excel.png')
        pyautogui.press('f5')
        distancePoint = int(POINT_DISTANCE[1]) + i
        distancePoint = POINT_DISTANCE[0] + str(distancePoint)
        pyautogui.typewrite(distancePoint)
        print(distancePoint)
        pyautogui.press('enter')
        pyautogui.press('del')
        pyautogui.typewrite(str(distance))
        pyautogui.press('enter')
        clickNow('chrome.png')

    close()


def openExcel():
    pyautogui.hotkey('win', 'r')
    ClipBoard.setClipboard("C:\Temp\거리측정 주소목록.xlsx")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

    time.sleep(3)
    pyautogui.press('enter')


def getStartAddress():
    pyautogui.press('f5')
    pyautogui.typewrite(POINT_START)
    pyautogui.press('enter')

    pyautogui.press('f8')
    pyautogui.press('right')
    pyautogui.press('enter')
    # pyautogui.hotkey('shift', 'right')
    pyautogui.hotkey('ctrl', 'c')
    ADDRESS_START = ClipBoard.getClipboardData()
    return ADDRESS_START


def getEndAddresses():
    pyautogui.press('f5')
    pyautogui.typewrite(POINT_ADDRESS)
    pyautogui.press('enter')

    pyautogui.hotkey('ctrl', 'down')
    pyautogui.hotkey('ctrl', 'down')
    pyautogui.hotkey('ctrl', 'up')

    pyautogui.press('right')
    pyautogui.press('right')
    pyautogui.press('f8')

    pyautogui.press('f5')
    pyautogui.typewrite(POINT_ADDRESS)
    pyautogui.press('enter')

    pyautogui.hotkey('ctrl', 'c')
    ADDRESS_END = ClipBoard.getClipboardData()
    ADDRESS_END = ADDRESS_END.split('\n')
    ADDRESS_END.pop()
    return ADDRESS_END


def close():
    os.system('TASKKILL /F /IM chrome.exe')


test()
