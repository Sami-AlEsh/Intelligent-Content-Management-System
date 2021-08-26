from pydantic import BaseModel

class OcrOutput(BaseModel):
    text: str