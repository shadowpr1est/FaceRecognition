

import base64

from django.core.files.base import ContentFile
from django.shortcuts import render
from face_recognition_core import load_known_faces, recognize_faces
from .models import Attendance
from .pdf_generator import generate_pdf_report
from django.conf import settings
from django.utils import timezone
import os, cv2



KNOWN_ENCODINGS = []
KNOWN_NAMES = []

if not KNOWN_ENCODINGS:
    KNOWN_ENCODINGS, KNOWN_NAMES = load_known_faces('known_faces')



def your_view(request):
    if request.method == 'POST':
        if 'snapshot' in request.POST:
            format, imgstr = request.POST['snapshot'].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='snapshot.' + ext)


def upload_view(request):
    recognized_names = []
    saved_photo_url = None
    pdf_url = None

    if request.method == 'POST':
        image_data = request.POST.get('snapshot') or request.POST.get('image')

        if not image_data:
            return render(request, 'recognition/upload.html', {'error': 'Изображение не получено'})

        if ';base64,' in image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_bytes = base64.b64decode(imgstr)
        else:
            uploaded_file = request.FILES.get('image')
            if not uploaded_file:
                return render(request, 'recognition/upload.html', {'error': 'Файл не получен'})
            ext = uploaded_file.name.split('.')[-1]
            image_bytes = uploaded_file.read()

        today = timezone.now().strftime('%Y-%m-%d')
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}.{ext}"
        folder = os.path.join('attendance', today)
        full_path = os.path.join(settings.MEDIA_ROOT, folder, filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'wb') as f:
            f.write(image_bytes)

        global KNOWN_ENCODINGS, KNOWN_NAMES
        if not KNOWN_ENCODINGS:
            KNOWN_ENCODINGS, KNOWN_NAMES = load_known_faces('known_faces')

        recognized_names = recognize_faces(full_path, KNOWN_ENCODINGS, KNOWN_NAMES)

        for name in recognized_names:
            Attendance.objects.create(
                name=name,
                photo=os.path.join(folder, filename)
            )

        saved_photo_url = os.path.join(settings.MEDIA_URL, folder, filename)


        pdf_filename = f"report_{timestamp}.pdf"
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'reports', pdf_filename)
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        generate_pdf_report(recognized_names, pdf_path)
        pdf_url = os.path.join(settings.MEDIA_URL, 'reports', pdf_filename)

    return render(request, 'recognition/upload.html', {
        'recognized_names': recognized_names,
        'photo_url': saved_photo_url,
        'pdf_url': pdf_url,
    })

