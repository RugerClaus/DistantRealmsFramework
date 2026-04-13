from core.state.ApplicationLayer.Debug.StateMonitor.state import MONITOR_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class StateMonitorStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            MONITOR_STATE.SYSTEM: [MONITOR_STATE.APPLICATION,MONITOR_STATE.GAME,MONITOR_STATE.ALL],
            MONITOR_STATE.APPLICATION: [MONITOR_STATE.SYSTEM,MONITOR_STATE.GAME,MONITOR_STATE.ALL],
            MONITOR_STATE.GAME: [MONITOR_STATE.APPLICATION,MONITOR_STATE.SYSTEM,MONITOR_STATE.ALL],
            MONITOR_STATE.ALL: [MONITOR_STATE.APPLICATION,MONITOR_STATE.SYSTEM,MONITOR_STATE.GAME]
        }

        super().__init__(
                initial_state=MONITOR_STATE.SYSTEM,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="STATEMONITORSTATE",
                type="SYSTEM"
            )
