import pygame

from functools import partial
from typing import Any, Callable, Tuple, List
from enum import Enum, auto


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


class Action(Enum):
    Cancel = auto()
    Yes = auto()
    No = auto()
    Close = auto()


class Constante:

    FONT22: pygame.font.Font
    FONT28: pygame.font.Font

    @classmethod
    def __init__(cls):
        pygame.init()
        cls.FONT22 = pygame.font.SysFont("arial", 18)
        cls.FONT28 = pygame.font.SysFont("arial", 28)

    @classmethod
    def close(cls):
        pygame.quit()


class Commande:

    callback: Callable

    def __init__(self, label: str, callback: Callable, *params, **kwparams):

        self.label = label
        self.callback = partial(callback, *params, *kwparams)

        self.surface = Constante.FONT22.render(label, False, (40, 40, 200))
        self.width, self.height = self.surface.get_size()


class Bouton:

    def __init__(self, screen: pygame.surface.Surface, 
            back_color: Tuple, coords: Tuple, commande: Commande):
        self.screen = screen
        self.back_color = back_color
        self.commande = commande

        self.init()
        self.set_coords(coords)

    def init(self):
        self.mouse_over = False
        self.mouse_button_pushed = False
        self.actual_back_color = self.back_color

        self.color_light = 3*(200,)
        self.color_shadow = 3*(0,)

    def set_coords(self, coords: Tuple):
        self.coords = pygame.Rect(*coords)

        self.coords_h1 = coords[:2], (coords[0]+coords[2], coords[1])
        self.coords_h2 = (coords[0], coords[1]+coords[3]), (coords[0]+coords[2], coords[1]+coords[3])

        self.coords_v1 = coords[:2], (coords[0], coords[1]+coords[3])
        self.coords_v2 = (coords[0]+coords[2], coords[1]), (coords[0]+coords[2], coords[1]+coords[3])

        self.texte_coords = (
            self.coords.x + (self.coords.width//2) - self.commande.width//2, 
            self.coords.y + (self.coords.height//2) - self.commande.height//2)

    def clicked(self):
        self.commande.callback()

    def mouse_button_down(self):
        self.mouse_button_pushed = self.mouse_over

        if self.mouse_button_pushed:
            self.color_light = 3*(0,)
            self.color_shadow = 3*(200,)
        else:
            self.color_light = 3*(200,)
            self.color_shadow = 3*(0,)

    def mouse_button_up(self):
        if self.mouse_button_pushed and self.mouse_over:
            self.clicked()
        self.mouse_button_pushed = False

        self.color_light = 3*(200,)
        self.color_shadow = 3*(0,)

    def mouse_move(self, position: Tuple):
        if self.coords.collidepoint(position):
            self.mouse_over = True
            self.actual_back_color = tuple(
                min(255, int(color*1.2)) for color in self.back_color)
        else:
            self.mouse_over = False
            self.actual_back_color = self.back_color
            
    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.screen, self.actual_back_color, self.coords)

        pygame.draw.line(self.screen, self.color_light, *self.coords_h1, 2)
        pygame.draw.line(self.screen, self.color_light, *self.coords_v1, 2)

        pygame.draw.line(self.screen, self.color_shadow, *self.coords_h2, 2)
        pygame.draw.line(self.screen, self.color_shadow, *self.coords_v2, 2)

        self.screen.blit(self.commande.surface, self.texte_coords)


class MessageBox:

    Value: Any

    def __init__(self, screen: pygame.surface.Surface, 
            size: Tuple, 
            btn_defs: List):
        self.screen = screen

        largeur_box, hauteur_box = size
        width, height = screen.get_size()
        self.coords = pygame.Rect(width//2 - largeur_box//2, 
            height//2 - hauteur_box//2, largeur_box, hauteur_box)

        self.coords_white = (self.coords[0]+10, self.coords[1]+10, 
            self.coords[2]-20, self.coords[3]-80)
        self.coords_lineh1 = (self.coords_white[0], self.coords_white[1]), (
            self.coords_white[0]+self.coords_white[2], 
            self.coords_white[1])
        self.coords_lineh2 = (self.coords_white[0], 
            self.coords_white[1]+self.coords_white[3]), (
            self.coords_white[0]+self.coords_white[2], 
            self.coords_white[1]+self.coords_white[3])

        self.coords_linev1 = (self.coords_white[0], self.coords_white[1]), (
            self.coords_white[0], 
            self.coords_white[1]+self.coords_white[3])
        self.coords_linev2 = (
            self.coords_white[0]+self.coords_white[2], 
            self.coords_white[1]), (
            self.coords_white[0]+self.coords_white[2], 
            self.coords_white[1]+self.coords_white[3])

        self.text_surface = Constante.FONT28.render("Quitter l'application ?", 
            False, (40, 40, 60))
        w, h = self.text_surface.get_size()
        self.text_coords = (
            self.coords_white[0] + self.coords_white[2]//2 - w//2, 
            self.coords_white[1] + self.coords_white[3]//2 - h//2)

        self.boutons: List = list()
        self.calculate(btn_defs)
        self.open()

    def calculate(self, btn_defs: List):
        # btn : str, Optional[str], Optional[tuple]
        # 1. str = Libelle bouton
        # 2. str = return value
        # 3. tuple = back color bouton

        nb_btns: int = len(btn_defs)
        footer_hauteur = self.coords[1] + self.coords[3] - self.coords_lineh2[0][1]
        largeur = min(120, (self.coords[2] - 15*(1+nb_btns)) // nb_btns)
        hauteur = 34

        largeur_zone = self.coords[2] // nb_btns
        y = (self.coords[1] + 
            self.coords[3] - 
            footer_hauteur // 2 - 
            hauteur // 2)

        for num_btn in range(nb_btns):
            x = (self.coords[0] + 
                num_btn * largeur_zone + 
                largeur_zone // 2 -
                largeur // 2)
            coords_btn = (x, y, largeur, hauteur)

            back_color = 3*(160,)
            if type(btn_defs[num_btn]) is str:
                label = btn_defs[num_btn]
                value = label.upper()

            else:
                label = btn_defs[num_btn][0]
                value = label.upper()

                if len(btn_defs[num_btn]) > 1:
                    if type(btn_defs[num_btn][1]) is tuple:
                        back_color = btn_defs[num_btn][1]
                    else:
                        value = btn_defs[num_btn][1]

                if len(btn_defs[num_btn]) > 2:
                    back_color = btn_defs[num_btn][2]

            # fprint("create bouton(", label, value, back_color, ")")
            self.boutons.append(
                Bouton(self.screen, back_color, 
                    coords_btn, 
                    Commande(label, self.click_bouton, value)))

    def click_bouton(self, valeur: Any):
        self.is_open = False
        self.value = valeur

    def open(self):
        self.is_open = True
        self.value = None
        self.mouse_over = False
        self.click_over = False

        [bouton.init() for bouton in self.boutons]

    def close(self):
        self.is_open = False

    def mouse_move(self, position: Tuple):
        if not self.coords.collidepoint(position):
            self.mouse_over = False
            return

        self.mouse_over = True
        for bouton in self.boutons:
            bouton.mouse_move(position)

    def mouse_button_down(self):
        self.click_over = self.mouse_over
        for bouton in self.boutons:
            bouton.mouse_button_down()

    def mouse_button_up(self):
        if not self.click_over and not self.mouse_over:
            self.click_bouton(Action.Close)
            return

        for bouton in self.boutons:
            bouton.mouse_button_up()

    def update(self):
        pass

    def draw(self):
        if not self.is_open:
            return 

        pygame.draw.rect(self.screen, (150, 150, 150), self.coords)
        pygame.draw.rect(self.screen, (240, 240, 240), self.coords_white)

        self.screen.blit(self.text_surface, self.text_coords)

        pygame.draw.line(self.screen, (0, 0, 0), *self.coords_lineh1, 2)
        pygame.draw.line(self.screen, (0, 0, 0), *self.coords_linev1, 2)
        pygame.draw.line(self.screen, 3*(200,), *self.coords_lineh2, 2)
        pygame.draw.line(self.screen, 3*(200,), *self.coords_linev2, 2)

        [bouton.draw() for bouton in self.boutons]


def msgbox_events(msg):

    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                msg.close()

        elif event.type == pygame.KMOD_LGUI:
            msg.mouse_move(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            msg.mouse_button_down()

        elif event.type == pygame.MOUSEBUTTONUP:
            msg.mouse_button_up()

        elif event.type == pygame.QUIT:
            msg.close()

    msg.draw()


def screen_events(msg):

    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                msg.value = Action.Yes

        elif event.type == pygame.QUIT:
            msg.open()
            msg.mouse_move((0, 0))

        elif event.type == pygame.MOUSEBUTTONUP:
            msg.open()
            msg.mouse_move(event.pos)


def main():
    Constante()

    screen = pygame.display.set_mode((800, 600), flags=pygame.SHOWN, vsync=1)
    clock = pygame.time.Clock()
    
    msg = MessageBox(screen, (400, 200), 
        [("Annuler", Action.Cancel), 
        ("Non", Action.No, (200, 100, 100)), 
        ("Oui", Action.Yes, (100, 180, 100))])

    Events: dict = {
        True: (msgbox_events, msg),
        False: (screen_events, msg)
    }

    while msg.value != Action.Yes:
        
        screen.fill((40, 40, 40))
        clock.tick(60)

        fonction, *params = Events[msg.is_open]
        fonction(*params)

        pygame.display.update()

    Constante.close()


if __name__ == '__main__':
    main()
