import requests

class plasz_utils:
    def __init__(self, token):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get(self, endpoint):
        response = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None):
        response = requests.post(f"{self.base_url}/{endpoint}", json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()
