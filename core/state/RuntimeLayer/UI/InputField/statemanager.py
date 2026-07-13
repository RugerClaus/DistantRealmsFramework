from core.state.RuntimeLayer.UI.InputField.state import INPUT_FIELD_STATE
from core.state.basestatemanager import BaseStateManager
from systemlogging import log_state_transition

class InputFieldStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            INPUT_FIELD_STATE.ACTIVE: [INPUT_FIELD_STATE.INACTIVE],
            INPUT_FIELD_STATE.INACTIVE: [INPUT_FIELD_STATE.ACTIVE],
        }

        super().__init__(
                initial_state=INPUT_FIELD_STATE.INACTIVE,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="INPUT_FIELD_STATE",
                type="RUNTIME"
            )
