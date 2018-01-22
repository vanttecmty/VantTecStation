from server import app, COURSES # app para agregar rutas
import json # modulo de json
import re # modulo de regex
from flask import jsonify
from random import randint

NUMS = ["1", "2", "3"]
LETTERS = ["X", "Y", "Z"]
NUMS_LEN = len(NUMS)
LETTERS_LEN = len(LETTERS)

@app.route("/obstacleAvoidance/<course>/<teamCode>", methods=["GET"])
def obstacleAvoidance(course=None, teamCode=None):
    '''Funcion para evadir obstaculo por un gate'''
    # validar llamada
    if course is None or teamCode is None:
        return jsonify(status=400, msg="Request is malformed")

    pattern = re.compile("[a-zA-Z]{2,5}$")
    # validar curso
    if course in COURSES:
        # validate team
        if pattern.match(teamCode):
            # status 200
            num = NUMS[randint(0, NUMS_LEN - 1)]
            letter = LETTERS[randint(0, LETTERS_LEN - 1)]
            gate_code = "(" + num + "," + letter + ")"
            return json.dumps({
                "gateCode": gate_code
            }), 200, {"ContentType":"application/json"}
    return jsonify(status=404, msg="Cannot find team or course")
