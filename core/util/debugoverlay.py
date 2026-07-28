from core.ui.font import FontEngine
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.state.RuntimeLayer.DevTools.StateMonitor.state import MONITOR_STATE


class DebugOverlay:
    def __init__(self, system):
        self.system = system
        self.surface = system.window.draw_overlay((0, 0, 0), 128)
        self.rect = self.surface.get_rect()

        self.font_left = FontEngine("UI").font
        self.font_right = FontEngine(25).font
        self.font_right_all = FontEngine(20).font
        self.devmodefont = FontEngine(20).font

        self.opacity = 0

    def create_options(self):
        pass

    def scale(self):
        self.surface = self.system.window.draw_overlay((0, 0, 0), 128)
        self.rect = self.surface.get_rect()

    def normalized_to_pixel(self, x, y):
        return (int(x * self.surface.get_width()), int(y * self.surface.get_height()))

    def handle_event(self, event):
        if event.type == self.system.input.video_resize_event():
            self.scale()

        command = self.system.input.handle_event(event)

        if command == "monitor_system_states":
            self.system.state_monitor_state.set_state(MONITOR_STATE.SYSTEM)

        elif command == "monitor_runtime_states":
            self.system.state_monitor_state.set_state(MONITOR_STATE.RUNTIME)

        elif command == "monitor_application_states":
            self.system.state_monitor_state.set_state(MONITOR_STATE.APPLICATION)

        elif command == "monitor_all_states":
            self.system.state_monitor_state.set_state(MONITOR_STATE.ALL)

        elif command == "raise_opacity":
            self.opacity = min(255, self.opacity + 32)

        elif command == "lower_opacity":
            self.opacity = max(0, self.opacity - 32)

    def draw(self):
        text_color = (255, 255, 255)

        self.surface.fill((0, 0, 0, self.opacity))

        width = self.surface.get_width()
        height = self.surface.get_height()

        left_margin = 0.01
        top_margin = 0.01
        right_margin = 0.01
        bottom_margin = 0.01

        line_spacing = 0.012
        telemetry_spacing = 0.001

        left_x, left_y = self.normalized_to_pixel(left_margin, top_margin)

        line_height = self.font_left.get_height()

        fps_text = f"FPS: {round(self.system.window.get_fps())}"
        fps_surf = self.font_left.render(fps_text, False, text_color)

        self.surface.blit(fps_surf, (left_x, left_y))

        left_y += int(line_height + height * line_spacing)

        stripped_title = self.system.sound.current_track.rsplit('.', 1)[0] if self.system.sound.current_track else None
        song_text = f"Song: {stripped_title or 'None'}"
        song_surf = self.font_left.render(song_text, False, text_color)

        self.surface.blit(song_surf, (left_x, left_y))

        left_y += int(line_height + height * line_spacing)

        opacity_text = f"Overlay Opacity: {self.opacity}"
        opacity_surf = self.font_left.render(opacity_text, False, text_color)

        opacity_x, opacity_y = self.normalized_to_pixel(left_margin, 1.0 - bottom_margin)

        self.surface.blit(opacity_surf, (opacity_x, opacity_y - opacity_surf.get_height()))

        for key, value in self.system.system_monitor.items():
            if value is None:
                continue

            inspector_text = f"{key}: {value}"
            inspector_surf = self.font_left.render(inspector_text, False, text_color)

            self.surface.blit(inspector_surf, (left_x, left_y))

            left_y += int(line_height + height * telemetry_spacing)

        for key, value in self.system.app_inspector.items():
            if value is None:
                continue

            inspector_text = f"{key}: {value}"
            inspector_surf = self.font_left.render(inspector_text, False, text_color)

            self.surface.blit(inspector_surf, (left_x, left_y))

            left_y += int(line_height + height * telemetry_spacing)

        right_x, right_y = self.normalized_to_pixel(1.0 - right_margin, top_margin)

        if self.system.state_monitor_state.is_state(MONITOR_STATE.SYSTEM):
            states = self.system.runtime_state.get_global_active_system_states()
            font = self.font_right

        elif self.system.state_monitor_state.is_state(MONITOR_STATE.RUNTIME):
            states = self.system.runtime_state.get_global_active_runtime_states()
            font = self.font_right

        elif self.system.state_monitor_state.is_state(MONITOR_STATE.APPLICATION):
            states = self.system.runtime_state.get_global_active_application_states()
            font = self.font_right

        else:
            states = self.system.runtime_state.get_all_global_active_states()
            font = self.font_right_all

        for state in states:
            surf = font.render(str(state), False, text_color)

            self.surface.blit(surf, (right_x - surf.get_width(), right_y))

            right_y += int(surf.get_height() + height * telemetry_spacing)

        if self.system.control_state.is_state(DEVELOPER_MODE.ON):
            padding = int(width * 0.01)
            warning_text = "WARNING: DEVELOPER MODE ENABLED"
            warning_surf = self.devmodefont.render(warning_text, False, text_color)

            background = self.system.window.make_surface(warning_surf.get_width() + padding, warning_surf.get_height() + padding, True)
            background.fill((255, 0, 0, 128))

            text_rect = warning_surf.get_rect(center=background.get_rect().center)
            background.blit(warning_surf, text_rect)

            bottom_right = self.normalized_to_pixel(1.0, 1.0)
            background_rect = background.get_rect(bottomright=bottom_right)

            self.surface.blit(background, background_rect)

        self.system.window.blit(self.surface, self.rect)

    def update(self):
        pass