from core.ui.font import FontEngine
from core.state.ApplicationLayer.dev import DEVELOPER_MODE
from core.state.ApplicationLayer.Debug.StateMonitor.state import MONITOR_STATE

class DebugOverlay:
    def __init__(self,system,loading):
        self.system = system
        self.loading = loading
        self.surface = system.window.draw_overlay((0, 0, 0), 128)
        self.rect = self.surface.get_rect()
        self.font_left = FontEngine("UI").font
        self.font_right = FontEngine("debug_state").font
        self.font_right_all = FontEngine("debug_all_state").font
        self.devmodefont = FontEngine(20).font
        self.opacity = 0

    def create_options(self):
        pass

    def scale(self):
        self.surface = self.system.window.draw_overlay((0, 0, 0), 128)
        self.rect = self.surface.get_rect()

    def handle_event(self,event):
        if event.type == self.system.input.video_resize_event():
            self.scale()

        command = self.system.input.handle_event(event)
        if command == "monitor_system_states":
            self.system.state_monitor_state.set_state(MONITOR_STATE.SYSTEM)
        elif command == "monitor_application_states":
            self.system.state_monitor_state.set_state(MONITOR_STATE.APPLICATION)
        elif command == "monitor_game_states":
            self.system.state_monitor_state.set_state(MONITOR_STATE.GAME)
        elif command == "monitor_all_states":
            self.system.state_monitor_state.set_state(MONITOR_STATE.ALL)
        elif command == "raise_opacity":
            self.opacity = min(255, self.opacity + 32)
        elif command == "lower_opacity":
            self.opacity = max(0, self.opacity - 32)

    def draw(self):
        text_color = (255, 255, 255)
        self.surface.fill((0, 0, 0),self.opacity)
        surface_width = self.surface.get_width()
        
        left_x = 10
        left_y = 10

        fps_text = f"FPS: {round(self.system.window.get_fps())}"
        fps_surf = self.font_left.render(fps_text, False, text_color)
        self.surface.blit(fps_surf, (left_x, left_y))
        left_y += fps_surf.get_height() * 1.2

        stripped_title = self.system.sound.current_track.rsplit('.', 1)[0] if self.system.sound.current_track else None
        song_text = f"Song: {stripped_title or 'None'}"
        
        song_surf = self.font_left.render(song_text, False, text_color)
        self.surface.blit(song_surf, (left_x, left_y))
        left_y += song_surf.get_height() * 1.2

        opacity_text = f"Overlay Opacity: {self.opacity}"
        opacity_surf = self.font_left.render(opacity_text, False, text_color)
        self.surface.blit(opacity_surf, (left_x, self.system.window.get_height() - opacity_surf.get_height() - 10))

        if self.system.runtime_inspector['seed'] is not None:
            world_seed_text = f"World Seed: {self.system.runtime_inspector['seed']}"
            world_seed_surf = self.font_left.render(world_seed_text,False,text_color)
            self.surface.blit(world_seed_surf,(left_x,left_y))
            left_y += world_seed_surf.get_height() * 1.2

        if self.system.runtime_inspector["coords"] is not None:
            coords_text = f"Coordinates: {self.system.runtime_inspector['coords']}"
            coords_surf = self.font_left.render(coords_text, False, text_color)
            self.surface.blit(coords_surf, (left_x, left_y))
            left_y += coords_surf.get_height() * 1.2
        
        if self.system.runtime_inspector["tile"] is not None:
            tile_text = f"Tile: {self.system.runtime_inspector['tile']}"
            tile_surf = self.font_left.render(tile_text, False, text_color)
            self.surface.blit(tile_surf, (left_x, left_y))
            left_y += tile_surf.get_height() * 1.2

        if self.system.runtime_inspector["chunk"] is not None:
            chunk_text = f"Chunk: {self.system.runtime_inspector['chunk']}"
            chunk_surf = self.font_left.render(chunk_text, False, text_color)
            self.surface.blit(chunk_surf, (left_x, left_y))
            left_y += chunk_surf.get_height() * 1.2

        right_x = surface_width - 10
        right_y = 10

        if self.system.state_monitor_state.is_state(MONITOR_STATE.SYSTEM):
            for state in self.system.app_state.get_global_active_system_states():
                appstate_text = f"{state}"
                appstate_surf = self.font_right.render(appstate_text, False, text_color)
                self.surface.blit(appstate_surf, (right_x - appstate_surf.get_width(), right_y))
                right_y += appstate_surf.get_height() * 1.2
                
        elif self.system.state_monitor_state.is_state(MONITOR_STATE.APPLICATION):
            for state in self.system.app_state.get_global_active_application_states():
                appstate_text = f"{state}"
                appstate_surf = self.font_right.render(appstate_text, False, text_color)
                self.surface.blit(appstate_surf, (right_x - appstate_surf.get_width(), right_y))
                right_y += appstate_surf.get_height() * 1.2

        elif self.system.state_monitor_state.is_state(MONITOR_STATE.GAME):
            for state in self.system.app_state.get_global_active_game_states():
                appstate_text = f"{state}"
                appstate_surf = self.font_right.render(appstate_text, False, text_color)
                self.surface.blit(appstate_surf, (right_x - appstate_surf.get_width(), right_y))
                right_y += appstate_surf.get_height() * 1.2
        
        elif self.system.state_monitor_state.is_state(MONITOR_STATE.ALL):
            for state in self.system.app_state.get_all_global_active_states():
                appstate_text = f"{state}"
                appstate_surf = self.font_right_all.render(appstate_text, False, text_color)
                self.surface.blit(appstate_surf, (right_x - appstate_surf.get_width(), right_y))
                right_y += appstate_surf.get_height() * 1.2
        


        if self.system.control_state.is_state(DEVELOPER_MODE.ON):
            padding = 10
            devmode_warning_text = "WARNING: DEVELOPER MODE ENABLED"
            devmode_warning_surf = self.devmodefont.render(devmode_warning_text, False, text_color)
            background = self.system.window.make_surface(
                devmode_warning_surf.get_width() + padding,
                devmode_warning_surf.get_height() + padding,
                True
            )
            background.fill((255, 0, 0,128))
            text_rect = devmode_warning_surf.get_rect(
                center=background.get_rect().center
            )
            background.blit(devmode_warning_surf, text_rect)
            background_rect = background.get_rect(
                bottomright=(self.system.window.get_width(), self.system.window.get_height())
            )
            self.surface.blit(background, background_rect)

        self.system.window.blit(self.surface, self.rect)


    def update(self):
        pass