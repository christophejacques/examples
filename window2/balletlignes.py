import random
from classes import Application
from colors import Colors


class Ligne:
    MAX_VELOCITY = 3

    def __init__(self, w, h):
        self.set_max(w, h)
        self.couleur = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.coords = [[random.randint(1, w-1), random.randint(1, h-1)], 
            [random.randint(1, w-1), random.randint(1, h-1)]]
        self.vel = [[random.randint(-self.MAX_VELOCITY, self.MAX_VELOCITY), random.randint(-self.MAX_VELOCITY, self.MAX_VELOCITY)], 
            [random.randint(-self.MAX_VELOCITY, self.MAX_VELOCITY), random.randint(-self.MAX_VELOCITY, self.MAX_VELOCITY)]]

    def set_max(self, max_x, max_y):
        self.w = max_x
        self.h = max_y

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

    def __init__(self, screen, args):
        super().__init__(screen)
        self.lignes = list()
        self.resize(screen)
        nombre = self.registre.load("nombre")
        if nombre is None:
            self.nombre = args[0]
        else:
            self.nombre = nombre
        self.title = self.DEFAULT_CONFIG[0]
        self.action = ""

        self.get_theme()

    def resize(self, screen):
        print(f"demineur resize({screen})", flush=True)
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        # update max ligne values
        for ligne in self.lignes:
            ligne.set_max(self.width, self.height)

    def get_action(self):
        return self.action

    def get_theme(self):
        if self.theme.get_theme() == "CLAIR":
            self.back_color = Colors.WHITE
        else:
            self.back_color = Colors.BLACK

    def keyreleased(self, event):
        self.touche = self.keys.get_key()
        if self.touche == 27:
            self.registre.save("nombre", self.nombre)
            self.action = "QUIT"
        elif self.touche == self.keys.K_KP_PLUS:
            self.nombre += 10
        elif self.touche == self.keys.K_KP_MINUS:
            self.nombre -= 10

    def update(self):
        nb_lignes = len(self.lignes)
        if nb_lignes < self.nombre:
            self.lignes.append(Ligne(self.width, self.height))
            self.set_title(self.title + f" ({1+nb_lignes})")
        elif nb_lignes > self.nombre:
            self.lignes.pop(0)
            self.set_title(self.title + f" ({nb_lignes-1})")

        for ligne in self.lignes:
            ligne.update()

    def draw(self):
        self.screen.fill(self.back_color)
        for ligne in self.lignes:
            self.tools.line(ligne.couleur, *ligne.coords)


if __name__ == '__main__':
    from exec import run
    run(locals())
