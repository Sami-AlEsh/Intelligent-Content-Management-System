
from enum import Enum

from fastapi import FastAPI, UploadFile, File
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from dto.face_recognition import FaceRecognitionOutput, AddFaceInput
from dto.auto_tagging import AutoTaggingInput, AutoTaggingOutPut
from dto.image_labeling import ImageLabelingOutPut
from dto.ocr import OcrOutput

from models import addFace, extractKeyphrases, proccessingImage, recognizeFaces, applyOcr, generateCaption

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

@app.post("/image-captioning", tags=["image-captioning"], name="generate caption for given image")
async def imageCaptioning(file: UploadFile = File(...)):
   
   return {
       'text': await generateCaption(file)
   }
