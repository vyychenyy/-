from flask import Blueprint
routes = Blueprint('routes', __name__)

from .information import *
from .image import*
from .forest import*
from .km import *

