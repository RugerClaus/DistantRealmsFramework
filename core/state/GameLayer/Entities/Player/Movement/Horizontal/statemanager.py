from helper import log_state_transition
from core.state.GameLayer.Entities.Player.Movement.Horizontal.state import PLAYER_MOVE_HORZ_STATE
from core.state.basestatemanager import BaseStateManager

class PlayerHorizontalMoveStateManager(BaseStateManager):
    def __init__(self, initial_state=PLAYER_MOVE_HORZ_STATE.NONE):
        allowed_transitions = {
            PLAYER_MOVE_HORZ_STATE.NONE: [
                PLAYER_MOVE_HORZ_STATE.MOVE_LEFT,
                PLAYER_MOVE_HORZ_STATE.MOVE_RIGHT
            ],
            PLAYER_MOVE_HORZ_STATE.MOVE_LEFT: [
                PLAYER_MOVE_HORZ_STATE.MOVE_RIGHT,
                PLAYER_MOVE_HORZ_STATE.NONE
            ],
            PLAYER_MOVE_HORZ_STATE.MOVE_RIGHT: [
                PLAYER_MOVE_HORZ_STATE.MOVE_LEFT,
                PLAYER_MOVE_HORZ_STATE.NONE
            ]
        }
        super().__init__(
            initial_state=initial_state,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="MOVESTATE",
            type="GAME"
        )