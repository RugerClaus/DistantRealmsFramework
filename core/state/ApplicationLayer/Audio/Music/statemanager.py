from core.state.ApplicationLayer.Audio.Music.state import MUSIC_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class MusicStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            MUSIC_STATE.NONE: [MUSIC_STATE.OFF,MUSIC_STATE.ON],
            MUSIC_STATE.ON: [MUSIC_STATE.OFF],
            MUSIC_STATE.OFF: [MUSIC_STATE.ON],
        }

        super().__init__(
                initial_state=MUSIC_STATE.NONE,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="MUSICSTATE",
                type="SYSTEM"
            )
