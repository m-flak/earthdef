import pygame
import earthdef as ed
import earthdef.ui as eui
from earthdef.resrc import find_resource
import earthdef.entities as ents
import earthdef.world as mir


#global resources
BACKDROP = pygame.image.load(find_resource('image',
            name='backdrop.png'))
FONT = None # fonts must be init'd after pygame.init

#game globals
LIVES = 10
LEVEL = 1
SCORE = 0
OLDSCORE = SCORE

def setup_world():
    world = mir.World()
    world.add_entity(ents.Earth().set_position(0,440))
    world.add_entity(ents.Player().set_position(0, 500))

    return world

def draw(world, ui):
    global BACKDROP

    # clear the board
    primary = pygame.display.get_surface()
    primary.blit(BACKDROP,(0,0))

    # draw all entities
    for ent in world.entities:
        ent.draw(primary)

    #draw ui stuff
    ui.draw_all(primary)

    return pygame.display.flip()

def main():
    global LEVEL
    global OLDSCORE
    global SCORE
    global LIVES
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

    # Create UI components
    ui = eui.GameUI()
    ui.add({ 'level': eui.StatusText(FONT, (0,0), lambda: "LEVEL: %d" % (LEVEL)),
             'score': eui.StatusText(FONT, (640,0), lambda: "SCORE: %d" % (SCORE)),
             'lives': eui.StatusText(FONT, (0,36), lambda: "LIVES: %d" % (LIVES)),
    })

    running = True
    oldlevel = 0
    dead = False

    while running:
        # limit 30fps
        clock.tick(30)

        if dead:
            if not ui.has_component('failure'):
                screen = pygame.Rect((0,0),ed.DISPLAY_MODE)
                ui.add({'failure': eui.StatusText(FONT, (screen.centerx, screen.centery), lambda: "MISSION FAILURE!").center()})

        draw(world, ui)

        world.update_entities()
        oldlevel = world.update_world({ 'level': LEVEL,
                                        'oldlevel': oldlevel,
        })

        for event in pygame.event.get():
            # move the player
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        world.get_player().move(15,0)
                    else:
                        world.get_player().move(5,0)
                elif event.key == pygame.K_LEFT:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        world.get_player().move(-15,0)
                    else:
                        world.get_player().move(-5,0)
                elif event.key == pygame.K_SPACE:
                    world.add_entity(world.get_player().shoot())
            # handle scoring and leveling
            if event.type == ed.SCORE_CHANGED:
                LEVEL = oldlevel+1
                SCORE += event.scoremod
                OLDSCORE = SCORE
            if event.type == ed.EARTH_IMPACT:
                LIVES -= event.num_impacts
                if LIVES > 0:
                    # keep 'em coming if none destroyed
                    if SCORE == 0 or OLDSCORE == SCORE:
                        LEVEL = oldlevel+1
                else:
                    dead = True
            # quit (like why?) ;)
            if event.type == pygame.QUIT:
                running = False


#################### *poof* ##############
main()
