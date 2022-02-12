import pygame
import math
import random
from window import AbstractZoneContent


class Variables:
    gauche, haut = 0, 0
    droite, bas = 0, 0
    width, height = 0, 0
    mouseX = 0
    mouseY = 0
    distanceMax = 0


class StarField(AbstractZoneContent):

    def __init__(self, nb_max):
        self.maximum = nb_max
        self.liste = []

    def set_zone(self, new_zone):
        Variables.gauche, Variables.haut = new_zone[0]
        Variables.droite, Variables.bas = new_zone[1]
        Variables.width = Variables.droite - Variables.gauche
        Variables.height = Variables.bas - Variables.haut
        Variables.mouseX = Variables.gauche + Variables.width/2
        Variables.mouseY = Variables.haut + Variables.height/2
        Variables.distanceMax = \
            math.sqrt(Variables.width*Variables.width/4 + Variables.height*Variables.height/4)

    def update(self):
        if len(self.liste) < self.maximum:
            self.liste.append(Star())

        for etoile in self.liste:
            etoile.update()

    def draw(self):
        for i, etoile in enumerate(self.liste):
            res = etoile.get_attrs()
            if res:
                couleur, pstar, star, taille = res
                pygame.draw.line(self.screen, couleur, pstar, star)
                pygame.draw.circle(self.screen, couleur, star, taille)
            else:
                self.liste.pop(i)


class Star:

    def __init__(this):

        boucle = True
        while boucle:
            this.x = Variables.width/2 - random.random() * Variables.width
            this.y = Variables.height/2 - random.random() * Variables.height
            boucle = math.sqrt(this.x*this.x + this.y*this.y) < 50 or abs(this.x) < 5 or abs(this.y) < 5

        this.z = 500 + random.random() * 1000
        this.pz = this.z

        this.zinit = this.z + random.random() * 1000

        this.distance = math.sqrt(this.x*this.x + this.y*this.y)
        this.vitesse = 4 * Variables.distanceMax / this.distance

        this.couleur = (random.random() * 100,
                        100 + random.random() * 155,
                        100 + random.random() * 155
                        )

    def get_attrs(this):
        cx = int(Variables.mouseX + this.x / this.z * Variables.width/2)
        cy = int(Variables.mouseY - this.y / this.z * Variables.height/2)

        taille = int(10 * abs(this.zinit - this.z) / this.zinit)
        if (cx+taille > Variables.droite or cx-taille < Variables.gauche or cy+taille > Variables.bas or cy-taille < Variables.haut):
            return

        pcx = int(Variables.mouseX + this.x / this.pz * Variables.width/2)
        pcy = int(Variables.mouseY - this.y / this.pz * Variables.height/2)

        if (this.z > 0):
            coef = (this.zinit - this.z) / this.zinit * \
                math.pow((Variables.distanceMax - this.distance) / Variables.distanceMax, 2)
        else:
            coef = 1
        couleur = [int(c*coef) for c in this.couleur]

        return couleur, (pcx, pcy), (cx, cy), taille

    def update(this):
        this.pz = this.z + 4*this.vitesse
        this.z -= this.vitesse


def main():

    pygame.init()
    window_size = (1440, 900)
    if False:
        screen = pygame.display.set_mode((1920, 1080), flags=pygame.NOFRAME)
    else:
        screen = pygame.display.set_mode(window_size, flags=pygame.RESIZABLE)
    print(help(screen.fill))

    s = StarField(100)
    s.set_screen(screen)
    s.set_zone(((0, 0), pygame.display.get_window_size()))

    clock = pygame.time.Clock()
    Application_launched = True
    while Application_launched:
        # 60 images/s
        clock.tick(60)

        screen.fill((0, 0, 0), rect=((50, 50), (500, 600)))
        s.update()
        s.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                key_code = event.dict.get("key", 0)

                if key_code == pygame.K_ESCAPE:
                    Application_launched = False

                if key_code == pygame.K_f:
                    print("Full screen")

            # - Croix "X" de la fenetre -------------------------------------------
            if event.type == pygame.QUIT:
                Application_launched = False

            # - fenetre redimensionnée ------------------------------------------------------------------------
            elif event.type == pygame.VIDEORESIZE:
                w = event.dict.get('w')
                h = event.dict.get('h')
                print(f"change Screen Resolution = {w}x{h}")
                window_size = (w, h)
                s.set_zone(((0, 0), window_size))


if __name__ == '__main__':
    main()
