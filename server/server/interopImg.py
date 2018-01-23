from server import app, upload_file, eprint, COURSES # app para las rutas
import json # modulo de jsons
import re # modulo de regex
from flask import request, after_this_request, jsonify, flash # ver requests recibidas en flask


@app.route("/interop/image/<course>/<teamCode>", methods=["POST"])
def interopImg(course=None, teamCode=None):
    '''Funcion para subir imagen'''
    # validar llamada
    if course is None or teamCode is None:
        return jsonify(result="Not OK", error="Teamcode o course es None")

    if 'file' not in request.files:
        flash('No incluye archivo')
        return jsonify(error="No incluye archivo")

    file = request.files['file']
    pattern = re.compile("[a-zA-Z]{2,5}$")

    # validar curso
    if course in COURSES:
        # validar team
        if pattern.match(teamCode):
            # status 200
            return upload_file(file)
        else:
            # error
            return jsonify(status=403, error="Codigo de equipo no permitido")
    return jsonify(status=404, error="Curso no encontrado")

@app.route("/interop/report/<course>/<teamCode>", methods=["POST"])
def reportImg(course=None, teamCode=None):
    '''Funcion para reportar forma de imagen'''
    if course is None or teamCode is None:
        return jsonify(status=400, message="Request is malformed")

    pattern = re.compile("[a-zA-Z]{2,5}$")

    if course in COURSES:
        if pattern.match(teamCode):
            eprint(request.data["shape"])
            return jsonify(success=True)
    return jsonify(status=404, message="Cannot find course or team")

