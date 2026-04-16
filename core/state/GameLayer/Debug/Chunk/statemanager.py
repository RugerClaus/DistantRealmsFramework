from helper import log_state_transition
from core.state.GameLayer.Debug.Chunk.state import CHUNK_BORDER_STATE
from core.state.basestatemanager import BaseStateManager

class ChunkBorderStateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            CHUNK_BORDER_STATE.ON: [CHUNK_BORDER_STATE.OFF],
            CHUNK_BORDER_STATE.OFF: [CHUNK_BORDER_STATE.ON]
        }
        super().__init__(
            initial_state=CHUNK_BORDER_STATE.OFF,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="GAMESTATE",
            type="GAME"
        )
