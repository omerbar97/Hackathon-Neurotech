import random
import threading
import time

from HeartRateSprite import HeartRateSprite, HeartRateText
from MovingBall import MovingBall
from settings import *
from tetris import Tetris, Text
import sys
import pathlib
from sound import Sound


def update_heart_rate_value(heart_rate_visualization, heart_rate_values, heart_rate_text_in, app, sound_danger, sound_track):

    while True:
        # sound_danger.volume = 0
        sound_track.play_sound(1)
        # sound_danger.play_sound(1)
        for value in heart_rate_values:
            proximity = abs(value - 2)
            probability = 1 - proximity  # Probability inversely proportional to proximity to 2

            # Calculate the mean and standard deviation based on probability
            mean = (60 - 5) * probability + 5
            std_deviation = (mean - 5) / 3

            mean2 = (8 - 2) * probability + 2
            std_deviation2 = (mean2 - 2) / 2

            # Generate a new value using a Gaussian distribution
            new_value = random.gauss(mean, std_deviation)
            new_value = max(5, min(60, new_value))  # Ensure the generated value is within the range [5, 60]
            heart_value = max(50, min(200, 5*new_value))
            print(new_value)
            new_speed = random.gauss(mean2, std_deviation2)
            new_speed = max(2, min(8, new_speed))  # Ensure the generated value is within the range [2, 8]

            heart_rate_visualization.amplitude = new_value
            heart_rate_visualization.speed = new_speed
            heart_rate_text_in.heart_rate = heart_value
            # converting to int
            heart_rate_text_in.heart_rate = int(heart_rate_text_in.heart_rate)
            heart_rate_text_in.text = 'Heart Rate: '

            lst = []
            if value > 1.1:
                # if(sound_track.is_playing()):
                #     sound_track.stop_sound()
                # if(not sound_danger.is_playing()):
                #     sound_danger.play_sound(1)
                sound_track.volume = 1
                app.isActive = True
                app.shake_screen(10 , 40)
                sound_track.volume = 0
                sound_danger.volume = 0
                heart_rate_visualization.line_color = 'red'
                heart_rate_text_in.font_color = 'red'
                app.field_color = (200, 0, 0)
                tetrominoLst = app.tetris.tetrominoLst
                for tetromino in tetrominoLst:
                    for block in tetromino.blocks:
                        l = random.randint(0, 1)
                        if(l == 0):
                            block.isBlur = True
                            lst.append(block)

            else:
                heart_rate_visualization.line_color = 'green'
                heart_rate_text.font_color = 'green'
                app.field_color = FIELD_COLOR
                sound_track.volume = 0.5
                sound_danger.volume = 0
                # if(not sound_track.is_playing()):
                #     sound_track.play_sound(1)
                # if(sound_danger.is_playing()):
                #     sound_danger.stop_sound()
            time.sleep(random.uniform(1, 2))

            # clearing the blur
            for block in lst:
                block.isBlur = False


def change_background_color(app, heart_rate_values, lock):
    for value in heart_rate_values:
        lock.acquire()
        if value > 1.5:
            app.field_color = (200, 0, 0)
        else:
            app.field_color = FIELD_COLOR
        lock.release()
    time.sleep(1)


num_samples = 1000
heart_rate_values = [random.uniform(0, 2) for _ in range(num_samples)]
print(heart_rate_values)
heart_rate = HeartRateSprite(300, 150, 50, 10, 'green', 2)
heart_rate_text = HeartRateText(530, 120, 'Heart Rate', 30, 'white')

class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris NeuroTech')
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.bg_color = BG_COLOR
        self.field_color = FIELD_COLOR
        self.images, self.files = self.load_images()
        self.tetris = Tetris(self, heart_rate)
        self.text = Text(self, heart_rate_text)
        self.isActive = False
        self.shake_intensity = 0
        self.shake_duration = 0

    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images, files

    def shake_screen(self, intensity, duration):
        self.isActive = True
        self.shake_intensity = intensity
        self.shake_duration = duration

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(color=self.bg_color)
        self.screen.fill(color=self.field_color, rect=(0, 0, *FIELD_RES))
        if self.isActive:
            # Generate random offsets for shake effect
            shake_offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            shake_offset_y = random.randint(-self.shake_intensity, self.shake_intensity)

            # Apply shake effect to the screen position
            screen_x = self.screen.get_width() // 2 + shake_offset_x
            screen_y = self.screen.get_height() // 2 + shake_offset_y
            self.screen.fill(self.bg_color)
            # Draw game objects here using the adjusted screen position

            self.tetris.draw(shake_offset_x, shake_offset_y)
            self.shake_duration -= 1
            if self.shake_duration <= 0:
                self.isActive = False

        else:
            self.tetris.draw(0, 0)

        self.text.draw()
        pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

app = App()
l1 = Sound('assets/brain-damage.mp3', 1)
l1.stop_sound()

l2 = Sound('assets/sound_track.mp3', 2)

lock = threading.Lock()
update_thread = threading.Thread(target=update_heart_rate_value,
                                 args=(heart_rate, heart_rate_values, heart_rate_text, app, l1, l2))
update_thread.start()



if __name__ == '__main__':
    app.run()
