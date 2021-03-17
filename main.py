import pygame
import math
from characters import characters

# initialization
def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("the game")
    screenx = 1280
    screeny = 720
    screen = pygame.display.set_mode((screenx, screeny))
    print(pygame.time.Clock().get_fps())
    player1 = characters.player(screenx / 2, screeny / 2)
    p1currentvelx = 0
    p1currentvely = 0
    running = True
    p1rotation = -90
    p1rotationmove = p1rotation
    p1throttling = 0

    # main loop
    while running:
        pygame.time.Clock().tick(60)
        player1.x += p1currentvelx
        player1.y += p1currentvely
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #controls, calculation of velocity and acceleration
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            p1rotation += 5
            #print(f'R: {p1rotation}')
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            p1rotation -= 5
            #print(f'R: {p1rotation}')
        if pygame.key.get_pressed()[pygame.K_UP]:
            p1currentvelx += player1.acceleration * math.cos(p1rotationmove * math.pi / 180)
            p1currentvely += player1.acceleration * math.sin(p1rotationmove * math.pi / 180)
            p1throttling = 1
            p1rotationmove = p1rotation
        #Refresh screen, draw/update player
        if p1throttling == 0 and p1currentvelx != 0 and p1currentvely != 0:
            if p1currentvelx != 0:
                p1currentvelx -= 0.01*p1currentvelx
            if p1currentvely != 0:
                p1currentvely -= 0.01*p1currentvely
        p1throttling = 0
        screen.fill((50,50,50))
        player1.update(screen, p1rotation, player1.x % screenx, player1.y % screeny)
        pygame.display.flip()

if __name__=="__main__":
    main()