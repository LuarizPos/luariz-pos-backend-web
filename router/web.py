from flask import Blueprint
from flask import request

web_blueprint = Blueprint('web', __name__, url_prefix='/')

@web_blueprint.route('/', methods=['GET'])
def hello_word():
    return "HELLO"
