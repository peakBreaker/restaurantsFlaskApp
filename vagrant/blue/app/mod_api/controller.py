from flask import Blueprint

mod = Blueprint('api', __name__)

@mod.route('/getstuff')
def getstuff():
    return '{"result" : "You are accessing the api"}'
