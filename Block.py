from settings import *
import Tetromino
import math

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos, color):
        self.tetromino = tetromino
        self.pos = pos
        self.color = color
        super().__init__(tetromino.tetris.spriteGroup)
        self.image = pg.Surface([GRID_SIZE, GRID_SIZE])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE

