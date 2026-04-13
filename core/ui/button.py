from core.ui.font import FontEngine

from core.state.ApplicationLayer.Audio.Interface.state import INTERFACE_SFX_STATE

class Button:
    def __init__(self, sound, window, text, x, y, width, height, text_unhovered_color, text_hovered_color, action=None,active=True,background_color=None):
        self.sound = sound
        self.window = window
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = FontEngine("button").font
        self.action = action
        self.active = active
        self.text_unhovered_color = text_unhovered_color
        self.text_hovered_color = text_hovered_color
        
        if background_color is None:
            self.color = (0, 0, 0)
        else:
            self.color = background_color

        self.surface = self.window.make_surface(self.width, self.height,True)
        self.rect = self.surface.get_rect()
        self.hover_sound_played = False

    def draw(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            text_color = self.text_hovered_color
            if not self.hover_sound_played:
                self.sound.play_ui_sfx('button_hover')
                self.hover_sound_played = True
        else:
            text_color = self.text_unhovered_color
            self.hover_sound_played = False

        self.text_surface = self.font.render(self.text, True, text_color)
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.window.draw_rect(self.surface, self.color, self.surface.get_rect(), border_radius=8)
        self.window.draw_rect(self.surface, (255, 0, 0), self.surface.get_rect(), width=2, border_radius=8)
        self.window.blit(self.surface, self.rect.topleft)
        self.window.blit(self.text_surface, self.text_rect)

        

    def is_clicked(self, mouse_pos, mouse_click):
        
        if self.active and self.rect.collidepoint(mouse_pos) and mouse_click:
            if self.action:
                if self.sound.interface_sfx_state.is_state(INTERFACE_SFX_STATE.ON):
                    self.sound.play_ui_sfx('button_clicked')
                else:
                    print(f'interface sfx is disabled.{self.sound.interface_sfx_state.get_state()}')
                self.action()
            if not self.action:
                self.action = None

    def get_text_height(self):
        return self.text_rect.height
    
    def set_new_text(self,new_text):
        self.text = new_text
        self.text_surface = self.font.render(self.text, True, self.text_unhovered_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)