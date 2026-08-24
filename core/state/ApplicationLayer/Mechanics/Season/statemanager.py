from systemlogging import log_state_transition
from core.state.ApplicationLayer.Mechanics.Season.state import SEASON_STATE
from core.state.basestatemanager import BaseStateManager

class SeasonStateManager(BaseStateManager):
    def __init__(self, initial_state=SEASON_STATE.WINTER):
        allowed_transitions = {
            SEASON_STATE.WINTER: [SEASON_STATE.SPRING],
            SEASON_STATE.SPRING: [SEASON_STATE.SUMMER],
            SEASON_STATE.SUMMER: [SEASON_STATE.AUTUMN],
            SEASON_STATE.AUTUMN: [SEASON_STATE.WINTER]
        }
        super().__init__(
            initial_state=initial_state,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="SEASONSTATE",
            type="APPLICATION"
        )
