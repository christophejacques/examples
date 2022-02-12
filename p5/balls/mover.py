import random
from __init__ import StaticVector, Vector, P5


gravity = Vector(0, 0.1)
wind = Vector(0.1, 0)


class Mover:
    def __init__(this, x, y, rayon):
        this.pos = Vector(x, y)
        this.r = rayon
        this.masse = rayon*rayon/100
        # this.vel = StaticVector.random2D()
        # this.vel.mult(3*random.random())
        this.vel = Vector()
        this.acc = Vector()

    def friction(this):
        if this.pos.y + this.r >= P5.HEIGHT//2:
            mu = 0.001
            # force = this.vel.copy().normalize().mult(-mu*this.masse)
            force = StaticVector.mult(this.vel, -mu*this.masse)
            # print("Friction:", force)
            this.applyForce(force)

    def update(this):
        wind_acc = Vector((3*random.random()-1.5)/10, 0)
        wind.add(wind_acc).limit(0.1)
        this.applyForce(gravity)
        this.applyForce(StaticVector.div(wind, this.masse))
        this.friction()

        this.vel.add(this.acc)
        this.pos.add(this.vel)
        this.acc.set(0, 0)

    def edges(this):
        if this.pos.x+this.vel.x+this.r >= P5.WIDTH:
            this.vel.x *= -1
            this.pos.x = P5.WIDTH-this.r
        elif this.pos.x+this.vel.x-this.r <= 0:
            this.vel.x *= -1
            this.pos.x = this.r

        if this.pos.y+this.vel.y+this.r >= P5.HEIGHT:
            this.vel.y *= -1
            this.pos.y = P5.HEIGHT-this.r

    def applyForce(this, force):
        this.acc.add(force)

    def draw(this):
        stroke(255)
        fill(150)
        circle(this.pos.x, this.pos.y, this.r) 
