from core.state.ApplicationLayer.Audio.Game.state import GAME_SFX_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class GameSFXStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            GAME_SFX_STATE.NONE: [GAME_SFX_STATE.OFF,GAME_SFX_STATE.ON],
            GAME_SFX_STATE.ON: [GAME_SFX_STATE.OFF],
            GAME_SFX_STATE.OFF: [GAME_SFX_STATE.ON],
        }

        super().__init__(
                initial_state=GAME_SFX_STATE.NONE,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="GAMESFXSTATE",
                type="SYSTEM"
            )
