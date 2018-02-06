import win32clipboard


class Clip:
    def getClipboardData(self):
        self.open()
        data = win32clipboard.GetClipboardData()
        self.close
        return data

    def setClipboard(self, text):
        self.open()
        self.clean()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, text)
        self.close

    def open(self):
        win32clipboard.OpenClipboard()

    def clean(self):
        win32clipboard.EmptyClipboard()

    def close(self):
        win32clipboard.CloseClipboard()
