from general import Variable, fprint
from typing import List, Tuple, Optional, Dict, Callable
from functools import partial

from general import Unique, Sauvegarde, pygame
from mail import MailConfig
from textes import Texte


class Bouton:

    espace: int = 6

    identifiant: str

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
            self.back_color = self.color_over
            self.color = self.color_around
        else:
            self.back_color = self.color_back
            self.color = self.color_around

        self.draw()

    def draw(self):
        # ombre
        if self.mouse_button_down and self.mouse_over:
            pygame.draw.rect(self.surface, (30, 40, 40), self.recto)
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
                 "OVER": (30, 80, 50)},
                (32, 140, 128, 32), "Oui", callback, *args, **kwargs))

        cls.boutons.append(
            Bouton(cls.msg_screen, "NON",
                {"BACK": (70, 40, 25),
                 "AROUND": (200, 150, 50),
                 "OVER": (80, 50, 30)},
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


class Menu(Unique):

    hauteur_ligne: int = 28

    surface: pygame.surface.Surface
    rect: pygame.Rect
    rect_ombre: pygame.Rect

    show: bool 

    color_back: Tuple
    color_around: Tuple
    color_ombre: Tuple

    liste: List[Texte]
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

        self.liste = list()
        self.mouse_over = None
        self.selected = selected
        self.selected_button_down = None
        self.show = False

    def load(self, usernames: List):
        def getColor(*args):
            return (200, 200, 200)

        for index, username in enumerate(sorted(usernames)):
            self.liste.append(Texte(Variable.SysFont3, username, getColor))

        self.rect.h = Menu.hauteur_ligne * (1+index)
        self.rect_ombre.h = Menu.hauteur_ligne * (1+index) + 5
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
                            "Lecteur.adresse", self.liste[self.mouse_over].libelle)

                except Exception as erreur:
                    fprint("Menu.mouse_button_up:", erreur)

        self.mouse_over = None
        self.selected_button_down = None
        
    def draw(self) -> None:
        if not self.show:
            return
        
        pygame.draw.rect(self.surface, self.color_ombre, self.rect_ombre)
        pygame.draw.rect(self.surface, self.color_back, self.rect)
        dx = self.rect.x + 8
        dy = self.rect.y + 6

        for index, texte in enumerate(self.liste):
            if index == self.selected:
                pygame.draw.rect(self.surface, (20, 100, 30), 
                    (self.rect.x, 
                        self.rect.y+Menu.hauteur_ligne*index, 
                        self.rect.w, Menu.hauteur_ligne))

            elif index == self.mouse_over:
                pygame.draw.rect(self.surface, (20, 50, 50), 
                    (self.rect.x, self.rect.y+Menu.hauteur_ligne*index, 
                        self.rect.w, Menu.hauteur_ligne))

            self.surface.blit(texte.surface, (dx, dy))
            dy += Menu.hauteur_ligne

        pygame.draw.rect(self.surface, self.color_around, self.rect, 1)


class Icone:

    surface: pygame.surface.Surface
    rect: pygame.Rect

    color_over: Tuple
    color_back: Tuple
    color_around: Tuple

    is_mouse_over: bool
    is_mouse_button_down: bool

    callback: Optional[Callable]

    def __init__(self, 
            surface: pygame.surface.Surface, 
            colors: Dict[str, Tuple],
            coords: Tuple,
            callback: Optional[Callable] = None,
            *args, **kwargs):

        espace: int = 5
        
        self.surface = surface
        self.rect = pygame.Rect(coords)
        self.menu = Menu()

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

        self.color_back = colors.get("BACK", (0, 0, 0))
        self.color_around = colors.get("AROUND", self.color_back)
        self.color_over = colors.get("OVER", self.color_back)

        self.back_color = self.color_back
        self.color = self.color_around

        self.is_mouse_over = False
        self.is_mouse_button_down = False

    def update_screen(self, screen):
        self.surface = screen

    def check(self):
        if self.menu.show:
            if self.polyrect != self.polyrect_up:
                self.polyrect = self.polyrect_up
                self.redraw()
        else:
            if self.polyrect != self.polyrect_down:
                self.polyrect = self.polyrect_down
                self.redraw()

    def mouse_move(self, position: Tuple) -> None:
        is_mouse_over: bool = self.is_mouse_over
        self.is_mouse_over = True

        if not is_mouse_over:
            # fprint("Icone.redraw()")
            self.redraw()

    def mouse_exit(self) -> None:
        if self.is_mouse_over:
            self.is_mouse_over = False
            self.redraw()

    def mouse_button_down(self):
        self.is_mouse_button_down = self.is_mouse_over

    def mouse_button_up(self):
        if self.is_mouse_button_down and self.is_mouse_over:
            # fprint("Icone.click()")
            self.menu.toggle()

        self.is_mouse_button_down = False

    def redraw(self):
        pygame.draw.rect(self.surface, self.color_back, self.rect)
        if self.is_mouse_over:
            pygame.draw.rect(self.surface, self.color_around, self.rect, 1)

        pygame.draw.polygon(self.surface, self.color, self.polyrect)

    def draw(self) -> None:
        pass


class Test(Unique):
    pass


if __name__ == "__main__":
    t1 = Test()
    t2 = Test()
    fprint("Instances 'Test' identiques:", id(t1) == id(t2))
