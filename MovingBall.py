import random

from settings import *
import pygame.freetype as ft

class MovingBall(pg.sprite.Sprite):
    def __init__(self, x, y, radius, color, speed, randomLst):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.ySpeed = 2
        self.start = 20
        self.end = 500
        self.font = ft.Font(FONT_PATH2)
        self.index = 0
        self.lst = randomLst

    def draw(self, screen):
        letter = self.lst[self.index]
        pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        self.font.render_to(screen, (int(self.x) - 5, int(self.y) - 15),
                            text=letter, fgcolor='black',
                            size=TILE_SIZE * 0.6)

    def update(self):
        self.x += self.speed

        # on random demand change the y
        if random.randint(0, 3) == 0:
            self.y += 1 * self.ySpeed
        if self.y < 20 or self.y > WIN_H:
            self.ySpeed *= -1

        if self.x < self.start or self.x > self.end:
            self.index += 1
            self.index %= len(self.lst)
            self.speed *= -1
