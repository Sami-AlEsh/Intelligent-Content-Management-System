from enum import Enum

from fastapi import FastAPI, UploadFile, File
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from dto.auto_tagging import AutoTaggingInput, AutoTaggingOutPut
from dto.image_labeling import ImageLabelingOutPut
from models import proccessingText, proccessingImage

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
        'tags': await proccessingText(input.text, input.method)
    }


@app.post("/image-labeling", response_model=ImageLabelingOutPut, tags=["image-labeling"], name="generate labels for image")
async def imageLabeling(file: UploadFile = File(...)):
    return {
        'labels': await proccessingImage(file)
    }
