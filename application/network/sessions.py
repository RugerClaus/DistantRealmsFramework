from .endpoints import CREATE_SESSION
from core.engine.network.system_endpoints import API_KEY
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.state.ApplicationLayer.Session.state import ONLINE_SESSION_STATE
from core.state.ApplicationLayer.Session.statemanager import OnlineSessionStateManager
class Session:
    def __init__(self,system):
        self.system = system
        self.state = OnlineSessionStateManager()
        self.sessionToken = None

    def start_online_session(self):

        app_pass = self.system.load.read_constant("clientAppPassword")
        cid = self.system.load.read_constant("clientID")
        if not self.system.control_state.is_state(DEVELOPER_MODE.ON):
            
            response = self.system.network.post(
                CREATE_SESSION,
                {
                    "key": API_KEY,
                    "clientID": cid,
                    "clientAppPassword": app_pass
                }
                
            )

            if not response["success"]:
                print(response)
                self.system.runtime_inspector["OnlineSession"] = False
                return False
            
            self.state.set_state(ONLINE_SESSION_STATE.ACTIVE)
            self.sessionToken = response["data"]["sessionToken"]
            self.system.runtime_inspector["OnlineSession"] = True
            

            return True
        else:
            if not self.state.is_state(ONLINE_SESSION_STATE.INACTIVE):
                self.state.set_state(ONLINE_SESSION_STATE.INACTIVE)
            self.system.runtime_inspector["OnlineSession"] = False
            return False

    def end_online_session(self):
        self.state.set_state(ONLINE_SESSION_STATE.INACTIVE)
        self.system.runtime_inspector["OnlineSession"] = False
        self.sessionToken = None

    