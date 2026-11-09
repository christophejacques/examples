import pygame  # noqa: E402

from general import Variable
from typing import List, Tuple, Optional, Dict
from textes import Lien, LienToggle
from functools import partial


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
                lien = LienToggle(Variable.SysFont3, key, position, 8, None, 
                    callback, id=ident)
                first = False
                lien.selected = True
            else:
                lien = Lien(Variable.SysFont3, key, position, 8, None, 
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
