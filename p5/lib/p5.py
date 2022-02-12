import pygame
import math
import random


class HISTO:
    BGCOLOR = []
    COLORB = []
    COLORF = []
    STROKE_WEIGHT = []
    STROKE = []
    FILL = []
    TRANSLATE = []


class P5:
    CANVAS = None
    WINDOW_STATE = ["NORMAL"]
    LOOP = True
    FRAME_RATE = 60
    WIDTH, HEIGHT = 0, 0
    BGCOLOR = (0, 0, 0)
    COLORB = (0, 0, 0)
    COLORF = (0, 0, 0)
    STROKE_WEIGHT = 1
    STROKE = True
    FILL = True
    RECT_MODE = ""
    FONT = None
    TRANSLATE = [0, 0]

    mouseX, mouseY = 0, 0
    pmouseX, pmouseY = 0, 0
    mouseIsPressed = 0
    keyIsPressed = False
    keyCode = 0
    frameCount = 0
    

preload = lambda: None
setup = lambda: None
draw = lambda: None
mousePressed = lambda: None
mouseReleased = lambda: None
keyPressed = lambda: None
keyReleased = lambda: None


def noLoop(): 
    P5.LOOP = False


def createCanvas(w, h):
    pygame.init()
    P5.CANVAS = pygame.display.set_mode((w, h))
    P5.WIDTH, P5.HEIGHT = w, h
    P5.FONT = pygame.font.SysFont("comicsans", 30)


def resizeCanvas(w, h):
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


def frameRate(fps):
    P5.FRAME_RATE = fps


def noStroke():
    P5.STROKE = False


def stroke(*s):
    P5.STROKE = True
    if len(s) == 1:
        P5.COLORF = (s[0],)*3
    else:
        P5.COLORF = s


def strokeWeight(w):
    P5.STROKE_WEIGHT = w


def push():
    HISTO.BGCOLOR.append(P5.BGCOLOR)
    HISTO.COLORB.append(P5.COLORB)
    HISTO.COLORF.append(P5.COLORF)
    HISTO.STROKE_WEIGHT.append(P5.STROKE_WEIGHT)
    HISTO.STROKE.append(P5.STROKE)
    HISTO.FILL.append(P5.FILL)
    HISTO.TRANSLATE.append(P5.TRANSLATE)
    

def pop():
    if HISTO.BGCOLOR: P5.BGCOLOR = HISTO.BGCOLOR.pop()
    if HISTO.COLORB: P5.COLORB = HISTO.COLORB.pop()
    if HISTO.COLORF: P5.COLORF = HISTO.COLORF.pop()
    if HISTO.STROKE_WEIGHT: P5.STROKE_WEIGHT = HISTO.STROKE_WEIGHT.pop()
    if HISTO.STROKE: P5.STROKE = HISTO.STROKE.pop()
    if HISTO.FILL: P5.FILL = HISTO.FILL.pop()
    if HISTO.TRANSLATE: P5.TRANSLATE = HISTO.TRANSLATE.pop()
    

def textSize(size):
    P5.FONT = pygame.font.SysFont("comicsans", size)


def text(texte, x, y):
    texte_surf = P5.FONT.render("{}".format(texte), False, P5.COLORF)
    P5.CANVAS.blit(texte_surf, (P5.TRANSLATE[0]+x, P5.TRANSLATE[1]+y))


def noFill():
    P5.FILL = False


def fill(*f):
    P5.FILL = True
    if len(f) == 1:
        P5.COLORB = (f[0],)*3
    else:
        P5.COLORB = f


def color(*c):
    if len(c) == 1:
        return (c[0],)*3
    else:
        return c


def background(*color):
    if len(color) == 1:
        P5.BGCOLOR = (color[0],)*3
    else:
        P5.BGCOLOR = color
    P5.CANVAS.fill(P5.BGCOLOR)


def translate(dx, dy):
    P5.TRANSLATE[0] += dx
    P5.TRANSLATE[1] += dy


def point(x, y):
    if P5.STROKE:
        P5.CANVAS.set_at((P5.TRANSLATE[0]+x, P5.TRANSLATE[1]+y), P5.COLORF)
        

def line(x1, y1, x2, y2):
    if P5.STROKE:
        pygame.draw.line(P5.CANVAS, P5.COLORF, 
            (P5.TRANSLATE[0]+x1, P5.TRANSLATE[1]+y1), (P5.TRANSLATE[0]+x2, P5.TRANSLATE[1]+y2), 
            P5.STROKE_WEIGHT)


def triangle(p1, p2, p3):
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


def rectMode(rm=""):
    P5.RECT_MODE = rm.upper()


def square(x, y, largueur):
    if P5.RECT_MODE == "CENTER":
        dx = largueur // 2
        dy = dx
    else:
        dx, dy = 0, 0
        
    if P5.FILL:
        pygame.draw.rect(P5.CANVAS, P5.COLORB, (P5.TRANSLATE[0]+x-dx, P5.TRANSLATE[1]+y-dy, largueur, largueur), )
    if P5.STROKE:
        pygame.draw.rect(P5.CANVAS, P5.COLORF, (P5.TRANSLATE[0]+x-dx, P5.TRANSLATE[1]+y-dy, largueur, largueur), P5.STROKE_WEIGHT)


def rect(x, y, w, h):
    if P5.RECT_MODE == "CENTER":
        dx, dy = w // 2, h // 2
    else:
        dx, dy = 0, 0

    if P5.FILL:
        pygame.draw.rect(P5.CANVAS, P5.COLORB, (P5.TRANSLATE[0]+x-dx, P5.TRANSLATE[1]+y-dy, w, h), )
    if P5.STROKE:
        pygame.draw.rect(P5.CANVAS, P5.COLORF, (P5.TRANSLATE[0]+x-dx, P5.TRANSLATE[1]+y-dy, w, h), P5.STROKE_WEIGHT)


def circle(x1, y1, r1):
    if P5.FILL:
        pygame.draw.circle(P5.CANVAS, P5.COLORB, (P5.TRANSLATE[0]+x1, P5.TRANSLATE[1]+y1), r1, )

    if P5.STROKE:
        pygame.draw.circle(P5.CANVAS, P5.COLORF, (P5.TRANSLATE[0]+x1, P5.TRANSLATE[1]+y1), r1, P5.STROKE_WEIGHT)


def ellipse(rect):
    rect = rect.move(*P5.TRANSLATE)

    if P5.FILL:
        pygame.draw.ellipse(P5.CANVAS, P5.COLORB, rect)

    if P5.STROKE:
        pygame.draw.circle(P5.CANVAS, P5.COLORF, rect, P5.STROKE_WEIGHT)


def constrain(n, low, high):
    return max(min(n, high), low)


def map(n, start1, stop1, start2, stop2):
    newval = (n - start1) / (stop1 - start1) * (stop2 - start2) + start2
    withinBounds = start2 <= newval <= stop2
    if withinBounds:
        return newval
    
    if start2 < stop2:
        return constrain(newval, start2, stop2)
    else:
        return constrain(newval, stop2, start2)


class Vector:

    def __init__(self, x=0, y=0):
        self.set(x, y)

    def set(self, x, y=0):
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

    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def sub(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def mult(self, coef: float):
        self.x *= coef
        self.y *= coef
        return self

    def div(self, coef: float):
        if coef != 0:
            self.mult(1/coef)
        return self

    def limit(self, value):
        mSq = self.magSq()
        if (mSq > value * value):
            self.div(math.sqrt(mSq)).mult(value)
        return self

    def setMag(self, value):
        self.normalize().mult(value)
        return self

    def dist(self, other):
        return StaticVector.sub(self, other).mag()

    def mag(self):
        return math.sqrt(self.magSq())

    def magSq(self):
        return self.x*self.x+self.y*self.y

    def normalize(self):
        m = self.mag()
        if m:
            self.x /= m
            self.y /= m
        return self

    def get_angle(self):
        """p5.heading() """
        h = math.atan2(self.y, self.x)
        return h

    def set_angle(self, angle):
        """p5.setHeading() """
        m = self.mag()
        self.x = m * math.cos(angle)
        self.y = m * math.sin(angle)
        return self

    def rotate(self, angle):
        newHeading = self.get_angle() + angle
        mag = self.mag()
        self.x = math.cos(newHeading) * mag
        self.y = math.sin(newHeading) * mag
        return self

    def dot(self, other):
        return self.x * other.x + self.y * other.y 

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def angleBetween(self, other):
        dotmagmag = self.dot(other) / (self.mag() * other.mag())
        # Mathematically speaking: the dotmagmag variable will be between -1 and 1
        # inclusive. Practically though it could be slightly outside this range due
        # to floating-point rounding issues. This can make Math.acos return NaN.
        # 
        # Solution: we'll clamp the value to the -1,1 range
        angle = math.acos(min(1, max(-1, dotmagmag)))
        angle = angle * math.copysign(1, self.cross(other))
        return angle

    def lerp(self, other, amt):
        self.x += (other.x - self.x) * amt
        self.y += (other.y - self.y) * amt
        self.z += (other.z - self.z) * amt
        return self

    def reflect(self, surfaceNormal):
        """Reflect the incoming vector about a normal to a line in 2D
        This method acts on the vector directly"""
        surfaceNormal.normalize()
        return self.sub(surfaceNormal.mult(2 * self.dot(surfaceNormal)))

    def __str__(self):
        return f"({self.x}, {self.y})"


class StaticVector:

    def add(a: Vector, b: Vector):
        return Vector(a.x+b.x, a.y+b.y)

    def sub(a: Vector, b: Vector):
        return Vector(a.x-b.x, a.y-b.y)

    def mult(a: Vector, coef: float):
        return Vector(a.x*coef, a.y*coef)

    def div(a: Vector, coef: float):
        if coef != 0:
            return Vector(a.x/coef, a.y/coef)
        return a

    def dist(x1, y1, x2, y2):
        return Vector(x1, y1).dist(Vector(x2, y2))

    def fromAngle(angle, length=1):
        return Vector(length * math.cos(angle), length * math.sin(angle))

    def random2D():
        return StaticVector.fromAngle(random.random() * math.pi * 2)

    def rotate(vecteur, angle):
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
