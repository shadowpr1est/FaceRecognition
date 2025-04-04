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


def recognize_faces(image_path, known_encodings, known_names):
    rgb_image = face_recognition.load_image_file(image_path)

    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    recognized_names = []

    for face_encoding in face_encodings:
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        name = "Не распознан"
        if face_distances[best_match_index] < 0.5:
            name = known_names[best_match_index]
        if name != "Не распознан":
            recognized_names.append(name)

    return recognized_names
