from pydantic import BaseModel
from typing import List


class ImageLabelingOutPut(BaseModel):
    labels: List[str]
