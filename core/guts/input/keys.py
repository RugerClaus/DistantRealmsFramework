import pygame

class Keys:
    def __init__(self):
        self.info = "This is a class of methods to return pygame keys, but can work for any other backend."
        #will make the whole system more robust so i can clean out and modularize the input system.
        # now we are officially ready to make a simple set of control schemes for the player to choose from later on

    def space_key(self):
        return pygame.K_SPACE
    
    def a_key(self):
        return pygame.K_a
    
    def d_key(self):
        return pygame.K_d
    
    def h_key(self):
        return pygame.K_h
    
    def s_key(self):
        return pygame.K_s

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

    def left_arrow_key(self):
        return pygame.K_LEFT
    
    def right_arrow_key(self):
        return pygame.K_RIGHT
    
    def left_shift_key(self):
        return pygame.K_LSHIFT
    
    def right_shift_key(self):
        return pygame.K_RSHIFT
    
    def return_key(self):
        return pygame.K_RETURN