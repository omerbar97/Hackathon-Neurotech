from pygame.examples.video import x, y

from settings import *
from tetris import Tetris, Text
import sys
import pathlib


class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)
        self.paused = False
        self.popup_time = pg.time.get_ticks()  # new attribute for popup timing
        self.popup_end_time = None  # time when popup will end
        self.popup_state = False  # new attribute for tracking popup state
        self.popup_message = 'You are doing amazing! Keep going!'  # the popup message
        self.profile_pic = pg.image.load('/home/shilopadael/PycharmProjects/Hackathon-Neurotech/assets/sprites/benGorion.jpeg')  # Load the profile picture
        self.game_state = 'running'  # add a ne

    def load_images(self):
        # self.profile_pic = pg.image.load('')  # Load the profile picture
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    def update(self):
        if not self.paused and self.game_state == 'running':
            current_time = pg.time.get_ticks()  # Get the current time
            # If 5 seconds have passed and no popup is currently showing, show the popup
            if current_time - self.popup_time >= 5000 and not self.popup_state:
                self.popup_state = True
                self.popup_time = current_time
                self.game_state = 'popup'  # switch game state
                self.popup_end_time = current_time + 3000  # set the time when popup will end

            self.tetris.update()
            self.clock.tick(FPS)

        elif self.game_state == 'popup':
            current_time = pg.time.get_ticks()
            if current_time >= self.popup_end_time:
                self.game_state = 'running'
                self.popup_state = False

    def draw(self):
        if self.game_state == 'running':
            self.screen.fill(color=BG_COLOR)
            self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
            self.tetris.draw()
            self.text.draw()
            pg.display.flip()

        elif self.game_state == 'popup':
            if self.popup_state:
                # Draw the popup with the profile picture
                self.screen.blit(self.profile_pic,
                                 (150, 150))  # Change (x, y) to the position where you want the picture to appear

                # Create the chat bubble
                bubble_width = 350
                bubble_height = 100
                bubble_color = (255, 255, 255)  # White color for the chat bubble
                text_color = (0, 0, 0)  # Black color for the text
                bubble_surface = pg.Surface((bubble_width, bubble_height),
                                            pg.SRCALPHA)  # Create a new surface with alpha channel
                bubble_rect = pg.Rect(0, 0, bubble_width, bubble_height)
                pg.draw.rect(bubble_surface, bubble_color, bubble_rect,
                             border_radius=20)  # Draw the bubble on the new surface

                # Render the text
                font = pg.font.Font('freesansbold.ttf', 16)  # Choose the font and size of the text
                text = font.render(self.popup_message, True, text_color)  # Black text
                text_rect = text.get_rect()
                text_rect.center = bubble_rect.center  # Center the text in the bubble

                # Draw the text on the bubble surface
                bubble_surface.blit(text, text_rect)

                # Draw the bubble on the screen
                self.screen.blit(bubble_surface, (150 + self.profile_pic.get_width(), 150))

                pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:   # Toggle pause state if 'P' key is pressed
                    self.paused = not self.paused
                else:
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


if __name__ == '__main__':
    app = App()
    app.run()


#TODO: heart rate
#TODO: change the color of the background
#TODO: change the color of the tetris pieces
#TODO: add noise
#TODO add vibration to the screen
#TODO:blur backround.
#TODO: add a picture of someone you kn200ow with a good job
#TODO: make that take the shape and reandoize the colorsrss/

