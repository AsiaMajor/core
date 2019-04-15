from modules.search import Search
from flask_restful import Resource
import pandas as pd
from flask import request

class AllSheets(Resource):
    def get(self):
        return {
            'status_code': 200,
            'message': "API endpoint for getting all the sheets"
        }

class Analyze(Resource):
    def post(self):
        message = Search.analyze()
        return {
            'status_code': 200,
            'sheets': message 
        }

class ReadFile(Resource):
    def post(self):
        df = pd.read_csv(request.files['']) #Might have to change the CURL filename on request.files['<CURL_FILENAME>']
        return {
            'status_code': 200,
            'sheets': df.shape 
        }