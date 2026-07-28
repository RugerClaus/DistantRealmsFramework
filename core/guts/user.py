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
    
    @username.setter
    def username(self,value):
        username = value
        self.system.save.write_constant(
            "username",
            username
        )