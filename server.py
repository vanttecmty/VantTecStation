from flask import Flask
import json
import re # modulo de regex

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    '''Funcion de testing para servidor'''
    return "Hello World!"

@app.route("/followLeader/<course>/<teamCode>", methods=["GET"])
def follow_leader(course, teamCode):
    '''Funcion para iniciar follow de leader challenge'''
    return json.dumps({"success":True, "course": course}), 200, {"ContentType":"application/json"}

@app.route("/heartbeat/<course>/<teamCode>", methods=['POST'])
def heartbeat(course, teamCode):
    '''Funcion heartbeat para log de estatus de bote'''
    return json.dumps({"success":True}), 200, {"ContentType":"application/json"}

@app.route("/run/start/<course>/<teamCode>", methods=['POST'])
def run_start(course, teamCode):
    '''Funcion para empezar el run del bote'''
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/run/end/<course>/<teamCode>", methods=['POST'])
def run_end(course, teamCode):
    '''Funcion para detener el bote'''
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/docking/image/<course>/<teamCode>")
def docking(course, teamCode):
    '''Funcion para mandar docking al bote'''
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/obstacleAvoidance/<course>/<teamCode>", methods=['GET'])
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

@app.route("/automatedDocking/<course>/<teamCode>", methods=["GET"])
def automatedDocking(course=None, teamCode=None):
    # validar llamada
    if course is None or teamCode is None:
        return json.dumps({
            "error": True,
            "msg": "course or teamCode None"
        }), 400, {"ContentType":"application/json"}

    pattern = re.compile("[a-zA-Z]{2,5}")
    # validar curso
    if course == "courseA":
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
