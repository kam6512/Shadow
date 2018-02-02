import uuid

def createPath(matchImage):
    return [createMatchImagePath(matchImage), createScreenShotPath()]

def createMatchImagePath(matchImage):
    handlePath = '.\\samples\\Handle\\'
    handle = handlePath 
    handle += matchImage
    return handle

def createScreenShotPath():
    screenShotPath = '.\\samples\\Temp\\'
    screenShot = screenShotPath
    screenShot += (uuid.uuid4().hex)
    screenShot += '.png'
    return screenShot
