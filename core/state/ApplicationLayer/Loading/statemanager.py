from core.state.ApplicationLayer.Loading.state import LOAD_SCREEN_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class LoadingStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            LOAD_SCREEN_STATE.NONE: [LOAD_SCREEN_STATE.STUDIO_SPLASH_SCREEN_ONE,LOAD_SCREEN_STATE.STUDIO_SPLASH_SCREEN_TWO],
            LOAD_SCREEN_STATE.STUDIO_SPLASH_SCREEN_ONE: [LOAD_SCREEN_STATE.NONE,LOAD_SCREEN_STATE.STUDIO_SPLASH_SCREEN_TWO],
            LOAD_SCREEN_STATE.STUDIO_SPLASH_SCREEN_TWO: [LOAD_SCREEN_STATE.NONE]
        }

        super().__init__(
                initial_state=LOAD_SCREEN_STATE.NONE,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="LOADSCREENSTATE",
                type="APPLICATION"
            )
