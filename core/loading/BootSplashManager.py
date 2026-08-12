from core.state.RuntimeLayer.state import RUNTIME_STATE
from core.state.RuntimeLayer.BootSplash.state import BOOT_SPLASH_STATE
from core.state.RuntimeLayer.BootSplash.statemanager import BootSplashStateManager
from core.state.RuntimeLayer.Audio.SFX.state import SYSTEM_SFX_STATE
from core.application.entities.entitymanager import EntityManager
from helper import asset

class BootSplashManager:
    def __init__(self,system):
        self.system = system
        self.state = BootSplashStateManager()
        self.entitymanager = EntityManager(self.system)
        self.splash_one_original = self.system.window.load_image(asset("splashpt1")).convert_alpha()
        self.splash_one = self.splash_one_original
        self.splash_one_rect = self.splash_one.get_rect(center=(self.system.window.get_width()//2,self.system.window.get_height()//2))
        self.splash_two_original = self.system.window.load_image(asset("splashpt2")).convert_alpha()
        self.splash_two = self.splash_two_original
        self.splash_two_rect = self.splash_two.get_rect(center=(self.system.window.get_width()//2,self.system.window.get_height()//2))
        self.splash_one_sfx_played = False
        self.splash_two_sfx_played = False
        self.splash_two_start_time = None
        self.start_time = self.system.time.get_current_time()
        self.state.set_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_ONE)

    def rescale_assets(self):
        window_w, window_h = self.system.window.get_size()
        self.splash_one_rect = self.splash_one.get_rect(center=(window_w // 2, window_h // 2 - 50))
        self.splash_two_rect = self.splash_two.get_rect(center=(window_w // 2, window_h // 2 - 50))

    def update(self):
        if self.state.is_state(BOOT_SPLASH_STATE.NONE):
            self.system.runtime_state.set_state(RUNTIME_STATE.APPLICATION)
        if not self.system.runtime_state.is_state(RUNTIME_STATE.SPLASH):

            self.system.sound.system_sfx_state.set_state(SYSTEM_SFX_STATE.OFF)
        
        if self.state.is_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_TWO):
            self.entitymanager.update_entities()
            # spawn entities here (self.entitymanager.spawn_x_entities())

    def play_splash_2_fade_in(self):
        current_time = self.system.time.get_current_time()
        
        if self.splash_two_start_time is None:
            self.splash_two_start_time = current_time
            if not self.splash_two_sfx_played:
                self.system.sound.play_sfx("splash2")
                self.splash_two_sfx_played = True
                
        el = current_time - self.splash_two_start_time
        du = 9300
        alpha = (el / du) * 255
        if alpha > 255:
            alpha = 255
        
        self.splash_two.set_alpha(alpha)

        self.system.window.blit(self.splash_two,self.splash_two_rect)

        if el >= du:
            self.state.set_state(BOOT_SPLASH_STATE.NONE)
            self.system.initialize_application()

    def draw(self):
        current_time = self.system.time.get_current_time()
        if self.state.is_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_ONE):
            self.system.window.blit(self.splash_one, self.splash_one_rect)

            if not self.splash_one_sfx_played:
                self.system.sound.play_sfx("splash1")
                self.splash_one_sfx_played = True
        if current_time - self.start_time > 2500:
            self.state.set_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_TWO)
        if self.state.is_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_TWO):
            
            self.play_splash_2_fade_in()  
            self.entitymanager.draw_entities()  