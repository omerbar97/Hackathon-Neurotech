from settings import *


class MovingBall(pg.sprite.Sprite):
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.start = 50
        self.end = 750

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        self.x += self.speed
        if self.x < self.start or self.x > self.end:
            self.speed *= -1
