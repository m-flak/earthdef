from earthdef.resrc import find_resource
import pygame

class Entity(object):
    def __new__(cls, *args, **kwargs):
        inst = super(Entity, cls).__new__(cls)
        # hack in collision detect routines >:0
        setattr(inst, 'collide_rect', pygame.sprite.collide_rect)
        return inst

    def __init__(self, x, y, **kwargs):
        w, h = kwargs.get('size', (0,0))
        if w == 0 or h == 0:
            w = kwargs.get('width', 0)
            h = kwargs.get('height', 0)

        self.coords = pygame.Rect(x,y,w,h)
        self.graphic = None

    # this makes us technically a sprite lol
    @property
    def rect(self):
        return self.coords

    @property
    def X(self):
        return self.coords.left

    @property
    def Y(self):
        return self.coords.top

    @X.setter
    def X(self, value):
        self.coords.left = value

    @Y.setter
    def Y(self, value):
        self.coords.top = value

    @property
    def W(self):
        return self.coords.width

    @W.setter
    def W(self, value):
        self.coords.width = value

    @property
    def H(self):
        return self.coords.height

    @H.setter
    def H(self, value):
        self.coords.height = value

    #override for the player
    def is_player(self):
        return False

    # chainable
    def set_position(self, x, y):
        self.X = x
        self.Y = y
        return self

    def move(self, x, y):
        self.X = self.X + x
        self.Y = self.Y + y

    def collide(self, other) -> bool:
        return self.collide_rect(self, other)

    def set_graphic(self, image_name):
        self.graphic = pygame.image.load(find_resource('image', name=image_name))
        # don't override an entity's current size if set
        if not self.W > 0:
            self.W = self.graphic.get_width()
        if not self.H > 0:
            self.H = self.graphic.get_height()

    def draw(self, draw_surface):
        draw_surface.blit(self.graphic, self.coords)

    def update(self):
        pass
