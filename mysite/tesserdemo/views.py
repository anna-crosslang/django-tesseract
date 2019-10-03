from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from . import ocr

def index(request):
    recognizer = ocr.OpticalCharacterRecognizer()
    recognizer.load_image()
    recognizer.check_thresholding()
    recognizer.write_img_to_disk()
    result = recognizer.get_result()
    return HttpResponse(result)

