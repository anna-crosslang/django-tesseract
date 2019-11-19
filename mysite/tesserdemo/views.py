import os
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
from celery import Celery
from . import tasks
import pycountry
from os import listdir
from os.path import isfile, join

def index(request):
    my_result = ""

    # fetch the available Tesseract languages and their names
    path_to_models = "/Users/annabardadym/git/django-tesseract/mysite/tessdata"
    trained_models = [f for f in listdir(path_to_models) if isfile(join(path_to_models, f))]

    available_languages = {}
    for trained_model in trained_models:
        if trained_model.endswith(".traineddata"):
            language_code = trained_model.split(".")[0]
            if pycountry.languages.get(alpha_3=language_code):
                available_languages[language_code] = pycountry.languages.get(alpha_3=language_code).name

    if 'image_file' in request.FILES:

        app = Celery('tesserdemo',
                     broker='amqp://anna:regnela8@localhost:5672/myvhost',
                     backend='rpc://',
                     include=['tesserdemo.tasks'])

        image_save_path = os.path.join(settings.MEDIA_ROOT, 'files_to_read', request.FILES['image_file'].name)
        image_path = default_storage.save(image_save_path, request.FILES['image_file'])

        #lang = ""
        #if request.POST['lang']:
        #    lang = request.POST['lang']

        config_path = None
        if 'config_file' in request.FILES:
            config_save_path = os.path.join(settings.MEDIA_ROOT, 'files_to_read', request.FILES['config_file'].name)
            config_path = default_storage.save(config_save_path, request.FILES['config_file'])

        #my_result = app.signature("ocr").delay(image_path, config_path).get()
        my_result = tasks.perform_ocr(image_path, config_path)

        app.close()

    context = {
        'ocr_result': my_result,
        'available_languages': available_languages
        #'available_languages' : enum_list = list(map(int, Color))
    }

    return render(request, 'tesserdemo/index.html', context)

