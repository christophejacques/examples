import pygame
import settings
from __init__ import fill, stroke, circle, noFill, line, rect
from random import random, choice


class Ball:

    def __init__(self, posx, posy):
        self.radius = 10
        self.posy = posy - self.radius
        self.posx = 0
        self.speed = 400
        self.init()

    def init(self):
        self.active = False
        self.pos = pygame.math.Vector2((self.posx, self.posy-self.radius))
        self.pos.x = self.posx
        self.pos.y = self.posy
        self.rect = pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, 2*self.radius, 2*self.radius)
        # self.vel = pygame.math.Vector2((choice([-1, 1])*random(), -1))
        self.vel = pygame.math.Vector2((0.3, -1))
        self.vel = self.vel.normalize()

    def check_walls(self):
        if self.pos.x - self.radius < 0: 
            self.pos.x = self.radius
            self.vel.x = -self.vel.x
        elif self.pos.x > settings.SCREEN_WIDTH - self.radius:
            self.pos.x = settings.SCREEN_WIDTH - self.radius
            self.vel.x = -self.vel.x

        if self.pos.y - self.radius < 0: 
            self.pos.y = self.radius 
            self.vel.y = -self.vel.y

    def checkbricks(self, bricks):
        tmp_bricks = bricks.copy()
        c = self.rect.collidelist(tmp_bricks)
        cotes = []
        while c != -1: 
            brick = tmp_bricks[c]
            res = brick.cote_touche(self)
            # print(res, brick.rect, self.pos, self.vel, end=", ")
            cotes.extend(res)

            # print(brick.type_brick)
            if brick.type_brick == 1:
                bricks.remove(brick)
            else:
                brick.type_brick -= 1
                
            tmp_bricks.pop(c)
            c = self.rect.collidelist(tmp_bricks)
        
        if cotes:
            if "LEFT" in cotes and self.vel.x < 0: 
                while "LEFT" in cotes:
                    cotes.remove("LEFT")
            if "RIGHT" in cotes and self.vel.x > 0: 
                while "RIGHT" in cotes:
                    cotes.remove("RIGHT")
            if "TOP" in cotes and self.vel.y < 0: 
                while "TOP" in cotes:
                    cotes.remove("TOP")
            if "BOTTOM" in cotes and self.vel.y > 0: 
                while "BOTTOM" in cotes:
                    cotes.remove("BOTTOM")

            nb_left = cotes.count("LEFT")
            nb_right = cotes.count("RIGHT")
            nb_top = cotes.count("TOP")
            nb_bottom = cotes.count("BOTTOM")

            # print()
            horiz = nb_left if nb_left > nb_right else nb_right
            verti = nb_bottom if nb_bottom > nb_top else nb_top

            if verti > horiz:
                # print("VERTICAL")
                self.vel.y = -self.vel.y
                return 
            elif horiz > verti:
                # print("HORIZONTAL")
                self.vel.x = -self.vel.x
                return 
            else:
                # print("COIN", cotes)
                if abs(self.vel.x) > abs(self.vel.y):
                    self.vel.x = -self.vel.x
                else:
                    self.vel.y = -self.vel.y
                return

        if cotes:
            if "LEFT" in cotes and "RIGHT" not in cotes or \
               "RIGHT" in cotes and "LEFT" not in cotes: 
                self.vel.x = -self.vel.x

            elif "BOTTOM" in cotes and "TOP" not in cotes or \
                 "TOP" in cotes and "BOTTOM" not in cotes:
                self.vel.y = -self.vel.y

    def checkplayer(self, player):
        if self.rect.colliderect(player.rect):
            dgauche = player.rect.left - self.rect.centerx
            ddroite = self.rect.centerx - player.rect.right
            dheight = player.rect.top - self.rect.centery

            if dgauche > 0 and pygame.math.Vector2(0, 0).angle_to(pygame.math.Vector2(dgauche, dheight)) < 45:
                self.vel.x = -self.vel.x
                return 

            elif ddroite > 0 and pygame.math.Vector2(0, 0).angle_to(pygame.math.Vector2(ddroite, dheight)) < 45:
                self.vel.x = -self.vel.x
                return 

            dx = self.pos.x-player.rect.centerx
            if dx == 0:
                vn = pygame.math.Vector2(0, -1)
            else:
                vn = pygame.math.Vector2(dx, -player.rect.width).normalize()

            self.vel += vn + player.vel
            self.pos.y = self.posy
            self.vel.y = -1
            self.vel = self.vel.normalize()

        elif self.pos.y + self.radius > settings.SCREEN_HEIGHT:
            self.init()

    def update(self, dt, posx=None):
        self.dt = dt
        if not self.active:
            self.rect = pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, 2*self.radius, 2*self.radius)
            self.pos.x = posx
            return

        self.posx = posx
        self.pos += self.vel * self.speed * self.dt
        self.rect = pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, 2*self.radius, 2*self.radius)
        self.check_walls()

    def draw(self):
        stroke(20, 200, 150)
        fill(150, 150, 150)
        circle(*self.pos, self.radius)
        stroke(250, 100, 0)
        # line(*self.pos, *(self.pos+100*self.radius*self.vel))
        noFill()
        # rect(*self.rect)
