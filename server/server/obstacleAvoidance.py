from server import app
import json
import re # modulo de regex

@app.route("/obstacleAvoidance/<course>/<teamCode>", methods=["GET"])
def obstacleAvoidance(course=None, teamCode=None):
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
            return json.dumps({
                "gateCode": "(1, X)"
            }), 200, {"ContentType":"application/json"}
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
            return json.dumps({
                "gateCode": "(2, Y)"
            }), 200, {"ContentType":"application/json"}
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
            return json.dumps({
                "gateCode": "(3, Z)"
            }), 200, {"ContentType":"application/json"}
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
