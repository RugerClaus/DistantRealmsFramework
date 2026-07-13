from systemlogging import log_state_transition
from core.state.ApplicationLayer.Session.state import ONLINE_SESSION_STATE
from core.state.basestatemanager import BaseStateManager

class OnlineSessionStateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            ONLINE_SESSION_STATE.INACTIVE: [ONLINE_SESSION_STATE.ACTIVE],
            ONLINE_SESSION_STATE.ACTIVE: [ONLINE_SESSION_STATE.INACTIVE],
        }
        super().__init__(
            initial_state=ONLINE_SESSION_STATE.INACTIVE,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="ONLINESESSIONSTATE",
            type="APPLICATION"
        )
