from core.state.ApplicationLayer.Debug.state import DEBUG_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class DebugStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            DEBUG_STATE.OFF: [DEBUG_STATE.ON],
            DEBUG_STATE.ON: [DEBUG_STATE.OFF]
        }

        super().__init__(
                initial_state=DEBUG_STATE.OFF,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="DEBUGSTATE",
                type="SYSTEM"
            )
