import pygame  # noqa: E402

from typing import List, Tuple, Optional, Dict
from textes import Lien
from functools import partial

from general import pygame, Variable, fprint
from outils import Icone


class Headers:

    surface: pygame.surface.Surface
    x: int
    y: int
    w: int
    h: int
    visible: bool
    liens: List[Lien]

    mouse_over: bool
    is_mouse_button_down: bool

    icones: List[Icone]

    def __init__(self, screen: pygame.surface.Surface, coords: Tuple):
        self.coords = pygame.Rect(coords)
        self.icones = list()
        self.liens = list()

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

            self.redraw()

    def add_icone(self, coords: Tuple):
        # (40, 30, 0) - (25, 70, 40)
        colors: Dict = {
            "BACK": (40, 30, 0),
            "AROUND": (50, 200, 150),
            "OVER": (30, 80, 50)
        }
        icone = Icone(self.surface, colors, coords)
        self.icones.append(icone)

    @property
    def icone(self):
        for icone in self.icones:
            return icone

        raise Exception("Aucun icone de défini.")

    def mouse_move(self, position: Tuple):
        self.mouse_over = True

        if not self.icone.rect.collidepoint(position):
            if self.icone.is_mouse_over:
                self.icone.mouse_exit()
            return

        self.icone.mouse_move(position)

    def mouse_exit(self):
        self.is_mouse_button_down = False
        if self.mouse_over:
            self.mouse_over = False

        if self.icone.is_mouse_over:
            self.icone.mouse_exit()            

    def mouse_button_down(self, *args):
        self.is_mouse_button_down = self.mouse_over
        self.icone.mouse_button_down()

    def mouse_button_up(self, *args):
        self.is_mouse_button_down = False
        self.icone.mouse_button_up()
        self.icone.check()

    def redraw(self):
        self.surface.fill((40, 30, 0))

        # header
        self.surface.blits([lien.to_draw() for lien in self.liens])
        pygame.draw.line(self.surface, (50, 200, 150), (0, self.h), (self.w, self.h))

        for icone in self.icones:
            icone.redraw()

    def draw(self) -> None:
        pass
