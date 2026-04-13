from helper import log_state_transition
from core.state.GameLayer.Entities.Player.Speed.state import SPEED_STATE
from core.state.basestatemanager import BaseStateManager

class SpeedStateManager(BaseStateManager):
    def __init__(self, initial_state=SPEED_STATE.NORMAL):
        allowed_transitions = {
            SPEED_STATE.NORMAL: 
            [
                SPEED_STATE.SLOW,SPEED_STATE.FAST
            ],
            SPEED_STATE.SLOW: 
            [
                SPEED_STATE.NORMAL
            ],
            SPEED_STATE.FAST: 
            [
                SPEED_STATE.NORMAL
            ]
        }
        super().__init__(
            initial_state=initial_state,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="PLAYERLIFESTATE",
            type="GAME"
        )
