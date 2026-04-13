from core.ui.font import FontEngine
from core.state.ApplicationLayer.Audio.Interface.state import INTERFACE_SFX_STATE
from core.state.ApplicationLayer.Audio.Music.state import MUSIC_STATE
from core.state.ApplicationLayer.Audio.Game.state import GAME_SFX_STATE

from helper import log_error
class BaseMenu:
    def __init__(self, system):
        self.system = system
        self.font = FontEngine(90).font
        self.query_font = FontEngine(40).font
        self.type_font = FontEngine(25).font
        self.title = None
        self.title_height = self.system.window.get_height() // 6
        self.query = None
        self.button_action_true_color = (128, 0, 200)
        self.button_action_false_color = (128,128,128)

    def update_toggle_buttons(self):
        if self.buttons:
            for button in self.buttons:
                if button.text.startswith("Music:") and self.system.sound is not None:
                    button.set_new_text(f"Music: {'On' if self.system.sound.music_state.is_state(MUSIC_STATE.ON) else 'Off'}")
                elif button.text.startswith("UI SFX:") and self.system.sound is not None:
                    button.set_new_text(f"UI SFX: {'On' if self.system.sound.interface_sfx_state.is_state(INTERFACE_SFX_STATE.ON) else 'Off'}")
                elif button.text.startswith("Music Vol:") and self.system.sound is not None:
                    button.set_new_text(f"Music Vol: {int(self.system.sound.volume*10)}")
                elif button.text.startswith("SFX Vol:") and self.system.sound is not None:
                    button.set_new_text(f"SFX Vol: {int(self.system.sound.sfx_volume*10)}")
                elif button.text.startswith("Game SFX:") and self.system.sound is not None:
                    button.set_new_text(f"Game SFX: {'On' if self.system.sound.game_sfx_state.is_state(GAME_SFX_STATE.ON) else 'Off'}")

    def set_title(self,text):
        if text == None:
            self.title = None
        else:
            self.title = text
    
    def set_title_height(self,divisor):
        self.title_height = self.system.window.get_height() // divisor

    def set_query(self,text):
        if text == None:
            self.query = None
        else:
            self.query = text

    def draw_title(self):
        if self.title is not None:
            text_color = (255, 255, 255)
            surf = self.font.render(self.title, False, text_color)
            rect = surf.get_rect(center=(self.system.window.get_width() // 2, self.title_height))
            self.system.window.blit(surf, rect)
        if self.query is not None:
            text_color = (255, 255, 255)
            surf = self.query_font.render(self.query, False, text_color)
            rect = surf.get_rect(center=(self.system.window.get_width() // 2, self.system.window.get_height() // 4))
            self.system.window.blit(surf, rect)

    def draw_update_text(self):
        text_color = (255, 128,0)
        surf = self.query_font.render("Update Available!", False, text_color)
        rect = surf.get_rect(center=(self.system.window.get_width() // 2, self.system.window.get_height() // 3.5))
        self.system.window.blit(surf, rect)

    def draw_username_text(self,username):
        text_color = (255, 255,255)
        username_color = (50,205,50)
        greeting_surf = self.query_font.render("Hello, ", False, text_color)
        greeting_rect = greeting_surf.get_rect()
        greeting_rect.left = 50
        greeting_rect.centery = 50
        username_surf = self.query_font.render(username,False,username_color)
        username_rect = username_surf.get_rect()
        username_rect.left = greeting_rect.right
        username_rect.centery = greeting_rect.centery
        bang_surf = self.query_font.render("!",False,text_color)
        bang_rect = bang_surf.get_rect()
        bang_rect.left = username_rect.right
        bang_rect.centery = greeting_rect.centery
        self.system.window.blit(username_surf, username_rect)
        self.system.window.blit(greeting_surf, greeting_rect)
        self.system.window.blit(bang_surf,bang_rect)

    def draw_score_text(self,score):
        text_color = (255, 255,255)
        score_color = (50,205,50)
        score_display_surf = self.query_font.render("High Score: ", False, text_color)
        score_display_rect = score_display_surf.get_rect()
        score_surf = self.query_font.render(score,False,score_color)
        score_rect = score_surf.get_rect()
        score_rect.right = self.system.window.get_width() - 50
        score_rect.centery = 50
        score_display_rect.right = score_rect.left
        score_display_rect.centery = score_rect.centery
        self.system.window.blit(score_surf, score_rect)
        self.system.window.blit(score_display_surf, score_display_rect)


    def update(self):
        self.update_toggle_buttons()

    def toggle_ui_sfx(self):
        if not self.system.sound.interface_sfx_state.is_state(INTERFACE_SFX_STATE.NONE):
            if not self.system.sound.interface_sfx_state.is_state(INTERFACE_SFX_STATE.ON):
                self.system.sound.interface_sfx_state.set_state(INTERFACE_SFX_STATE.ON)
            else:
                self.system.sound.interface_sfx_state.set_state(INTERFACE_SFX_STATE.OFF)
            self.update_toggle_buttons()
        else:
            log_error("No audio device found",f"{self.system.sound.interface_sfx_state.get_state()}: unable to enable button sound")
            return
        
    def toggle_game_sfx(self):
        if not self.system.sound.game_sfx_state.is_state(GAME_SFX_STATE.NONE):
            if not self.system.sound.game_sfx_state.is_state(GAME_SFX_STATE.ON):
                self.system.sound.game_sfx_state.set_state(GAME_SFX_STATE.ON)
            else:
                self.system.sound.game_sfx_state.set_state(GAME_SFX_STATE.OFF)
            self.update_toggle_buttons()
        else:
            log_error("No audio device found",f"{self.system.sound.game_sfx_state.get_state()}: unable to enable button sound")
            return
