import earthdef.entity
from earthdef.lane import random_lane
import earthdef.world
import earthdef.bullet

class Asteroid(earthdef.entity.Entity):
    def __init__(self, x, y):
        earthdef.entity.Entity.__init__(self, x, y)
        self.set_graphic('asteroid.png')

        self._velocity = 5

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

    @staticmethod
    def spawn_asteroids(count) -> list:
        asteroids = []
        for i in range(0, count):
            asteroids.insert(i, Asteroid(*random_lane(50)))
        return asteroids

class Earth(earthdef.entity.Entity):
    def __init__(self, *args, **kwargs):
        earthdef.entity.Entity.__init__(self, 0, 0)
        self.set_graphic('earth.png')

class Player(earthdef.entity.Entity):
    def __init__(self, *args, **kwargs):
        earthdef.entity.Entity.__init__(self, 0, 0)
        self.set_graphic('satellite.png')

    def is_player(self):
        return True

    def shoot(self):
        return earthdef.bullet.Bullet(self)
