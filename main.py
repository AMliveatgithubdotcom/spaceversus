# Import pygame module and characters from the characters folder
import pygame
import math
from math import copysign
from characters import characters

# --- Initialization, set up every important variable --- #
def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("the game")
    screenx = 1280
    screeny = 720
    screen = pygame.display.set_mode((screenx, screeny))
    debugfont = pygame.font.SysFont(None, 24)
    player1 = characters.player(screenx / 2, screeny / 2)
    p1currentvelx = 0
    p1currentvely = 0
    running = True
    p1rotation = -90
    p1throttling = False
    debugmode = False

    # ---Main loop. This is where moving the ships and reading button presses is handled. --- #
    while running:
        pygame.time.Clock().tick(60)
    # Move the ship by changing its coordinates. Speed and direction gets calculated when the UP button is pressed. #
        player1.x += p1currentvelx
        player1.y += p1currentvely
    # End the game #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # ---Controls, calculation of velocity and acceleration--- #
        # Rotation #
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            p1rotation += 5
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            p1rotation -= 5
        # Enable the ship throttle and accelerate. #
        if pygame.key.get_pressed()[pygame.K_UP]:
            if player1.maxspeed*-1 < p1currentvelx < player1.maxspeed:
                p1currentvelx += player1.acceleration * math.cos(p1rotation * math.pi / 180)
                p1currentvelx = round(p1currentvelx, 2)
            if player1.maxspeed*-1 < p1currentvely < player1.maxspeed:
                p1currentvely += player1.acceleration * math.sin(p1rotation * math.pi / 180)
                p1currentvely = round(p1currentvely, 2)
            p1throttling = True
        if pygame.key.get_pressed()[pygame.K_F5]:
            debugmode = not debugmode
        # Check if the ship is throttled. If not, decelerate it slowly. #
        # TODO: Round the final result? Movement feels weird. #
        if p1throttling == 0:
            if p1currentvelx != 0:
                p1currentvelx = round(p1currentvelx -copysign(player1.deceleration, p1currentvelx), 2)
            if p1currentvely != 0:
                p1currentvely = round(p1currentvely -copysign(player1.deceleration, p1currentvely), 2)
        # Set the throttle back to 0 after every check has been completed in one cycle. #
        p1throttling = False
        # Redraw the ships at a new position. #
        screen.fill((50,50,50))
        if debugmode:
            debugtextx = debugfont.render(f'X VELOCITY: {p1currentvelx}', True, (255, 0, 0))
            debugtexty = debugfont.render(f'Y VELOCITY: {p1currentvely}', True, (255, 0, 0))
            screen.blit(debugtextx, (64 , 64))
            screen.blit(debugtexty, (64 , 78))
        player1.update(screen, p1rotation, player1.x % screenx, player1.y % screeny)
        pygame.display.flip()

if __name__=="__main__":
    main()
