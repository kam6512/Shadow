import pyautogui
import math
def test():
    doublePI = 3.14 * 2.0
    (w, h) = pyautogui.size()
    h = h / 2

    for x in range(0, w):
        y = h * math.sin((doublePI * x)/w) + h
        pyautogui.moveTo(x, y, pyautogui.MINIMUM_DURATION)
