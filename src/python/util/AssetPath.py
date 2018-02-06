import uuid

class ImageAsset:

    handlePath = '.\samples\Handle\\'
    screenShotPath = '.\samples\Temp\\'
    
    def createPath(self, matchImage):
        return [self.createMatchImagePath(matchImage), self.createScreenShotPath()]

    def createMatchImagePath(self, matchImage):
        handle = self.handlePath 
        handle += matchImage
        return handle

    def createScreenShotPath(self):
        screenShot = self.screenShotPath
        screenShot += (uuid.uuid4().hex)
        screenShot += '.png'
        return screenShot
