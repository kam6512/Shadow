import time
import re
import cv2 as cv
import pyautogui
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from util import ClipBoard


class ExcelIO:
    startPoint = 'A2'
    addressPoint = 'A6'
    POINT_DISTANCE = ['D', '6']

    def __init__(self, path):
        self.clip = ClipBoard.Clip()
        self.openExcelFile(path)

    def openExcelFile(self, path="C:\Temp\거리측정 주소목록.xlsx"):
        pyautogui.hotkey('win', 'r')
        self.clip.setClipboard(path)

        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        time.sleep(3)
        pyautogui.press('enter')

    def getStartAddress(self):
        pyautogui.press('f5')
        pyautogui.typewrite(self.startPoint)
        pyautogui.press('enter')

        pyautogui.press('f8')
        pyautogui.press('right')
        pyautogui.press('enter')
        time.sleep(0.5)
        # pyautogui.hotkey('shift', 'right')
        pyautogui.hotkey('ctrl', 'c')
        ADDRESS_START = self.clip.getClipboardData()
        return ADDRESS_START

    def getEndAddresses(self):
        pyautogui.press('f5')
        pyautogui.typewrite(self.addressPoint)
        pyautogui.press('enter')

        pyautogui.hotkey('ctrl', 'down')
        pyautogui.hotkey('ctrl', 'down')
        pyautogui.hotkey('ctrl', 'up')

        pyautogui.press('right')
        pyautogui.press('right')
        pyautogui.press('f8')

        pyautogui.press('f5')
        pyautogui.typewrite(self.addressPoint)
        pyautogui.press('enter')

        pyautogui.hotkey('ctrl', 'c')
        ADDRESS_END = self.clip.getClipboardData()
        ADDRESS_END = ADDRESS_END.split('\n')
        ADDRESS_END.pop()
        return ADDRESS_END

    def setDistance(self, countIndex, distance):
        pyautogui.press('f5')
        distancePoint = int(self.POINT_DISTANCE[1]) + countIndex
        distancePoint = self.POINT_DISTANCE[0] + str(distancePoint)
        pyautogui.typewrite(distancePoint)
        pyautogui.press('enter')
        pyautogui.press('del')
        pyautogui.typewrite(str(distance))
        pyautogui.press('enter')


class Xpath:

    def __init__(self, link):
        browser = self.startSelenium(link)
        self.wait = WebDriverWait(browser, 1.0)

    def startSelenium(self, link="http://map.daum.net/"):
        browser = webdriver.Chrome('.\\util\\driver\\chromedriver')
        browser.get(link)

        pyautogui.hotkey('win', 'up')
        return browser

    def changeModeToWalk(self):
        self.getElement('//*[@id="search.tab2"]/a').click()

    def setStartAddress(self, address):
        self.getElement('//*[@id="info.route.waypointSuggest.input0"]').click()
        self.getElement(
            '//*[@id="info.route.waypointSuggest.input0"]').send_keys(address)

        pyautogui.press('enter')

    def setEndAddress(self, address):
        try:
            self.getElement(
                '//*[@id="info.route.waypointSuggest.input1"]').click()
        except:
            self.getElement(
                '//*[@id="info.route.searchBox"]/div[2]/span[1]/a').click()

        self.getElement(
            '//*[@id="info.route.waypointSuggest.input1"]').send_keys(address)
        pyautogui.press('enter')

    def searchAndGetDistance(self, addressInfos):
        addressText = addressInfos[0].strip() + ' ' + addressInfos[1].strip()
        self.setEndAddress(addressText)
        self.getElement('//*[@id="walktab"]').click()

        self.enableDistanceTool()
        distance = self.getDistance()
        self.disableDistanceTool()

        return distance

    def enableDistanceTool(self):
        # clickNow('distanceBtn.png')
        self.getElement('//*[@id="view.map"]/div[9]/div[3]/a[1]').click()

        while (True):
            try:
                # clickNow('start.png')
                self.getElement(
                    '//*[@id="view.map"]/div[3]/div/div[6]/div[1]/img').click()

                # clickNow('end.png')
                self.getElement(
                    '//*[@id="view.map"]/div[3]/div/div[6]/div[2]/img').click()
                break
            except:
                self.getElement(
                    '//*[@id="view.map"]/div[9]/div[2]/div[1]/div[3]').click()

        pyautogui.press('esc')

    def disableDistanceTool(self):
        # clickNow('exit.png')
        self.getElement(
            '//*[@id="view.map"]/div[3]/div/div[6]/div[6]/a').click()

    def getDistance(self):
        distance = self.getElement(
            '//*[@id="view.map"]/div[3]/div/div[6]/div[3]/div/ul/li[2]/strong').text
        unit = self.getElement(
            '//*[@id="view.map"]/div[3]/div/div[6]/div[3]/div/ul/li[2]/span[2]').text
        if unit == 'km':
            distance = float(distance) * 1000
        return distance

    def getElement(self, xpath):
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        return element


class OCR:

    def __init__(self, link):
        pytesseract.pytesseract.tesseract_cmd = 'C:\\DEV_MODULE\\Tesseract-OCR\\tesseract.exe'
        self.ocrPath = '.\\samples\\Temp\\ocr.png'
        self.clip = ClipBoard.Clip()
        self.startBrowser(link)

    def startBrowser(self, link="http://map.daum.net/"):
        pyautogui.hotkey('win', 'r')
        self.clip.setClipboard(link)
        pyautogui.typewrite('chrome.exe ')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.hotkey('win', 'up')

    def changeModeToWalk(self):
        pass

    def setStartAddress(self, address):
        self.clip.setClipboard(address)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

    def setEndAddress(self, address):
        self.clip.setClipboard(address)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

    def searchAndGetDistance(self, addressInfos):
        pass

    def enableDistanceTool(self):
        pass

    def disableDistanceTool(self):
        pass

    def getDistance(self, pos):
        pyautogui.screenshot(self.ocrPath, region=(pos[0] + 20, pos[1] - 10, 50, 20))
        image = cv.imread(self.ocrPath, cv.IMREAD_GRAYSCALE)
        image = cv.pyrUp(image)
        distance = pytesseract.image_to_string(image, lang='eng')

        distance = distance.replace(' ', '')
        units = re.compile('(\.|\d)')
        unit = units.sub('', distance)
        print(unit)
        distance = distance.replace(unit, '')
        print(distance)

        if unit == 'km':
            distance = float(distance) * 1000
        return distance

