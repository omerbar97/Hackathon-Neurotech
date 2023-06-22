from settings import *
from Block import *

class Tetromino:
    def __init__(self, tetris):
        self.tetris = tetris
        Block(self, (4,7),'orange')
        self.rotation = 0

    def update(self):
        pass