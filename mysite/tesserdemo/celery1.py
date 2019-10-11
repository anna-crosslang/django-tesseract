from __future__ import absolute_import, unicode_literals
from celery import Celery

#app = Celery('tesserdemo',
#             broker='amqp://anna:regnela8@localhost:5672/myvhost',
#             backend='rpc://',
#             include=['tesserdemo.tasks'])

# Optional configuration, see the application user guide.
#app.conf.update(
#    result_expires=3600,
#)

if __name__ == '__main__':
#    app.start()
    print('test')