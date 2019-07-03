import pygame
import earthdef.entity
from earthdef.lane import random_lane
import earthdef.world

class Asteroid(earthdef.entity.Entity):
    def __init__(self, x, y):
        earthdef.entity.Entity.__init__(self, x, y, kind_of='Asteroid')
        self.set_graphic('asteroid.png')

        self._velocity = 2

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        self._velocity = int(value)

    # accelerate
    def accel(bymuch=1):
        self.velocity += bymuch

    def update(self):
        # move the asteroid
        self.move(0, self.velocity)

    # dont draw purged asteroids
    def draw(self, draw_surface):
        if self.purgeable is True:
            return

        return super().draw(draw_surface)

    @staticmethod
    def spawn_asteroids(count) -> list:
        asteroids = []
        for i in range(0, count):
            asteroids.insert(i, Asteroid(*random_lane(50)))
        return asteroids

class Bullet(earthdef.entity.Entity):
    def __init__(self, player):
        earthdef.entity.Entity.__init__(self, 0, 0, size=(2,8),
                                        kind_of='Bullet')

        self.coords.centerx = player.coords.centerx
        self.coords.top = player.coords.top

    def update(self):
        self.coords.y -= 5

        if self.coords.y < 0:
            self.purgeable = True

    def draw(self, draw_surface):
        pygame.draw.rect(draw_surface, (255, 0, 0), self.coords)

class Earth(earthdef.entity.Entity):
    def __init__(self, *args, **kwargs):
        earthdef.entity.Entity.__init__(self, 0, 0, kind_of='Earth')
        self.set_graphic('earth.png')

class Player(earthdef.entity.Entity):
    def __init__(self, *args, **kwargs):
        earthdef.entity.Entity.__init__(self, 0, 0, kind_of='Player')
        self.set_graphic('satellite.png')

    def is_player(self):
        return True

    def shoot(self):
        return [Bullet(self)]
