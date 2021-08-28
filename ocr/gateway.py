from PIL import Image
import pytesseract
import io
from pdf2image import convert_from_bytes

def extract_text(_bytes: bytes):
    image = Image.open(io.BytesIO(_bytes))
    res = pytesseract.image_to_string(image, lang='ara')
    return res

def extract_text_pdf(_bytes: bytes):

    pages = convert_from_bytes(_bytes, 500)
    image_counter = 1
    for page in pages:
        filename = "page_"+str(image_counter)+".jpg"
        # Save the image of the page in system
        page.save(filename, 'JPEG')
        # Increment the counter to update filename
        image_counter = image_counter + 1
    # Variable to get count of total number of pages
    filelimit = image_counter-1
    text = []
    # Iterate from 1 to total number of pages
    for i in range(1, filelimit + 1):
        filename = "page_"+str(i)+".jpg"
        text.append(str(((pytesseract.image_to_string(Image.open(filename), lang = "ara")))))
    return " ".join(text)