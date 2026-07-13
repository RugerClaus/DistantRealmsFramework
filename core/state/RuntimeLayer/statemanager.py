from core.state.RuntimeLayer.state import RUNTIME_STATE
from core.state.basestatemanager import BaseStateManager
from systemlogging import log_state_transition

class RuntimeStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            RUNTIME_STATE.LOADING: [RUNTIME_STATE.MAIN_MENU,RUNTIME_STATE.APPLICATION,RUNTIME_STATE.QUIT],
            RUNTIME_STATE.MAIN_MENU: [RUNTIME_STATE.APPLICATION,RUNTIME_STATE.QUIT],
            RUNTIME_STATE.APPLICATION: [RUNTIME_STATE.MAIN_MENU,RUNTIME_STATE.QUIT]
        }
        
        super().__init__(
                initial_state=RUNTIME_STATE.LOADING,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="RUNTIME_STATE",
                type="RUNTIME"
            )
