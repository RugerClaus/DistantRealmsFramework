import pygame # this is probably the only place in the framework that imports pygame
# only for its key codes since i'll probably be using pygame's inpug for a long long time

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

    def t_key(self):
        return pygame.K_t

    def b_key(self):
        return pygame.K_b

    def c_key(self):
        return pygame.K_c

    def f_key(self):
        return pygame.K_f

    def g_key(self):
        return pygame.K_g

    def i_key(self):
        return pygame.K_i

    def j_key(self):
        return pygame.K_j

    def k_key(self):
        return pygame.K_k

    def l_key(self):
        return pygame.K_l

    def m_key(self):
        return pygame.K_m

    def n_key(self):
        return pygame.K_n

    def o_key(self):
        return pygame.K_o

    def p_key(self):
        return pygame.K_p

    def r_key(self):
        return pygame.K_r

    def u_key(self):
        return pygame.K_u

    def v_key(self):
        return pygame.K_v

    def x_key(self):
        return pygame.K_x

    def y_key(self):
        return pygame.K_y

    def z_key(self):
        return pygame.K_z

    def zero_key(self):
        return pygame.K_0

    def one_key(self):
        return pygame.K_1

    def two_key(self):
        return pygame.K_2

    def three_key(self):
        return pygame.K_3

    def four_key(self):
        return pygame.K_4

    def five_key(self):
        return pygame.K_5

    def six_key(self):
        return pygame.K_6

    def seven_key(self):
        return pygame.K_7

    def eight_key(self):
        return pygame.K_8

    def nine_key(self):
        return pygame.K_9

    def F1_key(self):
        return pygame.K_F1

    def F2_key(self):
        return pygame.K_F2
    
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

    def delete_key(self):
        return pygame.K_DELETE

    def l_ctrl_key(self):
        return pygame.K_LCTRL

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

    def right_ctrl_key(self):
        return pygame.K_RCTRL

    def l_alt_key(self):
        return pygame.K_LALT

    def r_alt_key(self):
        return pygame.K_RALT

    def l_gui_key(self):
        return pygame.K_LGUI

    def r_gui_key(self):
        return pygame.K_RGUI

    def caps_lock_key(self):
        return pygame.K_CAPSLOCK

    def num_lock_key(self):
        return pygame.K_NUMLOCK

    def scroll_lock_key(self):
        return pygame.K_SCROLLOCK

    def insert_key(self):
        return pygame.K_INSERT

    def home_key(self):
        return pygame.K_HOME

    def end_key(self):
        return pygame.K_END

    def print_screen_key(self):
        return pygame.K_PRINT

    def sys_req_key(self):
        return pygame.K_SYSREQ

    def pause_key(self):
        return pygame.K_PAUSE

    def break_key(self):
        return pygame.K_BREAK

    def menu_key(self):
        return pygame.K_MENU

    def help_key(self):
        return pygame.K_HELP

    def clear_key(self):
        return pygame.K_CLEAR

    def left_bracket_key(self):
        return pygame.K_LEFTBRACKET

    def right_bracket_key(self):
        return pygame.K_RIGHTBRACKET

    def backslash_key(self):
        return pygame.K_BACKSLASH

    def semicolon_key(self):
        return pygame.K_SEMICOLON

    def apostrophe_key(self):
        return pygame.K_QUOTE

    def comma_key(self):
        return pygame.K_COMMA

    def period_key(self):
        return pygame.K_PERIOD

    def slash_key(self):
        return pygame.K_SLASH

    def equals_key(self):
        return pygame.K_EQUALS

    def minus_key(self):
        return pygame.K_MINUS

    def underscore_key(self):
        return pygame.K_UNDERSCORE

    def plus_key(self):
        return pygame.K_PLUS

    def asterisk_key(self):
        return pygame.K_ASTERISK

    def colon_key(self):
        return pygame.K_COLON

    def question_mark_key(self):
        return pygame.K_QUESTION

    def less_than_key(self):
        return pygame.K_LESS

    def greater_than_key(self):
        return pygame.K_GREATER

    def ampersand_key(self):
        return pygame.K_AMPERSAND

    def caret_key(self):
        return pygame.K_CARET

    def dollar_key(self):
        return pygame.K_DOLLAR

    def percent_key(self):
        return pygame.K_PERCENT

    def hash_key(self):
        return pygame.K_HASH

    def at_key(self):
        return pygame.K_AT

    def left_parenthesis_key(self):
        return pygame.K_LEFTPAREN

    def right_parenthesis_key(self):
        return pygame.K_RIGHTPAREN

    def keypad_0_key(self):
        return pygame.K_KP0

    def keypad_1_key(self):
        return pygame.K_KP1

    def keypad_2_key(self):
        return pygame.K_KP2

    def keypad_3_key(self):
        return pygame.K_KP3

    def keypad_4_key(self):
        return pygame.K_KP4

    def keypad_5_key(self):
        return pygame.K_KP5

    def keypad_6_key(self):
        return pygame.K_KP6

    def keypad_7_key(self):
        return pygame.K_KP7

    def keypad_8_key(self):
        return pygame.K_KP8

    def keypad_9_key(self):
        return pygame.K_KP9

    def keypad_period_key(self):
        return pygame.K_KP_PERIOD

    def keypad_divide_key(self):
        return pygame.K_KP_DIVIDE

    def keypad_multiply_key(self):
        return pygame.K_KP_MULTIPLY

    def keypad_minus_key(self):
        return pygame.K_KP_MINUS

    def keypad_plus_key(self):
        return pygame.K_KP_PLUS

    def keypad_enter_key(self):
        return pygame.K_KP_ENTER

    def keypad_equals_key(self):
        return pygame.K_KP_EQUALS