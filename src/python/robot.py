import pyautogui
import matcher


(pointX, pointY) = matcher.calcCenterPoint(
    """.\samples\\temp.png""",   """.\samples\\test1.png""")

print(pointX)
print(pointY)
pyautogui.moveTo(pointX, pointY)
