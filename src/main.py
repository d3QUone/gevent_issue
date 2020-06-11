# Step 1 - patch
#from gevent import monkey
#monkey.patch_all(thread=False)

# Step 2 - import all
import threading

from flask import Flask
from flask import request


app = Flask(__name__)
app.debug = True


@app.route('/')
def index_view():
    x = request.args.get('x', type=str)
    if not x:
        x = 'unknown'
    return 'Hello, World!\nx={}'.format(x)


@app.route('/status')
def index_view():
    return 'Status OK'
