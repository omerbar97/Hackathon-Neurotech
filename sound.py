import pygame as pg

class Sound:
    def __init__(self, path, channel=0, volume=0.5):
        self.volume = volume
        self.path = path
        pg.mixer.init()
        self.channel = pg.mixer.Channel(channel)  # Use a different channel for each sound
        self.sound = pg.mixer.Sound(self.path)
        self.sound.set_volume(self.volume)

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
        self.channel.play(self.sound, fade_ms=1000)  # Play the sound on the assigned channel

    def stop_sound(self):
        self.channel.fadeout(1000)  # Fade out the sound on the assigned channel

    def fade_out_volume(self):
        self.channel.fadeout(1000)

    def fade_in_volume(self):
        self.channel.fadeout(1000)
