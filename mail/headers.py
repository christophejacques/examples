from typing import List, Tuple, Optional, Dict
from textes import Lien
from functools import partial

from general import pygame, Variable, fprint
from outils import Icone, Triangle, Proprietes


class Headers:

    surface: pygame.surface.Surface
    x: int
    y: int
    w: int
    h: int
    visible: bool
    liens: List[Lien]

    actions: Optional[str]

    mouse_over: bool
    is_mouse_button_down: bool

    icones: List[Icone]

    def __init__(self, screen: pygame.surface.Surface, coords: Tuple):
        self.coords = pygame.Rect(coords)
        self.icones = list()
        self.liens = list()
        self.actions = None

        self.update_screen(screen, coords)
        self.mouse_over = False
        self.is_mouse_button_down = False

    def update_screen(self, 
            screen: pygame.surface.Surface, coords: Optional[Tuple] = None) -> None:

        if coords is not None:
            self.coords = pygame.Rect(coords)

        self.surface = screen.subsurface(self.coords)
        self.x, self.y, self.w, h = self.coords
        self.h = h - 1

        for icone in self.icones:
            icone.update_screen(self.surface)

        self.redraw()

    def get_actions(self) -> Optional[str]:
        if self.actions is None:
            return None

        actions = self.actions
        self.actions = None
        return actions

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
            ident, lib, position, *args = values
            if args:
                # fprint(ident, lib, position, args)
                complement = args[0]
            else:
                complement = 0

            lien1 = Lien(Variable.SysFont3, key,
                position, 7, partial(self.get_color, 1), None)
            self.liens.append(lien1)

            largeur = lien1.w
            lien2 = Lien(Variable.SysFont4, lib,
                position+largeur+complement, 3, partial(self.get_color, 2), None,
                id=ident)
            self.liens.append(lien2)

        # (40, 30, 0) - (25, 70, 40)
        colors: Dict = {
            "BACK": (40, 30, 0),
            "AROUND": (50, 200, 150),
            "OVER": (30, 80, 50)
        }
        self.add_icone(Triangle("LIST", self.surface, colors, (84, 5, 20, 20)))
        self.add_icone(Proprietes("PROP", self.surface, colors, (0, 5, 20, 20),
            formula_x="self.surface.get_width() - 30",
            on_click=self.ask_for_quit))

        self.redraw()

    def ask_for_quit(self):
        self.actions = "QUIT"

    def get_icone_by_id(self, identifiant: str):
        for icone in self.icones:
            if icone.identifiant == identifiant:
                return icone

        raise Exception("Identifiant {identifiant!r} inconnu.")

    def add_icone(self, icone: Icone):
        self.icones.append(icone)

    def mouse_move(self, position: Tuple):
        self.mouse_over = True

        for icone in self.icones:
            if icone.rect.collidepoint(position):
                icone.mouse_move(position)
            elif icone.is_mouse_over:
                icone.mouse_exit()

    def mouse_exit(self):
        self.is_mouse_button_down = False
        if self.mouse_over:
            self.mouse_over = False

        for icone in self.icones:
            if icone.is_mouse_over:
                icone.mouse_exit()            

    def mouse_button_down(self, *args):
        self.is_mouse_button_down = self.mouse_over
        for icone in self.icones:
            icone.mouse_button_down()

    def mouse_button_up(self, *args):
        self.is_mouse_button_down = False
        for icone in self.icones:
            icone.mouse_button_up()
            icone.check()

    def check(self):
        for icone in self.icones:
            icone.check()

    def redraw(self):
        self.surface.fill((40, 30, 0))

        # header
        self.surface.blits([lien.to_draw() for lien in self.liens])
        pygame.draw.line(self.surface, (50, 200, 150), (0, self.h), (self.w, self.h))

        for icone in self.icones:
            icone.redraw()

    def draw(self) -> None:
        pass
