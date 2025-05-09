import cv2
import os
import time
from face_recognition_core import load_known_faces, recognize_faces
from recognition.pdf_generator import generate_pdf_report

KNOWN_ENCODINGS, KNOWN_NAMES = load_known_faces("known_faces")
attendance_log = []
today_folder = time.strftime('%Y-%m-%d')
os.makedirs(f"attendance/{today_folder}", exist_ok=True)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Не удалось открыть камеру")
    exit()

print("Нажмите 'q' для выхода и генерации PDF-отчета")

last_recognition_time = 0
recognition_interval = 2

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Камера', frame)

    current_time = time.time()
    if current_time - last_recognition_time >= recognition_interval:
        last_recognition_time = current_time

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        recognized = recognize_faces(rgb_frame, KNOWN_ENCODINGS, KNOWN_NAMES)

        for name in recognized:
            timestamp = time.strftime('%H:%M:%S')
            photo_filename = f"{name}_{timestamp}.jpg"
            photo_path = os.path.join("attendance", today_folder, photo_filename)
            cv2.imwrite(photo_path, frame)
            if name not in [entry[0] for entry in attendance_log]:
                attendance_log.append((name, timestamp, photo_path))
                print(f"[✓] {name} был распознан в {timestamp}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

pdf_filename = f"report_{time.strftime('%Y%m%d_%H%M%S')}.pdf"
pdf_path = os.path.join("reports", pdf_filename)
os.makedirs("reports", exist_ok=True)

names_only = [entry[0] for entry in attendance_log]
generate_pdf_report(names_only, pdf_path)

print(f"PDF-отчет создан: {pdf_path}")
