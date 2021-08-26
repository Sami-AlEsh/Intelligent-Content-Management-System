from pydantic import BaseModel, Field
from typing import List


class TextCorrectingInput(BaseModel):
    text: str = Field(..., description="text to get correction from it")


class WordCorrection(BaseModel):
    word: str = Field(..., descrption="the wrong word")
    correction: str = Field(..., description="the correct of the word")

class TextCorrectingOutPut(BaseModel):
    words: List[WordCorrection]
