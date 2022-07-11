import math
import pygame as pg
from player import Player
from fps import Fps
from bullet import Bullet
from collections import namedtuple

SIZE = namedtuple('SIZE', ('WIDTH', 'HEIGHT'))
SIZE_SCREEN = SIZE(1800, 800)
SIZE_FIELD = SIZE(20, 20)
MAX_DOTS = 1000

field = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0],
]

big_field = []


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
            if field[y][x] == 2:
                pg.draw.rect(screen, (255, 0, 0), (x * 40, y * 40, 40, 40))
            elif field[y][x] == 1:
                pg.draw.rect(screen, (0, 255, 255), (x * 40, y * 40, 40, 40))


def draw_bullets(screen, player, bullets):
    for bul in bullets:
        distance = math.dist((bul.x, bul.y), (player.x, player.y))

        vec_bul_norm = (bul.x - player.x) / distance, (bul.y - player.y) / distance
        vec_play_norm = math.cos(math.radians(player.angle)), math.sin(math.radians(player.angle))
        alpha = 0
        normal = vec_bul_norm[0] * vec_play_norm[1] - vec_bul_norm[1] * vec_play_norm[0]
        try:
            alpha = math.degrees(math.acos(vec_play_norm[0] * vec_bul_norm[0] + vec_play_norm[1] * vec_bul_norm[1]))
        except ValueError:
            print('alpha = ', alpha)

        pg.draw.circle(screen, (255, 255, 255), (bul.x, bul.y), 2)

        if alpha < 30:
            betta = (90 - alpha) if normal > 0 else (90 + alpha)
            radius_bullet = int(16 * 150 / distance)
            x1 = (betta - 30) / 60 * MAX_DOTS
            pg.draw.circle(screen, (255, 255, 255), (x1 + 300, 400), radius_bullet)


def ray_casting(screen, player):
    color = 0
    for x in range(0, MAX_DOTS):
        alpha = player.angle - 30 + x / (MAX_DOTS / 60)
        dx = math.cos(math.radians(alpha)) * 4
        dy = math.sin(math.radians(alpha)) * 4
        start_x = player.x
        start_y = player.y
        is_wall = False
        while True:
            start_x += dx
            start_y += dy
            if start_x < 0 or start_x > 799 or start_y < 0 or start_y > 799:
                start_x -= dx
                start_y -= dy
                break
            if big_field[int(start_y)][int(start_x)]:
                color = (255, 0, 0) if big_field[int(start_y)][int(start_x)] == 2 else (0, 255, 255)
                start_x -= dx
                start_y -= dy
                is_wall = True
                break
        pg.draw.line(screen, (50, 50, 50), (int(player.x), int(player.y)), (int(start_x), int(start_y)))
        if is_wall:
            distance = math.dist((player.x, player.y), (start_x, start_y))
            distance *= math.cos(math.radians(alpha - player.angle))  # remove the fisheye effect
            try:
                if distance > 1:
                    half_height_wall = int(16 * SIZE_SCREEN.HEIGHT / distance)
                    pg.draw.line(screen, color, (x + 800, 400 - half_height_wall),
                                 (x + 800, 400 + half_height_wall))
            except TypeError:
                print(x, distance)


def main():
    pg.init()
    screen = pg.display.set_mode(SIZE_SCREEN)
    is_running = True
    create_big_field()
    player = Player()
    fps = Fps()
    bullets = list()
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
                if event.key == pg.K_SPACE:
                    bullets.append(Bullet(player))
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                    player.rotation_direction = 0
                if event.key == pg.K_UP:
                    player.moving_forward = False
                if event.key == pg.K_DOWN:
                    player.moving_backwards = False

        player.update(big_field)
        for bullet in bullets:
            bullet.update(big_field)
        bullets = list(filter(None, bullets))

        screen.fill((0, 0, 0))
        pg.draw.rect(screen, (0, 191, 255), (800, 0, 1000, 400))
        pg.draw.rect(screen, (0, 191, 0), (800, 400, 1000, 400))
        ray_casting(screen, player)
        draw_field(screen)
        draw_bullets(screen, player, bullets)
        fps.render(screen)
        pg.display.flip()


if __name__ == '__main__':
    main()
