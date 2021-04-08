# Import pygame module and characters from the characters folder
import pygame
import math
from math import copysign
from characters import characters

class game():
    def main(self):
        # --- Initialization, set up every important variable --- #
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("the game")
        clock = pygame.time.Clock()
        screenx = 1280
        screeny = 720
        screen = pygame.display.set_mode((screenx, screeny))
        debugfont = pygame.font.SysFont(None, 24)
        projectiles = []
        player1 = characters.player(screenx / 2, screeny / 2)
        p1currentvelx, p1currentvely = 0, 0
        running = True
        p1rotation = -90
        p1throttling = False
        debugmode = False   

        # ---Main loop. This is where moving the ships and reading button presses is handled. --- #
        while running:
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
                p1tempvelx = p1currentvelx + player1.acceleration * math.cos(p1rotation * math.pi / 180)
                p1tempvely = p1currentvely + player1.acceleration * math.sin(p1rotation * math.pi / 180)
                if player1.maxspeed*-1 < p1tempvelx < player1.maxspeed:
                    p1currentvelx = round(p1tempvelx, 2)
                if player1.maxspeed*-1 < p1tempvely < player1.maxspeed:
                    p1currentvely = round(p1tempvely, 2)
                p1throttling = True
            # Projectiles. #
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                projectiles.append(characters.projectile(player1.x, player1.y, math.cos(p1rotation * math.pi / 180), math.sin(p1rotation * math.pi / 180)))
            # Switch to debug #
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
            # Move the ship by changing its coordinates. Speed and direction gets calculated when the UP button is pressed. #
            player1.x = (player1.x + p1currentvelx) % screenx
            player1.y = (player1.y + p1currentvely) % screeny
            # Redraw the ships at a new position. #
            screen.fill((50,50,50))
            # Debug Mode #
            if debugmode:
                fps = debugfont.render(str(int(clock.get_fps())), True, (255, 0, 0))
                debugtextx = debugfont.render(f'X VELOCITY: {p1currentvelx}', True, (255, 0, 0))
                debugtexty = debugfont.render(f'Y VELOCITY: {p1currentvely}', True, (255, 0, 0))
                screen.blit(debugtextx, (64 , 64))
                screen.blit(debugtexty, (64 , 78))
                screen.blit(fps, (64 , 92))
            # Debug Mode End #
            # Process every projectile, move them or delete them if their traveltime has reached the limit. #
            for projectile in projectiles:
                if projectile.traveltime < 500:
                    poldx = projectile.x
                    poldy = projectile.y
                    projectile.x = (projectile.x + (10 * projectile.cos)) % screenx
                    projectile.y = (projectile.y + (10 * projectile.sin)) % screeny
                    projectile.traveltime += math.sqrt((projectile.x - poldx) ** 2 + (projectile.y - poldy) ** 2)
                    projectile.draw(screen)
                else: 
                    projectiles.pop(projectiles.index(projectile))
            # Redraw player.
            player1.update(screen, p1rotation, player1.x % screenx, player1.y % screeny)
            pygame.display.flip()
            clock.tick(60)

game().main()