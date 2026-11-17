from core.state.SystemLayer.state import SYSTEM_STATE
from core.state.basestatemanager import BaseStateManager
from systemlogging import log_state_transition

class SystemStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            SYSTEM_STATE.SPLASH: [SYSTEM_STATE.APPLICATION,SYSTEM_STATE.QUIT],
            SYSTEM_STATE.APPLICATION: [SYSTEM_STATE.QUIT]
        }
        
        super().__init__(
                initial_state=SYSTEM_STATE.SPLASH,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="SYSTEM_STATE",
                type="SYSTEM"
            )
