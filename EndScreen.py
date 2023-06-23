from pygame.examples.eventlist import font

from settings import *


class EndScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.SysFont('frenchscript', 40)
        self.text_box = pg.Rect(75, 75, 100, 50)
        self.active = False
        self.color = pg.Color('purple')
        self.clock = pg.time.Clock()

    def run(self):
        user_ip = ''
        while True:
            for events in pg.event.get():
                if events.type == pg.QUIT:
                    pg.quit()
                    quit()
                if events.type == pg.MOUSEBUTTONDOWN:
                    if self.text_box.collidepoint(events.pos):
                        active = True
                    else:
                        active = False
                if events.type == pg.KEYDOWN:
                    if self.active:
                        if events.key == pg.K_BACKSPACE:
                            user_ip = user_ip[:-1]
                        else:
                            user_ip += events.unicode
            self.screen.fill('pink')
            if self.active:
                color = pg.Color('red')
            else:
                color = pg.Color('purple')
            pg.draw.rect(self.screen, color, self.text_box, 4)
            # surf = font.render(user_ip, True, 'orange')
            # self.screen.blit(surf, (self.text_box.x + 5, self.text_box.y + 5))
            self.text_box.w = max(100, surf.get_width() + 10)
            pg.display.update()
            self.clock.tick(50)
