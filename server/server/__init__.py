from flask import Flask
from werkzeug.utils import secure_filename
# http://flask.pocoo.org/docs/0.12/quickstart/

UPLOAD_FOLDER = '/static'
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    '''Checar si la extension del archiv es valida'''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from server.functions import *
from server.automatedDocking import automatedDocking
from server.obstacleAvoidance import obstacleAvoidance
from server.interopImg import interopImg