import os
import pyautogui
import DaumMap

from util import Scanner
from util import ClipBoard

import time

class Test:
    def __init__(self):
        self.clip = ClipBoard.Clip()
        self.scanner = Scanner.MatchTemplate()

    def ocr(self):
        excel = DaumMap.ExcelIO("C:\Temp\거리측정 주소목록.xlsx")
        startAddress = excel.getStartAddress()
        endAddress = excel.getEndAddresses()

        daumMap = DaumMap.OCR("http://map.daum.net/")
        time.sleep(5)
        self.clickNow('walkmode.png')
        daumMap.setStartAddress(startAddress)

        for i in range(0, len(endAddress)):
            addressInfos = endAddress[i].split('\t')
            permission = addressInfos[2].strip()
            if permission == '제외': continue
            self.scanner.clickRightTest('end_input.png')
            addressText = addressInfos[0].strip() + ' ' + addressInfos[1].strip()
            daumMap.setEndAddress(addressText)
            self.clickNow('walk_search.png')
            self.clickNow('distanceBtn.png')

            while(True):
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


Test().ocr()
