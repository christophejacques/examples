import traceback
import pygame
import json
from time import perf_counter


def get_pygame_const_name(index):
    for c in dir(pygame):
        if c[1] in "AZERTYUIOPMLKJHGFDSQWXCVBN":
            if type(getattr(pygame, c)) == int and getattr(pygame, c) == index:
                return c


class Couleur:
    def __init__(self, r: int, g: int, b: int, alpha: int = 255):
        self.r = r
        self.g = g
        self.b = b
        self.alpha = alpha

    def to_tuple(self):
        return (self.r, self.g, self.b, self.alpha)


class Position:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def in_zone(self, zone):
        res = zone.p1.x <= self.x <= zone.p2.x and zone.p1.y <= self.y <= zone.p2.y 
        return res

    def to_tuple(self):
        return (self.x, self.y)

    def copy(self):
        return Position(self.x, self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Zone:

    def __init__(self, p1: Position, p2: Position):
        if isinstance(p1, Position) and isinstance(p2, Position):
            self.p1 = p1
            self.p2 = p2

        elif (isinstance(p1, tuple) and isinstance(p2, tuple)) or (isinstance(p1, list) and isinstance(p2, list)):
            if len(p1) != 2 or len(p2) != 2:
                raise TypeError(f"les tuples {p1} et/ou {p2} ne sont pas de taille 2.")

            self.p1 = Position(*p1)
            self.p2 = Position(*p2)

        else:
            raise TypeError(f"les coordonnées {p1} et/ou {p2} ne sont pas de type Position.")

        self.dx = self.p2.x - self.p1.x
        self.dy = self.p2.y - self.p1.y
        self.decal = 5
        self.fonc_width = 35
        self.fonc_height = 25

    def move(self, decal: list):
        self.p1.x += decal[0]
        self.p1.y += decal[1]
        self.p2.x += decal[0]
        self.p2.y += decal[1]
        self.dx = self.p2.x - self.p1.x
        self.dy = self.p2.y - self.p1.y

    def contains(self, pos: Position):
        return pos.in_zone(self)

    def to_box(self, fonction, cut_left_border=False):
        if fonction.lower() == "close":
            return ((self.p2.x-self.decal-self.fonc_width, self.p1.y), (self.fonc_width, self.fonc_height))

        elif fonction.lower() == "left":
            return self.p1.to_tuple(), (self.decal, self.dy)
        elif fonction.lower() == "right":
            return (self.p2.x-self.decal, self.p1.y), (self.decal, self.dy)
        elif fonction.lower() == "bottom":
            if cut_left_border and self.p1.x < 0:
                return (0, self.p2.y-self.decal), (self.dx+self.p1.x, self.decal)
            else:
                return (self.p1.x, self.p2.y-self.decal), (self.dx, self.decal)

        elif fonction.lower() == "maximize_symbol":
            posx1 = self.p1.x + 1+(3*self.fonc_width)//8
            posy1 = self.p1.y + 9
            return pygame.Rect(posx1, posy1, self.fonc_width//4, 1+self.fonc_height//4)

    def to_line(self, cote):
        if cote.lower() == "close_slash":
            posx1 = self.p1.x + 3+self.fonc_width//3
            posx2 = self.p2.x - 3-self.fonc_width//3
            posy1 = self.p2.y - 10
            posy2 = self.p1.y + 9
            return (posx1, posy1), (posx2, posy2)
        if cote.lower() == "close_anti_slash":
            posx1 = self.p1.x + 3+self.fonc_width//3
            posx2 = self.p2.x - 3-self.fonc_width//3
            posy2 = self.p2.y - 10
            posy1 = self.p1.y + 9
            return (posx1, posy1), (posx2, posy2)

        elif cote.lower() == "maximize_symbol_top":
            posx = self.p1.x + 3+(3*self.fonc_width)//8
            posy = self.p1.y + 7
            return (posx, posy), (posx+8, posy)
        elif cote.lower() == "maximize_symbol_right":
            posx = self.p2.x - self.fonc_width//3
            posy1 = self.p1.y + 8
            posy2 = self.p2.y - 12
            return (posx, posy1), (posx, posy2)

        elif cote.lower() == "minimize_symbol":
            posx = self.p1.x + 1+self.fonc_width//3
            posy = self.p2.y - 10
            return (posx, posy), (posx+9, posy)

        elif cote.lower() == "left":
            return self.p1.to_tuple(), (self.p1.x, self.p2.y)
        elif cote.lower() == "right":
            return (self.p2.x-1, self.p1.y), (self.p2.x-1, self.p2.y)
        elif cote.lower() == "bottom":
            return (self.p1.x, self.p2.y), (self.p2.x-1, self.p2.y)
        elif cote.lower() == "top":
            return self.p1.to_tuple(), (self.p2.x-1, self.p1.y)

    def to_tuple(self, cut_left_border=False):
        if cut_left_border and self.p1.x < 0:
            return ((0, self.p1.y), (self.dx+self.p1.x, self.dy))
        else:
            return (self.p1.to_tuple(), (self.dx, self.dy))

    def __str__(self):
        return f"({self.p1}, {self.p2})"


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


class Ecran:

    def __init__(self, titre: str):
        self.windows = []
        self.icones = []
        self.raccourcis = []
        self.active_window = None
        self.active_icone = None
        pygame.init()

        self.theme_bg = Couleur(10, 130, 170).to_tuple()
        self.barre_color = Couleur(20, 20, 20, 100).to_tuple()
        self.image = pygame.image.load(r".\screenshots\black-wallpaper-hd-30.jpg")
        # self.image = pygame.image.load(r"D:\Mes Documents\Images\Wallpaper\Blacked_5_092.jpg")
        # self.image = pygame.image.load(r"D:\Mes Documents\Images\Wallpaper\Blue-and-Purple-Background-for-PC.jpg")
        *_, img_width, img_height = self.image.get_rect()
        self.img_coef = img_width / img_height
        
        self.set_zone((1600, 800))
        self.screen = pygame.display.set_mode(self.zone_barre_taches.p2.to_tuple(), flags=pygame.HWSURFACE+pygame.SRCALPHA+pygame.RESIZABLE, depth=32, display=0)

        pygame.display.set_caption(titre)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAIT)
        
    @property
    def active_raccourci(self):
        for raccourci in self.raccourcis:
            if raccourci.is_under_cursor:
                return raccourci
        return None

    def shutdown(self):
        self.save_raccourcis()
        self.windows = []
        self.icones = []
        self.raccourcis = []
        self.active_window = None
        self.active_icone = None

    def set_zone(self, zone):
        self.background = pygame.transform.scale(self.image, (zone[0], zone[0]//self.img_coef))
        self.zone = Zone(Position(0, 0), Position(zone[0], zone[1]-30))
        self.zone_barre_taches = Zone(
            Position(self.zone.p1.x, self.zone.p2.y), 
            Position(self.zone.p2.x, self.zone.p2.y+30))
        Tache_Icone.zoneb = self.zone_barre_taches
        for window in self.windows:
            if window.etat[-1] == "maximized":
                window.set_zone(self.zone)
        if self.active_window:
            if self.active_window.etat[-1] == "maximized":
                self.active_window.set_zone(self.zone)
        if self.active_icone:
            for icone in (self.icones+[self.active_icone]):
                icone.generate()

    def get_window_by_idx(self, index):
        for window in (self.windows + [self.active_window]):
            if window.index == index:
                return window
        return None

    def get_icone_by_idx(self, index):
        for icone in (self.icones + [self.active_icone]):
            if icone.idx_window == index:
                return icone
        return None

    def open_all_raccourcis(self):
        for raccourci in self.raccourcis:
            self.create_new_window(raccourci.get_window())

    def add_raccourci(self, window, zone=None):
        if not isinstance(window, Window):
            raise TypeError("Le paramètre n'est pas de type Window")
        raccourci = Raccourci(window, zone)
        if not zone:
            if self.raccourcis:
                px = self.raccourcis[-1].zone.p2.x + 10
                py = self.raccourcis[-1].zone.p1.y
                if px > self.zone.p2.x:
                    px = 10
                raccourci.zone = Zone(
                    Position(px, py),
                    Position(px+80, py+60))
            else:
                raccourci.zone = Zone(
                    Position(10, 10), 
                    Position(90, 70))
        raccourci.screen = self.screen
        self.raccourcis.append(raccourci)
    
    def create_new_window(self, window: Window):
        if not isinstance(window, Window):
            raise TypeError(f"La fenêtre {window} n'est pas de type Window.")

        if window == self.active_window and self.active_window.etat[-1] == "minimized":
            self.active_window_by_index(window.index)
            return 
        if window in self.windows:
            self.active_window_by_index(window.index)
            return

        self.add(window)

    def add(self, window: Window):
        if not isinstance(window, Window):
            raise TypeError(f"La fenêtre {window} n'est pas de type Window.")

        if self.active_window:
            self.windows.append(self.active_window)
            self.icones.append(self.active_icone)

        window.screen = self.screen
        self.active_window = window
        icone = Tache_Icone(window.index, window.title)
        icone.screen = self.screen
        self.active_icone = icone

    def check_win_buttons(self, mouse_position: Position):
        if self.active_window is None:
            return False

        for window in reversed(self.windows + [self.active_window]):
            window.cursor_zone = None

        window_spoted = False
        for window in reversed(self.windows + [self.active_window]):
            if window.etat[-1] == "minimized":
                continue
            if window.zone_title.contains(mouse_position):
                if mouse_position.in_zone(window.zone_close):
                    window_spoted = True
                    window.cursor_zone = window.zone_close
                    break
                elif mouse_position.in_zone(window.zone_maximize):
                    window_spoted = True
                    window.cursor_zone = window.zone_maximize
                    break
                elif mouse_position.in_zone(window.zone_minimize):
                    window_spoted = True
                    window.cursor_zone = window.zone_minimize
                    break

            if window.zone.contains(mouse_position) and not window_spoted:
                window_spoted = True
                if Zone(
                    (window.zone_title.p1.x, window.zone_title.p2.y), (
                     window.zone.p1.x+window.zone.decal, window.zone.p2.y)).contains(mouse_position):
                    window.cursor_zone = "LEFT"
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
                elif Zone(
                    (window.zone_title.p2.x-window.zone.decal, window.zone_title.p2.y), (
                     window.zone.p2.x, window.zone.p2.y)).contains(mouse_position):
                    window.cursor_zone = "RIGHT"
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
                elif Zone(
                    (window.zone.p1.x, window.zone.p2.y-window.zone.decal), (
                     window.zone.p2.x, window.zone.p2.y)).contains(mouse_position):
                    window.cursor_zone = "BOTTOM"
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                break

            elif not window_spoted:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        return window_spoted

    def get_raccourci_clicked(self):
        for raccourci in (self.raccourcis):
            if raccourci.is_under_cursor:
                return raccourci
        return None

    def check_mouse_over_raccourcis(self, mouse_position: Position, window_spoted):
        for raccourci in (self.raccourcis):
            raccourci.is_under_cursor = False
        if window_spoted:
            return False

        if not mouse_position.in_zone(self.zone):
            return False

        for raccourci in (self.raccourcis):
            if mouse_position.in_zone(raccourci.zone):
                raccourci.is_under_cursor = True

    def check_mouse_over_icones(self, mouse_position: Position):
        if self.active_window is None:
            return False
        for icone in (self.icones + [self.active_icone]):
            icone.is_under_cursor = False

        if not mouse_position.in_zone(self.zone_barre_taches):
            return False

        for icone in (self.icones + [self.active_icone]):
            if mouse_position.in_zone(icone.zone):
                icone.is_under_cursor = True

    def select_raccourci(self, mouse_position: Position):
        for raccourci in self.raccourcis:
            if raccourci.contains(mouse_position):
                return True
        return False

    def select_window(self, mouse_position: Position):
        if self.active_window:
            if self.active_window.etat[-1] == "minimized" or not self.active_window.contains(mouse_position):
                for window in reversed(self.windows):
                    if window.etat[-1] != "minimized" and window.contains(mouse_position):
                        self.add(self.active_window)
                        self.active_window = window
                        self.windows.remove(window)

                        self.active_icone = self.get_icone_by_idx(window.index)
                        self.icones.remove(self.get_icone_by_idx(window.index))
                        Tache_Icone.nombre -= 1
                        break
            return mouse_position.in_zone(
                Zone(self.active_window.zone_title.p1, Position(
                        self.active_window.zone_minimize.p1.x, self.active_window.zone_minimize.p2.y)))
        return False

    def active_last_window(self):
        for window in reversed(self.windows):
            if window.etat[-1] != "minimized":
                self.add(self.active_window)
                self.active_window = window
                self.windows.remove(window)

                self.active_icone = self.get_icone_by_idx(window.index)
                self.icones.remove(self.get_icone_by_idx(window.index))
                Tache_Icone.nombre -= 1
                break

    def active_window_by_index(self, index):
        if self.get_window_by_idx(index) == self.active_window:
            if self.active_window.etat[-1] == "minimized":
                self.active_window.etat.pop()
                self.active_window.animation = Animation(
                    self.active_icone.zone,
                    self.active_window.zone_title)
            return

        for window in self.windows:
            if window.index == index:
                window_was_minimized = False
                if window.etat[-1] == "minimized":
                    window.etat.pop()
                    window_was_minimized = True

                self.add(self.active_window)
                self.active_window = window
                self.windows.remove(window)

                self.active_icone = self.get_icone_by_idx(window.index)
                self.icones.remove(self.get_icone_by_idx(window.index))
                Tache_Icone.nombre -= 1

                if window_was_minimized:
                    self.active_window.animation = Animation(
                        self.active_icone.zone,
                        self.active_window.zone_title)
                break

    def active_window_by_icone(self):
        if self.active_icone:
            if self.active_icone.is_under_cursor and self.active_window.etat[-1] != "minimized":
                self.active_window.etat.append("minimized")
                self.active_window.animation = Animation(
                    self.active_window.zone_title, 
                    self.active_icone.zone)
                
                self.active_last_window()
                return

        for icone in self.icones:
            if icone.is_under_cursor:
                window = self.get_window_by_idx(icone.idx_window)
                # print("select window ID:", icone.idx_window, window.index)
                self.add(self.active_window)
                self.active_window = window
                self.windows.remove(window)
                self.active_icone = self.get_icone_by_idx(window.index)
                self.icones.remove(self.get_icone_by_idx(window.index))
                Tache_Icone.nombre -= 1
                break

        if self.active_icone:
            if self.active_icone.is_under_cursor and self.active_window.etat[-1] == "minimized":
                self.active_window.etat.pop()
                self.active_window.animation = Animation(
                    self.active_icone.zone,
                    self.active_window.zone_title)
                return

    def update_window_index(self):
        index_max = -1
        for window in self.windows:
            if window.index > index_max:
                index_max = window.index
        Window.cindex = index_max+1

    def kill(self):
        if self.active_window:
            Tache_Icone.nombre -= 1
            deleted_index = self.active_icone.index
            self.active_window = None
            self.active_icone = None
            self.update_window_index()
            if self.windows:
                self.active_window = self.windows.pop()
                self.active_icone = self.get_icone_by_idx(self.active_window.index)

            if self.active_window:
                if self.get_icone_by_idx(self.active_window.index) in self.icones:
                    self.icones.remove(self.get_icone_by_idx(self.active_window.index))
                    for icone in self.icones:
                        if icone.index > deleted_index:
                            icone.set_index(icone.index-1)

                if self.active_icone.index > deleted_index:
                    self.active_icone.set_index(self.active_icone.index-1)

    def load_raccourcis(self):
        contenu = {}
        # self.add_raccourci(Window("Sublime Text", Zone(Position(100, 20), Position(500, 300)), Couleur(50, 70, 100)))
        # self.add_raccourci(Window("Mozilla Firefox", Zone(Position(140, 60), Position(540, 340)), Couleur(50, 70, 100)))
        # self.add_raccourci(Window("Ce PC", Zone(Position(180, 100), Position(580, 380)), Couleur(50, 70, 100)))
        # self.add_raccourci(Window("Microsoft Edge", Zone(Position(220, 140), Position(620, 420)), Couleur(50, 70, 100)))

        with open('desktop.json') as file_handle:
            contenu = json.loads(file_handle.read())
            for nom, donnees in contenu.items():
                self.add_raccourci(Window(
                    nom, Zone(*donnees["window"]), 
                    Couleur(*donnees["couleur"])), 
                    Zone(*donnees["raccourci"]))
        
    def save_raccourcis(self):
        contenu = {}
        with open('desktop.json', 'w') as file_handle:
            for raccourci in self.raccourcis:
                contenu[raccourci.title] = {}
                contenu[raccourci.title]["raccourci"] = raccourci.zone.p1.to_tuple(), raccourci.zone.p2.to_tuple()
                contenu[raccourci.title]["window"] = raccourci.window.zone.p1.to_tuple(), raccourci.window.zone.p2.to_tuple()
                contenu[raccourci.title]["couleur"] = raccourci.window.bg_color.to_tuple()
            file_handle.write(json.dumps(contenu))

    def refresh(self):
        # self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        for raccourci in self.raccourcis:
            raccourci.draw()
        for win in self.windows:
            win.draw(False)
        if self.active_window:
            self.active_window.draw(True)

        self.screen.fill(self.barre_color, rect=self.zone_barre_taches.to_tuple())
        if self.active_icone:
            for tache_icone in (self.icones+[self.active_icone]):
                tache_icone.draw(False)
            self.active_icone.draw(True)

        pygame.display.update()


class Mouse:
    DBL_CLCIK_DELAY = 0.3
    left_button_down = False
    down_position = (0, 0)
    selected_object = None

    @classmethod
    def __init__(self):
        self.time = [perf_counter()]

    @classmethod
    def click(self):
        self.time.append(perf_counter())
        if len(self.time) > 2:
            self.time.pop(0)

    @classmethod
    def has_double_clicked(self):
        if len(self.time) > 1:
            res = self.time[-1]-self.time[-2] <= Mouse.DBL_CLCIK_DELAY
            return res
        else:
            return False


def main():
    mouse = Mouse()
    ecran = Ecran("My Windows pygame")
    ecran.load_raccourcis()

    application_affichee = True
    mouse.left_button_down = False

    while application_affichee:
        ecran.refresh()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.KEYUP:
                key_code = event.dict.get("key", 0)
                # key_mode = event.dict.get("mod", 0)

                if key_code == pygame.K_ESCAPE:
                    application_affichee = False

                elif key_code == pygame.K_k:
                    ecran.kill()

                elif key_code == pygame.K_n:
                    ecran.open_all_raccourcis()

            elif event.type == pygame.QUIT:
                application_affichee = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse.left_button_down = event.button == 1
                mouse.selected_object = None
                mouse.down_position = event.pos
                if mouse.left_button_down:
                    if ecran.select_window(Position(*mouse.down_position)):
                        mouse.selected_object = "WINDOW"
                    elif ecran.select_raccourci(Position(*mouse.down_position)):
                        mouse.selected_object = "RACCOURCI"
                    else:
                        window_spoted = ecran.check_win_buttons(Position(*event.pos))

            elif event.type == pygame.MOUSEBUTTONUP:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                if event.button == 1:
                    mouse.click()
                    if mouse.selected_object == "WINDOW" and mouse.has_double_clicked():
                        ecran.active_window.transparent = False
                        mouse.left_button_down = False
                        mouse.selected_object = None
                        if ecran.active_window.etat[-1] == "maximized":
                            ecran.active_window.etat.pop()
                            ecran.active_window.set_zone(ecran.active_window.zone_backup)
                            ecran.active_window.zone_backup = None
                        else:
                            ecran.active_window.zone_backup = ecran.active_window.zone
                            ecran.active_window.etat.append("maximized")
                            ecran.active_window.set_zone(ecran.zone)
                        continue

                    raccourci_clicked = ecran.get_raccourci_clicked()
                    if mouse.has_double_clicked() and raccourci_clicked:
                        mouse.left_button_down = False
                        mouse.selected_object = None
                        ecran.create_new_window(raccourci_clicked.get_window())
                        continue

                    if ecran.active_window is not None:
                        ecran.active_window.transparent = False
                        ecran.check_win_buttons(Position(*event.pos))
                        if ecran.active_window.cursor_zone is not None:
                            if ecran.active_window.cursor_zone == ecran.active_window.zone_minimize:
                                ecran.active_window.animation = Animation(
                                    ecran.active_window.zone_title, 
                                    ecran.active_icone.zone)
                                
                                ecran.active_window.etat.append("minimized")
                                ecran.active_last_window()
                            elif ecran.active_window.cursor_zone == ecran.active_window.zone_maximize:
                                if ecran.active_window.etat[-1] == "maximized":
                                    zone_title = ecran.active_window.zone_title
                                    ecran.active_window.etat.pop()
                                    ecran.active_window.set_zone(ecran.active_window.zone_backup)
                                    ecran.active_window.animation = Animation(zone_title, ecran.active_window.zone_title)
                                    ecran.active_window.zone_backup = None
                                else:
                                    zone_title = ecran.active_window.zone_title
                                    ecran.active_window.zone_backup = ecran.active_window.zone
                                    ecran.active_window.etat.append("maximized")
                                    ecran.active_window.set_zone(ecran.zone)
                                    ecran.active_window.animation = Animation(zone_title, ecran.active_window.zone_title)

                            elif ecran.active_window.cursor_zone == ecran.active_window.zone_close:
                                ecran.kill()
                        else:
                            ecran.active_window_by_icone()

                    mouse.left_button_down = False
                    mouse.selected_object = None

            elif event.type == pygame.KMOD_LGUI:
                if mouse.left_button_down and mouse.selected_object == "WINDOW":
                    ecran.active_window.transparent = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
                    dx = event.pos[0]-mouse.down_position[0]
                    dy = event.pos[1]-mouse.down_position[1]
                    mouse.down_position = event.pos
                    if ecran.active_window.etat[-1] == "maximized":
                        ecran.active_window.move_to(mouse.down_position)
                    ecran.active_window.move((dx, dy))
                elif mouse.left_button_down and mouse.selected_object == "RACCOURCI":
                    dx = event.pos[0]-mouse.down_position[0]
                    dy = event.pos[1]-mouse.down_position[1]
                    mouse.down_position = event.pos
                    ecran.active_raccourci.move((dx, dy))
                elif mouse.left_button_down and \
                    ecran.active_window.cursor_zone in ("LEFT", "RIGHT", "BOTTOM"):
                    if window_spoted:
                        if ecran.active_window.cursor_zone == "LEFT":
                            dx = event.pos[0]-mouse.down_position[0]
                            ecran.active_window.resize(dx, "LEFT")
                            mouse.down_position = event.pos
                        elif ecran.active_window.cursor_zone == "RIGHT":
                            dx = event.pos[0]-mouse.down_position[0]
                            ecran.active_window.resize(dx, "RIGHT")
                            mouse.down_position = event.pos
                        elif ecran.active_window.cursor_zone == "BOTTOM":
                            dy = event.pos[1]-mouse.down_position[1]
                            ecran.active_window.resize(dy, "BOTTOM")
                            mouse.down_position = event.pos

                else:
                    window_spoted = ecran.check_win_buttons(Position(*event.pos))
                    ecran.check_mouse_over_icones(Position(*event.pos))
                    ecran.check_mouse_over_raccourcis(Position(*event.pos), window_spoted)

            elif event.type == pygame.VIDEORESIZE:
                ecran.set_zone(event.size)
            elif event.type in (pygame.WINDOWRESIZED, pygame.WINDOWSIZECHANGED, 
                pygame.WINDOWRESTORED, pygame.WINDOWMOVED, pygame.WINDOWMAXIMIZED):
                pass
            elif event.type == pygame.ACTIVEEVENT:
                pass
            elif event.type == pygame.TEXTEDITING:
                pass
            elif event.type in [pygame.AUDIODEVICEADDED, pygame.AUDIO_S8, pygame.AUDIO_S16]:
                pass
            elif event.type == pygame.JOYDEVICEADDED:
                pass
            elif event.type == pygame.WINDOWSHOWN:
                pass
            elif event.type == pygame.WINDOWENTER:
                pass
            elif event.type == pygame.WINDOWFOCUSGAINED:
                pass
            elif event.type == pygame.VIDEOEXPOSE:
                pass

            else:
                print(get_pygame_const_name(event.type), end=" > ")
                print(event.dict, event.type)

    ecran.shutdown()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc()
    pygame.quit()
