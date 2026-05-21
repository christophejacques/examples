import pygame

from math import cos, sin, pi
from typing import List, Tuple
from time import sleep
from threading import Thread


class Var:
    page1: pygame.Surface
    page2: pygame.Surface

    x = 0
    y = 0
    acceleration = 0
    vitesse = 0
    p1 = [0, 0]
    p2 = [0, 0]

    LARGEUR = 800
    HAUTEUR = 600


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


# 5. Horloge pour contrôler la vitesse (FPS)
horloge = pygame.time.Clock()

# 3. Définition des couleurs (RGB)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
JAUNE = (255, 255, 0)
VIOLET = (255, 0, 250)
CYAN = (0, 255, 255)
BLANC = (255, 255, 255)


class Page:

    nom: str
    liste_switch: List[Tuple[int, int]]
    index_switch: int

    def __init__(self, nom: str, contenu, x: int = 0, y: int = 0, color: tuple = (0, 0, 0)): 
        self.nom = nom
        self.set(x, y)
        self.color = color
        self.content = pygame.Surface(Ecran.SIZE)

        self.contenu = contenu
        self.contenu.draw(self.content)

        self.vitesse = 0
        self.acceleration = Ecran.SIZE[0] // 40

    def resize(self):
        # fprint(f"Page resize({Ecran.SIZE})", self.index_switch)
        self.content = pygame.Surface(Ecran.SIZE)
        self.acceleration = Ecran.SIZE[0] // 40

        if self.x == self.liste_switch[self.index_switch][0]:
            index_coord = 0
        else:
            index_coord = 1

        msg = f"AVANT: x,y: ({self.x:5}, {self.y:5}), "
        msg += f"deb,fin: ({self.debut:5}, {self.fin:5})"
        msg += f" index: {index_coord}"
        # fprint(msg, end=" => ")

        self.contenu.resize()
        self.contenu.draw(self.content)

        for index, interval in enumerate(self.liste_switch):
            debut, fin = interval
            self.liste_switch[index] = (int(debut * Ecran.DELTA), int(fin * Ecran.DELTA))

        self.x = self.liste_switch[self.index_switch][index_coord]
        self.debut, self.fin = self.liste_switch[self.index_switch]
        
        # fprint(f"APRES: x,y: ({self.x:5}, {self.y:5}), deb,fin: ({self.debut:5}, {self.fin:5})")

        msg = f"self.liste_switch[{self.index_switch}][{index_coord}] : "
        msg += f"{self.liste_switch[self.index_switch]} => "
        msg += f"{self.liste_switch[self.index_switch][index_coord]}"
        msg += f" ?= x={self.x}"
        # fprint(msg)

    def set_liste_switch(self, liste: List[Tuple[int, int]]):
        
        # fprint(self.nom, "set_liste", liste)

        fin = liste[0][1]
        for interval in liste[1:]:
            if fin != interval[0]:
                raise Exception(f"La liste n'est pas continue ({fin} != {interval[0]})")
            fin = interval[1]

        index_trouve = False
        self.liste_switch = liste
        for index, interval in enumerate(liste):
            debut, fin = interval
            # fprint(self.nom, "seek", self.x, "in", (debut, fin))

            if self.x == debut or self.x == fin:
                self.index_switch = index
                index_trouve = True
                # fprint(f"done ({index})")
                break

        if not index_trouve:
            raise Exception(f"la coordonnée x ({self.x}) n'est pas au debut ou la fin d'un des intervals")

        self.debut, self.fin = self.liste_switch[self.index_switch]

    def switch(self, direction: str):
        if direction.upper() == "RIGHT":
            # Direction RIGHT
            coef = -1
            if self.x == self.fin:
                self.vitesse = coef * self.acceleration
                return

            if self.index_switch > 0:
                self.index_switch -= 1
            elif self.x == self.debut:
                return

        else:
            # Direction LEFT
            coef = 1
            if self.x == self.debut:
                self.vitesse = coef * self.acceleration
                return
                
            if self.index_switch < len(self.liste_switch)-1:
                self.index_switch += 1
            elif self.x == self.fin:
                return
                
        self.debut, self.fin = self.liste_switch[self.index_switch]
        # fprint(f"{self.nom}: [{self.x:5}] {self.debut:5} > {self.fin:5}")
        self.vitesse = coef * self.acceleration

    def animation(self):
        if self.vitesse == 0:
            return

        if self.vitesse > 0:
            if self.x >= self.fin:
                self.vitesse = 0
                self.x = self.fin
            else:
                self.x += self.vitesse

        else:
            if self.x <= self.debut:
                self.vitesse = 0
                self.x = self.debut
            else:
                self.x += self.vitesse

    def position(self):
        return self.x, self.y

    def set(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def move(self, dx: int = 0, dy: int = 0):
        self.x += dx
        self.y += dy


class Ecran:
    SIZE: List = [0, 0]
    DELTA: float = 0.0
    pages: List[Page] = list()

    def __init__(self, size):
        # 1. Initialisation de Pygame
        pygame.init()
        self.is_open = True
        self.switching = False
        self.go_left = True

        Ecran.SIZE = size
        self.screen = pygame.display.set_mode(Ecran.SIZE, pygame.RESIZABLE)
        pygame.display.set_caption("Switch 2 Ecrans")

    def add(self, page: Page):
        self.pages.append(page)

    def close(self):
        self.is_open = False
        pygame.quit()

    def resize(self):
        size = self.screen.get_size()
        Ecran.DELTA = size[0] / Ecran.SIZE[0]
        Ecran.SIZE = size
        fprint(f"Ecran resize({Ecran.SIZE})")

        for page in self.pages:
            page.resize()

    def switch(self, direction: str):
        if self.switching:
            return

        for page in self.pages:
            page.switch(direction)

        Thread(target=self.animation).start()

    def animation(self):
        self.switching = True
        while self.switching:
            sleep(0.006)
            for page in self.pages:
                page.animation()

            self.switching = any([page.vitesse != 0 for page in self.pages])

    def draw(self):

        for page in self.pages:
            # fprint(page.content, page.position())
            self.screen.blit(page.content, page.position())

        pygame.display.flip()


class Carre:

    def __init__(self, taille=20):
        self.taille = taille
        self.resize()

    def resize(self):
        self.largeur, self.hauteur = Ecran.SIZE
        self.x = self.largeur//2-self.taille 
        self.y = self.hauteur//2-self.taille

    def draw(self, content):
        # Dessine la page 1
        for i in range(self.largeur//10):
            pygame.draw.line(content, JAUNE, (10*i, 0), 
                (self.largeur-10*i, self.hauteur))
        pygame.draw.rect(content, ROUGE, (self.x, self.y, 
            2*self.taille, 2*self.taille))


class Cercle:
    def __init__(self, rayon=40):
        self.rayon = rayon
        self.resize()

    def resize(self):
        self.largeur, self.hauteur = Ecran.SIZE
        self.cx, self.cy = self.largeur//2, self.hauteur//2

    def draw(self, content):
        # Dessine la page 1
        for i in range(self.hauteur//10):
            pygame.draw.line(content, VIOLET, (0, 10*i), 
                (self.largeur, self.hauteur-10*i))
        pygame.draw.circle(content, CYAN, (self.cx, self.cy), self.rayon)


class Triangle:
    def __init__(self, rayon=40):
        self.rayon = rayon
        self.resize()

    def resize(self):
        pi_sur_2 = pi / 2
        deux_pi_sur_3 = 2 * pi / 3

        self.largeur, self.hauteur = Ecran.SIZE
        self.cx, self.cy = self.largeur//2, self.hauteur//2
        self.coords = [(self.cx, self.cy - self.rayon), 
            (self.cx + self.rayon*cos(pi_sur_2-deux_pi_sur_3), 
                self.cy - self.rayon*sin(pi_sur_2-deux_pi_sur_3)),
            (self.cx + self.rayon*cos(pi_sur_2+deux_pi_sur_3), 
                self.cy - self.rayon*sin(pi_sur_2+deux_pi_sur_3))]

    def draw(self, content):
        # Dessine la page 3
        for i in range(self.largeur//10):
            pygame.draw.line(content, VERT, (10*i, 0), 
                (self.largeur-10*i, self.hauteur))
        pygame.draw.polygon(content, ROUGE, self.coords)


def main():
    ecran = Ecran([800, 600])

    w = Ecran.SIZE[0]

    carre = Carre(40)
    page1 = Page("P1", carre, color=(20, 200, 20))
    page1.set_liste_switch([(-2*w, -w), (-w, 0)])
    ecran.add(page1)

    cercle = Cercle(40)
    page2 = Page("P2", cercle, w, 0, (20, 200, 200))
    page2.set_liste_switch([(-w, 0), (0, w)])
    ecran.add(page2)

    triangle = Triangle(50)
    page3 = Page("P3", triangle, 2*w, 0, (20, 200, 200))
    page3.set_liste_switch([(0, w), (w, 2*w)])
    ecran.add(page3)

    while ecran.is_open:
        # Réduire l'utilisation du processeur et fixer à 60 images par seconde
        horloge.tick(60)

        ecran.draw()
        
        for evenement in pygame.event.get():
            if evenement.type in (1541, 4352, 32770, 32774, 32776, 32768, 
                    32783, 32784, 32785):
                pass
            elif evenement.type in (769,):
                if evenement.key == pygame.K_ESCAPE:
                    ecran.close()

                elif evenement.key == pygame.K_LEFT:
                    ecran.switch("LEFT")

                elif evenement.key == pygame.K_RIGHT:
                    ecran.switch("RIGHT")

            elif evenement.type in (768, 770, 771):
                # key up & down + text
                pass
            elif evenement.type == 1024:
                # mouse move
                pass
            elif evenement.type == 32769:
                ecran.resize()
            else:
                pass
                # fprint(evenement)

            if evenement.type == pygame.QUIT:
                ecran.close()

    # touches = pygame.key.get_pressed()
    # if touches[pygame.K_LEFT]:
    # elif touches[pygame.K_RIGHT]:


if __name__ == "__main__":
    main()
