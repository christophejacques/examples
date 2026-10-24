from os import getcwd, chdir, sep as separator, environ

from typing import Callable, Tuple, Optional, List, Dict, Generator
from functools import partial
from threading import Thread
from time import perf_counter

from cmail import Mail

# Supprime l'affichage du chargement de pygame
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame  # noqa: E402


class Variable:

    DEBUG: bool = False


class Mouse:

    x: int
    y: int

    @classmethod
    def __init__(cls, x, y):
        cls.x = x
        cls.y = y


def fprint(*args, **kwargs) -> None:
    print(*args, **kwargs, flush=True)


def get_pygame_const_name(index):
    for c in dir(pygame):
        if c[0] in "AZERTYUIOPMLKJHGFDSQWXCVBN":
            if type(getattr(pygame, c)) == int and getattr(pygame, c) == index:
                return c


class Bouton:

    surface: pygame.surface.Surface
    text_surface: pygame.surface.Surface
    rect: pygame.Rect

    # BACK : couleur de fond
    # AROUND : couleur du contour
    # OVER : couleur si curseur souris sur bouton

    color_over: Tuple
    color_back: Tuple
    color_around: Tuple

    mouse_over: bool
    mouse_button_down: bool

    callback: Optional[Callable]

    def __init__(self, 
            surface: pygame.surface.Surface, 
            colors: Dict[str, Tuple],
            coords: Tuple,
            libelle: str,
            callback: Optional[Callable] = None,
            *args, **kwargs):

        self.surface = surface
        self.rect = pygame.Rect(coords)

        self.color_back = colors.get("BACK", (0, 0, 0))
        self.color_around = colors.get("AROUND", self.color_back)
        self.color_over = colors.get("OVER", self.color_back)

        self.back_color = self.color_back
        self.color = self.color_around

        self.mouse_over = False
        self.mouse_button_down = False
        self.set_libelle(libelle)
        self.set_callback(callback, *args, **kwargs)

    def set_libelle(self, libelle: str):
        color = (255, 255, 255)
        self.text_surface = Lecteur.SysFont3.render(libelle, False, color)
        width, height = self.text_surface.get_size()
        self.text_coords = (self.rect.x + self.rect.w // 2 - width // 2,
            self.rect.y + self.rect.h // 2 - height // 2)

    def set_callback(self, callback: Optional[Callable], *args, **kwargs):
        if callback:
            self.callback = partial(callback, *args, **kwargs)
        else:
            self.callback = None

    def set_mouse_over(self, mouse_over: bool):
        if self.mouse_over == mouse_over:
            return

        self.mouse_over = mouse_over
        if mouse_over:
            self.back_color = self.color_over
            self.color = self.color_around
        else:
            self.back_color = self.color_back
            self.color = self.color_around

        self.draw()

    def draw(self):
        pygame.draw.rect(self.surface, self.back_color, self.rect)
        pygame.draw.rect(self.surface, self.color, self.rect, 1)
        self.surface.blit(self.text_surface, self.text_coords)


class MessageBox:

    screen: pygame.surface.Surface
    msg_screen: pygame.surface.Surface

    text_surface: pygame.surface.Surface

    coords: Tuple
    coords_ombre: Tuple
    pos_screen: Tuple
    rect: pygame.Rect

    bouton_oui: Bouton
    bouton_non: Bouton

    show: bool

    @classmethod
    def __init__(cls, 
            screen: pygame.surface.Surface, 
            liste_message: List[str] = [],
            callback: Optional[Callable] = None, *args, **kwargs):
        largeur = 400
        hauteur = 200
        cls.msg_screen = pygame.Surface((largeur+10, hauteur+10), pygame.SRCALPHA)

        cls.coords = (0, 0, largeur, hauteur)
        cls.coords_ombre = (10, 10, largeur, hauteur)

        cls.update_screen(screen)

        cls.bouton_oui = Bouton(cls.msg_screen, 
            {"BACK": (25, 70, 40),
             "AROUND": (50, 200, 150),
             "OVER": (30, 80, 50)},
            (32, 140, 128, 32), "Oui", callback, *args, **kwargs)

        cls.bouton_non = Bouton(cls.msg_screen, 
            {"BACK": (70, 40, 25),
             "AROUND": (200, 150, 50),
             "OVER": (80, 50, 30)},
            (240, 140, 128, 32), "Non")

        cls.set_message(liste_message)
        cls.show = False

    @classmethod
    def update_screen(cls, screen: pygame.surface.Surface) -> None:
        width, height = screen.get_size()
        posx = width // 2 - 200
        posy = height // 2 - 100

        cls.pos_screen = (posx, posy)
        cls.rect = pygame.Rect(*cls.pos_screen, *cls.coords[2:])
        cls.screen = screen

    @classmethod
    def mouse_move(cls, pos: Tuple) -> None:
        if not cls.rect.collidepoint(pos):
            return

        x, y = pos
        sx, sy = cls.pos_screen
        mouse_pos = x - sx, y - sy

        if cls.bouton_oui.rect.collidepoint(mouse_pos):
            cls.bouton_oui.set_mouse_over(True)
            cls.bouton_non.set_mouse_over(False)

        elif cls.bouton_non.rect.collidepoint(mouse_pos):
            cls.bouton_oui.set_mouse_over(False)
            cls.bouton_non.set_mouse_over(True)

        else:
            cls.bouton_oui.set_mouse_over(False)
            cls.bouton_non.set_mouse_over(False)

    @classmethod
    def mouse_button_down(cls, pos: Tuple, button: int) -> None:
        if button != 1:
            return

        cls.bouton_oui.mouse_button_down = cls.bouton_oui.mouse_over
        cls.bouton_non.mouse_button_down = cls.bouton_non.mouse_over

    @classmethod
    def mouse_button_up(cls, pos: Tuple, button: int) -> None:

        if button != 1:
            cls.bouton_oui.mouse_button_down = False
            cls.bouton_non.mouse_button_down = False
            return

        if cls.bouton_oui.mouse_over and cls.bouton_oui.mouse_button_down:
            if cls.bouton_oui.callback:
                cls.bouton_oui.callback()
            MessageBox.deactivate()

        elif cls.bouton_non.mouse_over and cls.bouton_non.mouse_button_down:
            MessageBox.deactivate()
            
    @classmethod
    def set_message(cls, liste_message: List[str]):
        cls.msg_screen.fill((0, 0, 0, 0))
        pygame.draw.rect(cls.msg_screen, (10, 20, 10), cls.coords_ombre)
        pygame.draw.rect(cls.msg_screen, (30, 40, 40), cls.coords)
        pygame.draw.rect(cls.msg_screen, (50, 200, 150), cls.coords, 1)

        cls.bouton_oui.draw()
        cls.bouton_non.draw()
        
        y = 50
        for message in liste_message:
            cls.text_surface = Lecteur.SysFont3.render(message, False, (255, 255, 255))
            width, height = cls.text_surface.get_size()
            cls.msg_screen.blit(cls.text_surface, (cls.rect.w // 2 - width // 2, y))
            y += height + 4

    @classmethod
    def activate(cls):
        cls.bouton_oui.set_mouse_over(False)
        cls.bouton_non.set_mouse_over(False)
        cls.show = True

    @classmethod
    def deactivate(cls):
        cls.show = False

    @classmethod
    def draw(cls):
        if cls.show:
            cls.screen.blit(cls.msg_screen, cls.pos_screen)


class Lien:

    font: pygame.font.Font
    id: str
    libelle: str
    posx: int
    posy: int 
    getColor: Optional[Callable]
    callback: Optional[Callable]

    mouse_over: bool
    mouse_button_pushed: bool
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
        self.mouse_button_pushed = False
        self.selected = False

    def toggle(self) -> None:
        self.visible = not self.visible

    def set_visible(self, visible: bool) -> None:
        self.visible = visible

    def set_libelle(self, libelle: str) -> None:
        self.libelle = libelle
        self.surface = self.font.render(self.libelle, False, self.color)

    def set_max_width(self, width: int) -> None:
        libelle: str
        taille: int

        taille = len(self.libelle)
        while self.w > width:
            taille -= 1
            libelle = self.libelle[:taille]
            self.surface = self.font.render(libelle, False, self.color)
            self.w = self.surface.get_width()

    def set_get_color(self, get_color: Optional[Callable]) -> None:

        if get_color is None:
            self.color = (255, 0, 0)
            self.surface = self.font.render(self.libelle, False, self.color)
            return

        self.getColor = get_color
        self.color = (0, 0, 0)
        self.update_color()

    def update_color(self) -> None:
        new_color: Tuple

        if self.getColor is None:
            return

        new_color = self.getColor()
        if self.color != new_color:
            self.color = new_color
            self.surface = self.font.render(self.libelle, False, self.color)

    def click(self) -> None:
        if self.callback:
            self.callback()

    def draw_underline(self):
        pygame.draw.line(self.surface, (50, 255, 150), 
            (0, self.h-1), (self.w, self.h-1))

    def to_draw(self) -> Tuple:
        return (self.surface, self.coords)


class LienToggle(Lien):

    def click(self) -> None:
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
            screen: pygame.surface.Surface, coords: Optional[Tuple] = None) -> None:

        if coords is not None:
            self.coords = coords

        self.surface = screen.subsurface(self.coords)
        self.x, self.y, self.w, h = self.coords
        self.h = h - 1

    def get(self, ident: str) -> Lien:
        lien: Lien

        for lien in self.liens:
            if lien.id == ident:
                return lien

        raise Exception("Le lien {ident!r} n'existe pas")

    def get_color(self, index) -> Tuple:
        if index == 1:
            return (255, 255, 255)

        return (160, 240, 220)

    def load(self, datas: Dict) -> None:
        key: str
        values: Tuple
        ident: str
        lib: str
        position: int
        largeur: int

        lien1: Lien
        lien2: Lien

        self.liens = list()

        for key, values in datas.items():
            ident, lib, position = values

            lien1 = Lien(Lecteur.SysFont3, key,
                position, 7, partial(self.get_color, 1), None)
            self.liens.append(lien1)

            largeur = lien1.w
            lien2 = Lien(Lecteur.SysFont4, lib,
                position+largeur, 3, partial(self.get_color, 2), None,
                id=ident)
            self.liens.append(lien2)

    def draw(self) -> None:
        self.surface.fill((40, 30, 0))

        # header
        self.surface.blits([lien.to_draw() for lien in self.liens])
        pygame.draw.line(self.surface, (50, 200, 150), (0, self.h), (self.w, self.h))


class Texte:
    font: pygame.font.Font
    surface: pygame.surface.Surface
    width: int

    libelle: str
    getColor: Optional[Callable]

    mouse_over: bool
    visible: bool

    def __init__(self, 
            font: pygame.font.Font,
            libelle: str, 
            getColor: Optional[Callable],
            *args,
            **options):
        
        self.font = font
        self.color = (1, 1, 1)
        self.set_libelle(libelle)
        self.set_get_color(getColor, *args)

        self.mouse_over = False
        self.visible = options.get("visible", True)
        if "max_width" in options:
            self.set_max_width(options.get("max_width", 999))

    def set_visible(self, visible: bool) -> None:
        self.visible = visible

    def set_libelle(self, libelle: str) -> None:
        if "\x00" in libelle:
            # print("Caractère nul détecté, nettoyage en cours...")
            libelle = libelle.replace("\x00", "")

        self.libelle = libelle
        self.surface = self.font.render(self.libelle, False, self.color)
        self.width = self.surface.get_width()

    def set_max_width(self, width: int) -> None:
        libelle: str

        taille: int = len(self.libelle)
        while self.width > width:
            taille -= 1
            libelle = self.libelle[:taille]
            self.surface = self.font.render(libelle, False, self.color)
            self.width = self.surface.get_width()

    def set_get_color(self, get_color: Optional[Callable], *args) -> None:
        self.color_args = args
        if get_color is None:
            self.color = (255, 0, 0)
            self.surface = self.font.render(self.libelle, False, self.color)
            return

        self.getColor = get_color
        self.color = (-1, -1, -1)
        self.update_color()

    def update_color(self) -> None:
        new_color: Tuple

        if self.getColor is None:
            return

        new_color = self.getColor(self, *self.color_args)
        if self.color != new_color:
            self.color = new_color
            self.surface = self.font.render(self.libelle, False, self.color)


class Message:
    data: Dict[str, Texte]

    def __init__(self):
        self.data = dict()

    def load(self, cle: str, texte: Texte) -> None:
        self.data[cle] = texte

    def to_draw(self) -> Generator:
        for cle in self.data:
            texte = self.data[cle]
            yield cle, texte.surface


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
    nb_lignes: int
    nb_lignes_max: int

    selected: Optional[int]
    message_over: int 

    decal: int
    debut: int

    nb_colonnes: int
    data_titres: Dict
    titres: List[Lien]

    liste_datas: List[Dict]
    liste_messages: List[Message]

    actions: Optional[str]

    def __init__(self, screen: pygame.surface.Surface, coords: Tuple):

        self.decal = 0
        self.nb_lignes = 0
        self.nb_lignes_max = 0

        self.load_titres()
        self.update_screen(screen, coords)
        self.mouse_over = False
        self.nb_mails = 0
        self.selected = None
        self.message_over = 0

        self.actions = None
        self.directory = '"INBOX"'

    def get_actions(self) -> Optional[str]:
        actions: str

        if self.actions is None:
            return None

        actions = self.actions
        self.actions = None
        return actions

    def get_texte_color(self, *args) -> Tuple:
        attr = args[1]
        if "V" in attr:
            return (150, 150, 150)

        return (200, 240, 240)

    def get_color(self, index) -> Tuple:
        if index == 1:
            return (255, 255, 255)

        elif index == 2:
            return (255, 100, 100)

        elif index == "SEEN":
            return (150, 150, 150)

        elif index == "UNSEEN":
            return (200, 240, 240)

        return (160, 240, 220)

    def load_titres(self) -> None:
        cle: str
        lien: Lien

        self.data_titres = {
            "ATT": {"lib": "Attr", "pos": 10, "col": 1},
            "NUM": {"lib": "N°", "pos": 50, "col": 1},
            "EXP": {"lib": "Expéditeur", "pos": 50, "col": 1},
            "OBJ": {"lib": "Objet", "pos": 300, "col": 1},
            "DAT": {"lib": "Date", "pos": 580, "col": 1},
            "DIR": {"lib": r"\/", "pos": 50, "col": 2},
        }
        self.titres = list()
        self.coord_x: Dict = dict()

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
                    position, 7, 
                    partial(self.get_color, self.data_titres[cle]["col"]), None,
                    id=cle)
            self.titres.append(lien)

            self.coord_x[cle] = lien.x

    def mouse_exit(self) -> None:
        self.mouse_over = False
        self.message_over = 0

    def mouse_move(self, mouse_pos: Tuple) -> None:
        idx: int

        self.mouse_over = True

        if mouse_pos[1] < 30:
            # ligne des titres
            self.message_over = 0
            
        else:
            # ligne des messages
            idx = mouse_pos[1] // ListeMessages.hauteur_ligne
            if idx > self.nb_mails:
                idx = 0

            self.message_over = idx

    def mouse_wheel(self, x, y) -> None: 
        if y < 0 and self.decal - y + self.nb_lignes_max > self.nb_lignes:
            return

        if self.selected is not None:
            if self.decal-y >= 0:
                self.selected += y

        self.decal += -y
        if self.decal < 0:
            self.decal = 0

        self.ascenseur.update(self.decal)

    def mouse_button_up(self, mouse_pos: Tuple, button: int) -> None:
        self.selected = self.message_over
    
    @staticmethod
    def format_adresse(lib: str) -> str:
        if "<" in lib:
            return lib[:lib.index("<")-1]

        return lib

    def get_mails(self) -> None:
        mail: Mail
        user: str
        status: str
        response: List
        contenu: Dict

        data: str
        dossier: str
        messages: str
        unseen: str

        mail = Mail()
        user = mail.USERNAME

        try:
            mail.connect()
            mail.select(self.directory)

            status, response = mail.mail.status(self.directory, "(MESSAGES UNSEEN)")
            if status == "OK":
                # response contient une liste avec un seul élément en bytes
                data = response[0].decode("utf-8").strip("()")

                *lst_dossier, _, messages, _, unseen = data.split()
                dossier = " ".join(lst_dossier)

                self.actions = f"USER={user};DIR={dossier};ALL={messages};UNSEEN={unseen}"

                for contenu in mail.get_mails("ALL"):  # ALL, UNSEEN
                    self.liste_datas.append(contenu)

            else:
                fprint(self.directory, "Status:", status)

        except Exception as erreur:
            fprint("get_mails():", erreur)
            raise

        try:
            mail.disconnect()
        except Exception:
            pass

        if self.actions is None:
            self.actions = "LOADING=False"
        else:
            self.actions += ";LOADING=False"

    def load_mails(self) -> None:

        cle: str
        lib: str
        attr: str

        largeur_max: Dict[str, int]

        debut: float
        fin: float

        message: Message

        debut = perf_counter()

        self.get_mails()

        largeur_max = dict()
        for cle in self.data_titres:
            if cle == "DIR":
                continue

            largeur_max[cle] = self.data_titres[cle]["lar"] - 10

        for datas in reversed(sorted(self.liste_datas, key=lambda x: x["DAT"])):
            message = Message()
            attr = ""
            for cle in datas:
                if cle == "ATT":
                    attr = datas[cle]

                lib = self.format_adresse(datas[cle]) if cle == "EXP" else datas[cle]
                texte = Texte( 
                    Lecteur.SysFont3, 
                    lib, 
                    self.get_texte_color, attr)

                if cle != "DAT":
                    texte.set_max_width(largeur_max[cle])

                message.load(cle, texte)

            self.liste_messages.append(message)

        self.nb_mails = len(self.liste_datas)
        self.nb_lignes = self.nb_mails
        self.decal = 0

        fin = perf_counter()
        fprint(f"load messages : {fin - debut:.4f} secondes")

        self.ascenseur = Ascenseur(self.surface, self.w, self.h, self.nb_lignes, self.nb_lignes_max,
            hauteur=self.h - ListeMessages.hauteur_ligne, posy=ListeMessages.hauteur_ligne+2)

    def load(self) -> None:
        mails: Thread

        self.liste_datas = list()
        self.liste_messages = list()
        self.nb_mails = 0
        self.selected = None
        self.message_over = 0
        self.actions = "LOADING=True"

        mails = Thread(target=self.load_mails)
        mails.start()

    def delete_message(self, numero: int):

        fprint("Delete : ", end="id=")
        message = self.liste_messages[numero]
        fprint(message.data["NUM"].libelle, end=" ")
        fprint(f'{message.data["OBJ"].libelle!r}')

        del self.liste_messages[numero]
        self.nb_mails -= 1
        self.nb_lignes -= 1

        self.ascenseur = Ascenseur(self.surface, self.w, self.h, self.nb_lignes, self.nb_lignes_max,
            hauteur=self.h - ListeMessages.hauteur_ligne, posy=ListeMessages.hauteur_ligne+2)

        if self.decal + self.nb_lignes_max > self.nb_lignes and self.decal > 0:
            self.decal -= 1

        if self.selected and self.selected > self.nb_lignes:
            if self.selected > 1:
                self.selected -= 1
            else:
                self.selected = None

        self.ascenseur.update(self.decal)

    def delete_selected_message(self):
        if not self.selected:
            return

        message = self.liste_messages[self.decal + self.selected - 1]
        MessageBox.set_message([
            "Voulez-vous supprimer le message",
            f"Numéro : {message.data["NUM"].libelle} ?"])
        
        MessageBox.bouton_oui.set_callback(self.delete_message, self.decal + self.selected - 1)
        MessageBox.activate()
        MessageBox.mouse_move(pygame.mouse.get_pos())

    def refresh(self) -> None:
        self.load()

    def update_screen(self, 
            screen: pygame.surface.Surface, coords: Optional[Tuple] = None) -> None:
        hauteur: int
        h: int

        if coords is not None:
            self.coords = pygame.Rect(coords)

        self.surface = screen.subsurface(self.coords)
        self.x, self.y, self.w, h = self.coords
        self.h = h - 1

        # nombre maximal de messages à afficher
        hauteur = h // ListeMessages.hauteur_ligne
        self.nb_lignes_max = hauteur - 1

        if self.decal + self.nb_lignes_max > self.nb_lignes:
            self.decal = max(0, self.nb_lignes - self.nb_lignes_max)

        self.ascenseur = Ascenseur(self.surface, self.w, self.h, self.nb_lignes, self.nb_lignes_max,
            hauteur=self.h - ListeMessages.hauteur_ligne, posy=ListeMessages.hauteur_ligne+2)
        self.ascenseur.update(self.decal)

    def draw(self) -> None:
        coord_y: int
        ligne: int
        color: Tuple
        cle: str
        message: Message
        surface: pygame.surface.Surface

        self.surface.fill((10, 20, 20))

        # fond d'une ligne de message
        selected = self.selected if self.selected else 0
        for ligne in range(1, 1+min(self.nb_mails, self.nb_lignes_max)):
            if ligne == selected:
                color = (13, 64, 13)
            elif ligne == self.message_over:
                color = (20, 50, 50)
            else:
                color = (20, 30, 30)

            if ligne % 2 and ligne not in (self.selected, self.message_over):
                continue

            pygame.draw.rect(self.surface, color, 
                (0, ListeMessages.hauteur_ligne * ligne, 
                    self.coords.w, ListeMessages.hauteur_ligne))

        # Ligne des titres
        self.surface.blits([titre.to_draw() for titre in self.titres])
        pygame.draw.line(self.surface, (50, 200, 150), (0, 30), (self.coords.w, 30))

        # tableau des messages
        coord_y = 6
        for message in self.liste_messages[self.decal:self.decal+self.nb_lignes_max]:
            coord_y += ListeMessages.hauteur_ligne
            for cle, surface in message.to_draw():
                self.surface.blit(surface, (self.coord_x[cle], coord_y))

        if self.nb_lignes <= self.nb_lignes_max:
            return

        self.ascenseur.draw()


class Ascenseur:

    surface: pygame.surface.Surface

    espace: int
    largeur_a: int
    hauteur_a: int
    posx_a: int
    posy: int
    coef: float

    coords: Tuple
    coords_a: Tuple

    def __init__(self, surface: pygame.surface.Surface, 
            width: int, height: int, nb_lignes: int, nb_lignes_max: int, **options):

        largeur: int
        hauteur: int
        hauteur_d: int
        posx: int

        def do_nothing(*args):
            pass

        # fait en sort que les fonctions ne fassent rien
        # puisque l'initialisation n'est pas terminee
        self.update = do_nothing
        self.draw = do_nothing

        if nb_lignes <= nb_lignes_max:
            return

        self.surface = surface
        self.espace = options.get("espace", 2)

        # largeur
        largeur = options.get("largeur", 20)
        self.largeur_a = largeur - 2 - 2 * self.espace

        # hauteur
        hauteur = options.get("hauteur", height)
        hauteur_d = hauteur - 2 - 2 * self.espace
        self.hauteur_a = int(nb_lignes_max / nb_lignes * hauteur_d) 

        # position x
        posx = options.get("posx", width - largeur)
        self.posx_a = posx + 1 + self.espace

        # position y
        self.posy = options.get("posy", 0)
        self.coords = (posx, self.posy, largeur, hauteur)
        self.coords_ombre = (posx-4, self.posy+1, 4, hauteur-2)

        self.coef = (hauteur_d - self.hauteur_a) / (nb_lignes - nb_lignes_max)

        # puisque l'initialisation est terminee
        # mise a jour des fonctions
        self.update = self.update_real
        self.draw = self.draw_real

        self.update(0)

    def update_real(self, decal: int) -> None:
        posy_a: int

        posy_a = self.posy + 1 + self.espace + int(decal * self.coef)
        self.coords_a = (self.posx_a, posy_a, self.largeur_a, self.hauteur_a)

    def draw_real(self) -> None:
        pygame.draw.rect(self.surface, (10, 20, 10), self.coords_ombre)
        pygame.draw.rect(self.surface, (30, 40, 40), self.coords)
        pygame.draw.rect(self.surface, (50, 200, 150), self.coords, 1)
        pygame.draw.rect(self.surface, (50, 200, 150), self.coords_a)


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
            screen: pygame.surface.Surface, coords: Optional[Tuple] = None) -> None:

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

    def get_color(self, lien) -> Tuple:
        if lien.selected:
            return (50, 255, 150)

        elif lien.mouse_over:
            return (50, 200, 150)

        elif lien.id == "LOD":
            return (255, 100, 100)

        return (255, 255, 255)

    def load(self, datas: Dict) -> None:
        self.liens: List[Lien] = list()
        first: bool = True
        lien: Lien

        for key, values in datas.items():
            position, ident, callback, *args = values

            visible = args[0] if args else True

            if first:
                lien = LienToggle(Lecteur.SysFont3, key, position, 8, None, 
                    callback, id=ident)
                first = False
                lien.selected = True
            else:
                lien = Lien(Lecteur.SysFont3, key, position, 8, None, 
                    callback, id=ident, visible=visible)

            lien.set_get_color(partial(self.get_color, lien))

            self.liens.append(lien)

    def mouse_exit(self) -> None:
        self.mouse_over = False
        for lien in self.liens:
            if lien.mouse_over:
                lien.mouse_over = False
                lien.update_color() 

    def mouse_move(self, mouse_pos: Tuple) -> None:
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

    def mouse_button_down(self, mouse_pos: Tuple, button: int) -> None:
        for lien in self.liens:
            if lien.mouse_over:
                lien.mouse_button_pushed = True

            elif lien.mouse_button_pushed:
                lien.mouse_button_pushed = False

    def mouse_button_up(self, mouse_pos: Tuple, button: int) -> None:
        for lien in self.liens:
            if lien.mouse_over and lien.mouse_button_pushed:
                lien.mouse_button_pushed = False
                lien.click()

            elif lien.mouse_button_pushed:
                lien.mouse_button_pushed = False

    def draw(self) -> None:
        self.surface.fill((40, 40, 60))

        # footer
        self.surface.blits([lien.to_draw() for lien in self.liens if lien.visible])
        [lien.draw_underline() for lien in self.liens if lien.selected]

        pygame.draw.line(self.surface, (50, 200, 150), (0, 0), (self.w, 0))


class Repertoire:

    colors: Dict = {
        True: (50, 200, 150),
        False: (200, 200, 200)
    }

    hauteur_ligne: int = 24
    largeur_niveau: int = 12

    libelle: str
    sdir_libelle: str
    selected: bool
    niveau: int
    nb_sdir: int

    surface: pygame.surface.Surface
    sdir_surf: pygame.surface.Surface

    x: int
    w: int
    h: int
    sdir_x: int
    sdir_w: int
    sdir_h: int

    has_sdir: bool
    visible: bool

    mouse_over: bool
    sdir_mouse_over: bool
    mouse_button_pushed: bool
    sdir_mouse_button_pushed: bool

    def __init__(self, ident: str, libelle: str, affichage: str, 
            niveau: int, selected: bool = False, nb_dirs: int = 0):

        self.id = ident
        self.libelle = libelle
        self.sdir_libelle = ""
        self.affichage = affichage
        self.niveau = niveau
        self.nb_sdir = nb_dirs
        self.has_sdir = nb_dirs > 1
        self.x = Repertoire.largeur_niveau * self.niveau
        self.sdir_x = self.x - 18

        self.visible = True
        self.mouse_over = False
        self.sdir_mouse_over = False
        self.mouse_button_pushed = False
        self.sdir_mouse_button_pushed = False
        self.select(selected)

    @staticmethod
    def y(ligne: int) -> int:
        return 10 + Repertoire.hauteur_ligne * ligne
    
    def select(self, selected: bool) -> None:
        self.selected = selected
        self.set_libelle(self.libelle)
        if self.has_sdir:
            self.set_sdir_libelle("+")

    def set_visible(self, visible: bool):
        self.visible = visible

    def set_libelle(self, libelle: str):
        self.libelle = libelle
        self.surface = Lecteur.SysFont2.render(libelle, False, 
            Repertoire.colors.get(self.selected, (255, 0, 0)))

        self.w, self.h = self.surface.get_size()

    def set_sdir_libelle(self, libelle: str):
        self.sdir_libelle = libelle
        self.sdir_surf = Lecteur.SysFont2.render(libelle, False, 
            Repertoire.colors.get(self.selected, (255, 0, 0)))

        self.sdir_w, self.sdir_h = self.sdir_surf.get_size()

    def sdir_to_screen(self, ligne: int) -> Tuple:
        return (self.sdir_surf, (self.sdir_x, self.y(ligne)))

    def to_screen(self, ligne: int) -> Tuple:
        return (self.surface, (self.x, self.y(ligne)))
        

class Repertoires:

    liste: List[Repertoire]

    max: int 
    selected: str
    decal: int 
    nb_dirs: int

    surface: pygame.surface.Surface
    x: int
    y: int
    w: int
    h: int
    visible: bool
    loaded: bool
    mouse_over: bool

    mouse_over_y: int

    actions: Optional[str]

    def __init__(self, screen: pygame.surface.Surface, coords: Tuple):
        self.liste = list()

        self.decal = 0
        self.nb_dirs = 0

        self.coords = pygame.Rect(coords)
        self.update_screen(screen, coords)
        self.set_visible(True)

        self.loaded = False
        self.selected = "INBOX"
        self.mouse_over = False
        self.mouse_over_y = 0

        self.actions = None

    def update_screen(self, 
            screen: pygame.surface.Surface, coords: Optional[Tuple] = None) -> None:

        if coords is not None:
            self.coords = pygame.Rect(coords)

        self.surface = screen.subsurface(self.coords)
        self.x, self.y, w, self.h = self.coords
        self.w = w - 1
        self.max = self.h // Repertoire.hauteur_ligne

        if self.decal + self.max > self.nb_dirs:
            self.decal = max(0, self.nb_dirs - self.max)

        self.update_ascenseur()

    def update_ascenseur(self) -> None:
        liste: List[Repertoire]
        nb_dirs: int

        liste = list(filter(lambda x: x.visible, self.liste))
        nb_dirs = len(liste)

        self.ascenseur = Ascenseur(
            self.surface, self.w, self.h, nb_dirs, self.max, posy=-1, hauteur=self.h+2)
        self.ascenseur.update(self.decal)

    def get_actions(self) -> Optional[str]:
        if self.actions is None:
            return None

        actions = self.actions
        self.actions = None
        return actions

    def mouse_move(self, mouse_pos: Tuple) -> None:
        mx: int
        my: int
        liste: List[Repertoire]

        self.mouse_over = True
        self.mouse_over_y = 0
        mx, my = mouse_pos

        liste = list(filter(lambda x: x.visible, self.liste))[self.decal:self.decal+self.max]

        for idx, repertoire in enumerate(liste):
            if repertoire.id == "MAIL":
                continue

            surface, (x, y) = repertoire.to_screen(idx)

            if y < my < y + repertoire.hauteur_ligne:
                self.mouse_over_y = y - 2

                if repertoire.has_sdir:
                    repertoire.sdir_mouse_over = mx < x
                    repertoire.mouse_over = not repertoire.sdir_mouse_over
                else:
                    repertoire.mouse_over = True
                    repertoire.sdir_mouse_over = False

            else:
                repertoire.mouse_over = False
                repertoire.sdir_mouse_over = False

    def mouse_exit(self) -> None:
        self.mouse_over = False
        self.mouse_over_y = 0

    def mouse_wheel(self, x, y) -> None: 
        if y < 0 and self.decal - y + self.max > self.nb_dirs:
            return

        self.decal += -y
        if self.decal < 0:
            self.decal = 0

        self.ascenseur.update(self.decal)

    def mouse_button_down(self, mouse_pos: Tuple, button: int) -> None:
        for idx, repertoire in enumerate(self.liste[self.decal:self.decal+self.max]):
            if repertoire.id == "MAIL":
                continue

            repertoire.mouse_button_pushed = repertoire.mouse_over
            repertoire.sdir_mouse_button_pushed = repertoire.sdir_mouse_over
    
    def mouse_button_up(self, mouse_pos: Tuple, button: int) -> None:
        for idx, repertoire in enumerate(self.liste[self.decal:self.decal+self.max]):
            if repertoire.id == "MAIL" or not (
                    repertoire.mouse_button_pushed or repertoire.sdir_mouse_button_pushed):
                continue

            if repertoire.mouse_button_pushed:
                self.select(repertoire.id)
            else:
                self.toggle_sdir(repertoire.id)

            repertoire.mouse_button_pushed = False
            repertoire.sdir_mouse_button_pushed = False

    def clear(self) -> None:
        self.liste.clear()
    
    def get_repertoires(self) -> None:
        mail: Mail

        connu: bool
        num: int
        ident: str
        repertoire: str

        repertoires_connus: List[Tuple] = list()
        repertoires_autres: List[Tuple] = list()

        debut = perf_counter()

        self.liste.append(Repertoire("MAIL", "Boîte de réception", "", 1, False, 0))

        mail = Mail()

        try:
            mail.connect()
            for connu, num, ident, repertoire, true_name in mail.get_dirs():
                if connu:
                    repertoires_connus.append((num, ident, repertoire, true_name))
                else:
                    repertoires_autres.append((num, ident, repertoire, true_name))

        except Exception as erreur:
            fprint("get_dirs():", erreur)

        # tri des repertoire par id
        repertoires_connus.sort(key=lambda elt: elt[0])

        # tri des repertoire par libelle
        repertoires_autres.sort(key=lambda elt: elt[2])

        for value in repertoires_connus:
            num, ident, repertoire, true_name = value
            try:
                nombre_sous_repertoires = len(list(mail.get_dirs(true_name)))
            except Exception as erreur:
                nombre_sous_repertoires = 0
                fprint("Ss rep", true_name, ":", erreur)

            self.liste.append(Repertoire(ident, repertoire, true_name, 2, 
                ident == self.selected, nombre_sous_repertoires))

        for value in repertoires_autres:
            num, ident, repertoire, true_name = value
            try:
                nombre_sous_repertoires = len(list(mail.get_dirs(repertoire)))
            except Exception as erreur:
                nombre_sous_repertoires = 0
                fprint("Ss rep", true_name, ":", erreur)

            self.liste.append(Repertoire(ident, repertoire, true_name, 2, 
                ident == self.selected, nombre_sous_repertoires))

        try:
            mail.disconnect()
        except Exception:
            pass

        self.loaded = True

        self.nb_dirs = len(self.liste)

        self.ascenseur = Ascenseur(self.surface, self.w, self.h, self.nb_dirs, self.max)
        self.ascenseur.update(self.decal)

        fin = perf_counter()
        temps_execution = fin - debut
        fprint(f"load repertoires : {temps_execution:.4f} secondes")

    def load(self) -> None:
        thread: Thread

        self.loaded = False
        thread = Thread(target=self.get_repertoires)
        thread.start()

    def get(self, ident: str) -> Repertoire:
        for repertoire in self.liste:
            if repertoire.id == ident:
                return repertoire

        raise Exception(f"Le repertoire {ident} n'existe pas")

    def index(self, ident: str, visible_only: bool = False) -> int:
        index: int

        index = 0
        for repertoire in self.liste:
            if repertoire.id == ident:
                return index

            if visible_only:
                index += 1 if repertoire.visible else 0
            else:
                index += 1

        raise Exception(f"Le repertoire {ident} n'existe pas")

    def set_visible_sdir(self, index: int, visible: bool) -> None:
        niveau = self.liste[index].niveau

        for repertoire in self.liste[index:]:
            if repertoire.niveau < niveau:
                break

            repertoire.set_visible(visible)

    def show_sdir(self, index: int) -> None:
        self.set_visible_sdir(index, True)

    def hide_sdir(self, index: int) -> None:
        self.set_visible_sdir(index, False)

    def toggle_sdir(self, ident: str) -> None:
        repertoire = self.get(ident)

        if not repertoire.has_sdir:
            return

        libelle = " - " if repertoire.sdir_libelle == "+" else "+"
        repertoire.set_sdir_libelle(libelle)

        index = 1 + self.index(ident)
        if len(self.liste) > index and self.liste[index].niveau == 1+repertoire.niveau:
            self.set_visible_sdir(index, not self.liste[index].visible)
            self.update_ascenseur()
            return
        
        mail = Mail()
        repertoires = list()

        try:
            mail.connect()
            for connu, num, new_ident, new_repertoire, true_name in mail.get_dirs(ident):
                if new_ident == ident:
                    continue

                new_repertoire = new_repertoire.split("/")[-1]
                repertoires.append((num, new_ident, new_repertoire, new_repertoire))

        except Exception as erreur:
            fprint("get_dirs():", erreur)

        # tri des repertoire par libelle
        repertoires.sort(key=lambda elt: elt[2])

        for value in repertoires:
            num, ident, new_repertoire, true_name = value
            try:
                search_repertoire = f'"{new_repertoire}"'
                nombre_sous_repertoires = len(list(mail.get_dirs(search_repertoire)))
            except Exception as erreur:
                nombre_sous_repertoires = 0
                fprint("Ss rep", true_name, ":", erreur)

            self.liste.insert(index, Repertoire(
                ident, new_repertoire, true_name, 1+repertoire.niveau, 
                False, nombre_sous_repertoires))

            index += 1

        try:
            mail.disconnect()
        except Exception:
            pass

        self.nb_dirs = len(self.liste)
        self.ascenseur = Ascenseur(self.surface, self.w, self.h, self.nb_dirs, self.max)
        self.ascenseur.update(self.decal)

    def select(self, ident: str) -> None:
        if ident == self.selected:
            return

        # on commence à 1 car le numero 0 ne correspond à aucun répertoire
        for idx, repertoire in enumerate(self.liste[1:]):
            if ident == repertoire.id:
                repertoire.select(True)
                self.selected = repertoire.id
                self.actions = f"DIR={self.selected}"

            elif repertoire.selected:
                repertoire.select(False)

    def toggle(self) -> None:
        self.visible = not self.visible

    def set_visible(self, visible: bool) -> None:
        self.visible = visible

    def to_screen(self) -> List[Tuple]:
        dirs_texte: List[Tuple] = list()
        index: int

        index = 0
        # for repertoire in self.liste[self.decal:self.decal+self.max]:
        for repertoire in self.liste[self.decal:]:
            if not repertoire.visible:
                continue

            dirs_texte.append(repertoire.to_screen(index))
            index += 1
            if index > self.max:
                break

        return dirs_texte

    def draw(self) -> None:
        if not self.visible:
            return 

        # directories
        self.surface.fill((10, 20, 20))
        pygame.draw.line(self.surface, (50, 200, 150), (self.w, 0), (self.w, self.h))

        if not self.loaded:
            return 

        if self.mouse_over_y:
            pygame.draw.rect(self.surface, (30, 50, 50),
                (0, self.mouse_over_y, self.w, Repertoire.hauteur_ligne))                

        self.surface.blits(self.to_screen())

        liste: List[Repertoire]
        liste = list(filter(lambda x: x.visible, self.liste))[self.decal:self.decal+self.max]

        for idx, repertoire in enumerate(liste):
            if repertoire.has_sdir:
                surface, coords = repertoire.sdir_to_screen(idx)
                self.surface.blit(surface, coords)

                if repertoire.sdir_mouse_over:
                    rect_coords = (*coords, repertoire.sdir_w, repertoire.sdir_h)
                    pygame.draw.rect(self.surface, (150, 200, 130), rect_coords, 1)

        self.ascenseur.draw()

        index1 = self.index(self.selected)
        index2 = self.index(self.selected, True)
        if index2 < self.decal:
            return

        # ligne indiquant que l'option est selectionnee
        selected_repertoire = self.liste[index1]
        if not selected_repertoire.visible:
            return

        dx = selected_repertoire.x
        dy = selected_repertoire.y(index2 - self.decal) 
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

    dirs_size: int 
    line_height: int
    block_size: int

    nb_lines: int
    nb_cols: int
    color_diff: int

    idxx: int
    idxy: int

    mouse: Mouse
    mouse_button_down_pos: Tuple
    running: bool

    nb_messages: int
    messages_non_vu: int

    headers: Headers
    liste_messages: ListeMessages
    repertoires: Repertoires
    footers: Footers

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

    def init_fonts(self) -> None:
        Lecteur.SysFont1 = pygame.font.SysFont("couriernew", 18)
        Lecteur.SysFont2 = pygame.font.SysFont("dejavuserif", 16)
        Lecteur.SysFont3 = pygame.font.SysFont(["segoeuiemoji"], 17)
        Lecteur.SysFont4 = pygame.font.SysFont("linuxlibertineg", 18, bold=False, italic=True)

    def initialize(self) -> None:
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

        MessageBox(self.screen)

        self.mouse = Mouse(*pygame.mouse.get_pos())
        self.mouse_button_down_pos = (0, 0)

        # Initialisation du cadrillage
        self.block_size = 40

        self.nb_lines = (self.screen_height-20) // self.block_size 
        self.nb_cols = (self.screen_width-20) // self.block_size 
        self.color_diff = 255 // (self.nb_lines + self.nb_cols)

        self.idxx = (self.mouse.x-10) // self.block_size
        self.idxy = (self.mouse.y-10) // self.block_size

    def init_draw(self) -> None:
        self.dirs_size = 300
        self.line_height = 30

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
            (0, self.line_height, self.dirs_size, 
                self.screen_height-2*self.line_height))
        self.repertoires.load()

        self.footers = Footers(self.screen,
            (0, self.screen_height-self.line_height, 
                self.screen_width, self.line_height))
        self.footers.load({
            " Dossiers ": (10, "DIR", self.toggle_repertoire),
            " Rafraichir ": (100, "REF", self.refresh_mails),
            " Loading ... ": (300, "LOD", None, True)
        })

    def boot(self) -> None:
        pygame.init()
        self.init_fonts()
        self.initialize()
        self.init_draw()

    def shutdown(self) -> None:
        pygame.quit()

    def mouse_enter_leave(self) -> None: 
        self.liste_messages.mouse_exit()
        self.repertoires.mouse_exit()
    
    def mouse_move(self, pos) -> None:
        self.mouse = Mouse(*pos)

        if MessageBox.show:
            MessageBox.mouse_move(pos)
            return

        if self.repertoires.visible and self.repertoires.coords.collidepoint(pos):
            self.repertoires.mouse_move((pos[0], pos[1]-self.repertoires.y))

        elif self.repertoires.mouse_over:
            self.repertoires.mouse_exit()

        if self.liste_messages.coords.collidepoint(pos):
            dx = self.repertoires.w if self.repertoires.visible else 0
            self.liste_messages.mouse_move(
                (pos[0]-dx, pos[1]-self.liste_messages.y))

        elif self.liste_messages.mouse_over:
            self.liste_messages.mouse_exit()

        if self.footers.coords.collidepoint(pos):
            self.footers.mouse_move((pos[0], pos[1]-self.footers.y))

        elif self.footers.mouse_over:
            self.footers.mouse_exit()

    def mouse_button_down(self, pos, button): 
        if MessageBox.show:
            MessageBox.mouse_button_down(pos, button)
            return
        
        self.mouse_button_down_pos = pos
        mouse_pos = pos[0], pos[1]-self.screen_height+30

        if self.footers.coords.collidepoint(pos):
            self.footers.mouse_button_down(mouse_pos, button)

        elif (self.repertoires.visible and self.repertoires.coords.collidepoint(pos) and 
                self.repertoires.coords.collidepoint(self.mouse_button_down_pos)):
            self.repertoires.mouse_button_down((pos[0], pos[1]-self.repertoires.y), button)

    def mouse_button_up(self, pos, button) -> None:
        if MessageBox.show:
            MessageBox.mouse_button_up(pos, button)
            self.mouse_move(pygame.mouse.get_pos())
            return

        if button != 1:
            return

        mouse_pos = pos[0], pos[1]-self.screen_height+30
        if (self.footers.coords.collidepoint(pos) and 
                self.footers.coords.collidepoint(self.mouse_button_down_pos)):
            self.footers.mouse_button_up(mouse_pos, button)

        elif (self.repertoires.visible and self.repertoires.coords.collidepoint(pos) and 
                self.repertoires.coords.collidepoint(self.mouse_button_down_pos)):
            self.repertoires.mouse_button_up((pos[0], pos[1]-self.repertoires.y), button)

        elif self.liste_messages.coords.collidepoint(pos):
            self.liste_messages.mouse_button_up((pos[0], pos[1]-self.liste_messages.y), button)

    def mouse_wheel(self, x: int, y: int) -> None: 
        if MessageBox.show:
            MessageBox.mouse_move((x, y))
            return

        if self.liste_messages.coords.collidepoint(Mouse.x, Mouse.y):
            self.liste_messages.mouse_wheel(x, y)

        elif self.repertoires.visible and self.repertoires.coords.collidepoint(Mouse.x, Mouse.y):
            self.repertoires.mouse_wheel(x, y)

    def keypressed(self, event): ...

    def keyreleased(self, event) -> None: 
        if event.key == pygame.K_ESCAPE:
            if MessageBox.show:
                MessageBox.deactivate()
                self.mouse_move(pygame.mouse.get_pos())
            else:
                self.running = False
            return

        if event.key == pygame.K_DELETE:
            if self.liste_messages.mouse_over:
                self.liste_messages.mouse_exit()
                self.liste_messages.delete_selected_message()

    def update_screen(self) -> None: 
        decal_x: int

        self.screen_width, self.screen_height = self.screen.get_size()

        self.headers.update_screen(self.screen, 
            (0, 0, self.screen_width, self.line_height))
        
        self.repertoires.update_screen(self.screen,
            (0, self.line_height, self.dirs_size, self.screen_height-2*self.line_height))

        if self.repertoires.visible:
            decal_x = self.dirs_size
        else:
            decal_x = 0

        self.liste_messages.update_screen(self.screen, 
            (decal_x, self.line_height, self.screen_width-decal_x, 
                self.screen_height-2*self.line_height))

        self.footers.update_screen(self.screen,
            (0, self.screen_height-self.line_height, self.screen_width, self.line_height))

        MessageBox.update_screen(self.screen)

    def get_pygame_events(self) -> None:
        is_mouse_scrolling: bool = False
        for event in pygame.event.get(pygame.MOUSEWHEEL):
            is_mouse_scrolling = True
            self.mouse_wheel(event.x, event.y)
            break

        for event in pygame.event.get():
            match event.type:
                case pygame.KMOD_LGUI:
                    self.mouse_move(event.pos)

                case pygame.MOUSEBUTTONDOWN:
                    if is_mouse_scrolling:
                        continue

                    if event.button != 2:
                        self.mouse_button_down(event.pos, event.button)

                case pygame.MOUSEBUTTONUP:
                    if is_mouse_scrolling:
                        continue
                    
                    self.mouse_button_up(event.pos, event.button)

                case pygame.MOUSEWHEEL:
                    fprint("Event mouse wheel")
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

    def update_repertoires(self) -> None:
        actions: Optional[str]
        
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
                        self.liste_messages.directory = f'"{value}"'
                        self.liste_messages.load()

                case _:
                    raise Exception(f"Paramètre {key} inconnu.")

    def update_liste_messages(self) -> None:
        actions: Optional[str]
        
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

    def update(self) -> None:
        self.update_repertoires()
        self.update_liste_messages()

    def draw(self) -> None:
        self.clock.tick(60)

        self.headers.draw()
        self.repertoires.draw()
        self.liste_messages.draw()
        self.footers.draw()

        MessageBox.draw()

        pygame.display.update()

    def refresh_mails(self) -> None:
        self.liste_messages.refresh()

    def toggle_repertoire(self) -> None: 
        self.repertoires.toggle()

        if self.repertoires.visible:
            self.liste_messages.update_screen(self.screen, 
                (self.dirs_size, self.line_height, 
                self.screen_width-self.dirs_size, self.screen_height-2*self.line_height))
        else:
            self.liste_messages.update_screen(self.screen, 
                (0, self.line_height, self.screen_width, 
                    self.screen_height-2*self.line_height))

    def run(self) -> None:
        self.boot()
        while self.running:
            self.update()
            self.draw()
            self.get_pygame_events()

        self.shutdown()


def main() -> None:
    lect: Lecteur

    lect = Lecteur()
    lect.run()


if __name__ == '__main__':
    main()
