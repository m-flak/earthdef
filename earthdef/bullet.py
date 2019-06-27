import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Bullet, self).__init__()

        self.rect = pygame.Rect(0,0,2,8)
        self.rect.centerx = player.coords.centerx
        self.rect.top = player.coords.top

    def update(self):
        self.rect.y -= 5

    def draw(self, draw_surface):
        pygame.draw.rect(draw_surface, (255,0,0), self.rect)

    @staticmethod
    def update_bullets(bulletlist):
        for bullet in bulletlist:
            bullet.update()
