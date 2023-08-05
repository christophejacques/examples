from __init__ import P5, pygame
import settings
import time
from player import Player
from ball import Ball
from brick import Brick


class Game:

    def __init__(self):
        self.bricks: list[Brick] = []
        self.level: int = 0

        self.time: float = time.time()
        self.dt: float = 0
        self.player: Player = Player()

        self.load_next_level()

    def load_next_level(self):
        self.balls: list[Ball] = [Ball(*self.player.rect.topleft) for _ in range(1)]

        self.level += 1
        self.bricks.clear()

        if len(settings.LEVEL) >= self.level:
            self.design = settings.LEVEL[self.level-1].copy()

        for i, ligne in enumerate(self.design):
            for j, tb in enumerate(ligne):
                if tb:
                    self.bricks.append(Brick(tb, j, i))

    def activate(self):
        for ball in self.balls:
            ball.active = True

    def update(self):
        if P5.keys[pygame.K_LEFT]: self.player.goto_left()
        elif P5.keys[pygame.K_RIGHT]: self.player.goto_right()
        else: self.player.dont_move()

        self.dt = time.time() - self.time
        self.time = time.time()
        self.player.update(self.dt)

        x = self.player.pos.x + self.player.rect[2]//2
        for ball in self.balls:
            ball.update(self.dt, x)
            ball.checkplayer(self.player)
            ball.checkbricks(self.bricks)

        if not self.bricks:
            self.load_next_level()

    def draw(self):
        P5.CANVAS.fill(0)
        self.player.draw()
        for ball in self.balls:
            ball.draw()
        for brick in self.bricks:
            brick.draw()
