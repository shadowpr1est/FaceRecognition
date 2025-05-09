import base64
import os
from datetime import timezone

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from attendance_system import settings
from face_recognition_core import recognize_faces, load_known_faces
from recognition.models import Attendance
from recognition.pdf_generator import generate_pdf_report


@csrf_exempt
def recognize_view(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            image_data = body.get('snapshot')

            if not image_data or ';base64,' not in image_data:
                return JsonResponse({'error': 'Некорректные данные'}, status=400)

            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_bytes = base64.b64decode(imgstr)

            from django.utils import timezone

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

            if recognized_names:
                name = recognized_names[0]
                Attendance.objects.create(
                    name=name,
                    photo=os.path.join(folder, filename)
                )
                return JsonResponse({'name': name})
            else:
                return JsonResponse({'name': None})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)

def report_view(request):
    today = timezone.now().strftime('%Y-%m-%d')
    entries = Attendance.objects.filter(timestamp__date=today)

    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    pdf_filename = f"report_{timestamp}.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'reports', pdf_filename)
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    generate_pdf_report([entry.name for entry in entries], pdf_path)
    pdf_url = os.path.join(settings.MEDIA_URL, 'reports', pdf_filename)

    return render(request, 'recognition/report.html', {
        'pdf_url': pdf_url,
        'entries': entries,
    })
