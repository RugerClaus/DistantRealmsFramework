from core.state.ApplicationLayer.Menu.state import MENUSTATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class MenuStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            MENUSTATE.CREATEUSERNAME: [MENUSTATE.ROOT,MENUSTATE.CHANGELOG],
            MENUSTATE.ROOT: [MENUSTATE.SETTINGS,MENUSTATE.CREDITS,MENUSTATE.CHANGELOG,MENUSTATE.CREATEUSERNAME],
            MENUSTATE.SETTINGS: [MENUSTATE.ROOT,MENUSTATE.AUDIO,MENUSTATE.DEVELOPERSETTINGS],
            MENUSTATE.DEVELOPERSETTINGS: [MENUSTATE.SETTINGS,MENUSTATE.CREATEUSERNAME],
            MENUSTATE.AUDIO: [MENUSTATE.SETTINGS],
            MENUSTATE.CREDITS: [MENUSTATE.ROOT],
            MENUSTATE.CHANGELOG: [MENUSTATE.ROOT,MENUSTATE.CREATEUSERNAME]

        }

        super().__init__(
                initial_state=MENUSTATE.ROOT,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="MENUSTATE",
                type="APPLICATION"
            )
