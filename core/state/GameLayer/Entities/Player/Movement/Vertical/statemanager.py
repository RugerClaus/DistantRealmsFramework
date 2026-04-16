from helper import log_state_transition
from core.state.GameLayer.Entities.Player.Movement.Vertical.state import PLAYER_MOVE_VERT_STATE
from core.state.basestatemanager import BaseStateManager

class PlayerVerticalMoveStateManager(BaseStateManager):
    def __init__(self, initial_state=PLAYER_MOVE_VERT_STATE.NONE):
        allowed_transitions = {
            PLAYER_MOVE_VERT_STATE.NONE: [
                PLAYER_MOVE_VERT_STATE.MOVE_UP,
                PLAYER_MOVE_VERT_STATE.MOVE_DOWN
            ],
            PLAYER_MOVE_VERT_STATE.MOVE_UP: [
                PLAYER_MOVE_VERT_STATE.MOVE_DOWN,
                PLAYER_MOVE_VERT_STATE.NONE
            ],
            PLAYER_MOVE_VERT_STATE.MOVE_DOWN: [
                PLAYER_MOVE_VERT_STATE.MOVE_UP,
                PLAYER_MOVE_VERT_STATE.NONE
            ]
        }
        super().__init__(
            initial_state=initial_state,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="MOVESTATE",
            type="GAME"
        )