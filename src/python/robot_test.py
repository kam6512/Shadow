import uuid
import pyautogui
import matcher


def clickNow(matchImage):
    screenShot = '.\\samples\\'
    screenShot += (uuid.uuid4().hex)
    screenShot += '.png'
    pyautogui.screenshot(screenShot)

    (pointX, pointY) = matcher.calcCenterPoint(
        screenShot,  matchImage)

    print(pointX)
    print(pointY)
    pyautogui.moveTo(pointX, pointY)
    pyautogui.click()


clickNow(""".\samples\\test2.png""")
