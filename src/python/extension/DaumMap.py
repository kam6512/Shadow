
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Extension:
    wait = None

    def __init__(self, link):
        browser = self.startSelenium(link)
        self.wait = WebDriverWait(browser, 0.5)

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
        print(addressText)
        self.setEndAddress(addressText)
        self.getElement('//*[@id="walktab"]').click()

        self.enableDistanceTool()
        distance = self.getDistance()
        self.disableDistanceTool()

        return distance

    def enableDistanceTool(self):
        # clickNow('distanceBtn.png')
        self.getElement('//*[@id="view.map"]/div[9]/div[3]/a[1]').click()

        visible = False
        while(visible == False):
            try:
                # clickNow('start.png')
                self.getElement(
                    '//*[@id="view.map"]/div[3]/div/div[6]/div[1]/img').click()

                # clickNow('end.png')
                self.getElement(
                    '//*[@id="view.map"]/div[3]/div/div[6]/div[2]/img').click()
                visible = True
            except:
                self.getElement(
                    '//*[@id="view.map"]/div[9]/div[2]/div[1]/div[3]').click()
                visible = False

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
