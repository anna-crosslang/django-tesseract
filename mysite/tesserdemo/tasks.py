from __future__ import absolute_import, unicode_literals
#from celery import Celery
from .celery import app

#app = Celery('tasks', backend='rpc://', broker='amqp://anna:regnela8@localhost:5672/myvhost')

@app.task
def add(x, y):
    return x + y

@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

if __name__ == "__main__":
    result = add.delay(4, 4)

