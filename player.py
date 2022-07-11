import math


class Player:

    def __init__(self, x=180, y=200, angle=250):
        self.x = x
        self.y = y
        self.angle = angle
        self.rotation_direction = 0
        self.moving_forward = False
        self.moving_backwards = False

    def update(self, big_field):
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
