from core.state.ApplicationLayer.NetworkLayer.Loading.state import FETCH_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class FetchStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            FETCH_STATE.IDLE: [FETCH_STATE.FETCHING,FETCH_STATE.CANCELLED],
            FETCH_STATE.FETCHING: [FETCH_STATE.ERROR, FETCH_STATE.SUCCESS,FETCH_STATE.TIMEOUT],
            FETCH_STATE.ERROR: [FETCH_STATE.IDLE],
            FETCH_STATE.SUCCESS: [FETCH_STATE.IDLE],
            FETCH_STATE.TIMEOUT: [FETCH_STATE.IDLE],
            FETCH_STATE.CANCELLED: [FETCH_STATE.IDLE]
        }
        
        super().__init__(
                initial_state=FETCH_STATE.IDLE,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="FETCHSTATE",
                type="SYSTEM"
            )
