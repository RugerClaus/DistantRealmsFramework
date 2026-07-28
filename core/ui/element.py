class UIElement:
    def __init__(
        self,visible=True,enabled=True,focusable=False,position=(0.5,0.5)):
        if not isinstance(position, tuple):
            raise TypeError("UIElement position must be a tuple: (x,y)")
        
        self.visible = visible
        self.enabled = enabled
        self.focusable = focusable
        self.position = position

    def get_screen_position(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        return (
            int(ww * self.position[0]),
            int(wh * self.position[1])
        )