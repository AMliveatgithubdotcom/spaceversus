import pygame

class player(object):
    def __init__(self, x, y):
        self.icon = pygame.image.load('characters/canary.png').convert_alpha()
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.vel = 5
        self.maxspeed = 10
        self.acceleration = 0.1
    def update(self, screen, angle, x, y):
        newimage = pygame.transform.rotate(self.icon, angle * -1)
        screen.blit(newimage, (x - int(newimage.get_width() / 2) , y - int(newimage.get_height() / 2) % 720))

