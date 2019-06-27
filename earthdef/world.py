import earthdef.entity as ent
import earthdef.entities

class World(object):
    def __init__(self, *args, **kwargs):
        self.entities = []

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

        if oldlevel < level:
            self.add_entity(
                earthdef.entities.Asteroid.spawn_asteroids(level))

        return level
