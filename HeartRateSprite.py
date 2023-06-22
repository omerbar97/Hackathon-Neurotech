import pygame
import math

class HeartRateSprite(pygame.sprite.Sprite):

    def __init__(self, width, height, amplitude, frequency, line_color, speed):
        super().__init__()

        self.width = width
        self.height = height
        self.amplitude = amplitude
        self.frequency = frequency
        self.line_color = line_color
        self.speed = speed
        self.current_x = 0

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (530, 120)

    def convert_to_heart_rate(amplitude, frequency):
        heart_rate = amplitude * frequency * 60
        return heart_rate

    def update(self):
        self.image.fill((0, 0, 0, 0))  # Clear the surface

        points = []
        for x in range(self.width):
            y = self.amplitude * math.sin(
                2 * math.pi * self.frequency * (x + self.current_x) / self.width) + self.height / 2
            points.append((x, y))

        pygame.draw.lines(self.image, self.line_color, False, points, 3)

        self.current_x -= self.speed