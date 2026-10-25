import pygame  # noqa: E402

from general import Variable
from typing import List, Tuple, Optional, Dict
from textes import Lien
from functools import partial


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

            lien1 = Lien(Variable.SysFont3, key,
                position, 7, partial(self.get_color, 1), None)
            self.liens.append(lien1)

            largeur = lien1.w
            lien2 = Lien(Variable.SysFont4, lib,
                position+largeur, 3, partial(self.get_color, 2), None,
                id=ident)
            self.liens.append(lien2)

    def draw(self) -> None:
        self.surface.fill((40, 30, 0))

        # header
        self.surface.blits([lien.to_draw() for lien in self.liens])
        pygame.draw.line(self.surface, (50, 200, 150), (0, self.h), (self.w, self.h))
