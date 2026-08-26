from core.state.RuntimeLayer.BootSplash.state import BOOT_SPLASH_STATE
from core.state.RuntimeLayer.BootSplash.statemanager import BootSplashStateManager

from core.ui.widgets.image import Image
from helper import asset

class BootSplashManager:
    def __init__(self,system):
        self.system = system
        self.state = BootSplashStateManager()
        self.splash_one = Image(
            self.system,
            "splash_one",
            "splashpt1",
            position=(0.5, 0.5),
            scale=0.75
        )

        self.splash_two = Image(
            self.system,
            "splash_two",
            "splashpt2",
            position=(0.5, 0.5),
            scale=0.75
        )
        self.splash_one_sfx_played = False
        self.splash_two_sfx_played = False
        self.splash_two_start_time = None
        self.start_time = self.system.time.get_current_time()
        self.state.set_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_ONE)

    def handle_event(self,event,command=None):
        keys = self.system.input.keys
        if event.type == self.system.input.keydown():
            if event.key == keys.space_key() or event.key == keys.return_key() or event.key == keys.escape_key():
                self.system.sound.stop_all_sfx()
                self.state.set_state(BOOT_SPLASH_STATE.NONE)
        if event.type == self.system.input.mouse_button_down() and event.button == 1:
            if self.state.is_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_ONE):
                self.system.sound.stop_all_sfx()
                self.state.set_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_TWO)
            elif self.state.is_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_TWO):
                self.system.clean_up_states([self.state.state])
                self.system.sound.stop_all_sfx()
                self.state.set_state(BOOT_SPLASH_STATE.NONE)

    def scale(self):
        if self.state.is_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_ONE):
            self.splash_one.scale()
        elif self.state.is_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_TWO):
            self.splash_two.scale()

    def update(self):
        if self.state.is_state(BOOT_SPLASH_STATE.NONE):
            self.system.initialize_application()
            return

        if self.state.is_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_TWO):
            pass

    def play_splash_2_fade_in(self):
        current_time = self.system.time.get_current_time()

        if self.splash_two_start_time is None:
            self.splash_two_start_time = current_time

            if not self.splash_two_sfx_played:
                self.system.sound.play_sfx("splash2")
                self.splash_two_sfx_played = True

        el = current_time - self.splash_two_start_time
        du = 9300

        alpha = min((el / du) * 255, 255)

        self.splash_two.set_alpha(alpha)
        self.splash_two.draw()

        if el >= du:
            self.state.set_state(BOOT_SPLASH_STATE.NONE)

    def draw(self):
        current_time = self.system.time.get_current_time()

        if self.state.is_state(
            BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_ONE
        ):
            self.splash_one.draw()

            if not self.splash_one_sfx_played:
                self.system.sound.play_sfx("splash1")
                self.splash_one_sfx_played = True

        if self.state.is_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_ONE) and current_time - self.start_time > 2500:
            self.state.set_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_TWO)


        if self.state.is_state(
            BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_TWO
        ):
            self.play_splash_2_fade_in()