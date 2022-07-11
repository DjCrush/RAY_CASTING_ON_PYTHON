import pygame as pg


class Fps:
    def __init__(self):
        self.font = pg.font.SysFont("Arial", 24, bold=True)
        self.clock = pg.time.Clock()

    def render(self, screen):
        self.clock.tick()
        fps = 'FPS: ' + str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps, 1, pg.Color("RED"))
        screen.blit(fps_t, (0, 0))
        menu = 'CURSOR KEYS - MOVE, SPACE BAR - FIRE'
        menu_t = self.font.render(menu, 1, pg.Color("YELLOW"))
        screen.blit(menu_t, (0, 770))
