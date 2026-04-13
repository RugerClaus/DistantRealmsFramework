from core.state.ApplicationLayer.dev import DEVELOPER_MODE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class DevManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            DEVELOPER_MODE.ON: [DEVELOPER_MODE.OFF],
            DEVELOPER_MODE.OFF: [DEVELOPER_MODE.ON],
        }

        super().__init__(
                initial_state=DEVELOPER_MODE.OFF,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="DEVELOPER_MODE",
                type="SYSTEM"
            )
