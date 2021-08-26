from fastapi import UploadFile
from typing import List
from dto.text_correcting import WordCorrection

async def proccessingTaggingText(text: str) -> List[str]:
    return ['tag1', 'tag2']


async def proccessingImage(imageFile: UploadFile) -> List[str]:
    return ['label1', 'label2']


async def proccessingCorrectingText(text: str) -> List[WordCorrection]:
    return [
        {
            'word':'error1',
            'correction':'correct 1'
        },
        {
            'word':'error2',
            'correction':'correct 2'
        },
    ]