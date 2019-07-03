import pygame

class GameUI(object):
    def __init__(self, objects=dict()):
        self.ui_objects = objects

    def draw_all(self, draw_surface):
        for uio in self.ui_objects.values():
            uio.draw(draw_surface)

    def draw_only(self, draw_surface, id_key):
        try:
            self.ui_objects[id_key].draw(draw_surface)
        except:
            print("Error: Cannot draw non-existent \'{}\'".format(id_key))

    def add(self, objects):
        old = self.ui_objects
        self.ui_objects = {**old, **objects}

class UIObject(object):
    # O(rect, surface) or keyword args: rect, surface
    def __init__(self, *args, **kwargs):
        self.surface = None
        self.rect = None

        if len(args) != 0:
            for count, item in enumerate(args):
                if count == 0:
                    self.rect = item
                elif count == 1:
                    self.surface = item
        else:
            kwargs.get('rect', None)
            kwargs.get('surface', None)

    def draw(self, draw_surface):
        if self.surface is None or self.rect is None:
            return

        draw_surface.blit(self.surface, self.rect)

class StatusText(UIObject):
    def __init__(self, font, where, updater):
        self.font = font
        where_at = (0,0)
        if isinstance(where, pygame.Rect):
            where_at = where.topleft
        elif isinstance(where, tuple):
            where_at = where
        self.updater = updater

        super(StatusText, self).__init__(pygame.Rect(where_at,
                                self.font.size(self.updater())))

    def draw(self, draw_surface):
        self.surface = self.font.render(self.updater(), False, (0,255,0))

        return super(StatusText, self).draw(draw_surface)
    
