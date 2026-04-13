from core.guts.input.keys import Keys

class Controls:
    def __init__(self):
        keys = Keys()
        self.move_left = keys.a_key()
        self.move_right = keys.d_key()
        self.slow = keys.left_shift_key()

    def set_controls(self, move_left, move_right):
        self.move_left = move_left
        self.move_right = move_right