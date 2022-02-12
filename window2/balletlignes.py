import pygame
import random
from classes import Application
from colors import Colors


class Ligne:
    MAX_VELOCITY = 3

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.couleur = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.coords = [[random.randint(1, w-1), random.randint(1, h-1)], 
            [random.randint(1, w-1), random.randint(1, h-1)]]
        self.vel = [[random.randint(-self.MAX_VELOCITY, self.MAX_VELOCITY), random.randint(-self.MAX_VELOCITY, self.MAX_VELOCITY)], 
            [random.randint(-self.MAX_VELOCITY, self.MAX_VELOCITY), random.randint(-self.MAX_VELOCITY, self.MAX_VELOCITY)]]

    def update(self):
        for i in range(2):
            if (self.coords[i][0] + self.vel[i][0] < 0): 
                self.vel[i][0] = abs(self.vel[i][0])
            if (self.coords[i][0] + self.vel[i][0] > self.w): 
                self.vel[i][0] = -abs(self.vel[i][0])
                
            if (self.coords[i][1] + self.vel[i][1] < 0): 
                self.vel[i][1] = abs(self.vel[i][1])
            if (self.coords[i][1] + self.vel[i][1] > self.h): 
                self.vel[i][1] = -abs(self.vel[i][1])

        for i in range(2):
            for j in range(2):
                self.coords[i][j] += self.vel[i][j]


class BalletLignes(Application):
    MIN_SIZE = (300, 200)

    DEFAULT_CONFIG = ("BalletLignes 500", Colors.MIDDLE_RED, 500)

    def __init__(self, parent, screen, args):
        self.lignes = []
        self.resize(screen)
        self.nombre = args[0]
        self.parent = parent
        self.title = self.parent.title
        self.action = ""

    def set_parent(self, parent):
        self.parent = parent

    def resize(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        for ligne in self.lignes:
            ligne.w, ligne.h = self.width, self.height

    def get_action(self):
        return self.action

    def update(self):
        if self.parent.keypressed():
            self.touche = self.parent.get_key()
            if self.touche == 27:
                self.action = "QUIT"

        if len(self.lignes) < self.nombre:
            self.lignes.append(Ligne(self.width, self.height))
            self.parent.set_title(self.title + f" ({len(self.lignes)})")

        for ligne in self.lignes:
            ligne.update()

    def draw(self):
        self.screen.fill(Colors.BLACK)
        for ligne in self.lignes:
            pygame.draw.line(self.screen, ligne.couleur, *ligne.coords)


if __name__ == '__main__':
    print("Compilation : Ok")
