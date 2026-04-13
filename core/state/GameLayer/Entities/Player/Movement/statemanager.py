from helper import log_state_transition
from core.state.GameLayer.Entities.Player.Movement.state import PLAYER_MOVE_STATE
from core.state.basestatemanager import BaseStateManager

class PlayerMoveStateManager(BaseStateManager):
    def __init__(self, initial_state=PLAYER_MOVE_STATE.IDLE):
        allowed_transitions = {
            PLAYER_MOVE_STATE.IDLE: [
                PLAYER_MOVE_STATE.MOVE_LEFT,
                PLAYER_MOVE_STATE.MOVE_RIGHT
            ],
            PLAYER_MOVE_STATE.MOVE_LEFT: [
                PLAYER_MOVE_STATE.MOVE_RIGHT,
                PLAYER_MOVE_STATE.IDLE
            ],
            PLAYER_MOVE_STATE.MOVE_RIGHT: [
                PLAYER_MOVE_STATE.MOVE_LEFT,
                PLAYER_MOVE_STATE.IDLE
            ]
        }
        super().__init__(
            initial_state=initial_state,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="MOVESTATE",
            type="GAME"
        )