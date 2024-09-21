import pygame
import random
import math
import inspect
import traceback
from window import AbstractZoneContent


max_vel = 5
max_star_dist = 5000


class StarField(AbstractZoneContent):

    def __init__(self, nb_max):
        self.maximum = nb_max
        self.liste = []
        self.methods = []
        self.mouse_entered = False

    def set_zone(self, new_zone):
        self.zone = new_zone
        self.gauche, self.haut = new_zone[0]
        self.droite, self.bas = new_zone[1]
        self.width = self.droite - self.gauche
        self.height = self.bas - self.haut
        self.mouseX = self.gauche + self.width/2
        self.mouseY = self.haut + self.height/2
        self.distanceMax = \
            math.sqrt(self.width*self.width/4 + self.height*self.height/4)

    def update(self):
        if len(self.liste) < self.maximum:
            self.liste.append(
                Star(
                    self.width, self.height, self.distanceMax,
                    self.mouseX, self.mouseY,
                    self.gauche, self.droite, self.haut, self.bas
                    ))

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

    def __init__(this, width, height, distanceMax, mouseX, mouseY, gauche, droite, haut, bas):
        this.width = width
        this.height = height
        this.gauche = gauche
        this.droite = droite
        this.haut = haut
        this.bas = bas
        this.distanceMax = distanceMax
        this.mouseX = mouseX
        this.mouseY = mouseY

        boucle = True
        while boucle:
            this.x = this.width/2 - random.random() * this.width
            this.y = this.height/2 - random.random() * this.height
            boucle = math.sqrt(this.x*this.x + this.y*this.y) < 50 or abs(this.x) < 5 or abs(this.y) < 5

        this.z = 500 + random.random() * 1000
        this.pz = this.z

        this.zinit = this.z + random.random() * 1000

        this.distance = math.sqrt(this.x*this.x + this.y*this.y)
        this.vitesse = 4 * this.distanceMax / this.distance

        this.couleur = (random.random() * 100,
                        100 + random.random() * 155,
                        100 + random.random() * 155
                        )

    def get_attrs(this):
        cx = int(this.mouseX + this.x / this.z * this.width/2)
        cy = int(this.mouseY - this.y / this.z * this.height/2)

        taille = int(10 * abs(this.zinit - this.z) / this.zinit)
        if (cx+taille > this.droite or cx-taille < this.gauche or cy+taille > this.bas or cy-taille < this.haut):
            return

        pcx = int(this.mouseX + this.x / this.pz * this.width/2)
        pcy = int(this.mouseY - this.y / this.pz * this.height/2)

        if (this.z > 0):
            coef = (this.zinit - this.z) / this.zinit * \
                math.pow((this.distanceMax - this.distance) / this.distanceMax, 2)
        else:
            coef = 1
        couleur = [int(c*coef) for c in this.couleur]

        return couleur, (pcx, pcy), (cx, cy), taille

    def update(this):
        this.pz = this.z + 4*this.vitesse
        this.z -= this.vitesse


class Lignes(AbstractZoneContent):

    def __init__(self, nb_max: int):
        self.maximum = nb_max
        self.liste = []
        self.methods = []
        self.mouse_entered = False

    def set_zone(self, zone):
        self.zone = zone
        for ligne in self.liste:
            ligne.zone = self.zone
        # print("Lignes():", self.zone)

    def update(self):
        if len(self.liste) > self.maximum:
            self.liste.pop(0)

        elif len(self.liste) < self.maximum:
            self.liste.append(
                Ligne([random.randint(0, self.zone[1][0]), random.randint(0, self.zone[1][1])],
                      [random.randint(0, self.zone[1][0]), random.randint(0, self.zone[1][1])],
                      self.zone,
                      (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

        if len(self.liste) > 0:
            for ligne in self.liste:
                ligne.update()

    def draw(self):
        for ligne in self.liste:
            pygame.draw.line(self.screen, ligne.color, *ligne.get_coords())


class Ligne:

    def __init__(self, deb, fin, boite, color):
        self.deb = deb
        self.fin = fin
        self.zone = boite
        self.color = color

        self.veld = [0, 0]
        self.velf = [0, 0]
        while self.veld[0] == 0 or self.veld[1] == 0:
            self.veld = [random.randint(-max_vel, max_vel), random.randint(-max_vel, max_vel)]
        while self.velf[0] == 0 or self.velf[1] == 0:
            self.velf = [random.randint(max_vel, max_vel), random.randint(-max_vel, max_vel)]

    def update(self):

        for i in range(2):
            if self.deb[i] + self.veld[i] > self.zone[1][i]:
                self.veld[i] = -abs(self.veld[i])
            elif self.deb[i] + self.veld[i] < self.zone[0][i]:
                self.veld[i] = abs(self.veld[i])

            self.deb[i] += self.veld[i]

            if self.fin[i] + self.velf[i] > self.zone[1][i]:
                self.velf[i] = -abs(self.velf[i])
            elif self.fin[i] + self.velf[i] < self.zone[0][i]:
                self.velf[i] = abs(self.velf[i])

            self.fin[i] += self.velf[i]

    def get_coords(self):
        return (self.deb, self.fin)


class Graphical_Text(AbstractZoneContent):

    index = 0

    def __init__(self, texte, font="Arial", taille=12, couleur=(255, 255, 255),
            bg_color=None, alignement="Haut Gauche", decalage=(0, 0)):
        self.index = Graphical_Text.index
        Graphical_Text.index += 1
        self.couleur = couleur
        self.bg_color = bg_color
        self.pfont = pygame.font.SysFont(font, taille, 0, 0)
        self.alignement = alignement.lower()
        self.decalage = decalage
        self.set_texte(texte)
        self.mouse_entered = False
        self.methods = []

    def get_width(self):
        return self.texte[0].get_rect()[2]

    def get_height(self):
        return self.texte[0].get_rect()[3]

    def set_zone(self, boite):
        self.boite = boite
        self.calcul_position()

    def set_texte(self, texte):
        self.texte = [self.pfont.render(texte, 0, self.couleur)]

    def add_ligne(self, texte):
        self.texte.append(self.pfont.render(texte, 0, self.couleur))

    def set_color(self, couleur):
        for texte in self.texte:
            pass
            # texte.set_colorkey(None)

    def calcul_position(self):
        self.decaly = 0
        dx = 1
        dy = 2

        largeur = max([(self.texte[i].get_rect()[2]) for i in range(len(self.texte))])

        if "gauche" in self.alignement:
            dx += self.boite[0][0]
        elif "droite" in self.alignement:
            dx = self.boite[1][0] - dx - largeur
        elif "centre" in self.alignement:
            dx = self.boite[0][0] + (self.boite[1][0] - self.boite[0][0])//2 - largeur // 2 - dx

        if "haut" in self.alignement:
            dy += self.boite[0][1]
        elif "bas" in self.alignement:
            dy = self.boite[1][1] - dy - self.texte[0].get_rect()[3]
            self.decaly = -(len(self.texte)-1) * self.texte[0].get_rect()[3]
        elif "milieu" in self.alignement:
            dy = (self.boite[1][1] - self.boite[0][1]) + (self.boite[1][1] - self.boite[0][1])//2 - \
                  self.texte[0].get_rect()[3] // 2
            self.decaly = -(len(self.texte)-1) * self.texte[0].get_rect()[3] // 2

        self.dx = dx
        self.dy = dy

        self.zone = ((self.dx+self.decalage[0], self.dy+self.decalage[1] + self.decaly),
                     (self.dx+self.decalage[0]+largeur,
                         self.dy+self.decalage[1] + len(self.texte)*self.get_height() +
                         self.decaly))

    def update(self):
        pass

    def draw(self):
        if self.mouse_entered and self.bg_color is not None:
            rectangle = (self.zone[0], (self.zone[1][0]-self.zone[0][0], self.zone[1][1]-self.zone[0][1]))
            self.screen.fill(self.bg_color, rect=rectangle)

        hauteur = self.get_height()
        for i, texte in enumerate(self.texte):
            # print(texte)
            self.screen.blit(texte, (self.dx+self.decalage[0],
                                     self.dy+self.decalage[1] + i*hauteur + self.decaly))

    def on_click(self):
        res = self.methods.get(inspect.stack()[0][3])
        if res is None:
            return []
        else:
            return [res]

    # def on_mouse_enter(self):
    #     self.mouse_entered = True

    # def on_mouse_move(self, mouse_position):
    #     pass

    # def on_mouse_exit(self):
    #     self.mouse_entered = False


class Menu(AbstractZoneContent):

    def __init__(self):
        pass

    def set_zone(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass
        

def main():
    pygame.init()
    try:
        assert isinstance(StarField(0), AbstractZoneContent), "Problème de la classe StarField"
        assert isinstance(Lignes(0), AbstractZoneContent), "Problème de la classe Lignes"
        assert isinstance(Graphical_Text(""), AbstractZoneContent), "Problème de la classe Graphical_Text"
        assert isinstance(Menu(), AbstractZoneContent), "Problème de la classe Menu"
        
    except Exception:
        traceback.print_exc()

    pygame.quit()


if __name__ == '__main__':
    main()
