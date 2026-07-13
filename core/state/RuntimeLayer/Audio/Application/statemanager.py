from core.state.RuntimeLayer.Audio.Application.state import APP_SFX_STATE
from core.state.basestatemanager import BaseStateManager
from systemlogging import log_state_transition

class AppSFXStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            APP_SFX_STATE.NONE: [APP_SFX_STATE.OFF,APP_SFX_STATE.ON],
            APP_SFX_STATE.ON: [APP_SFX_STATE.OFF],
            APP_SFX_STATE.OFF: [APP_SFX_STATE.ON],
        }

        super().__init__(
                initial_state=APP_SFX_STATE.NONE,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="GAMESFXSTATE",
                type="SYSTEM"
            )
