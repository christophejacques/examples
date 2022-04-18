import random
from __init__ import background, createCanvas, stroke, fill, circle, rect, square, rectMode
from __init__ import P5, strokeWeight, noStroke, map, Vector, line, push, pop
from __init__ import *


class Mover:
    def __init__(this, x, y, r):
        this.pos = Vector(x, y)
        this.r = r
        this.vel = Vector(10, 0)
        this.acc = Vector()

    def update(this):
        # new_acc = Vector(P5.mouseX, P5.mouseY).sub(this.pos).normalize().mult(0.5)
        new_acc = Vector(P5.WIDTH//2, P5.HEIGHT//2).sub(this.pos).normalize().mult(0.5)
        this.acc.set(new_acc)
        this.vel.add(this.acc)
        this.pos.add(this.vel)

    def draw(this):
        circle(this.pos.x, this.pos.y, this.r)

        vel = this.vel.copy().mult(4)
        line(this.pos.x, this.pos.y, this.pos.x+vel.x, this.pos.y+vel.y)

        push()
        stroke(255, 50, 255)
        strokeWeight(2)
        acc = this.acc.copy().mult(40)
        line(this.pos.x, this.pos.y, this.pos.x+acc.x, this.pos.y+acc.y)
        pop()


movers = []
def preload():
    for i in range(5):
        movers.append(Mover(320+40*i, 100, 10))


def setup():
    createCanvas(800, 500)
    fill(0, 50, 50)
    stroke(20, 200, 150)


def draw():
    background(0)
    circle(P5.WIDTH//2, P5.HEIGHT//2, 50)
    for mover in movers:
        mover.update()
        mover.draw()
