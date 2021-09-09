from fastapi import UploadFile, File
from pydantic import BaseModel
from typing import List


class FaceRecognitionOutput(BaseModel):
    faces: List[str]

class AddFaceInput(BaseModel):
    name: str
    file: UploadFile = File(...)