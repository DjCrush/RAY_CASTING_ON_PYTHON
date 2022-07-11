import math


class Bullet:

    def __init__(self, player):
        self.dx = math.cos(math.radians(player.angle)) * 2
        self.dy = math.sin(math.radians(player.angle)) * 2
        self.x = player.x + self.dx * 2
        self.y = player.y + self.dy * 2
        self.is_live = True

    def update(self, big_field):
        if self.is_live:
            self.x += self.dx
            self.y += self.dy
            if self.x < 0 or self.x > 799 or self.y < 0 or self.y > 799 or big_field[int(self.y)][int(self.x)]:
                self.is_live = False

    def __bool__(self):
        return self.is_live
