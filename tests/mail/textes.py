import pygame  # noqa: E402

from typing import Callable, Tuple, Optional


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
