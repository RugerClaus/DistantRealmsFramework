from systemlogging import log_state_transition
from core.state.ApplicationLayer.state import APP_STATE
from core.state.basestatemanager import BaseStateManager

class AppStateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            APP_STATE.RUNNING: [APP_STATE.FROZEN,],
            APP_STATE.FROZEN: [APP_STATE.RUNNING],
        }
        super().__init__(
            initial_state=APP_STATE.RUNNING,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="APP_STATE",
            type="APPLICATION"
        )
