
import pyautogui
import time

import matcher
from util import ImagePath
from util import Language

def clickNow(matchImage):
    path = ImagePath.createPath(matchImage)
    handle = path[0]
    screenShot = path[1]
    pyautogui.screenshot(screenShot)
    point = matcher.calcCenterPoint(screenShot,  handle)

    pyautogui.moveTo(point[0], point[1])
    pyautogui.click()

def test():
    clickNow("""chrome.png""")
    pyautogui.hotkey('ctrl', 't')
    
    lang = Language.currentLang()
    if lang == 'kor': 
        pyautogui.press('hangul')

    pyautogui.typewrite('https://www.youtube.com/watch?v=ejkHVAgzQ7U')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.press('space')
    pyautogui.press('c')
    clickNow('captionOn.png')
    # pyautogui.press('space')
test()