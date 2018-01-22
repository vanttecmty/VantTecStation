from server import app, COURSES # app para agregar rutas
import json # modulo de json
import re # modulo de regex
from flask import jsonify
from random import randint

@app.route("/pinger/<course>/<teamCode>", methods=["POST"])
def pingLoc(course, teamCode):
    '''Funcion para ping de localizacion'''
    return
