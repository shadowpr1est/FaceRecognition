# Face Recognition Attendance System

An automatic attendance tracking system using face recognition via a device camera. The system allows students to register by taking a snapshot, and teachers can later download a full attendance report in PDF format.

# Overview

This project solves the problem of manual attendance tracking in classrooms. It allows students to check in via camera or photo upload, and automatically detects and logs their names. Teachers can download a well-formatted PDF report at any time.

# Features

🎥 Face recognition through webcam

🖼 Manual photo upload option

✅ Automatic name recognition

📄 PDF report generation for attendance logs

🔐 CSRF-protected forms

📁 Image and record storage

# Stack:

Python 3.13+

Django 5.2

face_recognition (dlib-based)

OpenCV (cv2)

reportlab (for PDF reports)

Bootstrap 5 (for frontend styling)


# Installation

### 1. Clone the repository

```git clone https://github.com/shadowpr1est/FaceRecognition.git```

### 2. Create and activate a virtual environment

```python venv .venv```

```.venv\Scripts\activate```

### 3. Install dependencies

```pip install -r requirements.txt```


### 4. Run database migrations

```python manage.py migrate```

### 5. Start the development server

```python manage.py runserver```

# Usage

Open http://127.0.0.1:8000/ in your browser.

Either take a snapshot using your webcam or upload a photo.

The system will recognize faces and log the names.

A downloadable PDF report will be generated for the teacher.


# Project structure


FaceRecognition/
│
├── recognition/               # Django app
│   ├── templates/
│   │   └── upload.html        # Main frontend page
│   ├── views.py               # View logic
│   ├── face_recognition_core.py  # Face detection logic
│   └── urls.py
│
├── media/                     # Uploaded images and reports
│   └── attendance/            # Saved snapshots
│
├── static/                    # Static files (if needed)
├── manage.py
├── requirements.txt
└── README.md



# Security

All forms are CSRF-protected.

Images and data are stored locally on the server, not in the cloud.

Access to PDF reports can be restricted via login (not implemented yet).


# Future Improvements

Teacher dashboard for managing attendance history

Responsive mobile interface

Emotion detection or face mask recognition

Cloud storage and analytics integration

