
import pyautogui
import time

from util import Scanner
from util import ImagePath
from util import Language

def clickNow(matchImage):
    path = ImagePath.createPath(matchImage)
    handle = path[0]
    screenShot = path[1]
    pyautogui.screenshot(screenShot)
    point = matcher.calcCenterPoint(screenShot,  handle)

    if len(point) == 0: return
    pyautogui.moveTo(point[0], point[1])
    pyautogui.click()

def test():
    runNotepad()
    clickNow('chrome.png')
    pyautogui.hotkey('ctrl', 't')
    convertToEng()
    pyautogui.typewrite('https://www.youtube.com/watch?v=ejkHVAgzQ7U')
    pyautogui.press('enter')
    for x in range(10):
        shareAndNext()


def runNotepad():
    pyautogui.hotkey('win', 'r')
    convertToEng()
    pyautogui.typewrite('notepad')
    pyautogui.press('enter')

def shareAndNext():
    time.sleep(2)
    clickNow('share.png')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    pyautogui.press('esc')
    clickNow('notepad.png')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    clickNow('chrome.png')
    pyautogui.hotkey('shift', 'n')

def convertToEng():
    lang = Language.currentLang()
    if lang == 'kor': 
        pyautogui.press('hangul')

    
test()
