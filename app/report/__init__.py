from flask import Blueprint


report_b = Blueprint('report_b', __name__, template_folder='./templates')

from . import views
