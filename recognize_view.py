
import base64

from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from face_recognition_core import load_known_faces, recognize_faces
from django.conf import settings
from django.utils import timezone
import os, cv2
import json

@csrf_exempt
def recognize_view(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        image_data = body.get('snapshot')

        if ';base64,' not in image_data:
            return JsonResponse({'error': 'Некорректные данные'}, status=400)

        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        image_bytes = base64.b64decode(imgstr)

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
