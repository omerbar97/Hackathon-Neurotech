import pygame


class Sound:
    def __init__(self):
        self.volume = 0.5
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound('/home/tomer/Downloads/brain-damage-148577.mp3')
        self.sound.set_volume(self.volume)
        self.sound.play()

    def set_volume(self, value):
        self.volume = value

    def get_volume(self):
        return self.volume

    def play_sound(self, alpha):
        if alpha == 1:
            new_volume = self.get_volume() + 0.1
            self.set_volume(new_volume)
            if self.get_volume() > 1:
                self.set_volume(1)
        elif alpha == 2:
            new_volume = self.get_volume() - 0.1
            self.set_volume(new_volume)
            if self.get_volume() < 0:
                self.set_volume(0)

        self.sound.set_volume(self.get_volume())
        self.sound.play()