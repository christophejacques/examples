import random

from general import Variable, fprint
from typing import List, Tuple, Optional, Dict, Callable, Any
from functools import partial
from abc import ABCMeta, abstractmethod
from math import pi, sin, cos

from general import Unique, Sauvegarde, Mouse, pygame
from mail import MailConfig
from textes import Texte


class Bouton:

    espace: int = 6

    identifiant: str

    surface: pygame.surface.Surface
    text_surface: pygame.surface.Surface
    rect: pygame.Rect
    recto: pygame.Rect

    text_coords: Tuple
    text_coordso: Tuple

    # BACK : couleur de fond
    # AROUND : couleur du contour
    # BACK_OVER : couleur de fond si curseur souris sur bouton
    # OVER : couleur du contour si curseur souris sur bouton

    color_around: Tuple
    color_back: Tuple
    color_over: Tuple
    color_back_over: Tuple

    mouse_over: bool
    mouse_button_down: bool

    callback: Optional[Callable]

    def __init__(self, 
            surface: pygame.surface.Surface, 
            identifiant: str,
            colors: Dict[str, Tuple],
            coords: Tuple,
            libelle: str,
            callback: Optional[Callable] = None,
            *args, **kwargs):

        self.identifiant = identifiant
        self.surface = surface
        self.rect = pygame.Rect(coords)
        self.recto = pygame.Rect(
            (coords[0] + Bouton.espace, coords[1] + Bouton.espace, *coords[2:]))

        self.color_back = colors.get("BACK", (0, 0, 0))
        self.color_around = colors.get("AROUND", self.color_back)
        self.color_over = colors.get("OVER", self.color_back)
        self.color_back_over = colors.get("BACK_OVER", self.color_back)

        self.back_color = self.color_back
        self.color = self.color_around

        self.mouse_over = False
        self.mouse_button_down = False
        self.set_libelle(libelle)
        self.set_callback(callback, *args, **kwargs)

    def set_libelle(self, libelle: str):
        color = (255, 255, 255)
        self.text_surface = Variable.SysFont3.render(libelle, False, color)
        width, height = self.text_surface.get_size()
        self.text_coords = (self.rect.x + self.rect.w // 2 - width // 2,
            self.rect.y + self.rect.h // 2 - height // 2)
        self.text_coordso = (
            self.rect.x + self.rect.w // 2 - width // 2 + Bouton.espace,
            self.rect.y + self.rect.h // 2 - height // 2 + Bouton.espace)

    def set_callback(self, callback: Optional[Callable], *args, **kwargs):
        if callback:
            self.callback = partial(callback, *args, **kwargs)
        else:
            self.callback = None

    def execute(self):
        if self.callback:
            self.callback()

    def set_mouse_over(self, mouse_over: bool):
        if self.mouse_over == mouse_over:
            return

        self.mouse_over = mouse_over
        if mouse_over:
            self.back_color = self.color_back_over
            self.color = self.color_over
        else:
            self.back_color = self.color_back
            self.color = self.color_around

        self.draw()

    def draw(self):
        # ombre
        if self.mouse_button_down and self.mouse_over:
            pygame.draw.rect(self.surface, (30, 40, 40), self.rect)
            # surface
            pygame.draw.rect(self.surface, self.back_color, self.recto)
            pygame.draw.rect(self.surface, self.color, self.recto, 1)

            self.surface.blit(self.text_surface, self.text_coordso)

        else:
            pygame.draw.rect(self.surface, (10, 20, 10), self.recto)

            # surface
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

    boutons: List[Bouton]
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

        cls.boutons = list()

        cls.boutons.append(
            Bouton(cls.msg_screen, "OUI",
                {"BACK": (25, 70, 40),
                 "AROUND": (50, 200, 150),
                 "BACK_OVER": (30, 80, 50),
                 "OVER": (50, 255, 150)},
                (32, 140, 128, 32), "Oui", callback, *args, **kwargs))

        cls.boutons.append(
            Bouton(cls.msg_screen, "NON",
                {"BACK": (70, 40, 25),
                 "AROUND": (200, 150, 50),
                 "BACK_OVER": (80, 50, 30),
                 "OVER": (255, 150, 50)},
                (240, 140, 128, 32), "Non"))

        cls.set_message(liste_message)
        cls.show = False

    @classmethod
    def get_bouton(cls, identifiant: str) -> Bouton:
        for bouton in cls.boutons:
            if bouton.identifiant == identifiant:
                return bouton

        raise Exception(f"Bouton {identifiant!r} inconnu.")

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

        for bouton in cls.boutons:
            if bouton.rect.collidepoint(mouse_pos):
                bouton.set_mouse_over(True)
            else:
                bouton.set_mouse_over(False)

    @classmethod
    def mouse_button_down(cls, pos: Tuple, button: int) -> None:
        if button != 1:
            return

        for bouton in cls.boutons:
            bouton.mouse_button_down = bouton.mouse_over
            bouton.draw()

    @classmethod
    def mouse_button_up(cls, pos: Tuple, button: int) -> None:

        if button != 1:
            for bouton in cls.boutons:
                bouton.mouse_button_down = False
                bouton.draw()

        for bouton in cls.boutons:
            if bouton.mouse_button_down:
                if bouton.mouse_over:
                    bouton.execute()
                    MessageBox.deactivate()

                bouton.mouse_button_down = False

    @classmethod
    def set_message(cls, liste_message: List[str]):
        cls.msg_screen.fill((0, 0, 0, 0))
        pygame.draw.rect(cls.msg_screen, (10, 20, 10), cls.coords_ombre)
        pygame.draw.rect(cls.msg_screen, (30, 40, 40), cls.coords)

        pygame.draw.line(cls.msg_screen, (0, 0, 0), (2, 2), (400, 2))
        pygame.draw.line(cls.msg_screen, (0, 0, 0), (2, 2), (2, 200))
        
        pygame.draw.rect(cls.msg_screen, (50, 200, 150), cls.coords, 1)

        for bouton in cls.boutons:
            bouton.draw()

        y = 50
        for message in liste_message:
            cls.text_surface = Variable.SysFont3.render(message, False, (255, 255, 255))
            width, height = cls.text_surface.get_size()
            cls.msg_screen.blit(cls.text_surface, (cls.rect.w // 2 - width // 2, y))
            y += height + 4

    @classmethod
    def activate(cls):
        for bouton in cls.boutons:
            bouton.set_mouse_over(False)

        cls.show = True
        cls.mouse_move(pygame.mouse.get_pos())

    @classmethod
    def deactivate(cls):
        cls.show = False

    @classmethod
    def draw(cls):
        if cls.show:
            cls.screen.blit(cls.msg_screen, cls.pos_screen)


class Ascenseur:

    surface: pygame.surface.Surface

    espace: int
    largeur_a: int
    hauteur_a: int
    posx_a: int
    posy: int
    coef: float

    show: bool

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

        self.largeur_a = 0
        self.espace = options.get("espace", 2)

        # fait en sort que les fonctions ne fassent rien
        # puisque l'initialisation n'est pas terminee
        self.update = do_nothing
        self.draw = do_nothing

        if nb_lignes <= nb_lignes_max:
            self.show = False
            return

        self.show = True
        self.surface = surface

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

    def get_width(self):
        if self.largeur_a == 0:
            return 0
        return self.largeur_a + 4 + 2 + 2 * self.espace

    def update_real(self, decal: int) -> None:
        posy_a: int

        posy_a = self.posy + 1 + self.espace + int(decal * self.coef)
        self.coords_a = (self.posx_a, posy_a, self.largeur_a, self.hauteur_a)

    def draw_real(self) -> None:
        pygame.draw.rect(self.surface, (10, 20, 10), self.coords_ombre)
        pygame.draw.rect(self.surface, (30, 40, 40), self.coords)
        pygame.draw.rect(self.surface, (50, 200, 150), self.coords, 1)
        pygame.draw.rect(self.surface, (50, 200, 150), self.coords_a)


class Ligne:

    donnees: Dict[str, Any]

    def __init__(self):
        self.donnees = dict()

    def load(self, donnees: Dict) -> None:
        for key, value in donnees.items():
            self.donnees[key] = value

    def set(self, code_colonne: str, value: Any) -> None:
        self.donnees[code_colonne] = value

    def get(self, code_colonne: str) -> Any:
        return self.donnees.get(code_colonne)

    def __setitem__(self, code_colonne: str, value: Any) -> None:
        self.set(code_colonne, value)

    def __getitem__(self, code_colonne: str) -> Any:
        return self.get(code_colonne)


class Tableau:

    positions: Ligne
    content: List[Ligne]

    def __init__(self, positions_colonnes: Ligne):
        self.positions = positions_colonnes
        self.reset()

    def reset(self) -> None:
        self.content = list()

    def add(self, ligne: Ligne) -> None:
        self.content.append(ligne)

    def load(self, donnees: Dict) -> None:
        ligne = Ligne()
        for key, value in donnees.items():
            ligne[key] = value

        self.add(ligne)

    def blits(self, decal: int, dy: int) -> List[Tuple]:
        result: List[Tuple]
        coords: Tuple

        result = list()
        for index, content in enumerate(self.content):
            for titre in self.positions.donnees:
                coords = (self.positions[titre], decal + index*dy)
                result.append((content[titre], coords))
        return result


class Menu(Unique):

    hauteur_ligne: int = 28

    surface: pygame.surface.Surface
    rect: pygame.Rect
    rect_ombre: pygame.Rect

    show: bool 

    color_back: Tuple
    color_around: Tuple
    color_ombre: Tuple

    content: Tableau
    mouse_over: Optional[int]
    selected: int
    selected_button_down: Optional[int]

    def init(self, 
            surface: pygame.surface.Surface, 
            colors: Dict[str, Tuple],
            coords: Tuple,
            selected: int,
            callback: Optional[Callable]):

        self.surface = surface
        self.rect = pygame.Rect(coords)
        self.rect_ombre = pygame.Rect(5+coords[0], 5+coords[1], *coords[2:])
        self.color_back = colors.get("BACK", (0, 0, 0))
        self.color_around = colors.get("AROUND", (0, 0, 0))
        self.color_ombre = (10, 20, 10)

        self.callback = callback

        positions = Ligne()
        positions.load({
            "texte_surface": self.rect.x + 8, 
            "nombre": 0})
        self.content = Tableau(positions)

        self.mouse_over = None
        self.selected = selected
        self.selected_button_down = None
        self.show = False

    def load(self, usernames: List):
        texte: Texte
        max_size: int = 0
        texte_size: int = 0

        def getColor(*args):
            return (200, 200, 200)

        for index, username in enumerate(sorted(usernames)):
            texte = Texte(Variable.SysFont3, username, getColor)
            texte_size = texte.surface.get_width()
            if texte_size > max_size:
                max_size = texte_size

            nombre = Texte(Variable.SysFont3, f"({random.randint(1, 20)})", getColor)
            self.content.load({
                "libelle": username,
                "texte_surface": texte.surface, 
                "nombre": nombre.surface})

        self.rect.h = Menu.hauteur_ligne * (1+index)
        self.rect_ombre.h = Menu.hauteur_ligne * (1+index) + 5
        max_size = max(400, 2*10 + 100 + max_size)
        self.rect.w = max_size
        self.content.positions["nombre"] = self.rect.x + self.rect.w - 50

        fprint("Nombre de messageries:", 1+index)

    def print(self) -> None:
        fprint("id=", id(self), self.color_back, self.rect)

    def toggle(self) -> None:
        self.show = not self.show

    def activate(self) -> None:
        self.show = True

    def deactivate(self, callback=None) -> None:
        self.show = False
        if callback:
            callback()

    def mouse_move(self, position):
        if self.rect.collidepoint(position):
            # fprint("Menu", position)
            self.mouse_over = (position[1] - self.rect.y) // Menu.hauteur_ligne
        else:
            self.mouse_over = None

    def mouse_button_down(self, position, button):
        if self.mouse_over is None:
            self.selected_button_down = None
        else:
            self.selected_button_down = self.mouse_over
            # fprint("down =", position, self.mouse_over)
        
    def mouse_button_up(self, position, button):
        if self.mouse_over is None:
            return

        # fprint("up =", position, self.mouse_over)
        if self.mouse_over == self.selected_button_down:
            # fprint(f"Menu.click({self.mouse_over})")

            mail_config = MailConfig()
            if self.mouse_over != mail_config.selected:
                self.selected = self.mouse_over
                mail_config.set_config(self.mouse_over)
                try:
                    if self.callback:
                        self.callback()
                    with Sauvegarde() as config:
                        config.set_content(
                            "Lecteur.email", 
                            self.content.content[self.mouse_over]["libelle"])

                except Exception as erreur:
                    fprint("Menu.mouse_button_up:", erreur)

        self.mouse_over = None
        self.selected_button_down = None
        
    def draw(self) -> None:
        if not self.show:
            return
        
        pygame.draw.rect(self.surface, self.color_ombre, self.rect_ombre)
        pygame.draw.rect(self.surface, self.color_back, self.rect)

        if self.selected is not None:
            pygame.draw.rect(self.surface, (20, 100, 30), 
                (self.rect.x, self.rect.y+Menu.hauteur_ligne*self.selected, 
                    self.rect.w, Menu.hauteur_ligne))

        if self.mouse_over is not None and self.mouse_over != self.selected:
            pygame.draw.rect(self.surface, (20, 50, 50), 
                (self.rect.x, self.rect.y+Menu.hauteur_ligne*self.mouse_over, 
                    self.rect.w, Menu.hauteur_ligne))

        self.surface.blits(self.content.blits(self.rect.y + 6, Menu.hauteur_ligne))

        pygame.draw.rect(self.surface, self.color_around, self.rect, 1)


class Icone(metaclass=ABCMeta):

    identifiant: str
    surface: pygame.surface.Surface
    rect: pygame.Rect

    color_over: Tuple
    color_back: Tuple
    color_around: Tuple

    back_color: Tuple
    color: Tuple

    is_mouse_over: bool
    is_mouse_button_down: bool

    def __init__(self, 
            identifiant: str,
            surface: pygame.surface.Surface, 
            colors: Dict[str, Tuple],
            coords: Tuple,
            *args, **kwargs):

        self.identifiant = identifiant
        self.kwargs = kwargs

        self.rect = pygame.Rect(coords)
        self.update_screen(surface)

        self.color_back = colors.get("BACK", (0, 0, 0))
        self.color_around = colors.get("AROUND", self.color_back)
        self.color_over = colors.get("OVER", self.color_back)

        self.back_color = self.color_back
        self.color = self.color_around

        self.is_mouse_over = False
        self.is_mouse_button_down = False

        self.__post_init__()

    def __post_init__(self): ...

    def update_screen(self, screen):
        self.surface = screen
        self.calc_draw()

    def mouse_move(self, position: Tuple) -> None:
        is_mouse_over: bool = self.is_mouse_over
        self.is_mouse_over = True

        if not is_mouse_over:
            self.redraw()

    def mouse_exit(self) -> None:
        if self.is_mouse_over:
            self.is_mouse_over = False
            self.redraw()

    def mouse_button_down(self):
        self.is_mouse_button_down = self.is_mouse_over

    def mouse_button_up(self):
        if self.is_mouse_button_down and self.is_mouse_over:
            self.click()

        self.is_mouse_button_down = False

    @abstractmethod
    def calc_draw(self) -> None: ...

    @abstractmethod
    def check(self) -> None: ...

    @abstractmethod
    def click(self) -> None: ...

    @abstractmethod
    def redraw(self) -> None: ...
    def draw(self) -> None: ...


class Proprietes(Icone):

    polyrect: List
    polyrect_down: List

    properties: bool

    def __post_init__(self):
        self.properties = False

    def calc_draw(self):
        # repositionne l'icone
        for attribute in ("x", "y", "w", "h"):
            formule = self.kwargs.get(f"formula_{attribute}")
            if formule:
                if attribute == "x":
                    self.rect.x = eval(formule)
                elif attribute == "y":
                    self.rect.y = eval(formule)
                elif attribute == "w":
                    self.rect.w = eval(formule)
                elif attribute == "h":
                    self.rect.h = eval(formule)

        rayon: float = (self.rect.w - 2) / 2

        self.on_click = self.kwargs.get("on_click", None)
        self.polyrect_down = list()

        for angle in range(16):
            if angle % 2:
                posx = self.rect.centerx+int(rayon*cos(angle*pi/8))//2
                posy = self.rect.centery+int(rayon*sin(angle*pi/8))//2
            else:
                posx = self.rect.centerx+int(rayon*cos(angle*pi/8))
                posy = self.rect.centery+int(rayon*sin(angle*pi/8))

            self.polyrect_down.append((posx, posy))

        self.polyrect = self.polyrect_down

    def check(self):
        pass

    def click(self):
        self.properties = not self.properties
        if self.properties and self.on_click:
            self.on_click()

        self.redraw()

    def redraw(self):
        pygame.draw.rect(self.surface, self.color_back, self.rect)
        if self.is_mouse_over:
            pygame.draw.rect(self.surface, self.color_around, self.rect, 1)

        if self.properties:
            pygame.draw.polygon(self.surface, self.color, self.polyrect)
        else:
            pygame.draw.polygon(self.surface, self.color, self.polyrect, 1)


class Triangle(Icone):

    polyrect_down: List
    polyrect_up: List
    polyrect: List

    menu: Menu

    def __post_init__(self):
        self.menu = Menu()

    def calc_draw(self):
        espace: int = 5
        
        self.polyrect_down = [
            (self.rect.x+espace, self.rect.y+espace),
            (self.rect.x+self.rect.w-espace, self.rect.y+espace),
            (self.rect.x+self.rect.w//2, self.rect.y+self.rect.h-espace),
        ]

        dy: int = self.rect.y+self.rect.h-espace
        self.polyrect_up = [
            (self.rect.x+espace, dy),
            (self.rect.x+self.rect.w-espace, dy),
            (self.rect.x+self.rect.w//2, self.rect.y+espace),
        ]
        self.polyrect = self.polyrect_down

    def check(self):
        if self.menu.show:
            if self.polyrect != self.polyrect_up:
                self.polyrect = self.polyrect_up
                self.redraw()
        else:
            if self.polyrect != self.polyrect_down:
                self.polyrect = self.polyrect_down
                self.redraw()

    def click(self):
        self.menu.toggle()

    def redraw(self):
        pygame.draw.rect(self.surface, self.color_back, self.rect)
        if self.is_mouse_over:
            pygame.draw.rect(self.surface, self.color_around, self.rect, 1)

        pygame.draw.polygon(self.surface, self.color, self.polyrect)


class Tooltip(Unique):

    surface_texte: pygame.surface.Surface
    screen: pygame.surface.Surface

    screen_width: int

    libelle: str
    width: int
    color: Tuple
    show: bool

    def __init__(self, screen: Optional[pygame.surface.Surface] = None):
        if screen is not None:
            self.update_screen(screen)

        self.show = False
        self.color = (255, 255, 255)
        self.set_libelle("")

    def update_screen(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.screen_width = self.screen.get_width()

    def activate(self):
        self.show = True

    def deactivate(self):
        self.show = False

    def set_libelle(self, libelle: str) -> None:
        self.libelle = libelle
        self.surface_texte = Variable.SysFont3.render(libelle, False, self.color)
        self.width = self.surface_texte.get_width()

    def draw(self) -> None:
        shape_surf: pygame.surface.Surface
        hauteur_ligne: int
        dx: int
        dy: int

        color_ombre: Tuple
        coordso: Tuple

        hauteur_ligne = 28

        dx = Mouse.x - self.width // 2
        dy = 2 + (Mouse.y - 30) // hauteur_ligne * hauteur_ligne
        if dy - 10 < 30:
            dy += 2 * hauteur_ligne + 10
        if dx < 10:
            dx = 10
        elif dx + self.width > self.screen_width - 48:
            dx = self.screen_width - self.width - 48  # 20+16+2

        color_ombre = (10, 10, 10, 120)
        coordso = (dx-10, dy-10, self.width+16+20, hauteur_ligne+20)

        # Ombre
        shape_surf = pygame.Surface(coordso[2:], pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color_ombre, shape_surf.get_rect())
        self.screen.blit(shape_surf, coordso)

        # Rectangle
        pygame.draw.rect(self.screen, (40, 60, 60), 
            (dx, dy, self.width+16, hauteur_ligne))

        # Texte
        self.screen.blit(self.surface_texte, (dx + 8, dy + 6))


class Test(Unique):
    pass


def main():

    positions = Ligne()
    positions["email"] = 8
    positions["nb"] = 120

    tab = Tableau(positions)
    tab.load({"email": "ligne1", "nb": 1})

    li = Ligne()
    li.set("email", "ligne2")
    li.set("nb", 22)
    tab.add(li)

    li = Ligne()
    li.set("email", "ligne3")
    li.set("nb", 333)
    tab.add(li)

    for index, blit in enumerate(tab.blits(0, 20)):
        print("-", blit, end="  ")
        if index % 2:
            print()


if __name__ == "__main__":
    t1 = Test()
    t2 = Test()
    fprint("Instances 'Test' identiques:", id(t1) == id(t2))

    main()
