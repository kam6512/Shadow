import win32clipboard
import time
import re
import pyautogui
import ClipBoard

class Typer:
    clip = None

    def __init__(self):
        clip = ClipBoard.Clip()
    def currentLang(self): 
        time.sleep(1)
        pyautogui.press('a')
        pyautogui.press('delete')
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'x')
        data = self.clip.getClipboardData()
        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
        res = hangul.findall(data)
        if len(res) == 0:
            return 'kor'
        else:
            return 'eng'

    def convertToEng(self):
        if self.currentLang() == 'kor': pyautogui.press('hangul')

    def convertToKor(self):
        if self.currentLang() == 'eng': pyautogui.press('hangul')

