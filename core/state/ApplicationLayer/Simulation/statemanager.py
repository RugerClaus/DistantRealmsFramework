from systemlogging import log_state_transition
from core.state.ApplicationLayer.Simulation.state import SIMULATION_STATE
from core.state.basestatemanager import BaseStateManager

class SimulationStateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            SIMULATION_STATE.ACTIVE: [SIMULATION_STATE.PAUSE],
            SIMULATION_STATE.PAUSE: [SIMULATION_STATE.ACTIVE,SIMULATION_STATE.NONE],
            SIMULATION_STATE.NONE: [SIMULATION_STATE.ACTIVE]
        }
        super().__init__(
            initial_state=SIMULATION_STATE.NONE,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="SIMULATION_STATE",
            type="APPLICATION"
        )
