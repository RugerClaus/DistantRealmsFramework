import requests
from config import config
from helper import log_error, log_event

TIMEOUT_SECONDS = 5

class Leaderboard:
    def __init__(self):
        self.leaderboardURL = config.get("API").get("LEADERBOARD")
        if not self.leaderboardURL:
            log_error("Leaderboard url not set in config")

    def fetch_leaderboard(self,setusername=False):
        try:
            response = requests.get(self.leaderboardURL, timeout=TIMEOUT_SECONDS)

            if response.status_code == 200:
                if not setusername:
                    leaderboard_data = response.json()
                    log_event(f"Fetched leaderboard data. Status: {response.status_code}; Response: {leaderboard_data}")
                    return ("success",leaderboard_data)
                else:
                    log_event(f"Setting high score to user's high score on server if it exists")
                    leaderboard_data = response.json()
                    return leaderboard_data

            else:
                log_error(f"Failed to fetch leaderboard. Status: {response.status_code}; Response: {response.text}")
                return ("error", f"HTTP {response.status_code}")

        except requests.exceptions.Timeout:
            log_error("Leaderboard fetch timed out.")
            return ("timeout", "Failed to fetch leaderboard: Timeout")

        except requests.exceptions.RequestException as e:
            log_error(f"Network error while fetching leaderboard: {e}")
            return ("error", str(e))
