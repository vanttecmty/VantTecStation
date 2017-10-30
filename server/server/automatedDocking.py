from server import app
import json
import re # modulo de regex

@app.route("/automatedDocking/<course>/<teamCode>", methods=["GET"])
def automatedDocking(course=None, teamCode=None):
    # validar llamada
    if course is None or teamCode is None:
        return json.dumps({
            "error": True,
            "msg": "course or teamCode None"
        }), 400, {"ContentType":"application/json"}

    pattern = re.compile("[a-zA-Z]{2,5}$")
    # validar curso
    if course == "courseA":
        # validate team
        if pattern.match(teamCode):
            # status 200
            return json.dumps({
                "dockingBaySequence": [
                    {
                        "symbol": "cruciform",
                        "color": "red"
                    },
                    {
                        "symbol": "cruciform",
                        "color": "red"
                    }
                ]
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
                "dockingBaySequence": [
                    {
                        "symbol": "triangle",
                        "color": "green"
                    },
                    {
                        "symbol": "triangle",
                        "color": "green"
                    }
                ]
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
                "dockingBaySequence": [
                    {
                        "symbol": "circle",
                        "color": "blue"
                    },
                    {
                        "symbol": "circle",
                        "color": "blue"
                    }
                ]
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
