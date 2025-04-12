import math
import random
from classes import Application
from colors import Colors


class Wall:

    def __init__(self, size, coords=None):
        self.width, self.height = size
        if coords:
            self.x1, self.y1, self.x2, self.y2 = coords
        else:
            self.x1 = random.randint(1, self.width)
            self.y1 = random.randint(1, self.height)
            self.x2 = random.randint(1, self.width)
            self.y2 = random.randint(1, self.height)

    def to_line(self):
        return (self.x1, self.y1), (self.x2, self.y2)

    def to_coords(self):
        return self.x1, self.y1, self.x2, self.y2


class Cercle:

    def __init__(self, size):
        self.width, self.height = size
        self.rayon = random.randint(20, 60)
        color = (0,)
        while sum(color) < 255*3//2:
            color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        self.color = color
        self.set_pos((random.randint(1, self.width), random.randint(1, self.height)))
        self.velx = 0
        self.vely = 0
        while self.velx == 0:
            self.velx = random.randint(-2, 2)
        while self.vely == 0:
            self.vely = random.randint(-2, 2)

    def set_pos(self, position):
        self.x, self.y = position

    def update(self):
        if self.x+self.velx < 0: 
            self.velx = abs(self.velx)
        if self.y+self.vely < 0: 
            self.vely = abs(self.vely)
        if self.x+self.velx > self.width: 
            self.velx = -abs(self.velx)
        if self.y+self.vely > self.height: 
            self.vely = -abs(self.vely)

        self.x += self.velx
        self.y += self.vely

    def to_dest(self):
        return (self.x, self.y), self.rayon


class Rayon:

    def __init__(self, source, angle):
        self.x1 = source.x1
        self.y1 = source.y1
        self.x2 = source.x1 + math.cos(math.radians(angle))
        self.y2 = source.y1 + math.sin(math.radians(angle))

        self.longueur = None
        self.destx = None
        self.desty = None

    def to_dest(self):
        if self.longueur:
            return self.destx, self.desty
        return None

    def to_line(self):
        return self.x1, self.y1, self.x2, self.y2

    def cast_to_cercle(self, cercles):

        Ax, Ay = self.x1, self.y1
        # if self.to_dest():
        #     Bx, By = self.to_dest()
        # else:
        Bx, By = self.x2, self.y2

        # compute the euclidean distance between A and B
        LAB = math.sqrt((Bx-Ax)*(Bx-Ax)+(By-Ay)*(By-Ay))

        # compute the direction vector D from A to B
        Dx = (Bx-Ax)/LAB
        Dy = (By-Ay)/LAB

        for cercle in cercles:
            Cx, Cy = cercle.x, cercle.y
            R = cercle.rayon

            # the equation of the line AB is x = Dx*t + Ax, y = Dy*t + Ay with 0 <= t <= LAB.
            # compute the distance between the points A and E, where
            # E is the point of AB closest the circle center (Cx, Cy)
            t = Dx*(Cx-Ax) + Dy*(Cy-Ay)    

            # compute the coordinates of the point E
            Ex = t*Dx + Ax
            Ey = t*Dy + Ay

            # compute the euclidean distance between E and C
            LEC = math.sqrt((Ex-Cx)*(Ex-Cx) + (Ey-Cy)*(Ey-Cy))

            # test if the line intersects the circle
            if LEC < R:
                # compute distance from t to circle intersection point
                dt = math.sqrt(R*R - LEC*LEC)

                # compute first intersection point
                Fx = (t-dt)*Dx + Ax
                Fy = (t-dt)*Dy + Ay

                # compute second intersection point
                # Gx = (t+dt)*Dx + Ax
                # Gy = (t+dt)*Dy + Ay
                if t >= 0:
                    LEF = math.sqrt((Fx-Ax)*(Fx-Ax) + (Fy-Ay)*(Fy-Ay))
                    if self.longueur is None or self.longueur > LEF:
                        self.longueur = LEF
                        self.destx, self.desty = Fx, Fy
            
            # else test if the line is tangent to circle
            elif LEC == R:
                # tangent point to circle is E
                LEF = math.sqrt((Ex-Ax)*(Ex-Ax) + (Ey-Ay)*(Ey-Ay))
                if self.longueur is None or self.longueur > LEF:
                    self.longueur = LEF
                    self.destx, self.desty = Ex, Ey

    def cast(self, walls):
        for wall in walls:
            x1, y1, x2, y2 = wall.to_coords()
            x3, y3, x4, y4 = self.to_line()

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if (den == 0):
                continue

            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
            if (0 < t < 1 and u > 0): 
                x = x1 + t * (x2 - x1)
                y = y1 + t * (y2 - y1)
                longueur = math.sqrt((self.x1-x)*(self.x1-x) + (self.y1-y)*(self.y1-y))
                if self.longueur:
                    if self.longueur > longueur:
                        self.longueur = longueur
                        self.destx, self.desty = x, y
                else:
                    self.longueur = longueur
                    self.destx, self.desty = x, y


class Source:

    def __init__(self, size):
        self.width, self.height = size
        color = (0,)
        while sum(color) < 255*3//2:
            color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        self.color = color
        self.set_pos((random.randint(1, self.width), random.randint(1, self.height)))
        self.velx = 0
        self.vely = 0
        while self.velx == 0:
            self.velx = random.randint(-5, 5)
        while self.vely == 0:
            self.vely = random.randint(-5, 5)

    def set_pos(self, position):
        self.x1, self.y1 = position
        self.rayons = []
        for angle in range(360):
            self.rayons.append(Rayon(self, angle))

    def update(self):
        if self.x1+self.velx < 0: 
            self.velx = abs(self.velx)
        if self.y1+self.vely < 0: 
            self.vely = abs(self.vely)
        if self.x1+self.velx > self.width: 
            self.velx = -abs(self.velx)
        if self.y1+self.vely > self.height: 
            self.vely = -abs(self.vely)

        self.x1 += self.velx
        self.y1 += self.vely
        self.set_pos((self.x1, self.y1))

    def to_point(self):
        return self.x1, self.y1


class RayCasting(Application):

    DEFAULT_CONFIG = ("Ray Casting 2", Colors.MIDDLE_GREEN, 2, 10)

    MIN_SIZE = (400, 300)

    def __init__(self, screen, args):
        super().__init__(screen)
        self.screen = screen
        self.action = ""
        self.nb_walls = args[1]
        self.nb_sources = args[0]
        self.set_zone(self.screen.get_size())
        self.get_theme()

    def get_theme(self):
        if self.theme.get_theme() == "CLAIR":
            self.color = Colors.WHITE
        else:
            self.color = Colors.BLACK

    def set_sources(self):
        self.sources = []
        for _ in range(self.nb_sources):
            self.sources.append(Source(self.size))

    def set_cercles(self):
        self.cercles = []
        self.cercles.append(Cercle(self.size))
        self.cercles.append(Cercle(self.size))
        self.cercles.append(Cercle(self.size))
        self.cercles.append(Cercle(self.size))

    def set_walls(self):
        self.walls = []
        self.walls.append(Wall(self.size, (-1, -1, self.size[0], -1)))
        self.walls.append(Wall(self.size, (-1, -1, -1, self.size[1])))
        self.walls.append(Wall(self.size, (self.size[0], 0, self.size[0], self.size[1])))
        self.walls.append(Wall(self.size, (0, self.size[1], self.size[0], self.size[1])))
        # return
        for _ in range(self.nb_walls):
            self.walls.append(Wall(self.size))

    def set_zone(self, new_zone):
        self.size = new_zone
        self.set_walls()
        self.set_cercles()
        self.set_sources()

    def resize(self, screen):
        self.screen = screen
        self.set_zone(self.screen.get_size())

    def get_action(self):
        return self.action

    def keyreleased(self, event):
        # return  # pour deboguage
        self.touche = self.keys.get_key()
        if self.touche == self.keys.K_ESCAPE:
            self.action = "QUIT"
        elif self.touche == self.keys.K_SPACE:
            self.set_zone(self.size)

    def update(self):
        for cercle in self.cercles:
            cercle.update()

        for source in self.sources:
            source.update()

            for rayon in source.rayons:
                rayon.cast(self.walls)
                rayon.cast_to_cercle(self.cercles)

    def draw(self):
        self.screen.fill(self.color)
        for source in self.sources:
            for rayon in source.rayons:
                couleur = source.color
                if rayon.longueur:
                    self.tools.line(couleur, source.to_point(), rayon.to_dest())

        for wall in self.walls:
            self.tools.line( (10, 200, 30), *wall.to_line())

        for cercle in self.cercles:
            self.tools.circle(self.color, *cercle.to_dest())
            self.tools.circle((10, 200, 30), *cercle.to_dest(), 1)


if __name__ == '__main__':
    from exec import run
    run(RayCasting)
