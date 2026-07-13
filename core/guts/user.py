class User:

    def __init__(self, system):

        self.system = system

    @property
    def username(self):

        username = self.system.load.read_constant("username")

        if username is None:
            username = "Player"
            self.system.save.write_constant(
                "username",
                username
            )

        return username

    @property
    def high_score(self):

        score = self.system.load.read_constant("high_score")

        if score is None:
            score = 0
            self.system.save.write_constant(
                "high_score",
                score
            )

        return int(score)