import requests, config

from core.network.leaderboard import Leaderboard

from helper import *
class User:
    def __init__(self):
        self.scores = Leaderboard()
        self.score = None
        self.setusernameURL = config.config.get("API").get("USER_AUTH")
        if not self.setusernameURL:
            log_error("Username Auth url not set in config")
        self.setuserhighscoreURL = config.config.get("API").get("UPDATE_SCORE")
        if not self.setuserhighscoreURL:
            log_error("Update Score url not set in config")

    def get_username(self):
        username = read_constant_from_file('username')
        if username is not None:
            return username
        else:
            return None

    def get_high_score(self):
        high_score = read_constant_from_file('high_score')
        if high_score is not None:
            return int(high_score)
        else:
            return None

    def send_username_to_api(self):
        username = self.get_username()
        if username:
            data = {"username": str(username),"key":config.config.get("API_KEY")}
            try:
                response = requests.post(self.setusernameURL, json=data)
                if response.status_code == 200:
                    write_constant_to_file("high_score",0)

                    log_event(f"Username added to global database. Status: {str(response.status_code)}; Response: {response.json()}")
                    response_data = response.json()
                    if response_data.get("message") == "Username already exists":
                        log_event("username already exists")
                else:
                    log_error(f"Failed to create username in global database. Status: {str(response.status_code)}; Response: {response.text}")
            except requests.exceptions.RequestException as e:
                log_error(f"Network error while sending username: {e} Status: {response.status_code}; Response: {response.text}")
        else:
            log_error("Username is blank or invalid.")
    
    def send_high_score_to_api(self):
        high_score = self.get_high_score()
        username = self.get_username()
        key = config.config.get("API_KEY")

        if high_score and username:
            data = {
                "username": str(username),
                "score": int(high_score),
                "key": str(key)
            }
            try:
                print("sending score to db")
                response = requests.post(self.setuserhighscoreURL, json=data)
                if response.status_code == 200:
                    log_event(f"Highscore added for {username}. Status: {response.status_code}; Response: {response.json()}")
                else:
                    log_error(f"Failed to send highscore for {username}. Status: {response.status_code}; Response: {response.text}")
            except requests.exceptions.RequestException as e:
                log_error(f"Network error while sending high score: {e} Status: {response.status_code}; Response: {response.text}")
        else:
            log_error(f"Highscore or Username is missing. Highscore: {high_score}, Username: {username}")

    def get_high_score_from_api(self):
        leaderboard = self.scores.fetch_leaderboard(True)
        username = self.get_username()
        high_score = self.get_high_score()
        if not username:
            log_error(f"Username is missing. Username: {username}")
        elif username and not high_score:
            log_event(f"High score is missing High Score: {high_score}")
    
        for line in leaderboard:
            if line.get("username") == username:
                if int(line.get("score")) > 0:
                    if int(line.get("score")) > high_score:
                        write_constant_to_file('high_score',line.get("score"))
                        self.score = line.get("score")
                    return int(line.get("score"))
                else:
                    return int(high_score)