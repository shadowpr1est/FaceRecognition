# recognition/face_recognition_core.py
import face_recognition
import os
import numpy as np

def load_known_faces(known_faces_dir='known_faces'):
    known_encodings = []
    known_names = []

    for filename in os.listdir(known_faces_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])

    return known_encodings, known_names


import face_recognition


def recognize_faces(image, known_encodings, known_names):
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    recognized_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Неизвестно"

        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]
        recognized_names.append(name)

    return recognized_names
