from helper import log_state_transition
from core.state.GameLayer.Debug.Tile.state import TILE_OVERLAY_STATE
from core.state.basestatemanager import BaseStateManager

class TileOverlayStateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            TILE_OVERLAY_STATE.STRUCTURE: [TILE_OVERLAY_STATE.NONE],
            TILE_OVERLAY_STATE.NONE: [TILE_OVERLAY_STATE.STRUCTURE]
        }
        super().__init__(
            initial_state=TILE_OVERLAY_STATE.NONE,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="GAMESTATE",
            type="GAME"
        )
