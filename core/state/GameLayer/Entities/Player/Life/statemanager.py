from helper import log_state_transition
from core.state.GameLayer.Entities.Player.Life.state import PLAYER_LIFE_STATE
from core.state.basestatemanager import BaseStateManager

class PlayerLifeStateManager(BaseStateManager):
    def __init__(self, initial_state=PLAYER_LIFE_STATE.ALIVE):
        allowed_transitions = {
            PLAYER_LIFE_STATE.ALIVE: [
                PLAYER_LIFE_STATE.DEAD
            ],
            PLAYER_LIFE_STATE.DEAD: [
                PLAYER_LIFE_STATE.ALIVE
            ]
        }
        super().__init__(
            initial_state=initial_state,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="PLAYERLIFESTATE",
            type="GAME"
        )
