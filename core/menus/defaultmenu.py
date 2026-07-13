import webbrowser
from helper import asset
from core.menus.basemenu import BaseMenu
from core.ui.newbutton import Button
from core.state.RuntimeLayer.Menu.statemanager import MenuStateManager
from core.state.RuntimeLayer.Menu.state import MENUSTATE
from core.state.RuntimeLayer.NetworkLayer.Update.state import UPDATE_STATE
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.state.RuntimeLayer.NetworkLayer.Loading.state import FETCH_STATE
from core.state.RuntimeLayer.Audio.Music.state import MUSIC_STATE
from core.menus.usercreator import UserCreator
from core.menus.changelog import ChangeLog
from core.menus.loginpage import LoginPage
from core.menus.credits import Credits

class Menu(BaseMenu):

    def __init__(self, system):
        self.system = system
        super().__init__(system)

        self.buttons = []

        self.state = MenuStateManager()

        self.state = MenuStateManager()
        self.credits = Credits(system)
        self.user_creator = UserCreator(system)
        self.login_page = LoginPage(system)
        self.change_log = ChangeLog(system)
        self.agreed_to_leaderboard = self.check_leaderboard_opt()
        self.recently_updated = self.check_recently_updated()

        self.title_image_original = self.system.window.load_image(asset("title"))
        self.title_image = self.title_image_original
        self.title_rect = self.title_image.get_rect()

        if self.agreed_to_leaderboard:
            self.state.set_state(MENUSTATE.ROOT)
            self.create_buttons()
        else:
            self.state.set_state(MENUSTATE.LEADERBOARDOPTIN)
            self.create_buttons()
        
        recently_updated_file = self.system.load.read_envar('recentlyupdated')
        if self.state.is_state(MENUSTATE.ROOT):
            if self.recently_updated:
                if recently_updated_file == "false":
                    self.state.set_state(MENUSTATE.ROOT)
                if recently_updated_file == "true":
                    self.state.set_state(MENUSTATE.CHANGELOG)
                    self.create_buttons()
        
        self.create_buttons()
        self.scale()

    def create_buttons(self):
        self.buttons.clear()
        if self.state.is_state(MENUSTATE.ROOT):
            self.create_root_buttons()
        elif self.state.is_state(MENUSTATE.SETTINGS):
            self.create_settings_buttons()
        elif self.state.is_state(MENUSTATE.AUDIO):
            self.create_audio_buttons()
        elif self.state.is_state(MENUSTATE.CREDITS):
            self.buttons.append(
                Button(
                    self.system,
                    40,
                    "Back",
                    (0.85,0.9),
                    self.back_to_root
                )
            )
        elif self.state.is_state(MENUSTATE.LEADERBOARDVIEWER):
            self.buttons.append(
                Button(
                    self.system,
                    40,
                    "Back",
                    (0.85,0.9),
                    self.back_to_root
                )
            )
        elif self.state.is_state(MENUSTATE.LEADERBOARDOPTIN):
            self.buttons.extend([
                Button(
                    self.system,
                    40,
                    "Yes",
                    (0.5,0.55),
                    self.leaderboard_opt_in
                ),
                Button(
                    self.system,
                    40,
                    "No",
                    (0.5,0.65),
                    self.leaderboard_opt_out
                )
            ])
        elif self.state.is_state(MENUSTATE.CREATEUSERNAME):
            self.create_username_buttons()
        
        elif self.state.is_state(MENUSTATE.LOGIN):
            self.create_login_buttons()

        elif self.state.is_state(MENUSTATE.DEVELOPERSETTINGS):
            self.buttons.extend([
                Button(
                    self.system,
                    40,
                    "Change Account",
                    (0.5,0.55),
                    self.change_account
                )
            ])

    def update(self):
        mouse_pos = self.system.input.get_mouse_pos()
        for button in self.buttons:
            button.update(mouse_pos)

    def draw(self):
        if self.system.sound.current_track is None and self.system.sound.music_state.is_state(MUSIC_STATE.ON):
            self.system.sound.play_music()
        
        t = self.system.time.get_current_time() / 1000
        pulse = (self.system.math.sin(t) + 1) / 2
        fade_color = (
            int(20 + (35 - 20) * pulse),
            0,
            int(20 + (35 - 20) * pulse)
        )
        self.system.window.fill(fade_color)

        if self.state.is_state(MENUSTATE.LEADERBOARDOPTIN):
            self.set_title(None)
            self.set_query("DO YOU AGREE TO HAVE YOUR SCORES POSTED ON A GLOBAL LEADERBOARD?")

        for button in self.buttons:
            button.draw()

        if self.state.is_state(MENUSTATE.CREATEUSERNAME):
            self.set_title(None)
            self.set_query(self.user_creator.error if self.user_creator.error else "Please enter a username and create a password:")
            self.user_creator.draw()

        if self.state.is_state(MENUSTATE.LOGIN):
            self.set_title(None)
            self.set_query(self.user_creator.error if self.user_creator.error else "Please enter your username and password:")
            self.login_page.draw()

        if self.state.is_state(MENUSTATE.ROOT) and self.system.updater.state.is_state(UPDATE_STATE.CURRENT):
            self.set_title("")
            self.draw_username_text(f"{self.system.user.username}")
            if self.system.user.high_score is not None:
                self.draw_score_text(f"{self.system.user.high_score}")
            else:
                self.draw_score_text(f"{self.system.load.read_constant('high_score')}")
            self.system.window.blit(self.title_image, self.title_rect)
        
        if self.state.is_state(MENUSTATE.ROOT) and self.system.updater.state.is_state(UPDATE_STATE.AVAILABLE):
            self.set_title("")
            self.draw_update_text()
            self.draw_username_text(f"{self.system.load.read_constant('username')}")
            self.draw_score_text(f"{self.system.load.read_constant('high_score')}")
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
        
        if self.state.is_state(MENUSTATE.LEADERBOARDVIEWER):
            self.leaderboard.fetch_and_display()
            self.set_title("Top 10 Leaderboard")

        self.draw_title()

    def scale(self):
        for button in self.buttons:
            button.scale()

        window_w, window_h = self.system.window.get_size()
        new_title_width = int(window_w * 0.5)
        scale_factor = new_title_width / self.title_image_original.get_width()
        new_title_height = int(self.title_image_original.get_height() * scale_factor)
        self.title_image = self.system.window.transform_scale(self.title_image_original, new_title_width, new_title_height)
        self.title_rect = self.title_image.get_rect(center=(window_w // 2, int(window_h * 0.2)))
        self.user_creator.scale()
        self.login_page.scale()


    def handle_event(self,event):

        if event.type == self.system.input.mouse_button_down():

            if event.button == 1:

                mouse_pos = self.system.input.get_mouse_pos()

                for button in self.buttons:
                    if button.is_clicked(mouse_pos,True):
                        break
        if self.state.is_state(MENUSTATE.LOGIN):
            self.login_page.handle_event(event)
        if self.state.is_state(MENUSTATE.CREATEUSERNAME):
            self.user_creator.handle_event(event)

    def create_root_buttons(self):

        buttons = [

            ("Endless Mode",
            (0.5,0.42),
            self.system.initialize_application),

            ("Blitz Mode",
            (0.5,0.52),
            None),

            ("Tutorial",
            (0.5,0.62),
            lambda: self.system.initialize_application(GAME_MODE.TUTORIAL)),

            ("Settings",
            (0.5,0.72),
            self.go_to_settings),

            ("Quit",
            (0.5,0.82),
            self.system.quit),
        ]


        for text,pos,action in buttons:

            self.buttons.append(
                Button(
                    self.system,
                    40,
                    text,
                    pos,
                    action
                )
            )


        self.buttons.extend([

            Button(
                self.system,
                30,
                "Credits",
                (0.85,0.9),
                self.credits_callback
            ),

            Button(
                self.system,
                30,
                "Leaderboard",
                (0.15,0.9),
                self.view_leaderboard
            ),

            Button(
                self.system,
                30,
                "Website",
                (0.15,0.8),
                self.open_website
            ),

            Button(
                self.system,
                30,
                "Our Discord",
                (0.85,0.8),
                self.discord_invite
            )

        ])


        if self.system.updater.state.is_state(UPDATE_STATE.AVAILABLE):

            self.buttons.append(
                Button(
                    self.system,
                    40,
                    "Update!",
                    (0.85,0.65),
                    self.system.updater.start,
                    styles="special_button"
                )
            )

    def create_settings_buttons(self):

        self.buttons.append(
            Button(
                self.system,
                40,
                "Audio",
                (0.5,0.45),
                self.audio_settings
            )
        )


        if self.system.control_state.is_state(DEVELOPER_MODE.ON):

            self.buttons.append(
                Button(
                    self.system,
                    40,
                    "Developer Settings",
                    (0.5,0.55),
                    self.developer_settings
                )
            )


        self.buttons.append(
            Button(
                self.system,
                40,
                "Back",
                (0.5,0.65),
                self.back_to_root
            )
        )

    def create_audio_buttons(self):

        self.buttons.extend([

            Button(
                self.system,
                35,
                "-",
                (0.35,0.4),
                self.system.sound.volume_down
            ),

            Button(
                self.system,
                30,
                f"Music Vol: {int(self.system.sound.volume*10)}",
                (0.5,0.4)
            ),

            Button(
                self.system,
                35,
                "+",
                (0.65,0.4),
                self.system.sound.volume_up
            ),


            Button(
                self.system,
                35,
                "-",
                (0.35,0.5),
                self.system.sound.sfx_volume_down
            ),

            Button(
                self.system,
                30,
                f"SFX Vol: {int(self.system.sound.sfx_volume*10)}",
                (0.5,0.5)
            ),

            Button(
                self.system,
                35,
                "+",
                (0.65,0.5),
                self.system.sound.sfx_volume_up
            ),


            Button(
                self.system,
                40,
                "Music",
                (0.5,0.6),
                self.system.sound.toggle_music
            ),

            Button(
                self.system,
                40,
                "UI SFX",
                (0.5,0.7),
                self.toggle_ui_sfx
            ),

            Button(
                self.system,
                40,
                "Game SFX",
                (0.5,0.8),
                self.toggle_game_sfx
            ),

            Button(
                self.system,
                40,
                "Back",
                (0.5,0.9),
                self.go_to_settings
            )

        ])

    def back_to_root_changelog(self):
        if self.system.control_state.is_state(DEVELOPER_MODE.ON):
            self.system.save.write_envar('recentlyupdated', 'true')
        else:
            self.system.save.write_envar('recentlyupdated', 'false')
        self.state.set_state(MENUSTATE.ROOT)
        self.create_buttons()

    def open_website(self):
        webbrowser.open("https://snowblitz.net", new=2)

    def create_username_buttons(self):

        self.buttons.extend([

            Button(
                self.system,
                40,
                "Submit",
                (0.5,0.65),
                self.create_account
            ),

            Button(
                self.system,
                35,
                "I already have an account",
                (0.5,0.75),
                self.go_to_login
            )

        ])

    def create_login_buttons(self):

        self.buttons.append(
            Button(
                self.system,
                40,
                "Log In",
                (0.5,0.65),
                self.login
            )
        )

    def discord_invite(self):
        webbrowser.open("https://discord.gg/PaWjydfUFX", new=2)


    def developer_settings(self):
        self.state.set_state(MENUSTATE.DEVELOPERSETTINGS)
        self.create_buttons()
    
    def change_opt_in(self):
        self.state.set_state(MENUSTATE.LEADERBOARDOPTIN)
        self.create_buttons()

    def change_account(self):
        self.state.set_state(MENUSTATE.CREATEUSERNAME)
        self.create_buttons()

    def go_to_login(self):
        self.state.set_state(MENUSTATE.LOGIN)
        self.create_buttons()

    def create_account(self):
        success = self.user_creator.submit()

        if not success:
            self.set_query(self.user_creator.error)
            return
        self.set_query("")
        self.state.set_state(MENUSTATE.ROOT)
        self.create_buttons()

    def check_leaderboard_opt(self):
        opt_in = self.system.load.read_constant('leaderboard_opt_in')
        if opt_in is not None:
            return True
        else:
            return False

    def check_recently_updated(self):
        updated = self.system.load.read_envar('recentlyupdated')
        if updated is not None:
            return True
        else:
            return False

    def leaderboard_back_to_root(self):
        self.leaderboard.fetch_manager.set_state(FETCH_STATE.CANCELLED)
        self.back_to_root()

    def leaderboard_opt_in(self):
        self.system.save.write_constant('leaderboard_opt_in','YES')
        self.query = None
        self.state.set_state(MENUSTATE.CREATEUSERNAME)
        self.create_buttons()
    
    def leaderboard_opt_in_dev(self):
        if self.system.load.read_constant('username') == None:
            self.system.save.write_constant('leaderboard_opt_in','YES')
            self.query = None
            self.state.set_state(MENUSTATE.CREATEUSERNAME)
            self.create_buttons()
        else:
            self.system.save.write_constant('leaderboard_opt_in','YES')
            self.query = None
            self.state.set_state(MENUSTATE.ROOT)
            self.create_buttons()

    
    def leaderboard_opt_out(self):
        self.system.save.write_constant('leaderboard_opt_in', 'NO')
        self.state.set_state(MENUSTATE.ROOT)
        self.system.save.write_constant("username","Player")
        self.system.save.write_constant("high_score",0)
        
        self.create_buttons()
        self.query = None

    def login(self):
        success = self.login_page.submit()
        print(success)

        if not success:
            self.set_query(self.login_page.error)
            return
        self.set_query("")
        self.state.set_state(MENUSTATE.ROOT)
        self.create_buttons()

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