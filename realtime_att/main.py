import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget, QMessageBox
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
from recognizer import FaceRecognizer
from report import generate_pdf
import datetime

class AttendanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система Учёта Посещаемости")
        self.setGeometry(300, 200, 800, 600)

        self.recognizer = FaceRecognizer()
        self.attended_names = set()

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setFixedSize(640, 480)

        self.names_list = QListWidget()

        self.start_button = QPushButton("Старт")
        self.stop_button = QPushButton("Стоп")
        self.report_button = QPushButton("Скачать PDF")

        self.start_button.clicked.connect(self.start_camera)
        self.stop_button.clicked.connect(self.stop_camera)
        self.report_button.clicked.connect(self.save_pdf)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Распознавание студентов</h2>", alignment=Qt.AlignCenter))
        layout.addWidget(self.video_label)
        layout.addWidget(self.names_list)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.report_button)
        self.setLayout(layout)

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        self.video_label.clear()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.5, fy=0.5)

        names = self.recognizer.recognize(small_frame)

        for name in names:
            if name not in self.attended_names:
                self.attended_names.add(name)
                self.names_list.addItem(f"{name} — {datetime.datetime.now().strftime('%H:%M:%S')}")

        h, w, ch = rgb_frame.shape
        qt_img = QImage(rgb_frame.data, w, h, ch * w, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_img))

    def save_pdf(self):
        if not self.attended_names:
            QMessageBox.warning(self, "Нет данных", "Сначала распознайте студентов.")
            return

        filepath = generate_pdf(list(self.attended_names))
        QMessageBox.information(self, "Готово", f"Отчёт сохранён в: {filepath}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AttendanceApp()
    win.show()
    sys.exit(app.exec_())
