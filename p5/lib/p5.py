import pygame
import math
import random

from typing import Tuple, Self


class HISTO:
    BGCOLOR: list = []
    COLORB: list = []
    COLORF: list = []
    STROKE_WEIGHT: list = []
    STROKE: list = []
    FILL: list = []
    TRANSLATE: list = []


class P5:
    CANVAS: pygame.surface.Surface 
    WINDOW_STATE: list = ["NORMAL"]
    LOOP: bool = True
    FRAME_RATE: int = 60
    WIDTH, HEIGHT = 0, 0
    BGCOLOR: Tuple[int, ...] = (0, 0, 0)
    COLORB: Tuple[int, ...] = (0, 0, 0)
    COLORF: Tuple[int, ...] = (0, 0, 0)
    STROKE_WEIGHT: int = 1
    STROKE: bool = True
    FILL: bool = True
    RECT_MODE: str = ""
    FONT: pygame.font.Font
    TRANSLATE: list = [0, 0]

    mouseX, mouseY = 0, 0
    pmouseX, pmouseY = 0, 0
    mouseIsPressed: int = 0
    keys: dict = {}
    keyIsPressed: bool = False
    keyCode: int = 0
    frameCount: int = 0
    joysticks: list = []
    

def preload():
    pass  # = lambda: None


def setup():
    pass  # = lambda: None


def draw():
    pass  # = lambda: None


def mousePressed():
    pass  # = lambda: None


def mouseReleased():
    pass  # = lambda: None


def keyPressed():
    pass  # = lambda: None


def keyReleased():
    pass  # = lambda: None


def JoyMotion():
    pass  # = lambda: None


def JoyButtonReleased():
    pass  # = lambda: None


def JoyButtonPressed():
    pass  # = lambda: None


def noLoop() -> None: 
    P5.LOOP = False


def createCanvas(w: int, h: int) -> None:
    pygame.init()
    P5.CANVAS = pygame.display.set_mode((w, h))
    P5.WIDTH, P5.HEIGHT = w, h
    P5.FONT = pygame.font.SysFont("comicsans", 30)


def resizeCanvas(w, h) -> None:
    P5.CANVAS = pygame.display.set_mode((w, h))
    P5.WIDTH, P5.HEIGHT = w, h


def fullscreen(*check):
    if len(check) == 1:
        if check[0]:
            P5.WINDOW_STATE.append("FULLSCREEN")
            P5.CANVAS = pygame.display.set_mode((1900, 1000))
        else:
            try:
                P5.WINDOW_STATE.remove("FULLSCREEN")
            except Exception:
                pass
            P5.CANVAS = pygame.display.set_mode((P5.WIDTH, P5.HEIGHT))
    else:
        return "FULLSCREEN" in P5.WINDOW_STATE


def frameRate(fps) -> None:
    P5.FRAME_RATE = fps


def noStroke() -> None:
    P5.STROKE = False


def stroke(*s: int) -> None:
    P5.STROKE = True
    if len(s) == 1:
        P5.COLORF = (s[0],)*3
    else:
        P5.COLORF = s


def strokeWeight(w) -> None:
    P5.STROKE_WEIGHT = w


def push() -> None:
    HISTO.BGCOLOR.append(P5.BGCOLOR)
    HISTO.COLORB.append(P5.COLORB)
    HISTO.COLORF.append(P5.COLORF)
    HISTO.STROKE_WEIGHT.append(P5.STROKE_WEIGHT)
    HISTO.STROKE.append(P5.STROKE)
    HISTO.FILL.append(P5.FILL)
    HISTO.TRANSLATE.append(P5.TRANSLATE)
    

def pop() -> None:
    if HISTO.BGCOLOR: 
        P5.BGCOLOR = HISTO.BGCOLOR.pop()
    if HISTO.COLORB: 
        P5.COLORB = HISTO.COLORB.pop()
    if HISTO.COLORF: 
        P5.COLORF = HISTO.COLORF.pop()
    if HISTO.STROKE_WEIGHT: 
        P5.STROKE_WEIGHT = HISTO.STROKE_WEIGHT.pop()
    if HISTO.STROKE: 
        P5.STROKE = HISTO.STROKE.pop()
    if HISTO.FILL: 
        P5.FILL = HISTO.FILL.pop()
    if HISTO.TRANSLATE: 
        P5.TRANSLATE = HISTO.TRANSLATE.pop()
    

def textSize(size) -> None:
    P5.FONT = pygame.font.SysFont("comicsans", size)


def textRect(texte: str) -> pygame.surface.Surface:
    return P5.FONT.render("{}".format(texte), False, P5.COLORF)
    

def text(texte, x, y) -> None:
    texte_surf = P5.FONT.render("{}".format(texte), False, P5.COLORF)
    P5.CANVAS.blit(texte_surf, (P5.TRANSLATE[0]+x, P5.TRANSLATE[1]+y))


def noFill() -> None:
    P5.FILL = False


def fill(*f) -> None:
    P5.FILL = True
    if len(f) == 1:
        P5.COLORB = (f[0],)*3
    else:
        P5.COLORB = f


def color(*c) -> Tuple[int, int, int]:
    if len(c) == 1:
        return (c[0],)*3
    else:
        return c


def background(*color) -> None:
    if len(color) == 1:
        P5.BGCOLOR = (color[0],)*3
    else:
        P5.BGCOLOR = color
    P5.CANVAS.fill(P5.BGCOLOR)


def translate(dx, dy) -> None:
    P5.TRANSLATE[0] += dx
    P5.TRANSLATE[1] += dy


def point(x, y) -> None:
    if P5.STROKE:
        P5.CANVAS.set_at((P5.TRANSLATE[0]+x, P5.TRANSLATE[1]+y), P5.COLORF)
        

def line(x1, y1, x2, y2) -> None:
    if P5.STROKE:
        pygame.draw.line(P5.CANVAS, P5.COLORF, 
            (P5.TRANSLATE[0]+x1, P5.TRANSLATE[1]+y1), (P5.TRANSLATE[0]+x2, P5.TRANSLATE[1]+y2), 
            P5.STROKE_WEIGHT)


def triangle(p1, p2, p3) -> None:
    if P5.FILL:
        pygame.draw.polygon(P5.CANVAS, P5.COLORB, 
            [(P5.TRANSLATE[0]+p1[0], P5.TRANSLATE[1]+p1[1]), 
             (P5.TRANSLATE[0]+p2[0], P5.TRANSLATE[1]+p2[1]), 
             (P5.TRANSLATE[0]+p3[0], P5.TRANSLATE[1]+p3[1])], )

    if P5.STROKE:
        pygame.draw.polygon(P5.CANVAS, P5.COLORB, 
            [(P5.TRANSLATE[0]+p1[0], P5.TRANSLATE[1]+p1[1]), 
             (P5.TRANSLATE[0]+p2[0], P5.TRANSLATE[1]+p2[1]), 
             (P5.TRANSLATE[0]+p3[0], P5.TRANSLATE[1]+p3[1])], 
             P5.STROKE_WEIGHT)


def rectMode(rm="") -> None:
    P5.RECT_MODE = rm.upper()


def square(x, y, largueur) -> None:
    if P5.RECT_MODE == "CENTER":
        dx = largueur // 2
        dy = dx
    else:
        dx, dy = 0, 0
        
    if P5.FILL:
        pygame.draw.rect(P5.CANVAS, P5.COLORB, (P5.TRANSLATE[0]+x-dx, P5.TRANSLATE[1]+y-dy, largueur, largueur), )
    if P5.STROKE:
        pygame.draw.rect(P5.CANVAS, P5.COLORF, (P5.TRANSLATE[0]+x-dx, P5.TRANSLATE[1]+y-dy, largueur, largueur), P5.STROKE_WEIGHT)


def rect(x, y, w, h) -> None:
    if P5.RECT_MODE == "CENTER":
        dx, dy = w // 2, h // 2
    else:
        dx, dy = 0, 0

    if P5.FILL:
        pygame.draw.rect(P5.CANVAS, P5.COLORB, (P5.TRANSLATE[0]+x-dx, P5.TRANSLATE[1]+y-dy, w, h), )
    if P5.STROKE:
        pygame.draw.rect(P5.CANVAS, P5.COLORF, (P5.TRANSLATE[0]+x-dx, P5.TRANSLATE[1]+y-dy, w, h), P5.STROKE_WEIGHT)


def arc(x, y, r, a1, a2) -> None:
    rect = (x-r, y-r, 2*r, 2*r)
    pygame.draw.arc(P5.CANVAS, P5.COLORF, rect, a1, a2, P5.STROKE_WEIGHT)


def circle(x1, y1, r1) -> None:
    if P5.FILL:
        pygame.draw.circle(P5.CANVAS, P5.COLORB, (P5.TRANSLATE[0]+x1, P5.TRANSLATE[1]+y1), r1, )

    if P5.STROKE:
        pygame.draw.circle(P5.CANVAS, P5.COLORF, (P5.TRANSLATE[0]+x1, P5.TRANSLATE[1]+y1), r1, P5.STROKE_WEIGHT)


def ellipse(rect) -> None:
    rect = rect.move(*P5.TRANSLATE)

    if P5.FILL:
        pygame.draw.ellipse(P5.CANVAS, P5.COLORB, rect)

    if P5.STROKE:
        pygame.draw.circle(P5.CANVAS, P5.COLORF, rect, P5.STROKE_WEIGHT)


def constrain(n, low, high) -> float:
    return max(min(n, high), low)


def map(n, start1, stop1, start2, stop2) -> float:
    newval = (n - start1) / (stop1 - start1) * (stop2 - start2) + start2
    withinBounds = start2 <= newval <= stop2
    if withinBounds:
        return newval
    
    if start2 < stop2:
        return constrain(newval, start2, stop2)
    else:
        return constrain(newval, stop2, start2)


class Vector:

    def __init__(self, x=0, y=0, z=0):
        self.set(x, y)

    def set(self, x, y=0) -> Self:
        if isinstance(x, Vector):
            self.x = x.x
            self.y = x.y
            return self

        if type(x) in (list, tuple):
            self.x = x[0]
            self.y = x[1]
            return self
      
        self.x = x
        self.y = y
        return self

    def copy(self):
        return Vector(self.x, self.y)

    def add(self, other: Self) -> Self:
        self.x += other.x
        self.y += other.y
        return self

    def sub(self, other: Self) -> Self:
        self.x -= other.x
        self.y -= other.y
        return self

    def mult(self, coef: float) -> Self:
        self.x *= coef
        self.y *= coef
        return self

    def div(self, coef: float) -> Self:
        if coef != 0:
            self.mult(1/coef)
        return self

    def limit(self, value) -> Self:
        mSq = self.magSq()
        if (mSq > value * value):
            self.div(math.sqrt(mSq)).mult(value)
        return self

    def setMag(self, value) -> Self:
        self.normalize().mult(value)
        return self

    def dist(self, other: Self) -> float:
        return StaticVector.sub(self, other).mag()

    def mag(self) -> float:
        return math.sqrt(self.magSq())

    def magSq(self) -> float:
        return self.x*self.x+self.y*self.y

    def normalize(self) -> Self:
        m = self.mag()
        if m:
            self.x /= m
            self.y /= m
        return self

    def get_angle(self) -> float:
        """p5.heading() """
        h = math.atan2(self.y, self.x)
        return h

    def set_angle(self, angle) -> Self:
        """p5.setHeading() """
        m = self.mag()
        self.x = m * math.cos(angle)
        self.y = m * math.sin(angle)
        return self

    def rotate(self, angle) -> Self:
        newHeading = self.get_angle() + angle
        mag = self.mag()
        self.x = math.cos(newHeading) * mag
        self.y = math.sin(newHeading) * mag
        return self

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y 

    def cross(self, other) -> float:
        return self.x * other.y - self.y * other.x

    def angleBetween(self, other) -> float:
        dotmagmag = self.dot(other) / (self.mag() * other.mag())
        # Mathematically speaking: the dotmagmag variable will be between -1 and 1
        # inclusive. Practically though it could be slightly outside this range due
        # to floating-point rounding issues. This can make Math.acos return NaN.
        # 
        # Solution: we'll clamp the value to the -1,1 range
        angle = math.acos(min(1, max(-1, dotmagmag)))
        angle = angle * math.copysign(1, self.cross(other))
        return angle

    def lerp(self, other: Self, amt: float) -> Self:
        self.x += (other.x - self.x) * amt
        self.y += (other.y - self.y) * amt
        self.z += (other.z - self.z) * amt
        return self

    def reflect(self, surfaceNormal: Self) -> Self:
        """Reflect the incoming vector about a normal to a line in 2D
        This method acts on the vector directly"""
        surfaceNormal.normalize()
        return self.sub(surfaceNormal.mult(2 * self.dot(surfaceNormal)))

    def __str__(self):
        return f"({self.x}, {self.y})"


class StaticVector:

    @staticmethod
    def add(a: Vector, b: Vector) -> Vector:
        return Vector(a.x+b.x, a.y+b.y)

    @staticmethod
    def sub(a: Vector, b: Vector) -> Vector:
        return Vector(a.x-b.x, a.y-b.y)

    @staticmethod
    def mult(a: Vector, coef: float) -> Vector:
        return Vector(a.x*coef, a.y*coef)

    @staticmethod
    def div(a: Vector, coef: float) -> Vector:
        if coef != 0:
            return Vector(a.x/coef, a.y/coef)
        return a

    @staticmethod
    def dist(x1, y1, x2, y2) -> float:
        return Vector(x1, y1).dist(Vector(x2, y2))

    @staticmethod
    def fromAngle(angle, length=1) -> Vector:
        return Vector(length * math.cos(angle), length * math.sin(angle))

    @staticmethod
    def random2D() -> Vector:
        return StaticVector.fromAngle(random.random() * math.pi * 2)

    @staticmethod
    def rotate(vecteur, angle) -> Vector:
        new_vecteur = vecteur.copy()
        new_vecteur.rotate(angle)
        return new_vecteur


if __name__ == "__main__":
    a = Vector(3, 4)
    b = Vector(3, 2)
    print(a, b)
    print("angle:", a.get_angle(), b.get_angle())
    print("angleBetween:", a.angleBetween(b), b.angleBetween(a))
    print("dist:", a.dist(b))

    c = StaticVector.add(a, b)
    d = StaticVector.sub(a, b)
    print("add:", c, " sub:", d)
    a.mult(3).limit(5), b.normalize(), c.normalize(), d.normalize()
    print(a, "norm:", b, c, d)
    print(a.mag(), b.setMag(5).mag(), c.mag(), d.mag())

    print("setangle:", c.set_angle(math.pi).get_angle())
    print("rotate:", c.rotate(math.pi).get_angle())

    f = StaticVector.fromAngle(-math.pi/4, math.sqrt(2))
    print("fromangle -Pi/4:", f)
    print("random2D:", StaticVector.random2D())
