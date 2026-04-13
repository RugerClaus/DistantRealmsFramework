import threading
from helper import *
from core.ui.font import FontEngine
from core.network.leaderboard import Leaderboard
from core.state.ApplicationLayer.NetworkLayer.Loading.state import FETCH_STATE
from core.state.ApplicationLayer.NetworkLayer.Loading.statemanager import FetchStateManager
from core.network.user import User
class LeaderboardViewer():
    def __init__(self,system,state,root_callback):
        self.system = system
        self.system.input
        self.state = state
        self.root_callback = root_callback
        self.leaderboard = Leaderboard()
        self.font = FontEngine(50).font
        
        self.fetch_manager = FetchStateManager()
        self.cached_data = None
        self.fetch_thread = None

        self.lock = threading.Lock()

        self.user = User()

    def start_fetch(self):
        if not self.fetch_manager.is_state(FETCH_STATE.IDLE):
            return

        self.fetch_thread = threading.Thread(target=self.fetch_task, daemon=True) # had to get creative for this of course
        self.fetch_thread.start()                                                  # users no likey frozen screens

    def fetch_task(self):
        self.fetch_manager.set_state(FETCH_STATE.FETCHING)
        
        try:
            status, data = self.leaderboard.fetch_leaderboard()
        except Exception as e:
            log_event("Fetch exception", str(e))
            with self.lock:
                self.cached_data = None
                self.fetch_manager.set_state(FETCH_STATE.ERROR)
            return

        with self.lock:
            self.cached_data = data if status == "success" else None

            if status == "success":
                self.fetch_manager.set_state(FETCH_STATE.SUCCESS)
            elif status == "timeout":
                self.fetch_manager.set_state(FETCH_STATE.TIMEOUT)
            else:
                self.fetch_manager.set_state(FETCH_STATE.ERROR)

    def fetch_and_display(self):
        if self.cached_data is None:
            if self.fetch_manager.is_state(FETCH_STATE.IDLE):
                self.start_fetch()
            elif self.fetch_manager.is_state(FETCH_STATE.TIMEOUT):
                self.cached_data = None
                self.display_timeout()
            elif self.fetch_manager.is_state(FETCH_STATE.ERROR):
                self.cached_data = None
                log_error("Error fetching leaderboard data.")
                self.fetch_manager.set_state(FETCH_STATE.IDLE)
            elif self.fetch_manager.is_state(FETCH_STATE.FETCHING):
                draw_loading(self.font, self.system.window, "Loading Leaderboard...")
            elif self.fetch_manager.is_state(FETCH_STATE.CANCELLED):
                self.cached_data = None
                self.fetch_manager.set_state(FETCH_STATE.IDLE)
            return

        self.display_leaderboard(self.cached_data)
        self.fetch_manager.set_state(FETCH_STATE.IDLE)


    def display_timeout(self):
        text = self.font.render("Leaderboard Timed Out. Please try again later.", True, (255, 0, 0))
        rect = text.get_rect(center=(self.system.window.get_screen().get_width() // 2, self.system.window.get_screen().get_height() // 2))
        self.system.window.blit(text, rect)

    def display_leaderboard(self, data):
        center_x = self.system.window.get_width() // 2
        start_y = self.system.window.get_height() // 3
        row_height = 40
        column_gap = 400

        username_x = center_x - column_gap
        score_x = center_x + column_gap // 2

        header_color = (255, 255, 0)
        text_color = (255, 255, 255)
        t = self.system.window.get_current_time() / 100
        pulse = (self.system.math.sin(t) + 1) / 2
        fade_color = (
            int(20 + (200 - 10) * pulse),
            255,
            int(20 + (200 - 10) * pulse),
        )
        player_text_color = fade_color
        
        

        header_y = start_y - (row_height/2+15)

        username_header = self.font.render("Username", True, header_color)
        score_header = self.font.render("Score", True, header_color)

        self.system.window.blit(username_header, username_header.get_rect(left=username_x, top=header_y))
        self.system.window.blit(score_header, score_header.get_rect(left=score_x, top=header_y))

        sorted_data = sorted(data, key=lambda x: x['score'], reverse=True)[:10]

        for row, entry in enumerate(sorted_data):
            y = start_y + (row + 1) * row_height

            row_number_text = f"{str(row+1)}. "
            username_text = entry['username']

            row_number_surf = self.font.render(row_number_text, True, text_color if username_text != self.user.get_username() else player_text_color)
            
            username_surf = self.font.render(username_text, True, text_color if username_text != self.user.get_username() else player_text_color)
            score_surf = self.font.render(str(entry["score"]), True, text_color if username_text != self.user.get_username() else player_text_color)

            row_number_x = username_x
            username_x_offset = row_number_surf.get_width()

            self.system.window.blit(row_number_surf, row_number_surf.get_rect(left=row_number_x, centery=y))
            self.system.window.blit(username_surf, username_surf.get_rect(left=row_number_x + row_number_surf.get_width(), centery=y))
            self.system.window.blit(score_surf, score_surf.get_rect(left=score_x, centery=y))

        
        log_event("Displaying leaderboard data.", f"{self.leaderboard}")



    def refresh(self):
        self.cached_data = None
        self.fetch_status = None
        self.start_fetch()
