import pygame

from math import cos, sin, pi
from typing import List, Tuple
from time import sleep
from threading import Thread


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


class Coord:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Coord({self.x}, {self.y})"


class Page:

    nom: str
    liste_switch: List[Tuple[Coord, Coord]]
    index_switch: int
    surface_page: pygame.surface.Surface

    def __init__(self, nom: str, instance_affichage, 
            coord: Coord, color: tuple = (0, 0, 0)): 
        self.nom = nom
        self.set(coord)
        self.color = color
        self.surface_page = pygame.Surface(Ecran.SIZE)
        self.surface_page.set_alpha(50)

        self.instance_affichage = instance_affichage
        self.instance_affichage.draw(self.surface_page)

        self.vitesse = 0
        self.acceleration = Ecran.SIZE[0] // 40

    def resize(self):
        # fprint(f"Page resize({Ecran.SIZE})", self.index_switch)
        self.surface_page = pygame.Surface(Ecran.SIZE)
        self.acceleration = Ecran.SIZE[0] // 40

        if Coord(self.x, self.y) == self.liste_switch[self.index_switch][0]:
            index_coord = 0
        else:
            index_coord = 1

        self.instance_affichage.resize()
        self.instance_affichage.draw(self.surface_page)

        for index, interval in enumerate(self.liste_switch):
            debut, fin = interval
            self.liste_switch[index] = (round(debut.x * Ecran.DELTA), 
                round(fin.x * Ecran.DELTA))

        self.x = self.liste_switch[self.index_switch][index_coord].x
        self.y = self.liste_switch[self.index_switch][index_coord].y
        self.debut, self.fin = self.liste_switch[self.index_switch]        
        
        # fprint(f"APRES: x,y: ({self.x:5}, {self.y:5}), deb,fin: ({self.debut:5}, {self.fin:5})")

    def switch(self, direction: str):
        pass

    def set(self, coord: Coord):
        self.x = coord.x
        self.y = coord.y

    def move(self, dx: int = 0, dy: int = 0):
        self.x += dx
        self.y += dy


class Push(Page):

    def __init__(self, nom: str, instance_affichage, 
            coord: Coord, color: tuple = (0, 0, 0)): 
        super().__init__(nom, instance_affichage, coord, color)

    def set_switch_list(self, liste: List[Tuple[Coord, Coord]]):
        # fprint(self.nom, "set_liste", liste)
        fin = liste[0][1]
        for interval in liste[1:]:
            if fin.x != interval[0].x:
                raise Exception(f"La liste n'est pas continue en x ({fin} != {interval[0]})")
            if fin.y != interval[0].y:
                raise Exception(f"La liste n'est pas continue en y ({fin} != {interval[0]})")
            fin = interval[1]

        index_trouve = False
        self.liste_switch = liste
        for index, interval in enumerate(liste):
            debut, fin = interval

            if Coord(self.x, self.y) == debut or Coord(self.x, self.y) == fin:
                self.index_switch = index
                index_trouve = True
                # fprint(f"index done ({index})")
                break

        if not index_trouve:
            raise Exception(f"la coordonnée x ({self.x}) n'est pas au debut ou la fin d'un des intervals")

        self.debut = self.liste_switch[self.index_switch][0]
        self.fin = self.liste_switch[self.index_switch][1]

    def position(self):
        return self.x, self.y

    def switch(self, direction: str):
        # fprint(f"switch({direction})")
        if direction.upper() == "RIGHT" or direction.upper() == "DOWN":
            # Direction RIGHT or DOWN
            coef = -1
            if Coord(self.x, self.y) == self.fin:
                self.vitesse = coef * self.acceleration
                return

            if self.index_switch > 0:
                self.index_switch -= 1
            elif Coord(self.x, self.y) == self.debut:
                return

        else:
            # Direction LEFT or UP
            coef = 1
            if Coord(self.x, self.y) == self.debut:
                self.vitesse = coef * self.acceleration
                # fprint("position Debut")
                return
                
            if self.index_switch < len(self.liste_switch)-1:
                self.index_switch += 1
            elif Coord(self.x, self.y) == self.fin:
                # fprint("position Fin")
                return
                
        self.debut = self.liste_switch[self.index_switch][0]
        self.fin = self.liste_switch[self.index_switch][1]
        self.vitesse = coef * self.acceleration

    def animation(self):
        if self.vitesse == 0:
            return

        if self.vitesse > 0:
            if self.x >= self.fin.x:
                self.x = self.fin.x
            else:
                self.x += self.vitesse

            if self.y >= self.fin.y:
                self.y = self.fin.y
            else:
                self.y += self.vitesse

            if Coord(self.x, self.y) == self.fin:
                self.vitesse = 0

        else:
            if self.x <= self.debut.x:
                self.x = self.debut.x
            else:
                self.x += self.vitesse

            if self.y <= self.debut.y:
                self.y = self.debut.y
            else:
                self.y += self.vitesse

            if Coord(self.x, self.y) == self.debut:
                self.vitesse = 0

            # fprint(self.index_switch, f"{self.x=}", f"{self.y=}", f"{self.vitesse=}")

    def surface_blit(self, surface_parent: pygame.surface.Surface):
        surface_parent.blit(self.surface_page, self.position())


class Ecran:
    SIZE: List = [0, 0]
    DELTA: float = 0.0
    pages: List[Page] = list()

    def __init__(self, size):
        # 1. Initialisation de Pygame
        pygame.init()
        
        self.is_open = True
        self.switching = False

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
            page.surface_blit(self.screen)

        pygame.display.flip()


class Carre:

    def __init__(self, taille=20):
        self.taille = taille
        self.resize()

    def resize(self):
        self.deltax = 100
        self.deltay = 100

        self.largeur = Ecran.SIZE[0] - 2*self.deltax
        self.hauteur = Ecran.SIZE[1] - 2*self.deltay

        self.x = self.largeur//2-self.taille 
        self.y = self.hauteur//2-self.taille

    def draw(self, surface_page: pygame.surface.Surface):
        # Dessine la page 1
        surface_page.fill((60, 60, 20))
        pygame.draw.rect(surface_page, NOIR, (
            self.deltax, self.deltay, self.largeur, self.hauteur))

        for i in range(self.largeur//10):
            pygame.draw.line(surface_page, JAUNE, (self.deltax+10*i, self.deltay), 
                (self.deltax+self.largeur-10*i, self.deltay+self.hauteur))
        pygame.draw.rect(surface_page, ROUGE, (self.deltax+self.x, self.deltay+self.y, 
            2*self.taille, 2*self.taille))

        pygame.draw.rect(surface_page, JAUNE, (
            self.deltax, self.deltay, 1+self.largeur, 1+self.hauteur), 1)


class Cercle:
    def __init__(self, rayon=40):
        self.rayon = rayon
        self.resize()

    def resize(self):
        self.largeur, self.hauteur = Ecran.SIZE
        self.cx, self.cy = self.largeur//2, self.hauteur//2

    def draw(self, surface_page: pygame.surface.Surface):
        # Dessine la page 1
        for i in range(self.hauteur//10):
            pygame.draw.line(surface_page, VIOLET, (0, 10*i), 
                (self.largeur, self.hauteur-10*i))
        pygame.draw.circle(surface_page, CYAN, (self.cx, self.cy), self.rayon)


class Triangle:
    def __init__(self, rayon=40):
        self.rayon = rayon
        self.resize()

    def resize(self):
        pi_sur_2 = pi / 2
        deux_pi_sur_3 = 2 * pi / 3

        self.deltax = 100
        self.deltay = 100

        self.largeur = Ecran.SIZE[0] - 2*self.deltax
        self.hauteur = Ecran.SIZE[1] - 2*self.deltay
        self.cx, self.cy = self.largeur//2, self.hauteur//2
        self.coords = [(self.cx, self.cy - self.rayon), 
            (self.cx + self.rayon*cos(pi_sur_2-deux_pi_sur_3), 
                self.cy - self.rayon*sin(pi_sur_2-deux_pi_sur_3)),
            (self.cx + self.rayon*cos(pi_sur_2+deux_pi_sur_3), 
                self.cy - self.rayon*sin(pi_sur_2+deux_pi_sur_3))]
        for i in range(len(self.coords)):
            self.coords[i] = (self.coords[i][0]+self.deltax, 
                self.coords[i][1]+self.deltay)

    def draw(self, surface_page: pygame.surface.Surface):
        # Dessine la page 3
        surface_page.fill((20, 60, 20))
        pygame.draw.rect(surface_page, NOIR, (
            self.deltax, self.deltay, self.largeur, self.hauteur))
        for i in range(self.largeur//10):
            pygame.draw.line(surface_page, VERT, (self.deltax+10*i, self.deltay), 
                (self.deltax + self.largeur-10*i, self.deltay+self.hauteur))

        pygame.draw.rect(surface_page, VERT, (
            self.deltax, self.deltay, 1+self.largeur, 1+self.hauteur), 1)
        pygame.draw.polygon(surface_page, ROUGE, self.coords)


def main():
    ecran = Ecran([1400, 800])

    width, height = Ecran.SIZE

    carre = Carre(40)
    page1 = Push("P1", carre, Coord(0, 0), color=(20, 200, 20))
    page1.set_switch_list([(Coord(0, -2*height), Coord(0, -height)), 
        (Coord(0, -height), Coord(0, 0))])
    ecran.add(page1)

    # carre = Carre(40)
    # page1 = Push("P1", carre, Coord(0, 0), color=(20, 200, 20))
    # page1.set_switch_list([(Coord(-2*width, 0), Coord(-width, 0)), 
    #     (Coord(-width, 0), Coord(0, 0))])
    # ecran.add(page1)

    cercle = Cercle(40)
    page2 = Push("P2", cercle, Coord(width, 0), (20, 200, 200))
    page2.set_switch_list([(Coord(-width, 0), Coord(0, 0)), 
        (Coord(0, 0), Coord(width, 0))])
    ecran.add(page2)

    triangle = Triangle(50)
    page3 = Push("P3", triangle, Coord(2*width, 0), (20, 200, 200))
    page3.set_switch_list([(Coord(0, 0), Coord(width, 0)), 
        (Coord(width, 0), Coord(2*width, 0))])
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

                elif evenement.key == pygame.K_UP:
                    ecran.switch("UP")

                elif evenement.key == pygame.K_RIGHT:
                    ecran.switch("RIGHT")

                elif evenement.key == pygame.K_DOWN:
                    ecran.switch("DOWN")

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
