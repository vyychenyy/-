from flask import Flask

from maintenanceapp.routes import *


app = Flask(__name__)


app.register_blueprint(routes)

