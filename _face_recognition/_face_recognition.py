import face_recognition
import pickle
import numpy as np

class FaceRecognition:
  

    def __init__(self, faces_encodings_path, faces_names_path):
        
        self.faces_encodings_path = faces_encodings_path
        self.faces_names_path = faces_names_path

        with open(faces_encodings_path, 'rb') as f:
            self.faces_encodings = pickle.load(f)

        with open(faces_names_path, 'rb') as f:
            self.faces_names = pickle.load(f)

    def update_data(self):
        with open(self.faces_encodings_path, 'wb') as f:
            pickle.dump(self.faces_encodings, f)

        with open(self.faces_names_path, 'wb') as f:
            pickle.dump(self.faces_names, f)

    def upper_first_letter(self, str):
        res = ""
        for s in str.split():
            s = s[0].capitalize() +  s[1:]
            res = res + " " + s
        return res
  

    def add_person_url(self, name, url):
        name = self.upper_first_letter(name)
        if name not in self.faces_names:
            person_image = face_recognition.load_image_file(url)
            person_face_encoding = face_recognition.face_encodings(person_image)[0]
            
            self.faces_encodings.append(person_face_encoding)
            self.faces_names.append(name)

            self.update_data()


    def add_person_file(self, name, image):
        name = self.upper_first_letter(name)
        if name not in self.faces_names:
            person_face_encoding = face_recognition.face_encodings(image)[0]
            
            self.faces_encodings.append(person_face_encoding)
            self.faces_names.append(name)

            self.update_data()

    # Load an image with an unknown face
    def check_faces_url(self, url):
        persons = []
        unknown_image = face_recognition.load_image_file(url)

        # Find all the faces and face encodings in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        # Loop through each face found in the unknown image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.faces_encodings, face_encoding, tolerance = 0.5)

            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.faces_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.faces_names[best_match_index].lstrip()
                
            persons.append(name)
        return persons

    def check_faces_file(self, image):
        persons = []
        unknown_image = image

        # Find all the faces and face encodings in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        # Loop through each face found in the unknown image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.faces_encodings, face_encoding, tolerance = 0.5)

            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.faces_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.faces_names[best_match_index].lstrip()
                
            persons.append(name)
        return persons 