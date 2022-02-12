from __init__ import P5, noLoop, background, rect, line, createCanvas, textSize, strokeWeight
from __init__ import fill, noFill, noStroke, circle, Vector, StaticVector, frameRate
from __init__ import *
import random


class VAR:
    size = 10
    w = 0
    h = 0


class Apples:

    def __init__(self):
        self.liste = []

    def init(self):
        self.liste.clear()
        for _ in range(500):
            self.create()

    def create(self):
        x = random.randint(1, VAR.w-2)
        y = random.randint(1, VAR.h-2)
        self.liste.append((x, y))

    def to_draw(self):
        fill(200, 20, 20)
        for a in self.liste:
            yield a[0]*VAR.size, a[1]*VAR.size


class Snake:

    def __init__(self):
        self.tail = []

    def init(self):
        self.tail.clear()
        self.is_alive = True
        self.pos = Vector(VAR.w//2, VAR.h//2)
        self.vel = Vector(1, 0)
        self.key_vel = Vector()

    def eat(self, position, apples):
        for i, apple in enumerate(apples.liste):
            if apple[0] == position.x and apple[1] == position.y:
                del apples.liste[i]
                apples.create()
                return True
                
    def update(self, apples):
        self.vel = self.key_vel
        suivant = StaticVector.add(self.pos, self.vel)
        if not pygame.Rect(0, 0, VAR.w, VAR.h).collidepoint(suivant.x, suivant.y):
            print("OUT", suivant)
            self.is_alive = False
            return 
        if (suivant.x, suivant.y) in [(v.x, v.y) for v in self.tail]:
            print("AUTO BITE", suivant)
            self.is_alive = False
            return 

        self.tail.append(self.pos.copy())
        if not self.eat(suivant, apples):
            self.tail.pop(0)

        self.pos.add(self.vel)

    def to_draw(self):
        fill(255)
        for c in self.tail:
            yield c.x*VAR.size, c.y*VAR.size

        yield self.pos.x*VAR.size, self.pos.y*VAR.size


s = Snake()
a = Apples()


def setup():
    createCanvas(400, 400)
    noStroke()
    VAR.w = P5.WIDTH // VAR.size
    VAR.h = P5.HEIGHT // VAR.size
    s.init()
    a.init()
    print("Board Size:", VAR.w, VAR.h)
    frameRate(60)


def keyPressed():
    if s.is_alive:
        if P5.keyCode == pygame.K_UP:
            if s.vel.y != 1:
                s.key_vel = Vector(0, -1)
        elif P5.keyCode == pygame.K_DOWN:
            if s.vel.y != -1:
                s.key_vel = Vector(0, 1)
        elif P5.keyCode == pygame.K_LEFT:
            if s.vel.x != 1:
                s.key_vel = Vector(-1, 0)
        elif P5.keyCode == pygame.K_RIGHT:
            if s.vel.x != -1:
                s.key_vel = Vector(1, 0)

    else:
        s.init()
        a.init()


def draw():
    background(0)

    for x, y in a.to_draw():
        rect(x, y, VAR.size, VAR.size)
    if P5.frameCount % 4 == 1:
        if s.is_alive:
            s.update(a)

    for x, y in s.to_draw():
        rect(x, y, VAR.size, VAR.size)
