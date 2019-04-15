from modules.search import Search
from flask_restful import Resource

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