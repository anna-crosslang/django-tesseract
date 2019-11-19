from __future__ import absolute_import, unicode_literals
from celery.task import task
from celery import Celery
#from .celery import app
from . import ocr

@task(name='ocr')
def perform_ocr(image_path, config_path):
    recognizer = ocr.OpticalCharacterRecognizer(image_path, config_path)
    return recognizer.perform_ocr()

#if __name__ == "__main__":
#    app = Celery('tesserdemo',
#                 broker='amqp://anna:regnela8@localhost:5672/myvhost',
#                 backend='rpc://',
#                 include=['tesserdemo.tasks'])
#    app.start()

