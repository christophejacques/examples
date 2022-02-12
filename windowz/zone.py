import pygame


class Couleur:
    def __init__(self, r: int, g: int, b: int, alpha: int = 255):
        self.r = r
        self.g = g
        self.b = b
        self.alpha = alpha

    def to_tuple(self):
        return (self.r, self.g, self.b, self.alpha)


class Position:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def in_zone(self, zone):
        res = zone.p1.x <= self.x <= zone.p2.x and zone.p1.y <= self.y <= zone.p2.y 
        return res

    def to_tuple(self):
        return (self.x, self.y)

    def copy(self):
        return Position(self.x, self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Zone:

    def __init__(self, p1: Position, p2: Position):
        if isinstance(p1, Position) and isinstance(p2, Position):
            self.p1 = p1
            self.p2 = p2

        elif (isinstance(p1, tuple) and isinstance(p2, tuple)) or (isinstance(p1, list) and isinstance(p2, list)):
            if len(p1) != 2 or len(p2) != 2:
                raise TypeError(f"les tuples {p1} et/ou {p2} ne sont pas de taille 2.")

            self.p1 = Position(*p1)
            self.p2 = Position(*p2)

        else:
            raise TypeError(f"les coordonnées {p1} et/ou {p2} ne sont pas de type Position.")

        self.dx = self.p2.x - self.p1.x
        self.dy = self.p2.y - self.p1.y
        self.decal = 5
        self.fonc_width = 35
        self.fonc_height = 25

    def move(self, decal: list):
        self.p1.x += decal[0]
        self.p1.y += decal[1]
        self.p2.x += decal[0]
        self.p2.y += decal[1]
        self.dx = self.p2.x - self.p1.x
        self.dy = self.p2.y - self.p1.y

    def contains(self, pos: Position):
        return pos.in_zone(self)

    def to_box(self, fonction, cut_left_border=False):
        if fonction.lower() == "close":
            return ((self.p2.x-self.decal-self.fonc_width, self.p1.y), (self.fonc_width, self.fonc_height))

        elif fonction.lower() == "left":
            return self.p1.to_tuple(), (self.decal, self.dy)
        elif fonction.lower() == "right":
            return (self.p2.x-self.decal, self.p1.y), (self.decal, self.dy)
        elif fonction.lower() == "bottom":
            if cut_left_border and self.p1.x < 0:
                return (0, self.p2.y-self.decal), (self.dx+self.p1.x, self.decal)
            else:
                return (self.p1.x, self.p2.y-self.decal), (self.dx, self.decal)

        elif fonction.lower() == "maximize_symbol":
            posx1 = self.p1.x + 1+(3*self.fonc_width)//8
            posy1 = self.p1.y + 9
            return pygame.Rect(posx1, posy1, self.fonc_width//4, 1+self.fonc_height//4)

    def to_line(self, cote):
        if cote.lower() == "close_slash":
            posx1 = self.p1.x + 3+self.fonc_width//3
            posx2 = self.p2.x - 3-self.fonc_width//3
            posy1 = self.p2.y - 10
            posy2 = self.p1.y + 9
            return (posx1, posy1), (posx2, posy2)
        if cote.lower() == "close_anti_slash":
            posx1 = self.p1.x + 3+self.fonc_width//3
            posx2 = self.p2.x - 3-self.fonc_width//3
            posy2 = self.p2.y - 10
            posy1 = self.p1.y + 9
            return (posx1, posy1), (posx2, posy2)

        elif cote.lower() == "maximize_symbol_top":
            posx = self.p1.x + 3+(3*self.fonc_width)//8
            posy = self.p1.y + 7
            return (posx, posy), (posx+8, posy)
        elif cote.lower() == "maximize_symbol_right":
            posx = self.p2.x - self.fonc_width//3
            posy1 = self.p1.y + 8
            posy2 = self.p2.y - 12
            return (posx, posy1), (posx, posy2)

        elif cote.lower() == "minimize_symbol":
            posx = self.p1.x + 1+self.fonc_width//3
            posy = self.p2.y - 10
            return (posx, posy), (posx+9, posy)

        elif cote.lower() == "left":
            return self.p1.to_tuple(), (self.p1.x, self.p2.y)
        elif cote.lower() == "right":
            return (self.p2.x-1, self.p1.y), (self.p2.x-1, self.p2.y)
        elif cote.lower() == "bottom":
            return (self.p1.x, self.p2.y), (self.p2.x-1, self.p2.y)
        elif cote.lower() == "top":
            return self.p1.to_tuple(), (self.p2.x-1, self.p1.y)

    def to_tuple(self, cut_left_border=False):
        if cut_left_border and self.p1.x < 0:
            return ((0, self.p1.y), (self.dx+self.p1.x, self.dy))
        else:
            return (self.p1.to_tuple(), (self.dx, self.dy))

    def __str__(self):
        return f"({self.p1}, {self.p2})"


if __name__ == "__main__":
    print("Compilation: OK")
