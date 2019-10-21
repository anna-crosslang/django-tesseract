import os
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
from celery import Celery
import time
from . import tasks

def index(request):
    my_result = ""

    if 'input_file' in request.FILES:

        app = Celery('tesserdemo',
                     broker='amqp://anna:regnela8@localhost:5672/myvhost',
                     backend='rpc://',
                     include=['tesserdemo.tasks'])

        save_path = os.path.join(settings.MEDIA_ROOT, 'files_to_read', request.FILES['input_file'].name)
        path = default_storage.save(save_path, request.FILES['input_file'])

        my_result = app.signature("ocr").delay(path).get()

        app.close()

    #    result = tasks.perform_ocr.delay(path)
    #    ocr_result = result.get(timeout=100000000000000000)

    context = {
        'ocr_result': my_result,
    }

    return render(request, 'tesserdemo/index.html', context)

