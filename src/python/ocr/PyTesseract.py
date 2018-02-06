try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\DEV_MODULE\\Tesseract-OCR\\tesseract.exe'
def OCR(path, language = 'eng'):
    image = Image.open(path)
    text = pytesseract.image_to_string(image, lang=language)
    print(text)

OCR('..\samples\OCR\\2.png')
