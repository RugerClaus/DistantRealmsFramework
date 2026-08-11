import pygame
from core.engine.input.controls import Controls
from core.engine.input.CommandModule import CommandModule
from core.engine.input.keys import Keys
from core.ui.font import FontEngine


class InputManager:
    def __init__(self, system):
        self.system = system
        self.CommandModule = CommandModule(self)
        self.current_keys = set()
        self.released_keys = set()
        self.key_history = {}
        self.surface = self.system.window.make_surface(self.system.window.get_width(), self.system.window.get_height(), True)
        self.font = FontEngine("keypress").font
        self.last_key = None
        self.last_key_time = 0
        self.key_display_timeout = 1000
        self.keys = Keys()
        self.game_controls = Controls()

    def video_resize_event(self):
        return pygame.VIDEORESIZE

    def mouse_button_down(self):
        return pygame.MOUSEBUTTONDOWN
    
    def mouse_button_up(self):
        return pygame.MOUSEBUTTONUP

    def mouse_motion(self):
        return pygame.MOUSEMOTION
    
    def get_mouse_pos(self):
        return pygame.mouse.get_pos()
    
    def keydown(self):
        return pygame.KEYDOWN

    def quit_event(self):
        return pygame.QUIT
    
    def mouse_scroll_event(self):
        return pygame.MOUSEWHEEL
    
    def reset_mouse_input(self):
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)
        pygame.event.clear(pygame.MOUSEBUTTONUP)

    def key_register(self,key):
        now = self.system.time.get_current_time()
        self.current_keys.add(key)
        self.key_history[key] = now
        self.last_key = key
        self.last_key_time = now

    def handle_event(self, event,needskeys=False):
        
        if needskeys:
            if event.type == pygame.KEYDOWN:
                self.key_register(event.key)
                return event.key
        else:
            if event.type == pygame.KEYDOWN:
                self.key_register(event.key)
                command = self.CommandModule.update(event)
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

    def scale(self,w,h):
        self.surface = self.system.window.make_surface(w,h,True)
        self.draw_most_recent_keypress()


    def draw_most_recent_keypress(self):
        self.surface.fill((0, 0, 0, 0))  
        now = self.system.time.get_current_time()

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

        self.system.window.blit(self.surface, (0, 0))

    def is_pressed(self, key):
        return key in self.current_keys

    def was_released(self, key):
        return key in self.released_keys

    def clear_released(self):
        self.released_keys.clear()

    def window_focus_gained(self):
        return pygame.WINDOWFOCUSGAINED
    
    def window_focus_lost(self):
        return pygame.WINDOWFOCUSLOST