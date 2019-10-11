import os
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from . import ocr
from django.core.files.storage import default_storage

from . import tasks

def index(request):
    result = tasks.add.delay(4, 4)
    testvar = result.get(timeout=1)

    ocr_result = 'No text has been read yet.'

    if 'input_file' in request.FILES:
        save_path = os.path.join(settings.MEDIA_ROOT, 'files_to_read', request.FILES['input_file'].name)
        path = default_storage.save(save_path, request.FILES['input_file'])

        recognizer = ocr.OpticalCharacterRecognizer(path)
        recognizer.load_image()
        recognizer.check_thresholding()
        recognizer.write_img_to_disk()
        ocr_result = recognizer.get_result()

    context = {
        'ocr_result': ocr_result,
        'testvar': testvar
    }

    return render(request, 'tesserdemo/index.html', context)

