import requests
import json

class AidiosAPI:
    def __init__(self):
        self.api_base_url = "https://blockstore.tunestamp.com"
        self.max_file_size = 2.5 * 1024  # Maximum file size in bytes (2.5KB)
        self.default_timeout = 60  # Default timeout in seconds

    def _handle_response(self, response):
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception(f'API Request failed with status code {response.status_code}: {response.text}')

    def _make_request(self, method, url, data=None, params=None, headers=None, timeout=None):
        if timeout is None:
            timeout = self.default_timeout

        response = requests.request(method, url, data=data, params=params, headers=headers, timeout=timeout)
        return response

    def retrieve(self, data_id):
        params = {"root_txid": data_id}
        response = self._make_request("GET", f'{self.api_base_url}/retrieve', params=params)
        return self._handle_response(response)

    def store(self, data):
        # Check if the file content size exceeds the API limit
        if len(data["file_content"]) > self.max_file_size:
            raise Exception("File size exceeds the API limit of 2.5KB")

        payload = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = self._make_request("POST", f'{self.api_base_url}/store', data=payload, headers=headers)
        return self._handle_response(response)

    def digest(self, data_id):
        params = {"txid": data_id}
        response = self._make_request("GET", f'{self.api_base_url}/digest', params=params)
        return self._handle_response(response)

    def confirmations(self, transaction_id):
        params = {"txid": transaction_id}
        response = self._make_request("GET", f'{self.api_base_url}/confirmations', params=params)
        return self._handle_response(response)
