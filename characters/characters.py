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
        self.deceleration = 0.01
    def update(self, screen, angle, x, y):
        newimage = pygame.transform.rotate(self.icon, angle * -1)
        screen.blit(newimage, (x - int(newimage.get_width() / 2) , y - int(newimage.get_height() / 2) % 720))

class projectile(object):
    def __init__(self, x, y, cos, sin):
        self.icon = pygame.image.load('characters/blast.png').convert_alpha()
        self.x = x
        self.y = y
        self.traveltime = 0
        self.cos = cos
        self.sin = sin
        self.velocity = 20
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 5)