import pygame as pg
import sys

class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Tetris Game NeurotechBIU")
        self.screen = pg.display.set_mode((800, 700))
        self.clock = pg.time.Clock()

    def update(self):
        self.clock = pg.time.Clock()