from fastapi import UploadFile
from typing import List
from PIL import Image
import io
import numpy as np

from keyphrases_extraction.gateway import extract_keyphrases
from _face_recognition.gateway import recognize_faces, add_face, load_image
from ocr.gateway import extract_text, extract_text_pdf
from image_captioning.gateway import generate_caption

from dto.text_correcting import WordCorrection


async def extractKeyphrases(text: str, method: str) -> List[str]:
    response = extract_keyphrases(text, method=method)
    print(response)
    return response


async def proccessingImage(imageFile: UploadFile) -> List[str]:
    return ['label1', 'label2']


async def recognizeFaces(file: UploadFile) -> List[str]:
    image = load_image(file.file.read())

    return recognize_faces(image)

async def addFace(name: str, file: UploadFile):
    image = load_image(file.file.read())
    
    add_face(name, image)


async def applyOcr(file: UploadFile):
    return extract_text(file.file.read())


async def applyOcrPdf(file: UploadFile):
    return extract_text_pdf(file.file.read())


async def generateCaption(file: UploadFile):
    return generate_caption(file.file.read())


async def proccessingCorrectingText(text: str) -> List[WordCorrection]:
    return [
        {
            'word':'error1',
            'correction':'correct 1'
        },
        {
            'word':'error2',
            'correction':'correct 2'
        },
    ]
