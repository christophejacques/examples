import pygame  # noqa: E402

from general import Variable
from typing import List, Tuple, Optional, Dict, Callable
from functools import partial


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
        self.text_surface = Variable.SysFont3.render(libelle, False, color)
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
            cls.text_surface = Variable.SysFont3.render(message, False, (255, 255, 255))
            width, height = cls.text_surface.get_size()
            cls.msg_screen.blit(cls.text_surface, (cls.rect.w // 2 - width // 2, y))
            y += height + 4

    @classmethod
    def activate(cls):
        cls.bouton_oui.set_mouse_over(False)
        cls.bouton_non.set_mouse_over(False)
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
