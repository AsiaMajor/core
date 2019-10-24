import os
import pandas as pd
from app import app
from flask import request
from modules.search import Search
from flask_restful import Resource

class Ping(Resource):
    def get(self):
        return {
                'success': True,
                'message': "Pong!"
            }

class Analyze(Resource):
    
    def __init__(self):
        self.ALLOWED_EXTENSIONS = set(['csv'])

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def post(self):
        input_file = request.files['file'] #Might have to change the CURL filename on request.files['<CURL_FILENAME>']
        print(input_file)

        if input_file.filename == '':
            return {
                'success': False,
                'message': 'Invalid request: No file detected.'
            }
        
        if not self.allowed_file(input_file.filename):
            return {
                'success': False,
                'message': 'File extension is not allowed'
            }
        else:
            input_file.save(os.path.join('/tmp/', input_file.filename))
            big_five, the_one = Search().analyze(os.path.join('/tmp/', input_file.filename))
            os.remove(os.path.join('/tmp/', input_file.filename))
            return {
                'success': True,
                'input_sheet': input_file.filename,
                'prediction': the_one,
                'predicted_sheets': big_five
            }