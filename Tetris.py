from Tetromino import *
from settings import *

class Tetris:

    def __init__(self, app):
        self.app = app
        self.spriteGroup = pg.sprite.Group()
        self.tetromino = Tetromino(self)

    def draw_gird(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'black', (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)


    def update(self):
        self.tetromino.update()
        self.spriteGroup.update()
        pass

    def draw(self):
        self.draw_gird()
        self.spriteGroup.draw(self.app.screen)