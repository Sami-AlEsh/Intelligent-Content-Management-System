from fastapi import UploadFile
from typing import List


async def proccessingText(text: str) -> List[str]:
    return ['tag1', 'tag2']


async def proccessingImage(imageFile: UploadFile) -> List[str]:
    return ['label1', 'label2']
