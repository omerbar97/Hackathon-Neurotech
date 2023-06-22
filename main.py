import 
import sys

class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Tetris Game NeurotechBIU")
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.clock = pg.time.Clock()

    def update(self):
        self.clock = pg.time.Clock()

    def draw(self):
        self.screen.fill((0, 0, 0))
        pg.display.flip()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.run()