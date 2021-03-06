from pydantic import BaseModel, Field
from typing import List


class AutoTaggingInput(BaseModel):
    text: str = Field(..., description="arabic text to generate tags from")
    method: str = Field(default='bert_cs', description="...")


class AutoTaggingOutPut(BaseModel):
    tags: List[str]




