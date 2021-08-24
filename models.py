from fastapi import UploadFile
from typing import List
from keyphrases_extraction.gateway import extract_keyphrases


async def proccessingText(text: str, method: str) -> List[str]:
    response = extract_keyphrases(text, method=method)
    print(response)
    return response


async def proccessingImage(imageFile: UploadFile) -> List[str]:
    return ['label1', 'label2']
