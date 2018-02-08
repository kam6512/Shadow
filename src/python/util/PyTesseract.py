import cv2

# try:
#     import Image
# except ImportError:
#     from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\DEV_MODULE\\Tesseract-OCR\\tesseract.exe'


def ocr(path):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    image = cv2.pyrUp(image)
    cv2.imwrite('..\\samples\\upscale.png', image)
    text = pytesseract.image_to_string(image, lang='eng', config="-psm 7 -oem 3")
    print(text)


ocr('..\samples\\km.png')
