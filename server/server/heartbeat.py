from server import app, COURSES, eprint # app para agregar rutas
import json # modulo de json
import re # modulo de regex
from flask import jsonify, request, make_response

@app.route("/heartbeat/<course>/<teamCode>", methods=["POST"])
def logHeart(course, teamCode):
    '''Funcion para hacer log de heartbeat'''
    if course is None or teamCode is None:
        return make_response(jsonify(success=False, msg="Request malformed"), 400)

    pattern = re.compile("[a-zA-Z]{2,5}$")
    if course in COURSES:
        if pattern.match(teamCode):
            eprint(request.data["timestamp"])
            eprint(request.data["challenge"])
            return make_response(jsonify(success=True), 200)
    return make_response(jsonify(success=False, msg="Cannot find team or course"), 404)
