from server import app # app para las rutas
import json # modulo de jsons
import re # modulo de regex
from flask import request, after_this_request, jsonify # ver requests recibidas en flask
import sys # usar system path


def eprint(*args, **kwargs):
    '''Funcion de ayuda para hacer print a consola'''
    print(*args, file=sys.stderr, **kwargs)

@app.route("/interop/image/<course>/<teamCode>", methods=["POST"])
def interopImg(course=None, teamCode=None):
    # validar llamada
    if course is None or teamCode is None:
        return "Not OK"

    pattern = re.compile("[a-zA-Z]{2,5}$")
    # validar curso
    if course == "courseA":
        # validate team
        if pattern.match(teamCode):
            # status 200
            return jsonify(status=200)
        else:
            # error
            return "404"

    elif course == "courseB":
        # validate team
        if pattern.match(teamCode):
            # status 200
            return "200"
        else:
            # error
            return "404"

    elif course == "openTest":
        # validate team
        if pattern.match(teamCode):
            # status 200
            return "200"
        else:
            # error
            return "500"
    else:
        return "Nope"

    @after_this_request
    def add_header(response):
        response.headers['Content-Type'] = 'Text'
        response.headers['Content-Length'] = '1500'
        return response
