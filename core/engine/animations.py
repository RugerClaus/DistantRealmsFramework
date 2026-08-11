class Animation:
    def __init__(self, frames, frame_delay):
        self.frames = frames
        self.frame_delay = frame_delay
        self.current_frame = 0
        self.frame_timer = 0

    def update(self):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_current_frame(self):
        return self.frames[self.current_frame]
    
    def reset(self):
        self.current_frame = 0
        self.frame_timer = 0