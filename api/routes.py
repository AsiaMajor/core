from flask import Blueprint, request
from .forms import ResponseForm
from modules import ping, preprocess

api_routes = Blueprint('api', __name__)

#PING Routes
@api_routes.route('/api/ping')
def PingController():
    res = ResponseForm()
    res.result = ping.Controller().mock()
    return res.__dict__

@api_routes.route('/api/preprocess', methods=['POST'])
def preprocessController():
    res = ResponseForm()
    file = request.files['file']
    res.result = preprocess.Controller(file).get_result()
    return res.__dict__