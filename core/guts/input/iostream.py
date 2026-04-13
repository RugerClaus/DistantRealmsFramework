#will integrate keys class later
from core.guts.input.keys import Keys
import pygame

class IOSTREAM:
    def __init__(self):
        self.keys = Keys()
        self.sequences = {
            "debug": [pygame.K_F9],
            "secret": [pygame.K_s, pygame.K_e, pygame.K_c, pygame.K_r, pygame.K_e, pygame.K_t],
            "developer": [pygame.K_F2],
            "fuck": [pygame.K_f,pygame.K_u,pygame.K_c,pygame.K_k],
            "musicon": [pygame.K_m,pygame.K_u,pygame.K_s,pygame.K_i,pygame.K_c,pygame.K_o,pygame.K_n],
            "musicoff": [pygame.K_m,pygame.K_u,pygame.K_s,pygame.K_i,pygame.K_c,pygame.K_o,pygame.K_f,pygame.K_f],
            "monitor_system_states": [pygame.K_F8,pygame.K_1],
            "monitor_application_states": [pygame.K_F8,pygame.K_2],
            "monitor_game_states": [pygame.K_F8,pygame.K_3],
            "monitor_all_states": [pygame.K_F8,pygame.K_4]
        }
        self.buffer = []
        self.buffer_timer = 0
        self.buffer_timeout = 5000

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            now = pygame.time.get_ticks()

            if now - self.buffer_timer > self.buffer_timeout:
                self.buffer.clear()

            self.buffer.append(event.key)
            self.buffer_timer = now

            for name, seq in self.sequences.items():
                if self.buffer[-len(seq):] == seq:
                    self.buffer.clear()
                    return name 
            
        return None
