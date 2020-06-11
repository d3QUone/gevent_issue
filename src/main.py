# Step 1 - patch
from gevent import monkey
monkey.patch_all(thread=False)

# Step 2 - import all
import threading
import time

from flask import Flask
from flask import request
from flask import current_app
import requests


class BackgroundWorker(threading.Thread):

    def __init__(self, _app):
        threading.Thread.__init__(self)
        self.daemon = True

        self._app = _app
        self.counter = 0

    def run(self):
        while True:
            # Add big http-request with slow json-parsing
            r = requests.get('https://gist.githubusercontent.com/d3QUone/1785ec792c720df2477d47180fc629e2/raw/a1c446274dc43a6a6f77ad86746d5008291e5062/big.json')
            data = r.json()

            with self._app.app_context():
                current_app.last_status = r.status_code
                self.counter += 1
                current_app.mega_counter = self.counter

            time.sleep(1)


app = Flask(__name__)
app.debug = True

BackgroundWorker(_app=app).start()


@app.route('/')
def index_view():
    x = request.args.get('x', type=str)
    if not x:
        x = 'unknown'
    time.sleep(0.5)
    return 'Hello, World!\nx={}'.format(x)


@app.route('/status')
def status_view():
    counter = getattr(current_app, 'mega_counter', None)
    return 'counter = {}'.format(counter)
