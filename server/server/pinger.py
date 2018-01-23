from server import app, COURSES # app para agregar rutas
import json # modulo de json
import re # modulo de regex
from flask import jsonify, request
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
                return jsonify(success=True)
            return jsonify(success=False)

    return jsonify(status=404, msg="Cannot find team or course")
