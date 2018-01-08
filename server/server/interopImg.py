from server import app
import json
import re # modulo de regex
from flask import request

REQUESTS_LOG = {}

@app.route("/interop/image/<course>/<teamCode>", methods=["POST"])
def interopImg(course=None, teamCode=None):
    # validar llamada
    if course is None or teamCode is None:
        return 'Not OK'

    pattern = re.compile("[a-zA-Z]{2,5}$")
    # validar curso
    if course == "courseA":
        # validate team
        if pattern.match(teamCode):
            # status 200
            return '200'
        else:
            # error
            return '404'

    elif course == "courseB":
        # validate team
        if pattern.match(teamCode):
            # status 200
            return '200'
        else:
            # error
            return '404'

    elif course == "openTest":
        # validate team
        if pattern.match(teamCode):
            # status 200
            return '200'
        else:
            # error
            return '500'
    else:
        return 'Nope'
