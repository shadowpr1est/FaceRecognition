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

#
# def downscale_image(image_path, max_width=1000):
#     image = cv2.imread(image_path)
#     height, width = image.shape[:2]
#     if width > max_width:
#         ratio = max_width / width
#         resized = cv2.resize(image, (int(width * ratio), int(height * ratio)))
#         cv2.imwrite(image_path, resized)



def upload_view(request):
    recognized_names = []
    saved_photo_url = None
    pdf_url = None

    if request.method == 'POST':
        image = request.FILES['image']
        today = timezone.now().strftime('%Y-%m-%d')
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')

        filename = f"{timestamp}_{image.name}"
        folder = os.path.join('attendance', today)
        full_path = os.path.join(settings.MEDIA_ROOT, folder, filename)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

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

        # PDF report
        pdf_filename = f"report_{timestamp}.pdf"
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'reports', pdf_filename)
        generate_pdf_report(recognized_names, pdf_path)
        pdf_url = os.path.join(settings.MEDIA_URL, 'reports', pdf_filename)

    return render(request, 'recognition/upload.html', {
        'recognized_names': recognized_names,
        'photo_url': saved_photo_url,
        'pdf_url': pdf_url,
    })

