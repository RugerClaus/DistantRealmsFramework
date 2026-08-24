class Temperature:

    def __init__(self, system, daycycle, season):
        self.math = system.math
        self.daycycle = daycycle
        self.season = season

        self.temperature = -10

        self.min_temp = 0
        self.max_temp = 0

        self.set_temperature_range()

    def update(self):

        self.set_temperature_range()

        if self.daycycle.is_day():

            sun_progress = self.daycycle.get_sun_progress()

            heat = self.math.sin(
                sun_progress * self.math.pi
            )

            target = (
                self.min_temp
                +
                (self.max_temp - self.min_temp)
                *
                heat
            )

        else:
            target = self.min_temp

        self.temperature += (
            target - self.temperature
        ) * 0.01

    def get_temperature(self):
        return int(self.temperature)

    def get_celsius(self):
        return int(self.temperature)

    def get_fahrenheit(self):
        return int(
            (self.temperature * 9 / 5) + 32
        )

    def set_temperature_range(self):
        self.min_temp = self.season.min
        self.max_temp = self.season.max
