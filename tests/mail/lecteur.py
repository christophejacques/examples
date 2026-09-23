import pygame

# from collections import namedtuple
from os import getcwd, chdir, sep as separator
from typing import Callable, Tuple, Optional, List, Dict
from functools import partial


class Variable:

    DEBUG: bool = False


class Mouse:

    x: int
    y: int

    @classmethod
    def __init__(cls, x, y):
        cls.x = x
        cls.y = y


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


def get_pygame_const_name(index):
    for c in dir(pygame):
        if c[0] in "AZERTYUIOPMLKJHGFDSQWXCVBN":
            if type(getattr(pygame, c)) == int and getattr(pygame, c) == index:
                return c


class Lien:

    font: pygame.font.Font
    libelle: str
    posx: int
    posy: int 
    getColor: Optional[Callable]
    callback: Optional[Callable]

    mouse_over: bool
    selected: bool

    def __init__(self, 
            font: pygame.font.Font,
            libelle: str, 
            posx: int, posy: int, 
            getColor: Optional[Callable],
            callback: Optional[Callable]):
        
        self.font = font
        self.libelle = libelle
        self.set_get_color(getColor)

        self.x = posx
        self.y = posy
        
        self.w, self.h = self.surface.get_size()
        self.coords = pygame.Rect(self.x, self.y, self.w, self.h)

        self.callback = callback
        self.mouse_over = False
        self.selected = False

    def set_get_color(self, get_color: Optional[Callable]):

        if get_color is None:
            self.color = (255, 0, 0)
            self.surface = self.font.render(self.libelle, False, self.color)
            return

        self.getColor = get_color
        self.color = (0, 0, 0)
        self.update_color()

    def update_color(self):
        new_color = self.getColor()
        if self.color != new_color:
            self.color = new_color
            self.surface = self.font.render(self.libelle, False, self.color)

    def click(self):
        if self.callback:
            self.callback()

    def to_draw(self):
        return (self.surface, self.coords)


class LienToggle(Lien):

    def click(self):
        self.selected = not self.selected
        if self.callback:
            self.callback()

        self.update_color()


class Headers:

    surface: pygame.surface.Surface
    x: int
    y: int
    w: int
    h: int
    visible: bool

    def __init__(self, screen: pygame.surface.Surface, coords: Tuple):
        self.coords = coords
        self.update_screen(screen, coords)

    def update_screen(self, 
            screen: pygame.surface.Surface, coords: Optional[Tuple] = None):

        if coords is not None:
            self.coords = coords

        self.surface = screen.subsurface(self.coords)
        self.x, self.y, self.w, h = self.coords
        self.h = h - 1

    def get_color(self, index):
        if index == 1:
            return (255, 255, 255)

        return (160, 240, 220)

    def load(self, datas: Dict):
        self.liens: List[Lien] = list()

        for key, values in datas.items():
            lib, position = values

            lien1 = Lien(Lecteur.SysFont3, key,
                position, 4, partial(self.get_color, 1), None)
            self.liens.append(lien1)

            largeur = lien1.w
            lien2 = Lien(Lecteur.SysFont4, lib,
                position+largeur, 3, partial(self.get_color, 2), None)
            self.liens.append(lien2)

    def draw(self):
        self.surface.fill((40, 30, 0))

        # header
        self.surface.blits([lien.to_draw() for lien in self.liens])
        pygame.draw.line(self.surface, (50, 200, 150), (0, self.h), (self.w, self.h))


class ListeMessages:

    hauteur_ligne: int = 24

    surface: pygame.surface.Surface
    x: int
    y: int
    w: int
    h: int
    visible: bool

    mouse_over: bool
    titres: List 

    def __init__(self, screen: pygame.surface.Surface, coords: Tuple):

        self.update_screen(screen, coords)
        self.mouse_over = False

    def get_color(self, index):
        if index == 1:
            return (255, 255, 255)
        elif index == 2:
            return (255, 100, 100)

        elif index == "SEEN":
            return (200, 200, 200)

        return (160, 240, 220)

    def set_titres(self):
        self.data_titres: Dict = {
            "ATT": {"lib": "Attr", "pos": 10, "col": 1},
            "NUM": {"lib": "N°", "pos": 50, "col": 1},
            "EXP": {"lib": "Expéditeur", "pos": 50, "col": 1},
            "OBJ": {"lib": "Objet", "pos": 300, "col": 1},
            "DAT": {"lib": "Date", "pos": 580, "col": 1},
            "DIR": {"lib": r"\/", "pos": 50, "col": 2},
        }
        self.titres: List[Lien] = list()

        position: int = 0

        for cle in self.data_titres:
            position += self.data_titres[cle]["pos"]
            self.data_titres[cle]["pos"] = position

            lien = Lien(Lecteur.SysFont3, self.data_titres[cle]["lib"],
                    position, 5, 
                    partial(self.get_color, self.data_titres[cle]["col"]), None)
            self.titres.append(lien)

    @staticmethod
    def format_adresse(lib: str):
        if "<" in lib:
            return lib[:lib.index("<")-1]

        return lib

    def load(self):
        self.messages: List[Lien] = list()
        self.liste_datas: List[Dict] = list()

        self.set_titres()

        # --- E-mail ID: 8 ---
        # Date2 : 2026-09-13T16:17:01+00:00 De : Christophe <christophe.michael.jacques@proton.me>
        # Sujet : test depuis proton

        datas: Dict = {
            "ATT": "",
            "NUM": "8",
            "EXP": "Christophe <christophe.michael.jacques@proton.me>",
            "OBJ": "test depuis proton",
            "DAT": "2026-09-13T16:17:01+00:00"
        }
        self.liste_datas.append(datas)

        # --- E-mail ID: 12 ---
        # Date2 : 2026-09-17T20:31:13+00:00 De : xHamsterLive <noreply@inbox.xhamsterlive.com>
        # Sujet : TiffanyDollxxx est en ligne

        datas: Dict = {
            "ATT": "x",
            "NUM": "12",
            "EXP": "xHamsterLive <noreply@inbox.xhamsterlive.com>",
            "OBJ": "TiffanyDollxxx est en ligne",
            "DAT": "2026-09-17T20:31:13+00:00"
        }
        self.liste_datas.append(datas)

        # --- E-mail ID: 14 ---
        # Date2 : 2026-09-22T03:10:47+00:00 De : xHamsterLive <noreply@inbox.xhamsterlive.com>
        # Sujet : L'Oktoberfest te monte à la tête 🍺

        datas: Dict = {
            "ATT": "x",
            "NUM": "14",
            "EXP": "xHamsterLive <noreply@inbox.xhamsterlive.com>",
            "OBJ": "L'Oktoberfest te monte à la tête 🍺",
            "DAT": "2026-09-22T03:10:47+00:00"
        }
        self.liste_datas.append(datas)

        # --- E-mail ID: 16 ---
        # Date2 : 2026-09-22T20:40:20+00:00 De : xHamsterLive <noreply@inbox.xhamsterlive.com>
        # Sujet : TiffanyDollxxx est en ligne

        datas: Dict = {
            "ATT": "x",
            "NUM": "16",
            "EXP": "xHamsterLive <noreply@inbox.xhamsterlive.com>",
            "OBJ": "TiffanyDollxxx est en ligne",
            "DAT": "2026-09-22T20:40:20+00:00"
        }
        self.liste_datas.append(datas)

        # --- E-mail ID: 18 ---
        # Date2 : 2026-09-23T06:04:10-06:00 De : "Carrefour Banque" <ne-pas-repondre@mail.carrefour-banque.fr>
        # Sujet : Foire aux Vins : des offres à ne pas manquer !

        datas: Dict = {
            "ATT": "",
            "NUM": "18",
            "EXP": "\"Carrefour Banque\" <ne-pas-repondre@mail.carrefour-banque.fr>",
            "OBJ": "Foire aux Vins : des offres à ne pas manquer !",
            "DAT": "2026-09-23T06:04:10-06:00"
        }
        self.liste_datas.append(datas)

        # --- E-mail ID: 19 ---
        # Date2 : 2026-09-23T08:03:56-06:00 De : "Carrefour Banque" <ne-pas-repondre@mail.carrefour-banque.fr>
        # Sujet : Découvrez vos offres PASS du moment !

        datas: Dict = {
            "ATT": "",
            "NUM": "19",
            "EXP": "\"Carrefour Banque\" <ne-pas-repondre@mail.carrefour-banque.fr>",
            "OBJ": "Découvrez vos offres PASS du moment !",
            "DAT": "2026-09-23T08:03:56-06:00"
        }
        self.liste_datas.append(datas)

        # --- E-mail ID: 20 ---
        # Date1 : Wed, 23 Sep 2026 18:00:30 +0000    De : Carrefour <carrefour@email.carrefour.fr>
        # Sujet : Votre avis nous est précieux 💚

        datas: Dict = {
            "ATT": "",
            "NUM": "20",
            "EXP": "Carrefour <carrefour@email.carrefour.fr>",
            "OBJ": "Votre avis nous est précieux",
            "DAT": "Wed, 23 Sep 2026 18:00:30 +0000"
        }
        self.liste_datas.append(datas)

        # --- E-mail ID: 21 ---
        # Date2 : 2026-09-23T18:04:36+00:00 De : xHamsterLive <noreply@inbox.xhamsterlive.com>
        # Sujet : JuliaKhaleesii- est en ligne

        datas: Dict = {
            "ATT": "x",
            "NUM": "21",
            "EXP": "xHamsterLive <noreply@inbox.xhamsterlive.com>",
            "OBJ": "JuliaKhaleesii- est en ligne",
            "DAT": "2026-09-23T18:04:36+00:00"
        }
        self.liste_datas.append(datas)

        dy = 5
        for datas in self.liste_datas:
            dy += 30
            for cle in datas:
                lib = self.format_adresse(datas[cle]) if cle == "EXP" else datas[cle]
                lien = Lien(Lecteur.SysFont3, lib,
                        self.data_titres[cle]["pos"], dy, 
                        partial(self.get_color, "SEEN"), None)
                self.messages.append(lien)

    def update_screen(self, 
            screen: pygame.surface.Surface, coords: Optional[Tuple] = None):

        if coords is not None:
            self.coords = pygame.Rect(coords)

        self.surface = screen.subsurface(self.coords)
        self.x, self.y, self.w, h = self.coords
        self.h = h - 1

    def draw(self):
        self.surface.fill((10, 20, 20))

        # Ligne des titres
        self.surface.blits([titre.to_draw() for titre in self.titres])
        pygame.draw.line(self.surface, (50, 200, 150), (0, 30), (self.coords.w, 30))

        # tableau des messages
        self.surface.blits([msg.to_draw() for msg in self.messages])


class Footers:

    surface: pygame.surface.Surface
    x: int
    y: int
    w: int
    h: int
    visible: bool

    mouse_over: bool

    def __init__(self, screen: pygame.surface.Surface, coords: Tuple):

        self.update_screen(screen, coords)
        self.mouse_over = False

    def update_screen(self, 
            screen: pygame.surface.Surface, coords: Optional[Tuple] = None):

        if coords is not None:
            self.coords = pygame.Rect(coords)

        self.surface = screen.subsurface(self.coords)
        self.x, self.y, self.w, h = self.coords
        self.h = h - 1

    def get_color(self, lien):
        if lien.selected:
            return (50, 255, 150)

        elif lien.mouse_over:
            return (50, 200, 150)
            return (160, 240, 220)

        return (255, 255, 255)

    def load(self, datas: Dict):
        self.liens: List[Lien] = list()
        first: bool = True
        lien: Lien

        for key, values in datas.items():
            position, callback = values

            if first:
                lien = LienToggle(Lecteur.SysFont3, key, position, 4, None, callback)
                first = False
                lien.selected = True
            else:
                lien = Lien(Lecteur.SysFont3, key, position, 4, None, callback)

            lien.set_get_color(partial(self.get_color, lien))

            self.liens.append(lien)

    def mouse_exit(self):
        self.mouse_over = False
        for lien in self.liens:
            if lien.mouse_over:
                lien.mouse_over = False
                lien.update_color() 

    def mouse_move(self, mouse_pos: Tuple):
        self.mouse_over = True
        for lien in self.liens:
            if not lien.coords.collidepoint(mouse_pos):
                if lien.mouse_over:
                    lien.mouse_over = False
                    lien.update_color()   
                continue

            lien.mouse_over = True     
            lien.update_color()   
            # fprint("mouse over", lien.libelle)

    def mouse_button_up(self, mouse_pos: Tuple, button: int):
        for lien in self.liens:
            if not lien.coords.collidepoint(mouse_pos):
                continue

            lien.click()

    def draw(self):
        self.surface.fill((40, 40, 60))

        # footer
        # self.surface.blits([lien.to_draw() for lien in self.liens])
        for lien in self.liens:
            self.surface.blit(*lien.to_draw())
            if lien.selected:
                # ligne sous le lien selectionne
                dy = lien.h - 1
                pygame.draw.line(lien.surface, (50, 255, 150), (0, dy), (lien.w, dy))

        pygame.draw.line(self.surface, (50, 200, 150), (0, 0), (self.w, 0))


class Repertoire:

    colors: Dict = {
        True: (50, 200, 150),
        False: (200, 200, 200)
    }

    hauteur_ligne: int = 24
    largeur_niveau: int = 12

    libelle: str
    selected: bool
    niveau: int

    surface: pygame.surface.Surface
    x: int
    w: int
    h: int

    def __init__(self, libelle: str, niveau: int, selected: bool = False):

        self.libelle = libelle
        self.niveau = niveau
        self.select(selected)
        self.x = Repertoire.largeur_niveau * self.niveau

    @staticmethod
    def y(ligne: int) -> int:
        return 10 + Repertoire.hauteur_ligne * ligne
    
    def select(self, selected: bool):
        self.selected = selected
        self.surface = Lecteur.SysFont2.render(
                self.libelle, False, 
                Repertoire.colors.get(selected, (255, 0, 0)))

        self.w, self.h = self.surface.get_size()

    def to_screen(self, ligne: int) -> Tuple:
        return (
            self.surface, (self.x, self.y(ligne)))
        

class Repertoires:

    liste: List[Repertoire]

    max: int 
    selected: int 
    decal: int 

    surface: pygame.surface.Surface
    x: int
    y: int
    w: int
    h: int
    visible: bool

    def __init__(self, screen: pygame.surface.Surface, coords: Tuple):
        self.liste = list()

        self.coords = coords
        self.update_screen(screen, coords)
        self.set_visible(True)

        self.max = 10
        self.selected = 0
        self.decal = 0

    def update_screen(self, 
            screen: pygame.surface.Surface, coords: Optional[Tuple] = None):

        if coords is not None:
            self.coords = coords

        self.surface = screen.subsurface(self.coords)
        self.x, self.y, w, self.h = self.coords
        self.w = w - 1

    def clear(self):
        self.liste.clear()
    
    def load(self, liste_repertoires: List[str]):
        self.liste.append(Repertoire("Boîte de réception", 1, False))

        for idx, repertoire in enumerate(liste_repertoires):
            self.liste.append(Repertoire(repertoire, 2, idx == self.selected))

    def select(self, numero: int):
        # on commence à 1 car le numero 0 ne correspond à aucun répertoire
        for idx, repertoire in enumerate(self.liste[1:]):
            if idx == numero:
                repertoire.select(True)
                self.selected = idx
            elif repertoire.selected:
                repertoire.select(False)

    def toggle(self):
        self.visible = not self.visible

    def set_visible(self, visible: bool):
        self.visible = visible

    def to_screen(self) -> List[Tuple]:
        dirs_texte: List[Tuple] = list()

        for idx, repertoire in enumerate(self.liste[self.decal:]):
            if idx > self.max:
                break

            dirs_texte.append(repertoire.to_screen(idx))

        return dirs_texte

    def draw(self):
        if not self.visible:
            return 

        # directories
        self.surface.fill((10, 20, 20))
        pygame.draw.line(
            self.surface, 
            (50, 200, 150), 
            (self.w, 0), (self.w, self.h))

        self.surface.blits(self.to_screen())

        if 1+self.selected < self.decal:
            return

        color_dossiers = (50, 200, 150)
        # ligne indiquant que l'option est selectionnee

        selected_repertoire = self.liste[1+self.selected]
        dx = selected_repertoire.x
        dy = selected_repertoire.y(1+self.selected-self.decal) 
        dy += self.y - 10

        w = selected_repertoire.surface.get_width()

        pygame.draw.line(self.surface, color_dossiers, (dx, dy), (dx+w, dy))


class Lecteur:

    SysFont1: pygame.font.Font
    SysFont2: pygame.font.Font
    SysFont3: pygame.font.Font
    SysFont4: pygame.font.Font

    clock: pygame.time.Clock
    screen: pygame.surface.Surface
    screen_width: int
    screen_height: int

    mouse: Mouse
    running: bool

    def __init__(self):
        # change le repertoire courant afin de trouver 
        # toutes les applications et le parametrage
        directory: str = separator.join(__file__.split(separator)[:-1])
        if directory != getcwd():
            fprint(f"change current directory to : {directory}")
            chdir(directory)

        # Récupération de la liste des noms de polices disponibles
        # polices = pygame.font.get_fonts()

        # Affichage des polices
        # print(f"Nombre total de polices disponibles : {len(polices)}")
        # for police in polices:
        #     print(f"{police:40}", end="")

        self.mouse = Mouse(-1, -1)

    def init_fonts(self):
        Lecteur.SysFont1 = pygame.font.SysFont("couriernew", 18)
        Lecteur.SysFont2 = pygame.font.SysFont("dejavuserif", 16)
        Lecteur.SysFont3 = pygame.font.SysFont("dejavusans", 17)
        Lecteur.SysFont4 = pygame.font.SysFont("linuxlibertineg", 18, bold=False, italic=True)

    def initialize(self):
        self.clock = pygame.time.Clock()
        self.running = True

        desktops: List[Tuple] = pygame.display.get_desktop_sizes()
        disp_size: Tuple

        if desktops[0][1] > 1000:
            # Full HD max resolution
            disp_size = (1600, 788)
        else:
            disp_size = desktops[0]
            
        # self.screen = pygame.display.set_mode(desktops[0], pygame.FULLSCREEN, 24)
        self.screen = pygame.display.set_mode(disp_size, pygame.RESIZABLE, 24)
        self.screen_width, self.screen_height = self.screen.get_size()

        # Initialisation du cadrillage
        self.block_size: int = 40

        self.nb_lines = (self.screen_height-20) // self.block_size 
        self.nb_cols = (self.screen_width-20) // self.block_size 
        self.color_diff = 255 // (self.nb_lines + self.nb_cols)

        self.idxx: int = (self.mouse.x-10) // self.block_size
        self.idxy: int = (self.mouse.y-10) // self.block_size

    def boot(self):
        pygame.init()
        self.init_fonts()
        self.initialize()

    def shutdown(self):
        pygame.quit()

    def mouse_enter_leave(self): ...
    
    def mouse_move(self, pos):
        self.mouse = Mouse(*pos)

        if self.footers.coords.collidepoint(pos):
            self.footers.mouse_move((pos[0], pos[1]-self.footers.y))

        elif self.footers.mouse_over:
            self.footers.mouse_exit()

        # self.idxx = (self.mouse.x-10) // self.block_size
        # self.idxy = (self.mouse.y-10) // self.block_size

    def mouse_button_down(self, pos, button): ...

    def mouse_button_up(self, pos, button): 
        mouse_pos = pos[0], pos[1]-self.screen_height+30
        if self.footers.coords.collidepoint(pos):
            self.footers.mouse_button_up(mouse_pos, button)

        #     self.repertoires.toggle()

    def mouse_wheel(self, x, y): ...
    def keypressed(self, event): ...

    def keyreleased(self, event): 
        if event.key == pygame.K_ESCAPE:
            self.running = False

    def update_screen(self): 
        # fprint("update_screen() =", self.screen.get_size())
        self.screen_width, self.screen_height = self.screen.get_size()

        self.headers.update_screen(self.screen, (0, 0, self.screen_width, self.line_height))
        self.repertoires.update_screen(self.screen,
            (0, self.line_height, self.dirs_size, self.screen_height-2*self.line_height))

        self.liste_messages.update_screen(self.screen, 
            (self.dirs_size, self.line_height, 
            self.screen_width-self.dirs_size, self.screen_height-2*self.line_height))

        self.footers.update_screen(self.screen,
            (0, self.screen_height-self.line_height, self.screen_width, self.line_height))

    def get_pygame_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.KMOD_LGUI:
                    self.mouse_move(event.pos)

                case pygame.MOUSEBUTTONDOWN:
                    if event.button != 2:
                        self.mouse_button_down(event.pos, event.button)

                case pygame.MOUSEBUTTONUP:
                    self.mouse_button_up(event.pos, event.button)

                case pygame.MOUSEWHEEL:
                    self.mouse_wheel(event.x, event.y)

                case pygame.KEYDOWN:
                    self.keypressed(event)

                case pygame.KEYUP:
                    self.keyreleased(event)

                case (pygame.AUDIO_S8 | 
                        pygame.AUDIO_S16 | 
                        pygame.WINDOWENTER | 
                        pygame.ACTIVEEVENT):
                    self.mouse_enter_leave()

                case (pygame.WINDOWMAXIMIZED |
                        pygame.WINDOWSIZECHANGED |
                        pygame.WINDOWRESIZED |
                        pygame.WINDOWRESTORED):
                    pass

                case pygame.VIDEORESIZE:
                    self.update_screen()

                case pygame.QUIT:
                    self.running = False

                case (pygame.WINDOWSHOWN | 
                        pygame.WINDOWMOVED |
                        pygame.VIDEOEXPOSE | 
                        pygame.WINDOWCLOSE | 
                        pygame.WINDOWFOCUSGAINED):
                    pass

                case pygame.TEXTEDITING:
                    pass

                case pygame.JOYDEVICEADDED | pygame.AUDIODEVICEADDED:
                    pass

                case _:
                    fprint(event.type, get_pygame_const_name(event.type))
                    pass

    def cadrillage(self):

        for idy in range(self.nb_lines):
            for idx in range(self.nb_cols):
                if idx == self.idxx and idy == self.idxy:
                    color = (50, 200, 150)
                else:
                    colors = 3*(self.color_diff*(idx+idy), )
                    color = tuple(min(255, c) for c in colors)

                pygame.draw.rect(self.screen, color, 
                    (self.block_size*idx+10, idy*self.block_size+10, 
                        self.block_size, self.block_size))

    def draw(self):
        self.clock.tick(60)

        self.screen.fill((0, 0, 0))

        self.headers.draw()
        self.repertoires.draw()
        self.liste_messages.draw()
        self.footers.draw()

        pygame.display.update()

    def toggle_repertoire(self): 
        self.repertoires.toggle()

        if self.repertoires.visible:
            self.liste_messages.update_screen(self.screen, 
                (self.dirs_size, self.line_height, 
                self.screen_width-self.dirs_size, self.screen_height-2*self.line_height))
        else:
            self.liste_messages.update_screen(self.screen, 
                (0, self.line_height, self.screen_width, 
                    self.screen_height-2*self.line_height))

    def init_draw(self):
        self.dirs_size: int = 300
        self.line_height: int = 30

        self.headers = Headers(self.screen, (0, 0, self.screen_width, self.line_height))
        self.headers.load({
            "Adresse : ": ("christophe.michael.jacques@numericable.fr", 10),
            "Messages : ": ("24", 500),
            "Non lus : ": ("7", 680)
        })

        self.liste_messages = ListeMessages(self.screen, 
            (
                self.dirs_size, 
                self.line_height, 
                self.screen_width-self.dirs_size, 
                self.screen_height-2*self.line_height))
        self.liste_messages.load()

        self.repertoires = Repertoires(self.screen,
            (0, self.line_height, self.dirs_size, self.screen_height-2*self.line_height))
        self.repertoires.load([
            "Courrier entrant", 
            "Brouillons", 
            "Envoyés", 
            "Indésirables", 
            "Corbeille"])

        # self.repertoires.select(1)

        self.footers = Footers(self.screen,
            (0, self.screen_height-self.line_height, self.screen_width, self.line_height))
        self.footers.load({
            " Dossiers ": (10, self.toggle_repertoire),
            " Rafraichir ": (100, None)
        })

    def run(self):
        self.boot()
        self.init_draw()
        while self.running:
            self.draw()
            self.get_pygame_events()

        self.shutdown()


def main():
    lect: Lecteur

    lect = Lecteur()
    lect.run()


if __name__ == '__main__':
    main()
