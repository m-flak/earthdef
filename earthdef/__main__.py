import pygame
import earthdef as ed
from earthdef.resrc import find_resource
import earthdef.entities as ents
import earthdef.world as mir
from earthdef.bullet import Bullet

#global resources
BACKDROP = pygame.image.load(find_resource('image',
            name='backdrop.png'))
FONT = None # fonts must be init'd after pygame.init

#game globals
LEVEL = 1

def setup_world():
    world = mir.World()
    world.add_entity(ents.Earth().set_position(0,440))
    world.add_entity(ents.Player().set_position(0, 500))

    return world

def draw(world, bullets):
    global BACKDROP
    global FONT
    global LEVEL

    primary = pygame.display.get_surface()
    primary.blit(BACKDROP,(0,0))

    for bul in bullets:
        bul.draw(primary)
    for ent in world.entities:
        ent.draw(primary)

    level_text_str = "LEVEL: %d" % (LEVEL)
    level_text = FONT.render(level_text_str, False,
                (0,255,0))
    primary.blit(level_text, (0,0))

    return pygame.display.flip()

def main():
    global LEVEL
    global FONT

    pygame.init()
    #setup font now
    FONT = pygame.font.Font(find_resource('font',
                        name='militech.ttf'), 32)

    pygame.display.set_caption("Earth Defense")

    surface = pygame.display.set_mode(ed.DISPLAY_MODE)

    pygame.key.set_repeat(1, 25)
    clock = pygame.time.Clock()

    # Create the "World"
    world = setup_world()

    running = True
    oldlevel = 0
    bullets = []

    while running:
        # limit 30fps
        clock.tick(30)
        draw(world, bullets)

        Bullet.update_bullets(bullets)
        world.update_entities()
        oldlevel = world.update_world({ 'level': LEVEL,
                                        'oldlevel': oldlevel,
        })

        for event in pygame.event.get():
            # move the player
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        world.get_player().move(10,0)
                    else:
                        world.get_player().move(5,0)
                elif event.key == pygame.K_LEFT:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        world.get_player().move(-10,0)
                    else:
                        world.get_player().move(-5,0)
                elif event.key == pygame.K_SPACE:
                    bullets.append(world.get_player().shoot())
            # quit (like why?) ;)
            if event.type == pygame.QUIT:
                running = False


#################### *poof* ##############
main()
