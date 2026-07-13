from .endpoints import LEADERBOARD, UPDATE_SCORE
from core.guts.network.system_endpoints import API_KEY
from systemlogging import log_error, log_event


class Leaderboard:
    def __init__(self, system):
        self.system = system
        self.leaderboardURL = LEADERBOARD
        self.submit_url = UPDATE_SCORE

        if not self.leaderboardURL:
            log_error("Leaderboard URL not set in config")

        if not self.submit_url:
            log_error("Leaderboard submission URL not set in config")

    def fetch_leaderboard(self):
        if not self.leaderboardURL:
            log_error("Unable to fetch leaderboard: No endpoint configured")
            return ("error", "Missing leaderboard endpoint")

        response = self.system.network.get(
            self.leaderboardURL
        )

        if not response["success"]:
            log_error(
                f"Failed to fetch leaderboard: {response['message']}"
            )
            return ("error", response["message"])

        log_event("Fetched leaderboard data.")

        return ("success", response["data"])

    def submit(self, score,session_token):

        if score is None:
            log_error("Unable to submit empty score")
            return False
        
        
        
        if session_token is None:
            log_error("Unable to update score without valid session token")
            return False

        if not self.submit_url:
            log_event(
                "No leaderboard submission endpoint configured. "
                "Score was not submitted."
            )
            return False

        app_password = self.system.load.read_constant("clientAppPassword")

        if not app_password:
            log_error("Missing application password, reauthenticate your client")
            return False
        

        data = {
            "key": API_KEY,
            "clientAppPassword": app_password,
            "sessionToken": session_token,
            "score": int(score)
        }

        response = self.system.network.post(
            self.submit_url,
            data
        )

        if not response["success"]:
            log_error(
                f"Leaderboard submission failed: "
                f"{response['message']}"
            )
            return False

        log_event(
            f"Submitted leaderboard score for {self.system.user.username}: {score}"
        )

        return True
    
