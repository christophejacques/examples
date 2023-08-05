# ! c:\bat\python.bat -3.11
import math
from __init__ import createCanvas, circle, stroke, fill, text, textRect
from __init__ import strokeWeight, StaticVector, Vector, line, arc
from __init__ import noFill, rect, background, P5, pygame
from __init__ import *


class Pie:
    def __init__(self, x: int, y: int, r: int):
        self.center: Vector = Vector(x, y)
        self.r: float = r
        self.parts: list = list()

    def create_from_numbers(self, valeurs: list, couleurs: list):
        self.parts.clear()
        self.valeurs: list = valeurs
        self.couleurs: list = couleurs

        total: float = sum(valeurs)
        angle1: float = 0
        angle2: float = 0
        pi2: float = 2*math.pi

        for i, nombre in enumerate(self.valeurs):
            angle2 += nombre / total * pi2
            self.add_part(self.couleurs[i], angle1, angle2, nombre)
            angle1 = angle2

    def add_part(self, color, a1, a2, valeur):
        self.parts.append(Part(self.center.x, self.center.y, self.r, color, a1, a2, valeur))

    def draw(self):
        for part in self.parts:
            part.draw()


class Part:
    def __init__(self, x: int, y: int, r: float, color, a1: float, a2: float, valeur):
        self.center: Vector = Vector(x, y)
        self.r: float = r
        self.a1 = a1
        self.a2 = a2
        self.color = color
        self.valeur = valeur

        self.midangle = a1 + (a2 - a1) / 2
        self.fromAngle = StaticVector.fromAngle(-self.midangle)
        self.center.add(StaticVector.mult(self.fromAngle, 10))

        _, _, w, h = textRect(self.valeur).get_rect()
        position = Vector(w, h)
        self.textpos = StaticVector.add(self.center, StaticVector.mult(self.fromAngle, r))
        self.circlepos = self.textpos.copy().add(StaticVector.mult(self.fromAngle, StaticVector.div(position, 1.5).mag()))
        self.textpos = self.circlepos.copy().sub(StaticVector.div(position, 2))

    def draw(self):
        strokeWeight(1)
        stroke(*self.color)
        for r in range(1, self.r):
            pass
            arc(self.center.x, self.center.y, r, self.a1, self.a2)

        stroke(255)
        strokeWeight(2)
        arc(self.center.x, self.center.y, r, self.a1, self.a2)
        line(self.center.x, self.center.y, self.center.x+r*math.cos(self.a1), self.center.y-r*math.sin(self.a1))
        line(self.center.x, self.center.y, self.center.x+r*math.cos(self.a2), self.center.y-r*math.sin(self.a2))
        text(f"{self.valeur:2}", self.textpos.x, self.textpos.y)


nombre: int = 7


def keyPressed() -> None:
    global nombre
    match P5.keyCode:
        case pygame.K_KP_PLUS:
            if nombre < 50:
                nombre += 1
        case pygame.K_KP_MINUS:
            if nombre > 1:
                nombre -= 1


def setup() -> None:
    createCanvas(800, 600)
    fill(0, 50, 50)
    stroke(250)
    strokeWeight(2)


def draw() -> None:
    background(0)

    p = Pie(400, 300, 200)

    cote_part: float = 2 * math.pi / nombre
    for angle in range(nombre):
        p.add_part((250/nombre*(angle+1), 255-(250/nombre*angle), abs(130-(310/nombre*angle))), angle * cote_part, (angle+1) * cote_part, angle)

    p.draw()
