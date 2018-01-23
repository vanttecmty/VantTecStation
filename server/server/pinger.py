from server import app, COURSES # app para agregar rutas
import json # modulo de json
import re # modulo de regex
from flask import jsonify, request, make_response
from random import randint

COLORS = ["yellow", "blue", "black", "green", "red"]

@app.route("/pinger/<course>/<teamCode>", methods=["POST"])
def pingLoc(course, teamCode):
    '''Funcion para ping de localizacion'''
    if course is None or teamCode is None:
        return jsonify(status=400, msg="Request is malformed")

    pattern = re.compile("[a-zA-Z]{2,5}$")

    if course in COURSES:
        if pattern.match(teamCode):
            buoyColor1Flag = request.data.get("buoyColor1", 0) in COLORS
            buoyColor2Flag = request.data.get("buoyColor2", 0) in COLORS
            frequency1Flag = 25 <= int(request.data.get("frequency1", 0)) <= 40
            frequency2Flag = 25 <= int(request.data.get("frequency2", 0)) <= 40
            if buoyColor1Flag and buoyColor2Flag and frequency1Flag and frequency2Flag:
                return make_response(jsonify(success=True), 200)
            return make_response(jsonify(success=False, msg="Invalid color or freq"), 503)

    return make_response(jsonify(success=False, msg="Cannot find team or course"), 404)
