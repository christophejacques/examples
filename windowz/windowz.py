import pygame
from zone import Couleur, Position, Zone


class Animation:

    def __init__(self, begin, end):

        if not (isinstance(begin, Zone) and isinstance(end, Zone)):
            raise TypeError("Les paramètres begin et end doivent être de type Zone")
        self.begin = begin
        self.end = end
        self.generate()

    def generate(self):
        self.zone = []
        taille = 20
        debut = self.begin
        fin = self.end

        dx1 = (fin.p1.x-debut.p1.x) / taille
        dx2 = (fin.p2.x-debut.p2.x) / taille
        dy1 = (fin.p1.y-debut.p1.y) / taille
        dy2 = (fin.p2.y-debut.p2.y) / taille
        for i in range(taille):
            self.zone.append(Zone(
                Position(debut.p1.x+int(i*dx1), debut.p1.y+int(i*dy1)),
                Position(debut.p2.x+int(i*dx2), debut.p2.y+int(i*dy2)),
                ))
        self.zone.append(fin)

    def print(self):
        for img in self.zone:
            print(img)


class Window:
    cindex = 0
    decal = 5
    fonc_width = 35
    fonc_height = 25

    def __init__(self, titre: str, zone: Zone, bg_color: Couleur):
        if not isinstance(zone, Zone):
            raise TypeError(f"La zone {zone} n'est pas de type Zone.")

        if not isinstance(bg_color, Couleur):
            raise TypeError(f"La couleur {bg_color} n'est pas de type Couleur.")

        self.index = Window.cindex
        self.title = titre
        Window.cindex += 1

        self.zone_backup = None
        self.etat = ["normal"]  # "minimized, maximized"
        self.set_zone(zone)
        self.bg_color = bg_color
        self.transparent = False
        self.cursor_zone = None
        self.animation = None

    def set_zone(self, zone: Zone):
        if self.etat[-1] == "normal":
            self.decal = 5
        else:
            self.decal = 0

        self.zone = zone
        self.zone_title = Zone(zone.p1.copy(), Position(zone.p2.x, zone.p1.y + self.fonc_height))
        self.zone_close = Zone(
            Position(self.zone_title.p2.x-self.decal-self.fonc_width, self.zone_title.p1.y), 
            Position(self.zone_title.p2.x-self.decal, self.zone_title.p2.y))
        self.zone_maximize = Zone(
            Position(self.zone_title.p2.x-self.decal-2*self.fonc_width, self.zone_title.p1.y), 
            Position(self.zone_title.p2.x-self.decal-self.fonc_width, self.zone_title.p2.y))
        self.zone_minimize = Zone(
            Position(self.zone_title.p2.x-self.decal-3*self.fonc_width, self.zone_title.p1.y), 
            Position(self.zone_title.p2.x-self.decal-2*self.fonc_width, self.zone_title.p2.y))

    def contains(self, pos: Position):
        return self.zone.contains(pos)

    def resize(self, decal, border):
        # print("resize " + str(decal) + " on " + border)
        p1 = self.zone.p1
        p2 = self.zone.p2
        if border == "LEFT":
            p1 = Position(self.zone.p1.x+decal, self.zone.p1.y)
        elif border == "RIGHT":
            p2 = Position(self.zone.p2.x+decal, self.zone.p2.y)
        elif border == "BOTTOM":
            p2 = Position(self.zone.p2.x, self.zone.p2.y+decal)

        self.set_zone(Zone(p1, p2))

    def move(self, decal):
        self.zone.move(decal)
        self.zone_title.move(decal)
        self.zone_minimize.move(decal)
        self.zone_maximize.move(decal)
        self.zone_close.move(decal)

    def move_to(self, mouse_position):
        self.etat.pop()
        dx = self.zone_backup.p2.x - self.zone_backup.p1.x
        dx_2 = dx // 2
        p1x = mouse_position[0] - dx_2
        p2x = p1x + dx
        p2y = self.zone_backup.p2.y - self.zone_backup.p1.y
        new_zone = Zone(Position(p1x, 0), Position(p2x, p2y))
        # print(mouse_position, self.zone_backup, ">", new_zone)
        self.set_zone(new_zone)
        self.zone_backup = None

    def draw_rect_alpha(self, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        self.screen.blit(shape_surf, rect)

    def draw(self, active_window):
        if active_window:
            theme_bg = Couleur(10, 130, 170, 50).to_tuple()
            noir = Couleur(0, 0, 0).to_tuple()
            rouge = Couleur(185, 85, 85).to_tuple()
        else:
            theme_bg = Couleur(130, 130, 150, 50).to_tuple()
            noir = Couleur(60, 60, 60).to_tuple()
            rouge = theme_bg

        if self.animation:
            if self.animation.zone:
                zone = self.animation.zone.pop(0)
                # self.screen.fill(theme_bg, rect=zone.to_tuple(True))
                self.draw_rect_alpha(theme_bg, rect=zone.to_tuple(True))
                return
            else:
                self.animation = None

        if self.etat[-1] == "minimized":
            return

        if self.transparent:
            self.draw_rect_alpha(self.bg_color.to_tuple(), rect=self.zone.to_tuple(True))
        else:
            self.screen.fill(self.bg_color.to_tuple(), rect=self.zone.to_tuple(True))
        self.screen.fill(theme_bg, rect=self.zone_title.to_tuple(True))

        font = pygame.font.SysFont("arial", 14, 0, 0)
        if active_window:
            texte = font.render(self.title, 0, Couleur(255, 255, 255).to_tuple())
        else:
            texte = font.render(self.title, 0, Couleur(50, 50, 50).to_tuple())
        self.screen.blit(texte, (self.zone_title.p1.x+25, self.zone_title.p1.y+4))

        if self.etat[-1] == "normal":
            self.screen.fill(theme_bg, rect=self.zone.to_box("left"))
            self.screen.fill(theme_bg, rect=self.zone.to_box("right"))
            self.screen.fill(theme_bg, rect=self.zone.to_box("bottom", True))

        theme_bg_clair = Couleur(70, 190, 220).to_tuple()

        if self.cursor_zone == self.zone_minimize:
            self.screen.fill(theme_bg_clair, rect=self.zone_minimize.to_tuple())
        elif self.cursor_zone == self.zone_maximize:
            self.screen.fill(theme_bg_clair, rect=self.zone_maximize.to_tuple())
        elif self.cursor_zone == self.zone_close:
            rouge = Couleur(240, 90, 90).to_tuple()

        self.screen.fill(rouge, rect=self.zone_close.to_tuple())

        pygame.draw.line(self.screen, noir, *self.zone_minimize.to_line("left"))
        pygame.draw.line(self.screen, noir, *self.zone_maximize.to_line("left"))
        pygame.draw.line(self.screen, noir, *self.zone_close.to_line("left"))
        pygame.draw.line(self.screen, noir, *self.zone_close.to_line("right"))

        pygame.draw.line(self.screen, noir, *self.zone_close.to_line("close_slash"), width=3)
        pygame.draw.line(self.screen, noir, *self.zone_close.to_line("close_anti_slash"), width=3)
        pygame.draw.line(self.screen, noir, *self.zone_minimize.to_line("minimize_symbol"), width=2)

        if self.etat[-1] == "normal":
            pygame.draw.rect(self.screen, noir, self.zone_maximize.to_box("maximize_symbol"), width=2)
        elif self.etat[-1] == "maximized":
            pygame.draw.rect(self.screen, noir, self.zone_maximize.to_box("maximize_symbol"), width=2)
            pygame.draw.line(self.screen, noir, *self.zone_maximize.to_line("maximize_symbol_top"))
            pygame.draw.line(self.screen, noir, *self.zone_maximize.to_line("maximize_symbol_right"))

        pygame.draw.line(self.screen, noir, (
             self.zone_minimize.p1.x, self.zone_minimize.p2.y), 
            (self.zone_close.p2.x-1, self.zone_close.p2.y))


if __name__ == "__main__":
    print("Compilation: OK")
