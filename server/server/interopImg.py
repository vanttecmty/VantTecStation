from server import app
import json
import re # modulo de regex
from flask import request

@app.route("/interop/image/<course>/<teamCode>", methods=["POST"])
def interopImg(course=None, teamCode=None):
     # validar llamada
    if course is None or teamCode is None:
        return json.dumps({
            "error": True,
            "msg": "course or teamCode None"
        }), 400, {"ContentType":"application/json"}

    pattern = re.compile("[a-zA-Z]{2,5}")

    # validar curso
    if course == "courseA":
        # validate team
        if pattern.match(teamCode):
            # status 200
            return
        else:
            # error
            return json.dumps({
                "error": True,
                "msg": "cannot find team"
            }), 404, {"ContentType":"application/json"}

    elif course == "courseB":
        # validate team
        if pattern.match(teamCode):
            # status 200
            return
        else:
            # error
            return json.dumps({
                "error": True,
                "msg": "cannot find team"
            }), 404, {"ContentType":"application/json"}

    elif course == "openTest":
        # validate team
        if pattern.match(teamCode):
            # status 200
            return
        else:
            # error
            return json.dumps({
                "error": True,
                "msg": "cannot find team"
            }), 404, {"ContentType":"application/json"}
    else:
        return json.dumps({
            "error": True,
            "msg": "Cannot find course"
        }), 404, {"ContentType":"application/json"}
