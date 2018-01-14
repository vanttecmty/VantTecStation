from flask import Flask, Response, make_response
from werkzeug.utils import secure_filename
from flask import jsonify, flash # modulo para regresar jsons
import os # acceso al sistema
import uuid # modulo para ids unicos
import sys # usar system path
# http://flask.pocoo.org/docs/0.12/quickstart/

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static\\uploads')
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def eprint(*args, **kwargs):
    '''Funcion de ayuda para hacer print a consola'''
    print(*args, file=sys.stderr, **kwargs)

def allowed_file(filename):
    '''Checar si la extension del archivo es valida'''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(file):
    # validar que la llamada tiene archivo
    if file.filename == '':
        flash("No se selecciono archivo")
        return jsonify(error="No se selecciono archivo")

    # validar extension de archivo
    if file and allowed_file(file.filename):
        # crear id para filename
        filename = str(uuid.uuid4())
        extension = '.' + file.filename.rsplit('.', 1)[1].lower()
        # cambiar filename
        file.filename = filename + extension
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        response = make_response(jsonify(id=filename))
        response.headers['Content-Type'] = 'application/json'
        response.headers['Content-Length'] = os.stat(file_path).st_size
        return response
    return jsonify(error="Subir archivo de nuevo")

from server.functions import *
from server.automatedDocking import automatedDocking
from server.obstacleAvoidance import obstacleAvoidance
from server.interopImg import interopImg