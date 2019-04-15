from modules.search import Search
from flask_restful import Resource

class AllSheets(Resource):
    def get(self):
        message = Search.analyze()
        return {
            'status_code': 200,
            'message': message
        }

class Analyze(Resource):
    def post(self):
        return {
            'status_code': 200,
            'message': 'API end-point for uploading a sheet for analysis'
        }