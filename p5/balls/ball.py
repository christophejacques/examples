import math

from __init__ import Vector, StaticVector
from __init__ import P5
from __init__ import noStroke, circle


class Ball:
  
    def __init__(this, x, y, r):
        this.position = Vector(x, y)
        this.velocity = StaticVector.random2D()
        this.velocity.mult(3)
        this.r = r
        this.m = r * 0.1
  
    def update(this):
        # print("UPDATE:", this.position, this.velocity, end=" => ")
        this.position.add(this.velocity)
        # print(this.position)

    def checkBoundaryCollision(this):
        if (this.position.x > P5.WIDTH - this.r):
            this.position.x = P5.WIDTH - this.r
            this.velocity.x *= -1
        elif (this.position.x < this.r):
            this.position.x = this.r
            this.velocity.x *= -1
        elif (this.position.y > P5.HEIGHT - this.r):
            this.position.y = P5.HEIGHT - this.r
            this.velocity.y *= -1
        elif (this.position.y < this.r):
            this.position.y = this.r
            this.velocity.y *= -1

    def checkCollision(this, other):
        # // Get distances between the balls components
        distanceVect = StaticVector.sub(other.position, this.position)

        # // Calculate magnitude of the vector separating the balls
        distanceVectMag = distanceVect.mag()

        # // Minimum distance before they are touching
        minDistance = this.r + other.r

        if (distanceVectMag < minDistance): 
            distanceCorrection = (minDistance - distanceVectMag) / 2.0
            d = distanceVect.copy()
            correctionVector = d.normalize().mult(distanceCorrection)
            other.position.add(correctionVector)
            this.position.sub(correctionVector)

            # // get angle of distanceVect
            theta = distanceVect.get_angle()
            # // precalculate trig values
            sine = math.sin(theta)
            cosine = math.cos(theta)

            # /* bTemp will hold rotated ball this.positions. You 
            #  just need to worry about bTemp[1] this.position*/
            bTemp = [Vector(), Vector()]

            # /* this ball's this.position is relative to the other
            # so you can use the vector between them (bVect) as the 
            # reference point in the rotation expressions.
            # bTemp[0].this.position.x and bTemp[0].this.position.y will initialize
            # automatically to 0.0, which is what you want
            # since b[1] will rotate around b[0] */
            bTemp[1].x = cosine * distanceVect.x + sine * distanceVect.y
            bTemp[1].y = cosine * distanceVect.y - sine * distanceVect.x

            # // rotate Temporary velocities
            vTemp = [Vector(), Vector()]

            vTemp[0].x = cosine * this.velocity.x + sine * this.velocity.y
            vTemp[0].y = cosine * this.velocity.y - sine * this.velocity.x
            vTemp[1].x = cosine * other.velocity.x + sine * other.velocity.y
            vTemp[1].y = cosine * other.velocity.y - sine * other.velocity.x

            # /* Now that velocities are rotated, you can use 1D
            # conservation of momentum equations to calculate 
            # the final this.velocity along the x-axis. */
            vFinal = [Vector(), Vector()]

            # // final rotated this.velocity for b[0]
            vFinal[0].x = ((this.m - other.m) * vTemp[0].x + 2 * other.m * vTemp[1].x) / (this.m + other.m)
            vFinal[0].y = vTemp[0].y

            # // final rotated this.velocity for b[0]
            vFinal[1].x = ((other.m - this.m) * vTemp[1].x + 2 * this.m * vTemp[0].x) / (this.m + other.m)
            vFinal[1].y = vTemp[1].y

            # // hack to avoid clumping
            bTemp[0].x += vFinal[0].x
            bTemp[1].x += vFinal[1].x

            # /* Rotate ball this.positions and velocities back
            # Reverse signs in trig expressions to rotate 
            # in the opposite direction */
            # // rotate balls
            bFinal = [Vector(), Vector()]

            bFinal[0].x = cosine * bTemp[0].x - sine * bTemp[0].y
            bFinal[0].y = cosine * bTemp[0].y + sine * bTemp[0].x
            bFinal[1].x = cosine * bTemp[1].x - sine * bTemp[1].y
            bFinal[1].y = cosine * bTemp[1].y + sine * bTemp[1].x

            # // update balls to screen this.position
            other.position.x = this.position.x + bFinal[1].x
            other.position.y = this.position.y + bFinal[1].y

            this.position.add(bFinal[0])

            # // update velocities
            this.velocity.x = cosine * vFinal[0].x - sine * vFinal[0].y
            this.velocity.y = cosine * vFinal[0].y + sine * vFinal[0].x
            other.velocity.x = cosine * vFinal[1].x - sine * vFinal[1].y
            other.velocity.y = cosine * vFinal[1].y + sine * vFinal[1].x
        
    def display(this):
        noStroke()
        circle(this.position.x, this.position.y, this.r)
