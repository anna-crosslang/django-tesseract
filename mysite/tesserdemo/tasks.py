from __future__ import absolute_import, unicode_literals
from celery.task import task
from celery import Celery
#from .celery import app
from . import ocr
#import time

#app = Celery('tasks', backend='rpc://', broker='amqp://anna:regnela8@localhost:5672/myvhost')


@task(name='ocr')
def perform_ocr(file_path):
    recognizer = ocr.OpticalCharacterRecognizer(file_path)
    recognizer.load_image()
    recognizer.check_thresholding()
    recognizer.write_img_to_disk()
    return recognizer.get_result()

if __name__ == "__main__":
    app = Celery('tesserdemo',
                 broker='amqp://anna:regnela8@localhost:5672/myvhost',
                 backend='rpc://',
                 include=['tesserdemo.tasks'])
    app.start()

