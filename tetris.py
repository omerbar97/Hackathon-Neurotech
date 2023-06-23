import random
import time

from EndScreen import EndScreen
from MovingBall import MovingBall
from settings import *
import math

from sound import Sound
from tetromino import Tetromino
import pygame.freetype as ft
from HeartRateSprite import *


class Text:
    def __init__(self, app, heartRateText):
        self.app = app
        self.heartRateText = heartRateText
        self.font = ft.Font(FONT_PATH2)

    def get_color(self):
        time = pg.time.get_ticks() * 0.001
        n_sin = lambda t: (math.sin(t) * 0.5 + 0.5) * 255
        return n_sin(time * 0.5), n_sin(time * 0.2), n_sin(time * 0.9)

    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.02),
                            text='TETRIS', fgcolor=self.get_color(),
                            size=TILE_SIZE * 1.65, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.6, WIN_H * 0.28),
                            text="Heart Rate: ", fgcolor='white',
                            size=TILE_SIZE * 0.6, bgcolor=self.heartRateText.font_color)
        self.font.render_to(self.app.screen, (WIN_W * 0.85, WIN_H * 0.28),
                            text=str(self.heartRateText.heart_rate), fgcolor=self.heartRateText.font_color,
                            size=TILE_SIZE * 0.6)
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.40),
                            text='next', fgcolor='orange',
                            size=TILE_SIZE * 1.4, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.72),
                            text='score', fgcolor='orange',
                            size=TILE_SIZE * 1.4, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.8),
                            text=f'{self.app.tetris.score}', fgcolor='white',
                            size=TILE_SIZE * 1.8)


class Tetris:
    def __init__(self, app, heart_rate_visualization, randomLst):
        self.app = app
        self.heartRate = heart_rate_visualization
        self.sprite_group = pg.sprite.Group()
        self.sprite_group.add(self.heartRate)
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.speed_up = False
        self.tetrominoLst = []
        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
        self.sound = Sound('assets/end_line.wav', volume=1)
        self.movingBall = MovingBall(150, 150, 25, (255, 255, 255), 10, randomLst)

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0

    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]

                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    self.sound.play_sound(1)
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0

                self.full_lines += 1

    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]

    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            return True

    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                self.app.online = False
            else:
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetrominoLst.append(self.tetromino)
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True

    def draw_grid(self, shake_offset_x, shake_offset_y):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'black',
                             (x * TILE_SIZE + shake_offset_x, y * TILE_SIZE + shake_offset_y, TILE_SIZE, TILE_SIZE), 1)

    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        if self.app.isActive:
            self.movingBall.update()
        self.sprite_group.update()

    def draw(self, shake_offset_x, shake_offset_y):
        self.draw_grid(shake_offset_x, shake_offset_y)
        if self.app.isActive:
            self.movingBall.draw(self.app.screen)
        self.sprite_group.draw(self.app.screen)
