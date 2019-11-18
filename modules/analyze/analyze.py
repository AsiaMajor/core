from ..preprocess import Controller as preprocessController
from ..search import Controller as searchController

class Controller():

    def __init__(self, filepath):
        self.filepath = filepath

    def get_result(self):
        preprocess_data = preprocessController(self.filepath).get_result()
        search_result = searchController(preprocess_data['hashkey'], preprocess_data['filename'], preprocess_data['fingerprint']).get_result()
        return search_result