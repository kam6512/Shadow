import uuid
import pyautogui
import matcher

screenShot = '.\\samples\\'
screenShot +=(uuid.uuid4().hex)
screenShot +='.png'
pyautogui.screenshot(screenShot)


(pointX, pointY) = matcher.calcCenterPoint(
   screenShot,   """.\samples\\test2.png""")

print(pointX)
print(pointY)
pyautogui.moveTo(pointX, pointY)
pyautogui.click()
