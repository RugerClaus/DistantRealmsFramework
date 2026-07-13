from core.state.RuntimeLayer.DevTools.StateMonitor.state import MONITOR_STATE
from core.state.basestatemanager import BaseStateManager
from systemlogging import log_state_transition

class StateMonitorStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            MONITOR_STATE.SYSTEM: [MONITOR_STATE.RUNTIME,MONITOR_STATE.APPLICATION,MONITOR_STATE.ALL],
            MONITOR_STATE.RUNTIME: [MONITOR_STATE.SYSTEM,MONITOR_STATE.APPLICATION,MONITOR_STATE.ALL],
            MONITOR_STATE.APPLICATION: [MONITOR_STATE.RUNTIME,MONITOR_STATE.SYSTEM,MONITOR_STATE.ALL],
            MONITOR_STATE.ALL: [MONITOR_STATE.RUNTIME,MONITOR_STATE.SYSTEM,MONITOR_STATE.APPLICATION]
        }

        super().__init__(
                initial_state=MONITOR_STATE.ALL,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="STATEMONITORSTATE",
                type="SYSTEM"
            )
