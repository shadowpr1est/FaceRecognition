import face_recognition
import os
import numpy as np

class FaceRecognizer:
    def __init__(self, faces_dir='known_faces'):
        self.known_encodings = []
        self.known_names = []
        self.load_known_faces(faces_dir)

    def load_known_faces(self, path):
        for filename in os.listdir(path):
            if filename.endswith(('.jpg', '.png')):
                image_path = os.path.join(path, filename)
                img = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(img)
                if encodings:
                    self.known_encodings.append(encodings[0])
                    self.known_names.append(os.path.splitext(filename)[0])

    def recognize(self, frame):
        names = []
        face_locations = face_recognition.face_locations(frame)
        encodings = face_recognition.face_encodings(frame, face_locations)

        for encoding in encodings:
            matches = face_recognition.compare_faces(self.known_encodings, encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(self.known_encodings, encoding)
            best_match = np.argmin(face_distances)
            if matches[best_match]:
                names.append(self.known_names[best_match])
        return names
