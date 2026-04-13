from core.state.ApplicationLayer.Menu.Pause.state import PAUSE_MENU_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class PauseMenuStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            PAUSE_MENU_STATE.ROOT: [PAUSE_MENU_STATE.SETTINGS,PAUSE_MENU_STATE.CREDITS],
            PAUSE_MENU_STATE.SETTINGS: [PAUSE_MENU_STATE.ROOT,PAUSE_MENU_STATE.AUDIO],
            PAUSE_MENU_STATE.AUDIO: [PAUSE_MENU_STATE.SETTINGS, PAUSE_MENU_STATE.ROOT],
            PAUSE_MENU_STATE.CREDITS: [PAUSE_MENU_STATE.ROOT]

        }

        super().__init__(
                initial_state=PAUSE_MENU_STATE.ROOT,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="PAUSE_MENU_STATE",
                type="GAME"
            )
