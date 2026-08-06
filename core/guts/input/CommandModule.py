#will integrate keys class later
from core.guts.input.keys import Keys

class CommandModule:
    def __init__(self,eventmanager):
        self.eventmanager = eventmanager
        self.keys = Keys()
        self.sequences = {
            "debug": [self.keys.F9_key()],
            "secret": [self.keys.s_key(), self.keys.e_key(), self.keys.c_key(), self.keys.r_key(), self.keys.e_key(), self.keys.t_key()],
            "developer": [self.keys.F2_key()],
            "monitor_system_states": [self.keys.F8_key(),self.keys.one_key()],
            "monitor_runtime_states": [self.keys.F8_key(),self.keys.two_key()],
            "monitor_application_states": [self.keys.F8_key(),self.keys.three_key()],
            "monitor_all_states": [self.keys.F8_key(),self.keys.four_key()],
            "raise_opacity": [self.keys.F8_key(),self.keys.five_key()],
            "lower_opacity": [self.keys.F8_key(),self.keys.six_key()],
            "reload_ui": [self.keys.F1_key(),self.keys.one_key()],
            "reload_application": [self.keys.F1_key(),self.keys.two_key()],
            "reload_menu_editor": [self.keys.F1_key(),self.keys.three_key()],
            "reload_form_editor": [self.keys.F1_key(),self.keys.four_key()]
        }
        self.buffer = []
        self.buffer_timer = 0
        self.buffer_timeout = 5000

    def update(self, event):
        if event.type == self.eventmanager.keydown():
            now = self.eventmanager.system.time.get_current_time()

            if now - self.buffer_timer > self.buffer_timeout:
                self.buffer.clear()

            self.buffer.append(event.key)
            self.buffer_timer = now

            for name, seq in self.sequences.items():
                if self.buffer[-len(seq):] == seq:
                    self.buffer.clear()
                    return name 
            
        return None
