import face_recognition
import cv2
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


def recognize_faces_in_image(image_path, known_encodings, known_names):
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    print(f"[INFO] Обнаружено лиц: {len(face_locations)}")

    recognized_names = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        name = "Unknown"


        if face_distances[best_match_index] < 0.5:
            name = known_names[best_match_index]

        recognized_names.append(name)


        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(image, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)


    cv2.imshow("Результат", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return recognized_names



if __name__ == "__main__":
    known_encodings, known_names = load_known_faces()
    results = recognize_faces_in_image("test-image3.jpg", known_encodings, known_names)
    print("Распознанные лица:", results)


