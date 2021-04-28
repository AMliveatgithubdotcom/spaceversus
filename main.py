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
        projectilesp1 = []
        projectilesp2 = []
        player1 = characters.player(screenx / 2, screeny / 2)
        player2 = characters.player(screenx / 4, screeny / 4)
        p1currentvelx, p1currentvely, p2currentvelx, p2currentvely = 0, 0, 0, 0
        running = True
        p1rotation = -90
        p2rotation = -90
        p1throttling = False
        p2throttling = False
        debugmode = False   

        # --- Main loop. This is where moving the ships and reading button presses is handled. --- #
        while running:
        # End the game #
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    # Projectiles #
                    if event.key == pygame.K_SPACE:
                        projectilesp1.append(characters.projectile(player1.x, player1.y, math.cos(p1rotation * math.pi / 180), math.sin(p1rotation * math.pi / 180), pygame.time.get_ticks()))
                    if event.key == pygame.K_KP_0:
                        projectilesp2.append(characters.projectile(player2.x, player2.y, math.cos(p2rotation * math.pi / 180), math.sin(p2rotation * math.pi / 180), pygame.time.get_ticks()))
                    # Debug enable #
                    if event.key == pygame.K_F5:
                        debugmode = not debugmode
            # --- Controls, calculation of velocity and acceleration--- #
            # Rotation #
            if pygame.key.get_pressed()[pygame.K_d]:
                p1rotation += 5
            if pygame.key.get_pressed()[pygame.K_a]:
                p1rotation -= 5
            if pygame.key.get_pressed()[pygame.K_KP_6]:
                p2rotation += 5
            if pygame.key.get_pressed()[pygame.K_KP_4]:
                p2rotation -= 5
            # Enable the ship throttle and accelerate. #
            if pygame.key.get_pressed()[pygame.K_w]:
                p1tempvelx = p1currentvelx + player1.acceleration * math.cos(p1rotation * math.pi / 180)
                p1tempvely = p1currentvely + player1.acceleration * math.sin(p1rotation * math.pi / 180)
                if player1.maxspeed*-1 < p1tempvelx < player1.maxspeed:
                    p1currentvelx = round(p1tempvelx, 2)
                if player1.maxspeed*-1 < p1tempvely < player1.maxspeed:
                    p1currentvely = round(p1tempvely, 2)
                p1throttling = True

            if pygame.key.get_pressed()[pygame.K_KP_8]:
                p2tempvelx = p2currentvelx + player2.acceleration * math.cos(p2rotation * math.pi / 180)
                p2tempvely = p2currentvely + player2.acceleration * math.sin(p2rotation * math.pi / 180)
                if player2.maxspeed*-1 < p2tempvelx < player2.maxspeed:
                    p2currentvelx = round(p2tempvelx, 2)
                if player2.maxspeed*-1 < p2tempvely < player2.maxspeed:
                    p2currentvely = round(p2tempvely, 2)
                p2throttling = True
            # Check if the ship is throttled. If not, decelerate it slowly. #
            if p1throttling == 0:
                if p1currentvelx != 0:
                    p1currentvelx = round(p1currentvelx -copysign(player1.deceleration, p1currentvelx), 2)
                if p1currentvely != 0:
                    p1currentvely = round(p1currentvely -copysign(player1.deceleration, p1currentvely), 2)
            if p2throttling == 0:
                if p2currentvelx != 0:
                    p2currentvelx = round(p2currentvelx -copysign(player2.deceleration, p2currentvelx), 2)
                if p2currentvely != 0:
                    p2currentvely = round(p2currentvely -copysign(player2.deceleration, p2currentvely), 2)
            # Set the throttle back to 0 after every check has been completed in one cycle. #
            p1throttling, p2throttling = False, False
            # Move the ship by changing its coordinates. Speed and direction gets calculated when the UP button is pressed. #
            player1.x, player1.y = (player1.x + p1currentvelx) % screenx, (player1.y + p1currentvely) % screeny
            player2.x, player2.y = (player2.x + p2currentvelx) % screenx, (player2.y + p2currentvely) % screeny
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
            # Player 1 #
            for projectile in projectilesp1:
                if projectile.traveltime < 1800:
                    projectile.x = (projectile.x + (10 * projectile.cos)) % screenx
                    projectile.y = (projectile.y + (10 * projectile.sin)) % screeny
                    projectile.traveltime = pygame.time.get_ticks() - projectile.starttime
                    projectile.draw(screen, (255, 0, 0))
                    if math.sqrt((max(projectile.x, player2.x) - min(projectile.x, player2.x))**2 + (max(projectile.y, player2.y) - min(projectile.y, player2.y))**2) < player2.radius + projectile.radius:
                        player2.health -= 10
                        projectilesp1.pop(projectilesp1.index(projectile))
                else: 
                    projectilesp1.pop(projectilesp1.index(projectile))
            # Player 2 #
            for projectile in projectilesp2:
                if projectile.traveltime < 1800:
                    projectile.x = (projectile.x + (10 * projectile.cos)) % screenx
                    projectile.y = (projectile.y + (10 * projectile.sin)) % screeny
                    projectile.traveltime = pygame.time.get_ticks() - projectile.starttime
                    projectile.draw(screen, (0, 0, 255))
                    if math.sqrt((max(projectile.x, player1.x) - min(projectile.x, player1.x))**2 + (max(projectile.y, player1.y) - min(projectile.y, player1.y))**2) < player1.radius + projectile.radius:
                        player1.health -= 10
                        projectilesp2.pop(projectilesp2.index(projectile))
                else:
                    projectilesp2.pop(projectilesp2.index(projectile))
            # End of Projectiles #

            # Game Over Conditions #
            if (player2.health or player1.health) <= 0:
                pygame.QUIT
            # Redraw player.
            player1.update(screen, p1rotation, player1.x % screenx, player1.y % screeny)
            player2.update(screen, p2rotation, player2.x % screenx, player2.y % screeny)
            pygame.display.flip()
            clock.tick(60)

game().main()