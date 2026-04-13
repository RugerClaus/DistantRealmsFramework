from core.state.ApplicationLayer.Audio.Interface.state import INTERFACE_SFX_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class InterfaceSFXStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            INTERFACE_SFX_STATE.NONE: [INTERFACE_SFX_STATE.OFF,INTERFACE_SFX_STATE.ON],
            INTERFACE_SFX_STATE.ON: [INTERFACE_SFX_STATE.OFF],
            INTERFACE_SFX_STATE.OFF: [INTERFACE_SFX_STATE.ON],
        }

        super().__init__(
                initial_state=INTERFACE_SFX_STATE.NONE,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="INTERFACESFXSTATE",
                type="SYSTEM"
            )
