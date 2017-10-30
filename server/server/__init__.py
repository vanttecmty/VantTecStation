from flask import Flask
# http://flask.pocoo.org/docs/0.12/quickstart/

app = Flask(__name__)

from server.functions import *
from server.automatedDocking import automatedDocking
from server.obstacleAvoidance import obstacleAvoidance
from server.interopImg import interopImg