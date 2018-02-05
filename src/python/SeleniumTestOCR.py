import os
import time
import pyautogui

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
    startBrowser()
    setStartAddress(ADDRESS_START)
    for i in range(0, len(ADDRESS_END)):
        addressInfos = ADDRESS_END[i].split('\t')

        permission = addressInfos[2].strip()
        if permission == '제외':
            continue
        distance = searchAndGetDistance(addressInfos)

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


def openExcel():
    pyautogui.hotkey('win', 'r')
    ClipBoard.setClipboard("C:\Temp\거리측정 주소목록.xlsx")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

    time.sleep(1)
    pyautogui.press('enter')


def getStartAddress():
    pyautogui.press('f5')
    pyautogui.typewrite(POINT_START)
    pyautogui.press('enter')

    pyautogui.hotkey('shift', 'right')
    pyautogui.hotkey('ctrl', 'c')
    ADDRESS_START = ClipBoard.getClipboardData()
    # print(ADDRESS_START)
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


def startBrowser():
    # browser = webdriver.Chrome('.\\util\\driver\\chromedriver')
    # browser.get("http://map.daum.net/")

    pyautogui.hotkey('win', 'r')

    pyautogui.hotkey('win', 'up')
    return browser


def setStartAddress(address):
    getElement('//*[@id="search.tab2"]/a').click()
    getElement('//*[@id="info.route.waypointSuggest.input0"]').click()
    getElement(
        '//*[@id="info.route.waypointSuggest.input0"]').send_keys(address)

    pyautogui.press('enter')


def setEndAddress(address):
    time.sleep(1)
    try:
        getElement('//*[@id="info.route.waypointSuggest.input1"]').click()
    except:
        getElement('//*[@id="info.route.searchBox"]/div[2]/span[1]/a').click()

    getElement(
        '//*[@id="info.route.waypointSuggest.input1"]').send_keys(address)
    pyautogui.press('enter')


def searchAndGetDistance(addressInfos):
    addressText = addressInfos[0].strip() + ' ' + addressInfos[1].strip()
    print(addressText)
    setEndAddress(addressText)
    time.sleep(1)
    getElement('//*[@id="walktab"]').click()

    clickNow('distanceBtn.png')
    
    clickNow('start.png')
    
    clickNow('end.png')
    
    pyautogui.press('esc')
    
    distance = getElement(
        '//*[@id="view.map"]/div[3]/div/div[6]/div[3]/div/ul/li[2]/strong').text

    unit = getUnit()
    if unit == 'km':
        distance = float(distance) * 1000

    clickNow('exit.png')
    print(distance)
    return distance


def getUnit():
    unit = getElement(
        '//*[@id="view.map"]/div[3]/div/div[6]/div[3]/div/ul/li[2]/span[2]').text
    return unit


def getElement(xpath):
    return browser.find_element_by_xpath(xpath)


def closeExcel():
    os.system('TASKKILL /F /IM excel.exe')


test()
