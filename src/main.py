# Step 1 - patch
#from gevent import monkey
#monkey.patch_all(thread=False)

# Step 2 - import all
import threading
import time

from flask import Flask
from flask import request
from flask import current_app


class BackgroundWorker(threading.Thread):

    def __init__(self, _app):
        threading.Thread.__init__(self)
        self.daemon = True

        self._app = _app
        self.counter = 0

    def run(self):
        while True:
            self.counter += 1

            with self._app.app_context():
                current_app.mega_counter = self.counter

            time.sleep(5)


app = Flask(__name__)
app.debug = True

BackgroundWorker(_app=app).start()


@app.route('/')
def index_view():
    x = request.args.get('x', type=str)
    if not x:
        x = 'unknown'
    return 'Hello, World!\nx={}'.format(x)


@app.route('/status')
def status_view():
    counter = getattr(current_app, 'mega_counter', None)
    return 'counter = {}'.format(counter)
