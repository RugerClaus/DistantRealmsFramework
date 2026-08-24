from core.state.ApplicationLayer.Mechanics.Season.state import SEASON_STATE
from core.state.ApplicationLayer.Mechanics.Season.statemanager import SeasonStateManager


class Season:

    YEAR_LENGTH = 100
    SEASON_LENGTH = YEAR_LENGTH // 4

    def __init__(self, dayc):
        self.dayc = dayc
        self.state = SeasonStateManager()

        self.min = 0
        self.max = 0

    def winter(self):
        self.min = -20
        self.max = 2

        self.dayc.day_length = 40000
        self.dayc.night_length = 60000

    def spring(self):
        self.min = 0
        self.max = 20

        self.dayc.day_length = 50000
        self.dayc.night_length = 50000

    def summer(self):
        self.min = 22
        self.max = 38

        self.dayc.day_length = 60000
        self.dayc.night_length = 40000

    def autumn(self):
        self.min = 5
        self.max = 21

        self.dayc.day_length = 50000
        self.dayc.night_length = 50000

    def update(self):
        self.update_season()

        if self.state.is_state(SEASON_STATE.WINTER):
            self.winter()

        elif self.state.is_state(SEASON_STATE.SPRING):
            self.spring()

        elif self.state.is_state(SEASON_STATE.SUMMER):
            self.summer()

        elif self.state.is_state(SEASON_STATE.AUTUMN):
            self.autumn()

    def update_season(self):
        day_of_year = self.dayc.day % self.YEAR_LENGTH

        if day_of_year < self.SEASON_LENGTH:
            self.state.set_state(SEASON_STATE.WINTER)

        elif day_of_year < self.SEASON_LENGTH * 2:
            self.state.set_state(SEASON_STATE.SPRING)

        elif day_of_year < self.SEASON_LENGTH * 3:
            self.state.set_state(SEASON_STATE.SUMMER)

        else:
            self.state.set_state(SEASON_STATE.AUTUMN)
