from ._face_recognition import FaceRecognition
from PIL import Image
import io
import numpy as np

def recognize_faces(image):

    fr = FaceRecognition('./_face_recognition/data/faces_encodings.pkl', './_face_recognition/data/faces_names.pkl')

    res = fr.check_faces_file(image)
    print(res)
    return res

def add_face(name, image):
    fr = FaceRecognition('./_face_recognition/data/faces_encodings.pkl', './_face_recognition/data/faces_names.pkl')

    fr.add_person_file(name, image)

    return


def load_image(_bytes: bytes):
    im = Image.open(io.BytesIO(_bytes))
    im = im.convert('RGB')
    im = np.array(im)
    return im