from enum import Enum

from fastapi import FastAPI, UploadFile, File
from typing import List
from dto.auto_tagging import AutoTaggingInput, AutoTaggingOutPut
from dto.image_labeling import ImageLabelingOutPut
from dto.text_correcting import TextCorrectingOutPut,TextCorrectingInput
from models import proccessingTaggingText, proccessingImage, proccessingCorrectingText
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auto-tagging", response_model=AutoTaggingOutPut, tags=["auto-tagging"], name="generate tags for some text")
async def textTagging(input: AutoTaggingInput):
    return {
        'tags': await proccessingTaggingText(input.text)
    }


@app.post("/image-labeling", response_model=ImageLabelingOutPut, tags=["image-labeling"], name="generate labels for image")
async def imageLabeling(file: UploadFile = File(...)):
    return {
        'labels': await proccessingImage(file)
    }


@app.post("/text-correcting", response_model=TextCorrectingOutPut, tags=["text-correcting"], name="get list of wrong words and their correction")
async def textCorrecting(input: TextCorrectingInput):
    return {
        'words': await proccessingCorrectingText(input.text)
    }