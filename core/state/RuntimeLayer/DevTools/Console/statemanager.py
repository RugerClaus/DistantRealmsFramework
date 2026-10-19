from core.state.RuntimeLayer.DevTools.Console.state import CONSOLE_STATE
from core.state.basestatemanager import BaseStateManager
from systemlogging import log_state_transition

class ConsoleStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            CONSOLE_STATE.ON: [CONSOLE_STATE.OFF],
            CONSOLE_STATE.OFF: [CONSOLE_STATE.ON],
        }

        super().__init__(
                initial_state=CONSOLE_STATE.OFF,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="CONSOLE_STATE",
                type="SYSTEM")
