from server import app, COURSES
import json
import re # modulo de regex
from flask import jsonify
from random import randint

COLORS = ["red", "green", "blue"]
SYMBOLS = ["cruciform", "triangle", "circle"]
COLORS_LEN = len(COLORS)
SYM_LEN = len(SYMBOLS)

@app.route("/automatedDocking/<course>/<teamCode>", methods=["GET"])
def automatedDocking(course=None, teamCode=None):
    '''Funcion con curso para automated docking'''
    # validar llamada
    if course is None or teamCode is None:
        return jsonify(status=400, msg="Request is malformed")

    pattern = re.compile("[a-zA-Z]{2,5}$")
    # validar curso
    if course in COURSES:
        # validate team
        if pattern.match(teamCode):
            return json.dumps({
                "dockingBaySequence": [
                    {
                        "symbol": SYMBOLS[randint(0, SYM_LEN - 1)],
                        "color": COLORS[randint(0, COLORS_LEN - 1)]
                    },
                    {
                        "symbol": SYMBOLS[randint(0, SYM_LEN - 1)],
                        "color": COLORS[randint(0, COLORS_LEN - 1)]
                    }
                ]
            }), 200, {"ContentType":"application/json"}
    return jsonify(status=404, msg="Cannot find team or course")
