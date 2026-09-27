import pygame

# from collections import namedtuple
from os import getcwd, chdir, sep as separator
from typing import Callable, Tuple, Optional, List, Dict
from functools import partial
from cmail import Mail
from threading import Thread


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
    id: str
    libelle: str
    posx: int
    posy: int 
    getColor: Optional[Callable]
    callback: Optional[Callable]

    mouse_over: bool
    selected: bool
    visible: bool

    def __init__(self, 
            font: pygame.font.Font,
            libelle: str, 
            posx: int, posy: int, 
            getColor: Optional[Callable],
            callback: Optional[Callable],
            **options):
        
        self.font = font
        self.libelle = libelle
        self.set_get_color(getColor)

        self.id = options.get("id", "")
        self.visible = options.get("visible", True)

        self.x = posx
        self.y = posy
        
        self.w, self.h = self.surface.get_size()
        self.coords = pygame.Rect(self.x, self.y, self.w, self.h)

        self.callback = callback
        self.mouse_over = False
        self.selected = False

    def toggle(self):
        self.visible = not self.visible

    def set_visible(self, visible: bool):
        self.visible = visible

    def set_libelle(self, libelle: str):
        self.libelle = libelle
        self.surface = self.font.render(self.libelle, False, self.color)

    def set_max_width(self, width):
        taille = len(self.libelle)
        while self.w > width:
            taille -= 1
            libelle = self.libelle[:taille]
            self.surface = self.font.render(libelle, False, self.color)
            self.w = self.surface.get_width()

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
    liens: List[Lien]

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

    def get(self, ident: str) -> Lien:
        for lien in self.liens:
            if lien.id == ident:
                return lien

        raise Exception("Le lien {ident!r} n'existe pas")

    def get_color(self, index):
        if index == 1:
            return (255, 255, 255)

        return (160, 240, 220)

    def load(self, datas: Dict):
        self.liens = list()

        for key, values in datas.items():
            ident, lib, position = values

            lien1 = Lien(Lecteur.SysFont3, key,
                position, 4, partial(self.get_color, 1), None)
            self.liens.append(lien1)

            largeur = lien1.w
            lien2 = Lien(Lecteur.SysFont4, lib,
                position+largeur, 3, partial(self.get_color, 2), None,
                id=ident)
            self.liens.append(lien2)

    def draw(self):
        self.surface.fill((40, 30, 0))

        # header
        self.surface.blits([lien.to_draw() for lien in self.liens])
        pygame.draw.line(self.surface, (50, 200, 150), (0, self.h), (self.w, self.h))


class ListeMessages:

    hauteur_ligne: int = 28

    surface: pygame.surface.Surface
    x: int
    y: int
    w: int
    h: int
    visible: bool

    mouse_over: bool

    directory: str
    nb_mails: int 
    selected: int 

    nb_colonnes: int
    data_titres: Dict
    titres: List[Lien]

    liens: List[Lien]
    liste_datas: List[Dict]

    actions: Optional[str]

    def __init__(self, screen: pygame.surface.Surface, coords: Tuple):

        self.update_screen(screen, coords)
        self.mouse_over = False
        self.nb_mails = 0
        self.selected = 0
        self.set_titres()
        self.actions = None
        self.directory = "INBOX"

    def get_actions(self) -> Optional[str]:
        if self.actions is None:
            return None

        actions = self.actions
        self.actions = None
        return actions

    def get_color(self, index):
        if index == 1:
            return (255, 255, 255)
        elif index == 2:
            return (255, 100, 100)

        elif index == "SEEN":
            return (200, 200, 200)

        return (160, 240, 220)

    def set_titres(self):
        self.data_titres = {
            "ATT": {"lib": "Attr", "pos": 10, "col": 1},
            "NUM": {"lib": "N°", "pos": 50, "col": 1},
            "EXP": {"lib": "Expéditeur", "pos": 50, "col": 1},
            "OBJ": {"lib": "Objet", "pos": 300, "col": 1},
            "DAT": {"lib": "Date", "pos": 580, "col": 1},
            "DIR": {"lib": r"\/", "pos": 50, "col": 2},
        }
        self.titres = list()
        self.nb_colonnes = len(self.data_titres) - 1

        position: int = 0
        position_old: int = 0
        prev_key: str = ""

        for cle in self.data_titres:
            position_old = position
            position += self.data_titres[cle]["pos"]
            largeur = position - position_old
            self.data_titres[cle]["pos"] = position
            if prev_key:
                self.data_titres[prev_key]["lar"] = largeur

            prev_key = cle

            lien = Lien(Lecteur.SysFont3, self.data_titres[cle]["lib"],
                    position, 5, 
                    partial(self.get_color, self.data_titres[cle]["col"]), None)
            self.titres.append(lien)

    def mouse_exit(self):
        self.mouse_over = False
        self.selected = 0

    def mouse_move(self, mouse_pos: Tuple):
        self.mouse_over = True

        if mouse_pos[1] < 30:
            # ligne des titres
            self.selected = 0
            
        else:
            # ligne des messages
            idx = mouse_pos[1] // ListeMessages.hauteur_ligne
            if idx > self.nb_mails:
                idx = 0

            self.selected = idx

    @staticmethod
    def format_adresse(lib: str):
        if "<" in lib:
            return lib[:lib.index("<")-1]

        return lib

    def get_mails(self):
        mail = Mail()
        user = mail.USERNAME

        try:
            mail.connect()
            mail.select(self.directory)

            status, response = mail.mail.status(self.directory, "(MESSAGES UNSEEN)")
            if status == "OK":
                # response contient une liste avec un seul élément en bytes
                data = response[0].decode("utf-8").strip("()")
                dossier, _, messages, _, unseen = data.split()

                self.actions = f"USER={user};DIR={dossier};ALL={messages};UNSEEN={unseen}"

                for contenu in mail.get_mails("UNSEEN"):
                    self.liste_datas.append(contenu)

            else:
                fprint(self.directory, "Status:", status)

        except Exception as erreur:
            fprint("get_mails():", erreur)

        try:
            mail.disconnect()
        except Exception:
            pass

        if self.actions is None:
            self.actions = "LOADING=False"
        else:
            self.actions += ";LOADING=False"

    def refresh(self):
        self.load()

    def load(self):
        self.liens = list()
        self.liste_datas = list()
        self.nb_mails = 0
        self.selected = 0
        self.actions = "LOADING=True"

        mails = Thread(target=self.load_mails)
        mails.start()

    def load_mails(self):
        # fprint("load_mails", self.directory)
        # return 

        self.get_mails()

        dy = 5
        largeur_max = self.data_titres["OBJ"]["lar"] - 10
        for datas in reversed(sorted(self.liste_datas, key=lambda x: x["DAT"])):
            dy += ListeMessages.hauteur_ligne  # 30
            for cle in datas:
                lib = self.format_adresse(datas[cle]) if cle == "EXP" else datas[cle]
                lien = Lien(Lecteur.SysFont3, lib,
                        self.data_titres[cle]["pos"], dy, 
                        partial(self.get_color, "SEEN"), None)
                if cle == "OBJ":
                    lien.set_max_width(largeur_max)

                self.liens.append(lien)

        self.nb_mails = len(self.liste_datas)

    def update_screen(self, 
            screen: pygame.surface.Surface, coords: Optional[Tuple] = None):

        if coords is not None:
            self.coords = pygame.Rect(coords)

        self.surface = screen.subsurface(self.coords)
        self.x, self.y, self.w, h = self.coords
        self.h = h - 1

    def draw(self):
        self.surface.fill((10, 20, 20))

        # fond d'une ligne de message
        for ligne in range(1, 1+self.nb_mails):
            color = (30, 50, 50) if ligne == self.selected else (20, 30, 30)
            if ligne % 2 and ligne != self.selected:
                continue

            pygame.draw.rect(self.surface, color, 
                (0, ListeMessages.hauteur_ligne * ligne, 
                    self.coords.w, ListeMessages.hauteur_ligne))

        # Ligne des titres
        self.surface.blits([titre.to_draw() for titre in self.titres])
        pygame.draw.line(self.surface, (50, 200, 150), (0, 30), (self.coords.w, 30))

        # tableau des liens (messages)
        self.surface.blits([lien.to_draw() for lien in self.liens])


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

    def get(self, ident: str) -> Lien:
        for lien in self.liens:
            if lien.id == ident:
                return lien

        raise Exception("Le lien {ident!r} n'existe pas")

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
            position, ident, callback, *args = values

            visible = args[0] if args else True

            if first:
                lien = LienToggle(Lecteur.SysFont3, key, position, 4, None, 
                    callback, id=ident)
                first = False
                lien.selected = True
            else:
                lien = Lien(Lecteur.SysFont3, key, position, 4, None, 
                    callback, id=ident, visible=visible)

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
            if not lien.visible:
                continue

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

    mouse_over: bool

    def __init__(self, ident: str, libelle: str, niveau: int, selected: bool = False):

        self.id = ident
        self.libelle = libelle
        self.niveau = niveau
        self.select(selected)
        self.x = Repertoire.largeur_niveau * self.niveau
        self.mouse_over = False

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
    selected: str
    decal: int 

    surface: pygame.surface.Surface
    x: int
    y: int
    w: int
    h: int
    visible: bool
    mouse_over: bool

    mouse_over_y: int

    actions: Optional[str]

    def __init__(self, screen: pygame.surface.Surface, coords: Tuple):
        self.liste = list()

        self.coords = pygame.Rect(coords)
        self.update_screen(screen, coords)
        self.set_visible(True)

        self.max = self.h // Repertoire.hauteur_ligne

        self.selected = "INBOX"
        self.decal = 0

        self.mouse_over = False
        self.mouse_over_y = 0

        self.actions = None

    def update_screen(self, 
            screen: pygame.surface.Surface, coords: Optional[Tuple] = None):

        if coords is not None:
            self.coords = pygame.Rect(coords)

        self.surface = screen.subsurface(self.coords)
        self.x, self.y, w, self.h = self.coords
        self.w = w - 1

    def get_actions(self) -> Optional[str]:
        if self.actions is None:
            return None

        actions = self.actions
        self.actions = None
        return actions

    def mouse_move(self, mouse_pos: Tuple):
        self.mouse_over = True
        self.mouse_over_y = 0

        for idx, repertoire in enumerate(self.liste[self.decal:self.decal+self.max]):
            if repertoire.id == "MAIL":
                continue

            surface, (x, y) = repertoire.to_screen(idx)

            if y < mouse_pos[1] < y + repertoire.hauteur_ligne:
                repertoire.mouse_over = True
                self.mouse_over_y = y - 2

            elif repertoire.mouse_over:
                repertoire.mouse_over = False

    def mouse_exit(self):
        self.mouse_over = False
        self.mouse_over_y = 0

    def mouse_button_up(self, mouse_pos: Tuple, button: int):
        for idx, repertoire in enumerate(self.liste[self.decal:self.decal+self.max]):
            if repertoire.id == "MAIL":
                continue

            surface, (x, y) = repertoire.to_screen(idx)
            if y < mouse_pos[1] < y + repertoire.hauteur_ligne:
                self.select(repertoire.id)
                break

    def clear(self):
        self.liste.clear()
    
    def load(self):
        mail: Mail

        connu: bool
        num: int
        ident: str
        repertoire: str

        repertoires_connus: List[Tuple] = list()
        repertoires_autres: List[Tuple] = list()

        self.liste.append(Repertoire("MAIL", "Boîte de réception", 1, False))

        mail = Mail()

        try:
            mail.connect()
            for connu, num, ident, repertoire in mail.get_dirs():
                if connu:
                    repertoires_connus.append((num, ident, repertoire))
                else:
                    repertoires_autres.append((num, ident, repertoire))

        except Exception as erreur:
            fprint("get_dirs():", erreur)

        try:
            mail.disconnect()
        except Exception:
            pass

        # tri des repertoire par id
        repertoires_connus.sort(key=lambda elt: elt[0])

        # tri des repertoire par libelle
        repertoires_autres.sort(key=lambda elt: elt[2])

        for value in repertoires_connus + repertoires_autres:
            num, ident, repertoire = value
            self.liste.append(Repertoire(ident, repertoire, 2, 
                ident == self.selected))

    def select(self, ident: str):
        if ident == self.selected:
            return

        # on commence à 1 car le numero 0 ne correspond à aucun répertoire
        for idx, repertoire in enumerate(self.liste[1:]):
            if ident == repertoire.id:
                repertoire.select(True)
                self.selected = repertoire.id
                # fprint("repertoire selected:", self.selected)
                self.actions = f"DIR={self.selected}"

            elif repertoire.selected:
                repertoire.select(False)

    def toggle(self):
        self.visible = not self.visible

    def set_visible(self, visible: bool):
        self.visible = visible

    def to_screen(self) -> List[Tuple]:
        dirs_texte: List[Tuple] = list()

        for idx, repertoire in enumerate(self.liste[self.decal:self.decal+self.max]):
            dirs_texte.append(repertoire.to_screen(idx))

        return dirs_texte

    def index(self, ident: str) -> int:
        for idx, repertoire in enumerate(self.liste[1:]):
            if repertoire.id == ident:
                return idx

        raise Exception(f"L'identifiant {ident!r} n'existe pas")

    def draw(self):
        if not self.visible:
            return 

        # directories
        self.surface.fill((10, 20, 20))
        pygame.draw.line(
            self.surface, 
            (50, 200, 150), 
            (self.w, 0), (self.w, self.h))

        if self.mouse_over_y:
            pygame.draw.rect(self.surface, (30, 50, 50),
                (0, self.mouse_over_y, self.w, Repertoire.hauteur_ligne))                

        self.surface.blits(self.to_screen())

        index = self.index(self.selected)
        if 1+index < self.decal:
            return

        # ligne indiquant que l'option est selectionnee
        selected_repertoire = self.liste[1+index]
        dx = selected_repertoire.x
        dy = selected_repertoire.y(1+index-self.decal) 
        dy += self.y - 10

        w = selected_repertoire.surface.get_width()

        pygame.draw.line(self.surface, (50, 200, 150), (dx, dy), (dx+w, dy))


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

    def mouse_enter_leave(self): 
        self.liste_messages.mouse_exit()
        self.repertoires.mouse_exit()
    
    def mouse_move(self, pos):
        self.mouse = Mouse(*pos)

        if self.repertoires.visible and self.repertoires.coords.collidepoint(pos):
            self.repertoires.mouse_move((pos[0], pos[1]-self.repertoires.y))

        elif self.repertoires.mouse_over:
            self.repertoires.mouse_exit()

        if self.liste_messages.coords.collidepoint(pos):
            dx = self.repertoires.w if self.repertoires.visible else 0
            self.liste_messages.mouse_move((pos[0]-dx, pos[1]-self.repertoires.y))

        elif self.liste_messages.mouse_over:
            self.liste_messages.mouse_exit()

        if self.footers.coords.collidepoint(pos):
            self.footers.mouse_move((pos[0], pos[1]-self.footers.y))

        elif self.footers.mouse_over:
            self.footers.mouse_exit()

    def mouse_button_down(self, pos, button): ...

    def mouse_button_up(self, pos, button): 
        mouse_pos = pos[0], pos[1]-self.screen_height+30
        if self.footers.coords.collidepoint(pos):
            self.footers.mouse_button_up(mouse_pos, button)

        elif self.repertoires.visible and self.repertoires.coords.collidepoint(pos):
            self.repertoires.mouse_button_up((pos[0], pos[1]-self.repertoires.y), button)

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

    def update_repertoires(self):
        actions = self.repertoires.get_actions()
        if actions is None:
            return

        key: str
        value: str

        for action in actions.split(";"):
            key, value = action.split("=")
            match key:
                case "DIR":
                    if value != self.liste_messages.directory:
                        self.liste_messages.directory = value
                        self.liste_messages.load()

                case _:
                    raise Exception(f"Paramètre {key} inconnu.")

    def update_liste_messages(self):
        actions = self.liste_messages.get_actions()
        if actions is None:
            return

        key: str
        value: str
        repertoire: str = ""

        for action in actions.split(";"):
            key, value = action.split("=")
            match key:
                case "USER":
                    if value != self.headers.liens[1].libelle:
                        # compte connecte
                        self.headers.get("ADDR").set_libelle(value)

                case "DIR":
                    repertoire = value
                    repertoire = repertoire

                case "ALL":
                    self.nb_messages = int(value)

                case "UNSEEN":
                    self.messages_non_vu = int(value)

                case "LOADING":
                    # self.footers.get("LOD").toggle()
                    self.footers.get("LOD").set_visible(eval(value))

        if self.nb_messages != int(self.headers.liens[3].libelle):
            # nb total de messages
            self.headers.get("ALL").set_libelle(str(self.nb_messages))

        if self.messages_non_vu != int(self.headers.liens[5].libelle):
            # nb de messages non lu
            self.headers.get("UNSEEN").set_libelle(str(self.messages_non_vu))

    def update(self):
        self.update_repertoires()
        self.update_liste_messages()

    def draw(self):
        self.clock.tick(60)

        self.headers.draw()
        self.repertoires.draw()
        self.liste_messages.draw()
        self.footers.draw()

        pygame.display.update()

    def refresh_mails(self):
        self.liste_messages.refresh()

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

        self.nb_messages = 0
        self.messages_non_vu = 0

        self.headers = Headers(self.screen, (0, 0, self.screen_width, self.line_height))
        self.headers.load({
            "Adresse : ": ("ADDR", "", 10),
            "Messages : ": ("ALL", "0", 500),
            "Non lus : ": ("UNSEEN", "0", 680)
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
        self.repertoires.load()

        self.footers = Footers(self.screen,
            (0, self.screen_height-self.line_height, self.screen_width, self.line_height))
        self.footers.load({
            " Dossiers ": (10, "DIR", self.toggle_repertoire),
            " Rafraichir ": (100, "REF", self.refresh_mails),
            " Loading ... ": (300, "LOD", None, True)
        })

    def run(self):
        self.boot()
        self.init_draw()
        while self.running:
            self.update()
            self.draw()
            self.get_pygame_events()

        self.shutdown()


def main():
    lect: Lecteur

    lect = Lecteur()
    lect.run()


if __name__ == '__main__':
    main()
