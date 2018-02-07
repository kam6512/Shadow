import os
import time
import pyautogui
import DaumMap
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

from util import Scanner
from util import ClipBoard
from util.Scanner import Direction


class Test:
    def __init__(self):
        self.clip = ClipBoard.Clip()
        self.scanner = Scanner.MatchTemplate()
        pytesseract.pytesseract.tesseract_cmd = 'C:\\DEV_MODULE\\Tesseract-OCR\\tesseract.exe'

    def ocr(self):
        excel = DaumMap.ExcelIO("C:\Temp\거리측정 주소목록.xlsx")
        startAddress = excel.getStartAddress()
        endAddress = excel.getEndAddresses()

        daumMap = DaumMap.OCR("http://map.daum.net/")
        time.sleep(1)
        self.clickNow('walkmode.png')
        daumMap.setStartAddress(startAddress)

        for i in range(0, len(endAddress)):
            addressInfos = endAddress[i].split('\t')
            permission = addressInfos[2].strip()
            if permission == '제외': continue
            time.sleep(1)
            self.scanner.clickNow('end_input.png', Direction.E, [50, 0])
            addressText = addressInfos[0].strip() + ' ' + addressInfos[1].strip()
            daumMap.setEndAddress(addressText)
            self.clickNow('walk_search.png')
            self.clickNow('distanceBtn.png')

            while True:
                try:
                    time.sleep(2)
                    self.clickNow('start.png')
                    self.clickNow('end.png')
                    break
                except:
                    self.scanner.clickNow('depth_out.png', Direction.S)

            pyautogui.press('esc')

            pos = self.scanner.clacPointWithDirection('distance_label.png')

            # image = pyautogui.screenshot('.\\samples\\res.png', region=(pos[0]+20, pos[1]-10, 30, 20))
            image = pyautogui.screenshot('.\\samples\\res.png', region=(pos[0] + 20, pos[1] - 10, 30, 20))
            text = pytesseract.image_to_string(image, lang='eng')
            print(text)


            # pyautogui.hotkey('ctrl', 'c')
            # distance = self.clip.getClipboardData()

            # self.clickNow('exit.png')

            # self.clickNow('excel.png')
            # excel.setDistance(i, distance)
            # self.clickNow('chrome.png')
            break

        # self.close()

    def drag(self):
        excel = DaumMap.ExcelIO("C:\Temp\거리측정 주소목록.xlsx")
        startAddress = excel.getStartAddress()
        endAddress = excel.getEndAddresses()

        daumMap = DaumMap.OCR("http://map.daum.net/")
        time.sleep(1)
        self.clickNow('walkmode.png')
        # self.scanner.clickWithDirection('walkmode.png', Direction.CENTER)
        daumMap.setStartAddress(startAddress)

        for i in range(0, len(endAddress)):
            addressInfos = endAddress[i].split('\t')
            permission = addressInfos[2].strip()
            if permission == '제외': continue
            time.sleep(1)
            self.scanner.clickNow('end_input.png', Direction.E, [50, 0])
            addressText = addressInfos[0].strip() + ' ' + addressInfos[1].strip()
            daumMap.setEndAddress(addressText)
            self.clickNow('walk_search.png')
            self.clickNow('distanceBtn.png')

            while True:
                try:
                    time.sleep(1)
                    self.clickNow('start.png')
                    self.clickNow('end.png')
                    break
                except:
                    self.clickNow('depth_out.png')

            pyautogui.press('esc')
            self.scanner.dragTest('distance_label.png')

            pyautogui.hotkey('ctrl', 'c')
            distance = self.clip.getClipboardData()

            self.clickNow('exit.png')

            self.clickNow('excel.png')
            excel.setDistance(i, distance)
            self.clickNow('chrome.png')

        # self.close()

    def test(self):
        excel = DaumMap.ExcelIO("C:\Temp\거리측정 주소목록.xlsx")
        startAddress = excel.getStartAddress()
        endAddress = excel.getEndAddresses()

        daumMap = DaumMap.Xpath("http://map.daum.net/")
        daumMap.changeModeToWalk()
        daumMap.setStartAddress(startAddress)

        for i in range(0, len(endAddress)):
            addressInfos = endAddress[i].split('\t')
            permission = addressInfos[2].strip()
            if permission == '제외': continue
            distance = daumMap.searchAndGetDistance(addressInfos)

            self.clickNow('excel.png')
            excel.setDistance(i, distance)
            self.clickNow('chrome.png')

        self.close()

    def clickNow(self, templateImage):
        self.scanner.clickNow(templateImage)

    def close(self):
        os.system('TASKKILL /F /IM chrome.exe')

    def ocrtest(self, language = 'kor'):
        image = pyautogui.screenshot(region=(0, 0, 300, 400))
        text = pytesseract.image_to_string(image, lang=language)
        print(text)



Test().ocr()
