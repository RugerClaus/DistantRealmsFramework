import requests

from systemlogging import log_error


class Network:

    def __init__(self, timeout=5):
        self.timeout = timeout

    def check_network_status(self):
        try:
            response = requests.get("https://snowblitz.net", timeout=5)
            if response.status_code is not None:
                return True
            else:
                return False
        except requests.RequestException:
            return False

    def get(self, url, params=None):
        try:
            response = requests.get(
                url,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()

            return {
                "success": True,
                "data": response.json()
            }

        except requests.RequestException as e:
            log_error(e)

            return {
                "success": False,
                "message": str(e)
            }

    def post(self, url, data=None):
        try:
            response = requests.post(
                url,
                json=data,
                timeout=self.timeout
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            log_error(e)

            return {
                "success": False,
                "message": str(e)
            }