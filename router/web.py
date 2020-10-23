from flask import Blueprint
from flask import request

web_blueprint = Blueprint('urls', __name__,)

@urls_blueprint.route('/', methods=['GET'])
def hello_word():
    return "HELLO WORD"
