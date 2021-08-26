from PIL import Image
import pytesseract
import io

def extract_text(_bytes: bytes):
    image = Image.open(io.BytesIO(_bytes))
    res = pytesseract.image_to_string(image, lang='ara')
    return res