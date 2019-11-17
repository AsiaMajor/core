import os
from flask import Blueprint, request
from .forms import ResponseForm
from modules import ping, preprocess, search

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
    file.save(os.path.join('tmp/', file.filename))
    res.result = preprocess.Controller(os.path.join('tmp/', file.filename)).get_result()
    return res.__dict__

@api_routes.route('/api/search', methods=['POST'])
def searchController():
    res = ResponseForm()
    #hash_key = request.get_json()['hash_key']
    #sheet_name = request.get_json()['sheet_name']
    #fingerprint = request.get_json()['fingerprint']
    #res.result = search.Controller(hash_key, sheet_name, fingerprint).get_result()
    res.result = "cole bitch"
    return res.__dict__