from core.state.ApplicationLayer.NetworkLayer.Patch.state import PATCH_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class PatchStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            PATCH_STATE.AVAILABLE: [PATCH_STATE.CURRENT],
            PATCH_STATE.CURRENT: [PATCH_STATE.AVAILABLE]
        }
        
        super().__init__(
                initial_state=PATCH_STATE.CURRENT,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="PATCHSTATE",
                type="SYSTEM"
            )
