import requests

class Network:
    def __init__(self):
        pass

    def check_network_status(self):
        try:
            response = requests.get("https://snowblitz.net", timeout=5)
            return True
        except requests.ConnectionError:
            return False