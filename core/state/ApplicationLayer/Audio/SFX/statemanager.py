from core.state.ApplicationLayer.Audio.SFX.state import SYSTEM_SFX_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class SystemSFXStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            SYSTEM_SFX_STATE.NONE: [SYSTEM_SFX_STATE.OFF,SYSTEM_SFX_STATE.ON],
            SYSTEM_SFX_STATE.ON: [SYSTEM_SFX_STATE.OFF],
            SYSTEM_SFX_STATE.OFF: [SYSTEM_SFX_STATE.ON],
        }

        super().__init__(
                initial_state=SYSTEM_SFX_STATE.NONE,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="SYSTEMSFXSTATE",
                type="SYSTEM"
            )
