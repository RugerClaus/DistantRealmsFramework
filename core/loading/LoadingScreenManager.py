class LoadingScreenManager:
    def __init__(self, system):
        self.system = system

    def draw(self,text_string):
        import math
        t = self.system.time.get_current_time() / 500
        pulse = (math.sin(t) + 1) / 2  # 0 → 1

        dark = 40
        light = 255   

        fade_color = (
            int(dark + (light - dark) * pulse),
            int(dark + (light - dark) * pulse),
            int(dark + (light - dark) * pulse),
        )
        text = self.font.render(text_string, True, fade_color)
        rect = text.get_rect(center=(
            self.system.window.get_width() // 2,
            self.system.window.get_height() // 2
        ))
        self.system.window.blit(text, rect)