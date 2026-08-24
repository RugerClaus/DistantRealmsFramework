#will integrate keys class later
from core.engine.input.keys import Keys

class CommandModule:
    def __init__(self,eventmanager):
        self.eventmanager = eventmanager
        self.keys = Keys()
        self.sequences = {
            "debug": [self.keys.F9_key()],
            "developer": [self.keys.F2_key()],
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
