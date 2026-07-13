from core.state.RuntimeLayer.UI.Button.state import BUTTON_STATE
from core.state.basestatemanager import BaseStateManager
from systemlogging import log_state_transition

class ButtonStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            BUTTON_STATE.IDLE: [BUTTON_STATE.HOVER,BUTTON_STATE.FOCUSED,BUTTON_STATE.DISABLE],
            BUTTON_STATE.HOVER: [BUTTON_STATE.IDLE,BUTTON_STATE.PRESS,
            BUTTON_STATE.FOCUSED,BUTTON_STATE.DISABLE],
            BUTTON_STATE.FOCUSED: [BUTTON_STATE.IDLE,BUTTON_STATE.PRESS,BUTTON_STATE.DISABLE],
            BUTTON_STATE.PRESS: [BUTTON_STATE.HOVER,BUTTON_STATE.FOCUSED,BUTTON_STATE.IDLE],
            BUTTON_STATE.DISABLE: [BUTTON_STATE.IDLE]
        }

        super().__init__(
                initial_state=BUTTON_STATE.IDLE,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="BUTTON_STATE",
                type="RUNTIME"
            )
