import pygame
import settings
from __init__ import *


class Player:
    def __init__(self):
        self.init()
        
    def init(self):
        self.speed = 1000
        self.accel = 0.1
        self.vel = pygame.math.Vector2((0, 0))

        self.pos = pygame.math.Vector2((settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT - 30))
        self.rect = pygame.Rect(*self.pos, settings.SCREEN_WIDTH//10, settings.SCREEN_HEIGHT//40)
        self.pos.x -= self.rect.width//2

    def dont_move(self):
        self.vel.x = 0

    def goto_left(self):
        self.vel.x -= self.accel
        self.vel.x = self.vel.x if self.vel.x > -1 else -1

    def goto_right(self):
        self.vel.x += self.accel
        self.vel.x = self.vel.x if self.vel.x < 1 else 1
        # print(self.vel)

    def update(self, dt):
        self.pos.x += self.vel.x * self.speed * dt
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x + self.rect.width > settings.SCREEN_WIDTH:
            self.pos.x = settings.SCREEN_WIDTH - self.rect.width
        self.rect.left = self.pos.x

    def draw(self):
        fill(0, 50, 50)
        stroke(20, 200, 150)
        # line(self.rect.centerx, 0, self.rect.centerx, self.rect.centery)
        rect(*self.rect)
