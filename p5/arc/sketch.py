
import math
from __init__ import createCanvas, circle, stroke, fill, point
from __init__ import strokeWeight, StaticVector, Vector, line
from __init__ import noFill, background
from __init__ import *

angle: float

def poubelle():
    s = StaticVector()
    s.add()
    v = Vector()
    v.add(s)


def setup() -> None:
    global angle

    createCanvas(800, 600)
    fill(0, 50, 50)
    noFill()
    strokeWeight(1)

    rayon = 200
    cx, cy = 400, 300

    stroke(100)
    circle(cx, cy, rayon)
    stroke(200, 50, 50)

    angle = math.pi/4
    for y in range(int(rayon * math.sin(angle))):
        # maximum = math.asin(y/rayon)
        x = cx + (y) / angle
        x = cx + y * math.cos(angle)
        point(int(x), cy - y)

    print(f"{y=}")


def draw() -> None:
    global angle
    background(0)
    cx, cy = 400, 300
    rayon = 200
    # angle = math.pi/4
    angle += 0.01

    for y in range(cy-rayon, cy):
        # angle = math.asin((cy-y)/rayon)
        x = cx + (cy-y) / angle
        point(int(x), y)

        # line(cx, y, cx + rayon*math.cos(angle), y)
        # stroke(50, 200, 50)
        # line(cx, y, cx - rayon*math.cos(angle), y)
        continue
        stroke(50, 50, 200)
        hauteur = 2*cy-y
        line(cx, hauteur, cx + rayon*math.cos(angle), hauteur)
        stroke(50, 200, 200)
        line(cx, hauteur, cx - rayon*math.cos(angle), hauteur)
