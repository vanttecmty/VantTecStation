from server import app, eprint, COURSES, TEAM_PATTERN
from flask import jsonify, make_response

@app.route("/run/start/<course>/<teamCode>", methods=["POST"])
def start(course, teamCode):
    '''Funcion para iniciar el run del concurso'''
    if course is None or teamCode is None:
        return make_response(jsonify(success=False, msg="Request is malformed"), 400)

    if course in COURSES:
        if TEAM_PATTERN.match(teamCode):
            eprint("Start " + course)
            return make_response(jsonify(success=True), 200)
    return make_response(jsonify(success=False, msg="Cannot find team or course"), 404)


