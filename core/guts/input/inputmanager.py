import pygame
from core.guts.input.controls import Controls
from core.guts.input.iostream import IOSTREAM
from core.guts.input.keys import Keys
from core.ui.font import FontEngine


class InputManager:
    def __init__(self, window):
        self.iostream = IOSTREAM()
        self.current_keys = set()
        self.released_keys = set()
        self.key_history = {}
        self.surface = window.make_surface(window.get_width(), window.get_height(), True)
        self.font = FontEngine("keypress").font
        self.window = window
        self.last_key = None
        self.last_key_time = 0
        self.key_display_timeout = 1000
        self.keys = Keys()
        self.game_controls = Controls()

    def get_current_left_control(self):
        return self.get_key_name(self.game_controls.move_left).capitalize()
    
    def get_current_right_control(self):
        return self.get_key_name(self.game_controls.move_right).capitalize()
    
    def get_current_up_control(self):
        return self.get_key_name(self.game_controls.move_up).capitalize()
    
    def get_current_down_control(self):
        return self.get_key_name(self.game_controls.move_down).capitalize()

    def video_resize_event(self):
        return pygame.VIDEORESIZE

    def mouse_button_down(self):
        return pygame.MOUSEBUTTONDOWN
    
    def get_mouse_pos(self):
        return pygame.mouse.get_pos()
    
    def keydown(self):
        return pygame.KEYDOWN

    def quit_event(self):
        return pygame.QUIT

    def set_game_controls(self,move_left=None, move_right=None, move_up=None, move_down=None):
        if move_left is not None and move_right is not None:
            self.game_controls.set_controls(move_left, move_right, move_up, move_down)
        elif move_left is not None:
            self.game_controls.set_controls(move_left, self.game_controls.move_right, self.game_controls.move_up, self.game_controls.move_down)
        elif move_right is not None:
            self.game_controls.set_controls(self.game_controls.move_left, move_right, self.game_controls.move_up, self.game_controls.move_down)
        elif move_up is not None:
            self.game_controls.set_controls(self.game_controls.move_left, self.game_controls.move_right, move_up, self.game_controls.move_down)
        elif move_down is not None:
            self.game_controls.set_controls(self.game_controls.move_left, self.game_controls.move_right, self.game_controls.move_up, move_down)

    def key_register(self,key):
        now = self.window.get_current_time()
        self.current_keys.add(key)
        self.key_history[key] = now
        self.last_key = key
        self.last_key_time = now

    def handle_event(self, event,needskeys=False):
        
        if needskeys: # returns the key that was pressed. Good for UI input
            if event.type == pygame.KEYDOWN:
                self.key_register(event.key)
                return event.key
        else: # returns a command based on the internal input stream service. for handling application wide functionality
            if event.type == pygame.KEYDOWN:
                self.key_register(event.key)
                command = self.iostream.update(event)
                return command

            elif event.type == pygame.KEYUP:
                self.current_keys.discard(event.key)
                self.released_keys.add(event.key)

            return None
        
    def input_event(self):
        return pygame.event.get()
        
    def get_key_name(self,key):
        return pygame.key.name(key)
    
    def get_pressed_keys(self):
        return pygame.key.get_pressed()

    def rescale(self,w,h):
        self.surface = self.window.make_surface(w,h,True)
        self.draw_most_recent_keypress()


    def draw_most_recent_keypress(self):
        self.surface.fill((0, 0, 0, 0))  
        now = self.window.get_current_time()

        self.key_history = {k: t for k, t in self.key_history.items() if now - t < self.key_display_timeout}

        recent_keys = list(self.key_history.keys())

        if recent_keys:
            key_names = [pygame.key.name(key) for key in recent_keys]
            keys_str = ", ".join(key_names)
            letter = self.font.render(keys_str, False, (255, 255, 255))
            rect = letter.get_rect(center=(self.surface.get_width() // 2,
                                           letter.get_rect().height))
            self.surface.blit(letter, rect)
        else:
            self.last_key = None

        self.window.blit(self.surface, (0, 0))

    def is_pressed(self, key):
        return key in self.current_keys

    def was_released(self, key):
        return key in self.released_keys

    def clear_released(self):
        self.released_keys.clear()