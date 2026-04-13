from core.state.ApplicationLayer.NetworkLayer.Update.state import UPDATE_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class UpdateStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            UPDATE_STATE.AVAILABLE: [UPDATE_STATE.CURRENT],
            UPDATE_STATE.CURRENT: [UPDATE_STATE.AVAILABLE]
        }
        
        super().__init__(
                initial_state=UPDATE_STATE.CURRENT,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="UPDATESTATE",
                type="SYSTEM"
            )
