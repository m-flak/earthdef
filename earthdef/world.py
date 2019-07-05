import pygame
import earthdef
import earthdef.entity as ent
import earthdef.entities

class World(object):
    def __init__(self, *args, **kwargs):
        self.entities = []

    # Will return an entity, if it is the only occurence of 'key'
    # Otherwise, a list of all entities matching 'key' will be
    def __getitem__(self, key):
        item = self.list_by_type(key)
        if len(item) < 1:
            raise KeyError("{} is not in World.".format(key))
        elif len(item) == 1:
            return item[0]
        else:
            return item

    def add_entity(self, entity):
        if isinstance(entity, ent.Entity):
            self.entities.append(entity)
        elif isinstance(entity, list):
            i = len(self.entities)
            self.entities[i:i] = entity

    def update_entities(self):
        upd = lambda: [e.update() for e in self.entities]
        return upd()

    def get_player(self):
        player = [p for p in self.entities if p.is_player() is True]
        return player[0]

    def update_world(self, params):
        if not isinstance(params, dict):
            raise TypeError("params must be a dict")

        level = params['level']
        oldlevel = params['oldlevel']
        num_asteroids = level

        #purge things
        for e in self.entities:
            if e.purgeable is True:
                self.entities.remove(e)

        if oldlevel < level:
            self.add_entity(
                earthdef.entities.Asteroid.spawn_asteroids(level))

        # find & destroy asteroids that the player kills
        asteroids = self.list_by_type('Asteroid')
        destroyed = self.get_collides(asteroids,
                                      self.list_by_type('Bullet'))
        if len(destroyed) > 0:
            i = 0
            for d in destroyed:
                for a in asteroids:
                    if a is d:
                        a.purgeable = True
                self.entities.remove(d)
                i = i + 1
            pygame.event.post(pygame.event.Event(earthdef.SCORE_CHANGED,{
                'scoremod': i,
            }))

        #re-get 'alive' asteroids
        asteroids = self.list_by_type('Asteroid')
        # find & cull/purge all asteroids that hit the earth :o
        hit_da_earth = self.get_collides(asteroids,[self['Earth']])
        howmany = len(hit_da_earth)
        if howmany > 0:
            for d in hit_da_earth:
                for a in asteroids:
                    if a is d:
                        a.purgeable = True
                self.entities.remove(d)
            pygame.event.post(pygame.event.Event(earthdef.EARTH_IMPACT,{
                'num_impacts': howmany,
            }))

        return level

    def list_by_type(self, type_str):
        return [e for e in self.entities if e.kind_of == type_str]

    # Returns a list of type_a's that have collided with type_b's
    # BOTH PARAMS ARE LISTS, USE list_by_type FIRST :)
    def get_collides(self, type_a, type_b):
        def filifunc(a, i=0):
            try:
                result = a.collide(type_b[i])
                if result is False:
                    return filifunc(a,i+1)
                else:
                    return result
            except:
                return False

        return list(filter(filifunc, type_a))
