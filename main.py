import math
import pygame as pg
from collections import namedtuple

SIZE = namedtuple('SIZE', ('WIDTH', 'HEIGHT'))
SIZE_SCREEN = SIZE(1800, 800)
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

    def __init__(self, x=180, y=200, angle=250):
        self.x = x
        self.y = y
        self.angle = angle
        self.rotation_direction = 0
        self.moving_forward = False
        self.moving_backwards = False

    def update(self):
        dx = math.cos(math.radians(self.angle))
        dy = math.sin(math.radians(self.angle))
        if self.moving_forward:
            self.x += dx
            self.y += dy
            if big_field[int(self.y)][int(self.x)] or self.x < 0 or self.x > 799:
                self.x -= dx
                self.y -= dy

        elif self.moving_backwards:
            self.x -= dx
            self.y -= dy
            if big_field[int(self.y)][int(self.x)] or self.y < 0 or self.y > 799:
                self.x += dx
                self.y += dy

        self.angle += self.rotation_direction
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
    x1 = 0
    for alpha in range(0, 91):
        alpha = player.angle - 45 + alpha
        dx = math.cos(math.radians(alpha)) * 2
        dy = math.sin(math.radians(alpha)) * 2
        x = player.x
        y = player.y
        is_wall = False
        while True:
            x += dx
            y += dy
            if x < 0 or x > 799 or y < 0 or y > 799:
                x -= dx
                y -= dy
                break
            if big_field[int(y)][int(x)]:
                x -= dx
                y -= dy
                is_wall = True
                break
        pg.draw.line(screen, (0, 0, 255), (int(player.x), int(player.y)), (int(x), int(y)))
        if is_wall:
            distance = math.dist((player.x, player.y), (x, y))
            distance *= math.cos(math.radians(alpha - player.angle))  # remove the fisheye effect
            try:
                if distance > 0:
                    half_height_wall = int(16 * SIZE_SCREEN.HEIGHT / distance)
                    pg.draw.line(screen, (0, 255, 255), (int(x1) + 800, 400 - half_height_wall),
                                 (int(x1) + 800, 400 + half_height_wall))
            except TypeError:
                print(x1, distance)

        x1 += (SIZE_SCREEN.WIDTH - 800) / 90


def main():
    pg.init()
    screen = pg.display.set_mode(SIZE_SCREEN)
    is_running = True
    create_big_field()

    player = Player()
    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    player.moving_forward = True
                    player.moving_backwards = False
                elif event.key == pg.K_DOWN:
                    player.moving_forward = False
                    player.moving_backwards = True
                if event.key == pg.K_LEFT:
                    player.rotation_direction = -1
                elif event.key == pg.K_RIGHT:
                    player.rotation_direction = 1
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                    player.rotation_direction = 0
                if event.key == pg.K_UP:
                    player.moving_forward = False
                if event.key == pg.K_DOWN:
                    player.moving_backwards = False

        player.update()
        screen.fill((0, 0, 0))
        draw_field(screen)
        ray_casting(screen, player)
        pg.display.flip()


if __name__ == '__main__':
    main()
