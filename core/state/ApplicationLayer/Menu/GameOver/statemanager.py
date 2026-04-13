from core.state.ApplicationLayer.Menu.GameOver.state import GAME_OVER_MENU_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class GameOverMenuStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            GAME_OVER_MENU_STATE.BASE: [GAME_OVER_MENU_STATE.HIGHSCORE],
            GAME_OVER_MENU_STATE.HIGHSCORE: [GAME_OVER_MENU_STATE.BASE]

        }

        super().__init__(
                initial_state=GAME_OVER_MENU_STATE.BASE,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="GAMEOVERMENUSTATE",
                type="GAME"
            )
