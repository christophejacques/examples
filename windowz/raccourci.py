import pygame
from zone import Couleur, Zone, Position


class Raccourci:

    def __init__(self, window, zone):
        self.window = window
        self.title = window.title
        self.is_under_cursor = False
        self.zone = zone

    def get_window(self):
        return self.window

    def contains(self, mouse_position):
        return self.zone.contains(mouse_position)

    def move(self, decal):
        self.zone.move(decal)

    def draw(self):
        if self.zone:
            if self.is_under_cursor:
                couleur = Couleur(100, 250, 100).to_tuple()
            else:
                couleur = Couleur(150, 150, 150).to_tuple()

            pygame.draw.line(self.screen, couleur, *self.zone.to_line("top"))
            pygame.draw.line(self.screen, couleur, *self.zone.to_line("left"))
            pygame.draw.line(self.screen, couleur, *self.zone.to_line("right"))
            pygame.draw.line(self.screen, couleur, *self.zone.to_line("bottom"))

            font = pygame.font.SysFont("arial", 14, 0, 0)
            if self.is_under_cursor:
                texte = font.render(self.title, 0, Couleur(255, 255, 255).to_tuple())
            else:
                texte = font.render(self.title, 0, Couleur(125, 115, 115).to_tuple())
            self.screen.blit(texte, (self.zone.p1.x, self.zone.p2.y+4))


class Tache_Icone:

    nombre: int = 0
    zoneb: Zone = None
    decalx: int = 1
    decaly: int = 3
    decalimg: int = 7

    def __init__(self, idx: int, titre: str):
        self.set_index(Tache_Icone.nombre)
        Tache_Icone.nombre += 1
        self.idx_window = idx
        self.title = titre
        self.bg_color = Couleur(50, 50, 50).to_tuple()
        self.is_under_cursor = False

    def set_index(self, index):
        self.index = index
        self.generate()

    def generate(self):
        x1 = Tache_Icone.decalx+(Tache_Icone.decalx+140)*self.index
        y1 = self.zoneb.p1.y
        x2 = (Tache_Icone.decalx+140)*(self.index+1)
        y2 = self.zoneb.p2.y-Tache_Icone.decaly
        self.zone = Zone(Position(x1, y1), Position(x2, y2))

    def draw(self, active):
        if active:
            pygame.draw.rect(self.screen, (80, 80, 80), self.zone.to_tuple())
        else:
            pygame.draw.rect(self.screen, self.bg_color, self.zone.to_tuple())

        if self.is_under_cursor:
            pygame.draw.line(self.screen, (10, 130, 255), *self.zone.to_line("bottom"), width=2)

        font = pygame.font.SysFont("arial", 14, 0, 0)
        texte = font.render(self.title, 0, Couleur(255, 255, 255).to_tuple())

        self.screen.blit(texte, (self.zone.p1.x+Tache_Icone.decalimg, Tache_Icone.decaly+self.zone.p1.y))


if __name__ == "__main__":
    print("Compilation: OK")
