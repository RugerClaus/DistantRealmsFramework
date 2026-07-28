from core.state.RuntimeLayer.NetworkLayer.Login.state import LOGIN_STATE
from core.state.basestatemanager import BaseStateManager
from systemlogging import log_state_transition

class LoginStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            LOGIN_STATE.LOGGED_OUT: [LOGIN_STATE.LOGGED_IN],
            LOGIN_STATE.LOGGED_IN: [LOGIN_STATE.LOGGED_OUT, ],
        }
        
        super().__init__(
                initial_state=LOGIN_STATE.LOGGED_OUT,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="FETCHSTATE",
                type="SYSTEM"
            )
