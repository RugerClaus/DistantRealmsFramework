import pygame

class Keys:
    def __init__(self):
        self.info = "This is a class of methods to return pygame keys, but can work for any other backend."
        #will make the whole system more robust so i can clean out and modularize the input system.
        # now we are officially ready to make a simple set of control schemes for the player to choose from later on

    def space_key(self):
        return pygame.K_SPACE
    
    def w_key(self):
        return pygame.K_w

    def a_key(self):
        return pygame.K_a
    
    def s_key(self):
        return pygame.K_s
    
    def d_key(self):
        return pygame.K_d
    
    def h_key(self):
        return pygame.K_h
    
    def e_key(self):
        return pygame.K_e
    
    def q_key(self):
        return pygame.K_q

    def seven_key(self):
        return pygame.K_7
    
    def F3_key(self):
        return pygame.K_F3
    
    def F4_key(self):
        return pygame.K_F4
    
    def F5_key(self):
        return pygame.K_F5
    
    def F6_key(self):
        return pygame.K_F6
    
    def F7_key(self):
        return pygame.K_F7
    
    def F8_key(self):
        return pygame.K_F8
    
    def F9_key(self):
        return pygame.K_F9
    
    def F10_key(self):
        return pygame.K_F10
    
    def F11_key(self):
        return pygame.K_F11
    
    def F12_key(self):
        return pygame.K_F12

    def up_arrow_key(self):
        return pygame.K_UP

    def down_arrow_key(self):
        return pygame.K_DOWN

    def left_arrow_key(self):
        return pygame.K_LEFT
    
    def right_arrow_key(self):
        return pygame.K_RIGHT
    
    def left_shift_key(self):
        return pygame.K_LSHIFT
    
    def right_shift_key(self):
        return pygame.K_RSHIFT
    
    def page_up_key(self):
        return pygame.K_PAGEUP
    
    def page_down_key(self):
        return pygame.K_PAGEDOWN
    
    def return_key(self):
        return pygame.K_RETURN
    
    def backtick(self):
        return pygame.K_BACKQUOTE
    
    def backspace_key(self):
        return pygame.K_BACKSPACE
    
    def tab_key(self):
        return pygame.K_TAB
    
    def enter_key(self):
        return pygame.K_RETURN
    
    def escape_key(self):
        return pygame.K_ESCAPE