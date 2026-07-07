from core.state.ApplicationLayer.DevTools.Debug.state import DEBUG_OVERLAY_STATE
from core.state.basestatemanager import BaseStateManager
from systemlogging import log_state_transition

class DebugStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            DEBUG_OVERLAY_STATE.OFF: [DEBUG_OVERLAY_STATE.ON],
            DEBUG_OVERLAY_STATE.ON: [DEBUG_OVERLAY_STATE.OFF]
        }

        super().__init__(
                initial_state=DEBUG_OVERLAY_STATE.OFF,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="DEBUGSTATE",
                type="SYSTEM"
            )
