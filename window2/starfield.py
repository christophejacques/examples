import math
import random
from classes import Application
from colors import Colors


class Variables:
    gauche, haut = 0, 0
    droite, bas = 0, 0
    width, height = 0, 0
    mouseX = 0
    mouseY = 0
    distanceMax = 0


class StarField(Application):

    DEFAULT_CONFIG = ("Starfiel 50", Colors.DARK_ORANGE, 50)
    MIN_SIZE = (400, 300)

    def __init__(self, args):
        self.title = self.DEFAULT_CONFIG[0]
        self.maximum = args[0]
        self.action = ""
        self.liste = []

    def post_init(self):
        self.set_zone(((0, 0), self.tools.get_size()))

    def set_zone(self, new_zone):
        Variables.gauche, Variables.haut = new_zone[0]
        Variables.droite, Variables.bas = new_zone[1]
        Variables.width = Variables.droite - Variables.gauche
        Variables.height = Variables.bas - Variables.haut
        Variables.mouseX = Variables.gauche + Variables.width/2
        Variables.mouseY = Variables.haut + Variables.height/2
        Variables.distanceMax = \
            math.sqrt(Variables.width*Variables.width/4 + Variables.height*Variables.height/4)

    def resize(self):
        window_size = self.tools.get_size()
        # print(f"change Screen Resolution = {window_size}")
        self.set_zone(((0, 0), window_size))

    def get_action(self):
        return self.action

    def keyreleased(self, event):
        self.set_title(self.title + f" ({len(self.liste)})")
        self.touche = self.keys.get_key()
        if self.touche == self.keys.K_ESCAPE:
            self.action = "QUIT"
        elif self.touche == self.keys.K_KP_MINUS:
            if self.maximum > 10: 
                self.maximum -= 10
        elif self.touche == self.keys.K_KP_PLUS:
            self.maximum += 10

    def update(self):
        if len(self.liste) < self.maximum:
            self.liste.append(Star())

        for etoile in self.liste:
            etoile.update()

    def draw(self):
        self.tools.fill((0, 0, 0))
        for i, etoile in enumerate(self.liste):
            res = etoile.get_attrs()
            if res:
                couleur, pstar, star, taille = res
                self.tools.line(couleur, pstar, star)
                self.tools.circle(couleur, star, taille)
            else:
                self.liste.pop(i)


class Star:

    def __init__(self):

        boucle = True
        while boucle:
            self.x = Variables.width/2 - random.random() * Variables.width
            self.y = Variables.height/2 - random.random() * Variables.height
            boucle = math.sqrt(self.x*self.x + self.y*self.y) < 50 or abs(self.x) < 5 or abs(self.y) < 5

        self.z = 500 + random.random() * 1000
        self.pz = self.z

        self.zinit = self.z + random.random() * 1000

        self.distance = math.sqrt(self.x*self.x + self.y*self.y)
        self.vitesse = 4 * Variables.distanceMax / self.distance

        self.couleur = (random.random() * 100,
                        100 + random.random() * 155,
                        100 + random.random() * 155
                        )

    def get_attrs(self):
        cx = int(Variables.mouseX + self.x / self.z * Variables.width/2)
        cy = int(Variables.mouseY - self.y / self.z * Variables.height/2)

        taille = int(10 * abs(self.zinit - self.z) / self.zinit)
        if (cx+taille > Variables.droite or cx-taille < Variables.gauche or cy+taille > Variables.bas or cy-taille < Variables.haut):
            return

        pcx = int(Variables.mouseX + self.x / self.pz * Variables.width/2)
        pcy = int(Variables.mouseY - self.y / self.pz * Variables.height/2)

        if (self.z > 0):
            coef = (self.zinit - self.z) / self.zinit * \
                math.pow((Variables.distanceMax - self.distance) / Variables.distanceMax, 2)
        else:
            coef = 1
        couleur = [int(c*coef) for c in self.couleur]

        return couleur, (pcx, pcy), (cx, cy), taille

    def update(self):
        self.pz = self.z + 4*self.vitesse
        self.z -= self.vitesse


if __name__ == '__main__':
    from exec import run
    run(locals())
