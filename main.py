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
            p1rotation += 1
            #print(f'R: {p1rotation}')
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            p1rotation -= 1
            #print(f'R: {p1rotation}')
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            p1currentvelx -= 1
            p1currentvely -= 1
            print(f'Y: {p1currentvely}')
            print(f'X: {p1currentvelx}')
        if pygame.key.get_pressed()[pygame.K_UP] and player1.maxspeed * -1 < p1currentvely < player1.maxspeed and player1.maxspeed * -1 < p1currentvelx < player1.maxspeed:
            p1currentvelx += math.cos(p1rotation * math.pi / 180)
            p1currentvely += math.sin(p1rotation * math.pi / 180)
            print(f'Y: {p1currentvely}')
            print(f'X: {p1currentvelx}')
        #Refresh screen, draw/update player
        screen.fill((50,50,50))
        player1.update(screen, p1rotation, player1.x % 1280, player1.y % 720)
        pygame.display.flip()

if __name__=="__main__":
    main()