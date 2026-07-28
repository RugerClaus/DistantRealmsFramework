from core.application.network.endpoints import LOGIN,REGISTER
from core.guts.network.system_endpoints import API_KEY,VERSION
from core.state.RuntimeLayer.NetworkLayer.Login.state import LOGIN_STATE

class Authentication:

    def __init__(self, system):
        self.system = system
        self.network = system.network

    def register(self, username, password):

        response = self.network.post(
            REGISTER,
            {
                "username": username,
                "password": password,
                "key": API_KEY,
                "client_version": VERSION
            }
        )

        if not response.get("success"):
            return response
        data = response.get("data", {})

        if "clientAppPassword" not in data:
            return {
                "success": False,
                "message": "Invalid server response",
                "data": response
            }

        self.system.save.write_constant(
            "username",
            username
        )

        self.system.save.write_constant(
            "clientAppPassword",
            data["clientAppPassword"]
        )

        self.system.save.write_constant(
            "clientID",
            data["clientID"]
        )
        self.system.login_state.set_state(LOGIN_STATE.LOGGED_IN)
        return {
            "success": True
        }

    def login(self, username, password):

        client_id = self.system.load.read_constant("clientID")
        

        response = self.network.post(
            LOGIN,
            {
                "username": username,
                "password": password,
                "key": API_KEY,
                "clientID": client_id,
                "client_version": VERSION
            }
        )

        if not response["success"]:
            return response

        data = response["data"]

        self.system.persistence.save.write_constant(
            "username",
            username
        )

        self.system.persistence.save.write_constant(
            "clientAppPassword",
            data["clientAppPassword"]
        )

        self.system.persistence.save.write_constant(
            "clientID",
            data["clientID"]
        )

        self.system.system_monitor["ClientConnected"] = True
        self.system.login_state.set_state(LOGIN_STATE.LOGGED_IN)
        return {
            "success": True,
            "data": data
        }


    def auto_login(self):

        username = self.system.persistence.load.read_constant("username")
        client_app_password = self.system.persistence.load.read_constant("clientAppPassword")
        client_id = self.system.persistence.load.read_constant("clientID")

        if not username or not client_app_password or not client_id:
            return {
                "success": False
            }

        response = self.network.post(
            LOGIN,
            {
                "username": username,
                "clientID": client_id,
                "clientAppPassword": client_app_password,
                "key": API_KEY,
                "client_version": VERSION
            }
        )           

        if response["success"]:
            data = response["data"]
            self.system.login_state.set_state(LOGIN_STATE.LOGGED_IN)
            self.system.system_monitor["ClientConnected"] = True

        return response

    def log_out(self):
        self.system.persistence.save.clear("clientID")
        self.system.persistence.save.clear("clientAppPassword")
        self.system.user.username = "Player"
        self.system.login_state.set_state(LOGIN_STATE.LOGGED_OUT)