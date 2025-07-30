import requests
from utils.logger import simple_logger

class HTTPClient:
    def __init__(self, url, logger):
        self.base_url = url.rstrip('/')
        self.logger = logger
        self.session = requests.Session()


    @simple_logger
    def post(self, endpoint: str, data=None, headers=None):
        url = self.base_url + endpoint
        response = self.session.post(url, data=data, headers=headers)
        response.raise_for_status()

        return response


    @simple_logger
    def get(self, endpoint: str, params=None, headers=None):
        url = self.base_url + endpoint
        response = self.session.get(url, params=params, headers=headers)
        response.raise_for_status()

        return response