from core.state.RuntimeLayer.BootSplash.state import BOOT_SPLASH_STATE
from core.state.basestatemanager import BaseStateManager
from systemlogging import log_state_transition

class BootSplashStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            BOOT_SPLASH_STATE.NONE: [BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_ONE],
            BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_ONE: [BOOT_SPLASH_STATE.NONE,BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_TWO],
            BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_TWO: [BOOT_SPLASH_STATE.NONE,BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_THREE],
            BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_THREE: [BOOT_SPLASH_STATE.NONE,BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_FOUR],
            BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_FOUR: [BOOT_SPLASH_STATE.NONE,BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_FIVE],
            BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_FIVE: [BOOT_SPLASH_STATE.NONE],
        }

        super().__init__(
                initial_state=BOOT_SPLASH_STATE.NONE,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="BOOTSPLASHSCREENSTATE",
                type="RUNTIME"
            )
