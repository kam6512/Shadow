import os
import pyautogui
import DaumMap

from util import Scanner
from util import ClipBoard


class Test:
    def __init__(self):
        self.clip = ClipBoard.Clip()
        self.scanner = Scanner.MatchTemplate()

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


Test().test()
