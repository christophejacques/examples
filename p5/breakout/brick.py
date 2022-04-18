import settings
from __init__ import pygame, fill, rect, stroke, text


class TypeBrick:
    NORMALE = 1
    DOUBLE_TAP = 2
    TRIPLE_TAP = 3
    EXPLOSE = 5
    INDESTRUCTIBLE = 99


class Brick:
    SPACE = 2
    WIDTH = settings.SCREEN_WIDTH // settings.COLUMNS_NUMBER - SPACE
    HEIGHT = 20

    def __init__(self, type_brick: TypeBrick, x: int, y: int):
        self.type_brick = type_brick
        self.rect = pygame.Rect(
            Brick.SPACE+x*(Brick.SPACE+Brick.WIDTH), 
            Brick.SPACE+y*(Brick.SPACE+Brick.HEIGHT), Brick.WIDTH, Brick.HEIGHT)

    def angle_to_center(self, centre):
        c0 = pygame.math.Vector2(0, 0)
        cx, cy = centre
        return c0.angle_to(pygame.math.Vector2(cx - self.rect.centerx, cy - self.rect.centery))

    def cote_touche(self, ball):
        # print(f"[brick:{self.rect}, ball:{ball.pos}]")
        gd = []
        hb = []

        if ball.pos.x < self.rect.left:
            gd.append("LEFT")
            dx = self.rect.left - ball.pos.x
        if ball.pos.x > self.rect.right:
            gd.append("RIGHT")
            dx = ball.pos.x - self.rect.right
        if len(gd) == 2: 
            gd.clear()

        if ball.pos.y < self.rect.top:
            hb.append("TOP")
            dy = self.rect.top - ball.pos.y 
        if ball.pos.y > self.rect.bottom:
            hb.append("BOTTOM")
            dy = ball.pos.y - self.rect.bottom

        if len(hb) == 2: 
            hb.clear()
        cotes = gd + hb

        return cotes

    def draw(self):
        stroke(100, 100, 0)
        fill(50, 150, 80)
        rect(*self.rect)
        stroke(0)
        text(self.type_brick, self.rect.left - 8 + self.rect.width//2, self.rect.top-5)
