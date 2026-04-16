import webbrowser
from core.menus.basemenu import BaseMenu
from core.menus.usercreator import UserCreator
from core.ui.button import Button
from helper import *
from core.state.ApplicationLayer.Audio.Music.state import MUSIC_STATE
from core.state.ApplicationLayer.dev import DEVELOPER_MODE
from core.state.ApplicationLayer.Menu.state import MENUSTATE
from core.state.ApplicationLayer.Menu.statemanager import MenuStateManager
from core.menus.credits import Credits
from core.network.update import Update
from core.state.ApplicationLayer.NetworkLayer.Update.state import UPDATE_STATE

from core.menus.changelog import ChangeLog

class Menu(BaseMenu):
    def __init__(self,system, game):
        self.system = system
        self.game = game
        super().__init__(system)
        self.state = MenuStateManager()
        self.credits = Credits(system)
        self.user_creator = UserCreator(system)
        self.username_exists = check_username()
        self.recently_updated = check_recently_updated() # checks for if a file exists containing the recentlyupdated boolean
        self.updater = Update()
        self.change_log = ChangeLog(system)

        self.title_image_original = self.system.window.load_image(asset("title"))
        self.title_image = self.title_image_original
        self.title_rect = self.title_image.get_rect()
        
        recently_updated_file = self.system.load.read_environment_variable('recentlyupdated')
        if self.state.is_state(MENUSTATE.ROOT):
            if self.recently_updated:
                if recently_updated_file == "false":
                    self.state.set_state(MENUSTATE.ROOT)
                    if not self.username_exists:
                        self.state.set_state(MENUSTATE.CREATEUSERNAME)
                        self.create_buttons()
                    else:
                        self.state.set_state(MENUSTATE.ROOT)
                        self.create_buttons()
                if recently_updated_file == "true":
                    self.state.set_state(MENUSTATE.CHANGELOG)
                    self.create_buttons()

        self.create_buttons()
        self.rescale_assets()
        

    def rescale_assets(self):
        window_w, window_h = self.system.window.get_size()
        new_title_width = int(window_w * 0.5)
        scale_factor = new_title_width / self.title_image_original.get_width()
        new_title_height = int(self.title_image_original.get_height() * scale_factor)
        self.title_image = self.system.window.transform_scale(self.title_image_original, new_title_width, new_title_height)
        self.title_rect = self.title_image.get_rect(center=(window_w // 2, int(window_h * 0.2)))
        self.credits.rescale()

    def create_buttons(self):
        
        window_w, window_h = self.system.window.get_size()
        btn_width, btn_height = window_w // 3.6, 70
        spacing = btn_height * 1.2
        start_y = window_h // 4 + window_h // 7
        center_x = window_w // 2
        

        if self.state.is_state(MENUSTATE.ROOT) and self.updater.state.is_state(UPDATE_STATE.CURRENT):
            self.buttons = [
                Button(self.system.sound, self.system.window, "New Game", center_x, start_y, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, None,False),
                Button(self.system.sound, self.system.window, "Continue", center_x, start_y + spacing, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, None,False),
                Button(self.system.sound, self.system.window, "Load Game", center_x, start_y + spacing * 2, btn_width, btn_height,
                    (255, 255, 255), self.button_action_false_color, None,False),
                Button(self.system.sound, self.system.window, "Settings", center_x, start_y + spacing * 3, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.go_to_settings),
                Button(self.system.sound, self.system.window, "Quit", center_x, start_y + spacing * 4, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.system.quit),
                Button(self.system.sound, self.system.window, "Credits", window_w - window_w // 8, window_h - 100, 200, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.credits_callback),
            ]
        if self.state.is_state(MENUSTATE.ROOT) and self.updater.state.is_state(UPDATE_STATE.AVAILABLE):
            self.buttons = [
                Button(self.system.sound, self.system.window, "New Game", center_x, start_y, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, None,False),
                Button(self.system.sound, self.system.window, "Continue", center_x, start_y + spacing, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, None,False),
                Button(self.system.sound, self.system.window, "Load Game", center_x, start_y + spacing * 2, btn_width, btn_height,
                    (255, 255, 255), self.button_action_false_color, None,False),
                Button(self.system.sound, self.system.window, "Settings", center_x, start_y + spacing * 3, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.go_to_settings),
                Button(self.system.sound, self.system.window, "Quit", center_x, start_y + spacing * 4, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.system.quit),
                Button(self.system.sound, self.system.window, "Update!", window_w - window_w // 8, window_h - 300, 220, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.updater.start, True, (255, 165, 0)),
                Button(self.system.sound, self.system.window, "Credits", window_w - window_w // 8, window_h - 100, 200, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.credits_callback),
            ]
        elif self.state.is_state(MENUSTATE.SETTINGS):
            if self.system.control_state.is_state(DEVELOPER_MODE.ON):
                self.buttons = [
                    Button(self.system.sound, self.system.window, f"Audio", center_x, start_y, btn_width, btn_height, (255, 255, 255), self.button_action_true_color, self.audio_settings),
                    Button(self.system.sound, self.system.window, f"Developer Settings", center_x, start_y + spacing * 1, btn_width * 2, btn_height, (255, 255, 255), self.button_action_true_color, self.developer_settings),
                    Button(self.system.sound, self.system.window, "Back", center_x, start_y + spacing * 2, btn_width, btn_height,
                        (255, 255, 255), self.button_action_true_color, self.back_to_root),
                ]
            else:
                self.buttons = [
                    Button(self.system.sound, self.system.window, f"Audio", center_x, start_y, btn_width, btn_height, (255, 255, 255), self.button_action_true_color, self.audio_settings),
                    Button(self.system.sound, self.system.window, "Back", center_x, start_y + spacing * 1, btn_width, btn_height,
                        (255, 255, 255), self.button_action_true_color, self.back_to_root),
                ]
        elif self.state.is_state(MENUSTATE.CREDITS):

            self.buttons = [
                Button(self.system.sound, self.system.window, "Back", window_w - window_w // 8, window_h - 100, 150, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.back_to_root),
            ]
        elif self.state.is_state(MENUSTATE.CHANGELOG):

            self.buttons = [
                Button(self.system.sound, self.system.window, "Go To Menu", window_w - window_w // 8 - 50, window_h - 100, 300, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.back_to_root_changelog),
            ]
            
        elif self.state.is_state(MENUSTATE.AUDIO):
            self.buttons = [
                Button(self.system.sound, self.system.window, f"-", center_x - 200, self.system.window.get_height() // 2 - spacing, 50, btn_height, (255, 255, 255), self.button_action_true_color, self.system.sound.volume_down),
                Button(self.system.sound, self.system.window, f"Music Vol: {int(self.system.sound.volume*10)}", center_x, self.system.window.get_height() // 2 - spacing, 0, btn_height, (255, 255, 255), (255,255,255), None,False),
                Button(self.system.sound, self.system.window, f"+", center_x + 200, self.system.window.get_height() // 2 - spacing, 50, btn_height, (255, 255, 255), self.button_action_true_color, self.system.sound.volume_up),
                
                Button(self.system.sound, self.system.window, f"-", center_x - 200, self.system.window.get_height() // 2 + spacing * 0.01, 50, btn_height, (255, 255, 255), self.button_action_true_color, self.system.sound.sfx_volume_down),
                Button(self.system.sound, self.system.window, f"SFX Vol: {int(self.system.sound.sfx_volume*10)}", center_x, self.system.window.get_height() // 2 + spacing * 0.01, 0, btn_height, (255, 255, 255), (255,255,255), None,False),
                Button(self.system.sound, self.system.window, f"+", center_x + 200, self.system.window.get_height() // 2 + spacing * 0.01, 50, btn_height, (255, 255, 255), self.button_action_true_color, self.system.sound.sfx_volume_up),
                
                Button(self.system.sound, self.system.window, f"Music:", center_x, self.system.window.get_height() // 2 + spacing * 1, 240, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.system.sound.toggle_music),
                Button(self.system.sound, self.system.window, f"UI SFX:", center_x, self.system.window.get_height() // 2 + spacing * 2, 240, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.toggle_ui_sfx),
                Button(self.system.sound, self.system.window, f"Game SFX:", center_x, self.system.window.get_height() // 2 + spacing * 3, 340, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.toggle_game_sfx),
                Button(self.system.sound, self.system.window, "Back", center_x, self.system.window.get_height() // 2 + spacing * 4, 150, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.go_to_settings)
            ]
        elif self.state.is_state(MENUSTATE.CREATEUSERNAME):
            self.buttons = [
                Button(self.system.sound, self.system.window, f"Submit", center_x, self.system.window.get_height() // 2 + spacing * 0.4, btn_width, btn_height, (255, 255, 255), self.button_action_true_color, self.submit_username),
                Button(self.system.sound, self.system.window, f"Back", center_x, self.system.window.get_height() // 2 + spacing * 1.4, btn_width, btn_height, (255, 255, 255), self.button_action_true_color, self.back_to_root),
            ]
        elif self.state.is_state(MENUSTATE.DEVELOPERSETTINGS):
            self.buttons = [
                Button(self.system.sound, self.system.window, "Reset Username", center_x, self.system.window.get_height() // 2 - spacing, btn_width + 50, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.reset_username),
                Button(self.system.sound, self.system.window, "Back", center_x, self.system.window.get_height() // 2 + spacing, 150, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.go_to_settings),
            ]

    def back_to_root_changelog(self):
        if self.system.control_state.is_state(DEVELOPER_MODE.ON):
            self.system.save.write_environment_variable('recentlyupdated', 'true')
        else:
            self.system.save.write_environment_variable('recentlyupdated', 'false')
        self.state.set_state(MENUSTATE.ROOT)
        self.create_buttons()

    def developer_settings(self):
        self.state.set_state(MENUSTATE.DEVELOPERSETTINGS)
        self.create_buttons()

    def reset_username(self):
        self.state.set_state(MENUSTATE.CREATEUSERNAME)
        self.create_buttons()

    def submit_username(self):
        username = self.user_creator.text_box.get_return_string()
        if len(username) > 5:
            self.user_creator.submit()
            self.set_query(None)
            self.state.set_state(MENUSTATE.ROOT)
            self.create_buttons()
        else:
            self.set_query("Username must be at least 6 characters")

    def credits_callback(self):
        self.state.set_state(MENUSTATE.CREDITS)
        self.create_buttons()

    def audio_settings(self):
        self.state.set_state(MENUSTATE.AUDIO)
        self.create_buttons()

    def back_to_root(self):
        self.state.set_state(MENUSTATE.ROOT)
        self.set_query("")
        self.create_buttons()
    
    def go_to_settings(self):
        self.state.set_state(MENUSTATE.SETTINGS)
        self.create_buttons()

    def handle_event(self, event):
        if event.type == self.system.input.mouse_button_down() and event.button == 1:
            mouse_pos = self.system.input.get_mouse_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)
        elif event.type == self.system.input.video_resize_event():
            self.scale()
        self.user_creator.handle_event(event)
        if self.state.is_state(MENUSTATE.CREATEUSERNAME):
            keys = self.system.input.get_pressed_keys()
            if keys[self.system.input.keys.return_key()]:
                self.submit_username()

    def scale(self):
        self.rescale_assets()
        self.create_buttons()

    def draw(self):
        if self.system.sound.current_track is None and self.system.sound.music_state.is_state(MUSIC_STATE.ON):
            self.system.sound.play_music()
        
        t = self.system.window.get_current_time() / 1000
        pulse = (self.system.math.sin(t) + 1) / 2
        fade_color = (
            int(20 + (35 - 20) * pulse),
            0,
            int(20 + (35 - 20) * pulse)
        )
        self.system.window.fill(fade_color)

        mouse_pos = self.system.input.get_mouse_pos()
        for button in self.buttons:
            button.draw(mouse_pos)

        if self.state.is_state(MENUSTATE.CREATEUSERNAME):
            self.set_title(None)
            self.set_query("Please enter a username: ")
            self.user_creator.draw()

        if self.state.is_state(MENUSTATE.ROOT) and self.updater.state.is_state(UPDATE_STATE.CURRENT):
            self.set_title("")
            self.draw_username_text(self.system.load.read_constant("username"))
            self.system.window.blit(self.title_image, self.title_rect)
        
        if self.state.is_state(MENUSTATE.ROOT) and self.updater.state.is_state(UPDATE_STATE.AVAILABLE):
            self.set_title("")
            self.draw_update_text()
            self.draw_username_text(self.system.load.read_constant("username"))
            self.draw_score_text(f"{read_constant_from_file('high_score')}")
            self.system.window.blit(self.title_image, self.title_rect)

        if self.state.is_state(MENUSTATE.SETTINGS):
            self.set_title("SETTINGS")
        
        if self.state.is_state(MENUSTATE.DEVELOPERSETTINGS):
            self.set_title('DEVELOPER SETTINGS')

        if self.state.is_state(MENUSTATE.CREDITS):
            self.set_title("CREDITS:")
            self.credits.draw()

        if self.state.is_state(MENUSTATE.CHANGELOG):
            self.set_title("CHANGELOG:")
            self.change_log.draw()

        if self.state.is_state(MENUSTATE.AUDIO):
            self.set_title("AUDIO SETTINGS")

        self.draw_title()