import win32clipboard
import time
import re
import pyautogui

def currentLang(): 
    time.sleep(1)
    pyautogui.press('a')
    pyautogui.press('delete')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'x')
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    res = hangul.findall(data)
    if len(res) == 0:
        return 'kor'
    else:
        return 'eng'

def convertToEng():
    lang = Language.currentLang()
    if lang == 'kor': 
        pyautogui.press('hangul')

