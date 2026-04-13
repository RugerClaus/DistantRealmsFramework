from core.ui.button import Button
from core.menus.basemenu import BaseMenu

class Win(BaseMenu):
    def __init__(self, system, restart_callback):
        self.system = system
        super().__init__(system)
        self.restart_callback = restart_callback
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        screen_w, screen_h = self.system.window.get_screen().get_size()
        btn_width, btn_height = screen_w // 4, 50
        spacing = btn_height * 1.2
        start_y = screen_h // 4 + screen_h // 7

        center_x = screen_w // 2

        self.buttons = [
            Button(self.system.sound, self.system.window, "Restart", center_x, start_y, btn_width, btn_height, (255, 255, 255), self.button_action_true_color, self.restart_callback),
            Button(self.system.sound, self.system.window, "Main Menu", center_x, start_y + spacing, btn_width, btn_height, (255, 255, 255), self.button_action_true_color, self.system.go_to_menu),
            Button(self.system.sound, self.system.window, "Quit", center_x, start_y + spacing * 2, btn_width, btn_height, (255, 255, 255), self.button_action_true_color, self.system.quit),
        ]

    def on_resize(self):
        self.create_buttons()

    def handle_event(self, event):
        if event.type == self.system.input.mouse_button_down() and event.button == 1:
            mouse_pos = self.system.input.get_mouse_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)
        elif event.type == self.system.input.video_resize_event():
            self.on_resize()

    def draw(self):
        t = self.system.window.get_current_time() / 1000
        pulse = (self.system.math.sin(t) + 1) / 2
        fade_color = (
            int(20 + (35 - 20) * pulse),
            0,
            int(20 + (35 - 20) * pulse)
        )
        self.system.window.fill(fade_color)

        text = self.font.render(f"YOU WIN!", True, (50, 200, 50))
        rect = text.get_rect(center=(self.system.window.get_screen().get_width() // 2, self.system.window.get_screen().get_height() // 4))
        self.system.window.blit(text, rect)

        mouse_pos = self.system.input.get_mouse_pos()
        for button in self.buttons:
            button.draw(mouse_pos)
