import json

import requests


class SearchService:
    # todo: pass in the search service info in environment
    def __init__(self):
        self.search_endpoint = 'http://search_service:8080/api/search'
        self.headers = {"Host": "localhost"}

    def get_images_for_query(self, query):
        req = requests.get(f"{self.search_endpoint}/?query={query}", headers=self.headers)
        body = json.loads(req.content)
        return body['filenames']

