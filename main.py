import math
import pygame as pg
from collections import namedtuple

SIZE = namedtuple('SIZE', ('WIDTH', 'HEIGHT'))
SIZE_SCREEN = SIZE(800, 800)
SIZE_FIELD = SIZE(20, 20)

field = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
]

big_field = []


class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.direction = 0

    def update(self):
        self.angle += self.direction
        if self.angle == 360:
            self.angle -= 360
        elif self.angle == -1:
            self.angle += 360


def create_big_field():
    global big_field
    for line in field:
        big_line = []
        for sym in line:
            big_line += [sym] * 40
        for _ in range(40):
            big_field.append(big_line)


def draw_field(screen):
    for y in range(len(field)):
        for x in range(len(field[0])):
            if field[y][x]:
                pg.draw.rect(screen, (255, 0, 0), (x * 40, y * 40, 40, 40))


def ray_casting(screen, player):
    for alpha in range(player.angle - 45, player.angle + 45):
        dx = math.cos(alpha * math.pi / 180)
        dy = math.sin(alpha * math.pi / 180)
        x = player.x
        y = player.y
        while True:
            x += dx
            y += dy
            if x < 0 or x > 799 or y < 0 or y > 799 or big_field[int(y)][int(x)]:
                x -= dx
                y -= dy
                break
        pg.draw.line(screen, (0, 0, 255), (int(player.x), int(player.y)), (int(x), int(y)))


def main():
    pg.init()
    screen = pg.display.set_mode(SIZE_SCREEN)
    is_running = True
    create_big_field()

    player = Player(180, 200, 250)
    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    player.x += math.cos(player.angle * math.pi / 180)
                    player.y += math.sin(player.angle * math.pi / 180)
                if event.key == pg.K_DOWN:
                    player.x -= math.cos(player.angle * math.pi / 180)
                    player.y -= math.sin(player.angle * math.pi / 180)
                if event.key == pg.K_LEFT:
                    player.direction = -1
                if event.key == pg.K_RIGHT:
                    player.direction = 1
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                    player.direction = 0

        player.update()
        screen.fill((0, 0, 0))
        draw_field(screen)
        ray_casting(screen, player)
        pg.display.flip()


if __name__ == '__main__':
    main()
