from fastapi import UploadFile
from typing import List

from keyphrases_extraction.gateway import extract_keyphrases
from _face_recognition.gateway import recognize_faces, add_face, load_image
from ocr.gateway import extract_text, extract_text_pdf
from image_captioning.gateway import generate_caption
from text_correction.gateway import correct_text

from dto.text_correcting import WordCorrection

import cProfile, pstats


async def extractKeyphrases(text: str, method: str) -> List[str]:
    # profile = cProfile.Profile()
    # profile.enable()
    # response = profile.runcall(extract_keyphrases, text, method=method)
    response = extract_keyphrases(text, method=method)
    # profile.disable()
    # print(response)
    # stats = pstats.Stats(profile).sort_stats('ncalls')
    # profile.print_stats()
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


async def correctText(text: str):
    return correct_text(text)
