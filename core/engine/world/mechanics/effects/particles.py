from core.util.colors import *

class Particle:
    def __init__(self,system,origin):
        self.system = system
        self.origin = origin
        self.color = blue
        self.surface = system.window.make_surface(2,2)
        self.rect = self.surface.get_rect(center = self.origin)
        self.velocity = self.system.random.uniform(2,5)
        math = self.system.math
        angle = self.system.random.uniform(0, math.tau)

        self.vector_x = math.cos(angle)
        self.vector_y = math.sin(angle)
        

    def update(self):
        
        self.rect.centerx += self.vector_x * self.velocity
        self.rect.centery += self.vector_y * self.velocity


    def draw(self):
        self.surface.fill((self.color))

        self.system.window.blit(self.surface,self.rect)

class Particles:
    def __init__(self, system, entity):
        self.entity = entity
        self.system = system
        self.max_particles = 10
        self.particles = []

    def handle_event(self,event,command):
        pass

    def update(self):
        current_temperature = self.entity.environment.temperature.get_celsius()
        if current_temperature <= 5:
            self.max_particles = 10
        elif current_temperature <= 10:
            self.max_particles = 20
        else:
            self.max_particles = 30

        if current_temperature <= 0:
            self.max_particles = 0

        math = self.system.math

        for particle in self.particles[:]:
            particle.update()

            distance = math.hypot(
                particle.rect.centerx - particle.origin[0],
                particle.rect.centery - particle.origin[1]
            )

            if distance >= self.entity.size + (self.entity.size * self.entity.size):
                self.particles.remove(particle)

        if len(self.particles) < self.max_particles:
            particle = Particle(self.system, self.entity.rect.center)
            self.particles.append(particle)

    def draw(self):
        for particle in self.particles:
            particle.draw()