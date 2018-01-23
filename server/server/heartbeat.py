from server import app, eprint, COURSES, TEAM_PATTERN # app para agregar rutas
from flask import jsonify, request, make_response

@app.route("/heartbeat/<course>/<teamCode>", methods=["POST"])
def logHeart(course, teamCode):
    '''Funcion para hacer log de heartbeat'''
    if course is None or teamCode is None:
        return make_response(jsonify(success=False, msg="Request malformed"), 400)

    if course in COURSES:
        if TEAM_PATTERN.match(teamCode):
            eprint(request.data["timestamp"])
            eprint(request.data["challenge"])
            return make_response(jsonify(success=True), 200)
    return make_response(jsonify(success=False, msg="Cannot find team or course"), 404)
