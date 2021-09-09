
from enum import Enum

from fastapi import FastAPI, UploadFile, File
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from dto.face_recognition import FaceRecognitionOutput, AddFaceInput
from dto.auto_tagging import AutoTaggingInput, AutoTaggingOutPut
from dto.image_labeling import ImageLabelingOutPut
from dto.text_correcting import TextCorrectingOutPut,TextCorrectingInput
from dto.ocr import OcrOutput

from copy import deepcopy
import re

from models import addFace, extractKeyphrases, proccessingImage, recognizeFaces, applyOcr, applyOcrPdf, generateCaption, correctText

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/auto-tagging", response_model=AutoTaggingOutPut, tags=["auto-tagging"], name="generate tags for some text")
async def textTagging(input: AutoTaggingInput):
    print(input.method)
    return {
        'tags': await extractKeyphrases(input.text, input.method)
    }


@app.post("/image-labeling", response_model=ImageLabelingOutPut, tags=["image-labeling"], name="generate labels for image")
async def imageLabeling(file: UploadFile = File(...)):
    return {
        'labels': await proccessingImage(file)
    }


@app.post("/face-recognition", response_model=FaceRecognitionOutput, tags=["face-recognition"], name="generate names of faces in given image")
async def faceRecognition(file: UploadFile = File(...)):
    return {
        'faces': await recognizeFaces(file)
    }

@app.post("/add-face", tags=["add-face"], name="add new face with name")
async def addNewFace( name: str, file: UploadFile = File(...)):
    await addFace(name, file)
    return 'done'

@app.post("/image-ocr", response_model=OcrOutput, tags=["image-ocr"], name="extract text from image using ocr")
async def imageOcr(file: UploadFile = File(...)):
   
   return {
       'text': await applyOcr(file)
   }

@app.post("/pdf-ocr", response_model=OcrOutput, tags=["pdf-ocr"], name="extract text from pdf using ocr")
async def pdfOcr(file: UploadFile = File(...)):
   
   return {
       'text': await applyOcrPdf(file)
   }

@app.post("/image-captioning", tags=["image-captioning"], name="generate caption for given image")
async def imageCaptioning(file: UploadFile = File(...)):

    caption = await generateCaption(deepcopy(file))

    caption = ' '.join([t for t in caption.split(' ') if t != '<end>'])

    ocr = await applyOcr(deepcopy(file))
    persons = await recognizeFaces(deepcopy(file))

    if len(ocr.strip()) > 0 :
        caption += f'و يوجد نص: {ocr}'

    known_persons = []
    if len(persons) > 0:
        un_cnt = 0
        cnt = 0
        for x in persons: 
            if x == 'Unknown': 
                un_cnt += 1
            else:
                known_persons.append(x)
                cnt += 1
        
        if cnt > 0:
            caption += ' | '
            caption += f'و يوجد {",".join(known_persons)}'
        
        if un_cnt > 0 and un_cnt == 1:
            caption += ' | '
            caption += f'و يوجد شخص غير معروف'
        
        if un_cnt > 1:
            caption += ' | '
            caption += f'و يوجد {un_cnt} شخص غير معروف'
    
    return {
        'text': caption
    }


@app.post("/text-correcting", tags=["text-correcting"], name="get list of wrong words and their correction")
async def textCorrecting(input: TextCorrectingInput):
    return {
        'words': await correctText(input.text)
    }

@app.post("/format-correcting", tags=["text-correcting"], name="get list of wrong words and their correction")
async def formatCorrecting(input: TextCorrectingInput):
    
    formats_re  = [("[\s]{2,}", " "), ("\s،", "،"), ("،[^\s]" ,"، "), ("\s\.","."),("[^\s]\(", " \("),("\s\)", ")"), ("\([\s]", "(")]
    
    res = []

    for wrong_format, correct_format in formats_re:
      for match in re.finditer(wrong_format, input.text):
        res.append((match.start(), match.end(), input.text[match.start(): match.end()], correct_format))

    return {
        'words': res
    }

@app.get("/", name="get list of wrong words and their correction")
async def index():
    return {
        'words': 'hello world'
    }