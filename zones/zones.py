from __future__ import annotations
from typing import Optional

import pygame


OPTIONS: tuple = (
    "side", "color",
    "x", "y", 
    "relx", "rely", 
    "width", "height", 
    "relwidth", "relheight", 
    "pad", "padx", "pady")


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


class Screen:
    size: list[int] = [1200, 600]


class Variable:
    TICK: int = 0

    @classmethod
    def update_tick(cls):
        if cls.TICK > 30:
            cls.TICK = 0
        else:
            cls.TICK += 1

    @classmethod
    def is_tick_actif(cls):
        return cls.TICK <= 15    


class Zone:
    parent: Optional[Zone]

    color: Optional[tuple]

    coords: list[int]
    contenu: list[Zone]

    x: Optional[int]
    y: Optional[int]
    width: Optional[int]
    height: Optional[int]

    mouse_over: bool

    def __init__(self, 
        position: str="", 
        **options):

        for option in options:
            if option not in OPTIONS:
                raise TypeError(f"'{option}' est un argument keyword invalide pour {self.__class__.__name__}()")

        self.parent = None
        self.contenu = list()

        self.color = options.get("color", (255, 255, 255))

        self.x = None
        self.y = None
        self.width = None
        self.height = None

        self.position = position.upper()
        self.options = options

        self.mouse_over = False

        # Mettre en place calcul de la zone
        if self.position == "ROOT":
            self.set_rect([0, 0] + Screen.size)

    def __str__(self):
        res: str = ""
        if self.contenu:
            res = "["
            for zone in self.contenu:
                res += f"{zone},"

            res = res[:-1]
            res += "]"

        return f"{self.position} {self.coords}" + res

    def set_rect(self, coords: list[int]):
        self.coords = coords.copy()
        self.x, self.y, self.width, self.height = self.coords

    def get_rect(self) -> tuple[int, int, int, int]:
        if self.parent is None:
            return (
                self.coords[0], 
                self.coords[1], 
                self.coords[2], 
                self.coords[3])

        return (
            self.coords[0] + self.parent.get_rect()[0], 
            self.coords[1] + self.parent.get_rect()[1], 
            self.coords[2], 
            self.coords[3])

    def get_size(self) -> tuple[int, int]:
        return self.coords[2], self.coords[3]

    def set_width(self, width: int):
        self.width = width
        self.coords[2] = width

    def calc_coords(self, zone: Zone) -> Zone:

        update_options: Optional[dict] = None
        side: str

        # fprint(zone.options)
        side = zone.options.get("side", "").upper()

        for option in zone.options:
            match option:
                case "pad":
                    if zone.options.get("padx") is not None:
                        raise Exception("Option 'pad' incompatible avec 'padx'")

                    if zone.options.get("pady") is not None:
                        raise Exception("Option 'pad' incompatible avec 'pady'")

                    valeur = zone.options.get(option, 0)
                    if isinstance(valeur, tuple):
                        pad = valeur
                    else:
                        pad = (valeur, valeur)

                    update_options = {
                        "padx": pad,
                        "pady": pad}

                case "x":
                    if zone.options.get("relx") is not None:
                        raise Exception("Option 'x' incompatible avec 'relx'")

                    if side == "RIGHT":
                        zone.x = self.coords[2] - zone.options.get(option, 0)
                    else:
                        zone.x = zone.options.get(option, 0)

                case "relx":
                    if zone.options.get("x") is not None:
                        raise Exception("Option 'relx' incompatible avec 'x'")

                    relx = zone.options.get(option, 0)
                    if side == "RIGHT":
                        zone.x = int(self.coords[2] * (1-relx))
                    else:
                        zone.x = int(self.coords[2] * relx)

                case "y":
                    if zone.options.get("rely") is not None:
                        raise Exception("Option 'y' incompatible avec 'rely'")

                    if side == "RIGHT":
                        zone.y = self.coords[3] - zone.options.get(option, 0)
                    else:
                        zone.y = zone.options.get(option, 0)

                case "rely":
                    if zone.options.get("y") is not None:
                        raise Exception("Option 'rely' incompatible avec 'y'")

                    rely = zone.options.get(option, 0)
                    if side == "BOTTOM":
                        zone.y = int(self.coords[3] * (1-rely))
                    else:
                        zone.y = int(self.coords[3] * rely)

                case "width":
                    if zone.options.get("relwidth") is not None:
                        raise Exception("Option 'width' incompatible avec 'relwidth'")

                    zone.width = zone.options[option]

                case "height":
                    if zone.options.get("relheight") is not None:
                        raise Exception("Option 'height' incompatible avec 'relheight'")

                    zone.height = zone.options.get(option, 0)

                case default:
                    pass

        if update_options:
            zone.options.pop("pad")
            zone.options.update(update_options)

        zone.x, zone.width = self.update_size("relwidth", 
            zone.x, zone.width, self.width, 
            side, "RIGHT", zone.options)

        zone.y, zone.height = self.update_size("relheight", 
            zone.y, zone.height, self.height, 
            side, "BOTTOM", zone.options)

        zone.x, zone.width = self.update_padding( "padx", 
            zone.x, zone.width, side, "RIGHT",
            self.width, self.x, zone.options)

        zone.y, zone.height = self.update_padding( "pady", 
            zone.y, zone.height, side, "BOTTOM",
            self.height, self.y, zone.options)

        zone.coords = [zone.x, zone.y, zone.width, zone.height]

        return zone

    @classmethod
    def update_size(cls, 
        option_str, 
        debut_zone, taille_zone, 
        ref_size, 
        side, direction, 
        options) -> tuple[int, int]:

        if taille_zone is None:
            relwidth = options.get(option_str, 1)
            taille_zone = int(ref_size * relwidth)

            if debut_zone is None:
                if side == direction:
                    debut_zone = ref_size - taille_zone
                else:
                    debut_zone = 0

        return debut_zone, taille_zone

    @classmethod
    def update_padding(cls, 
        pad_str, 
        debut_zone, taille_zone, 
        side, direction, 
        ref_size, ref_debut, 
        options) -> tuple[int, int]:

        padding: tuple[int, int]

        valeur = options.get(pad_str, 0)
        if isinstance(valeur, tuple):
            padding = valeur
        else:
            padding = (valeur, valeur)

        if debut_zone is None:
            if side == direction:
                debut_zone = ref_size - ref_debut - taille_zone + padding[1]
            else:
                debut_zone = ref_debut + padding[0]
        else:
            debut_zone += padding[0]

        taille_zone -= sum(padding)

        return debut_zone, taille_zone


    def add(self, zone: Zone) -> Zone:
        zone.parent = self
        zone.color = zone.options.get("color", self.color)

        # calcul les coordonnees a partir des options
        zone_calculee = self.calc_coords(zone)
        self.contenu.append(zone_calculee)

        return zone_calculee

    def recalc_zones(self, coords: Optional[list]=None):
        if not coords is None:
            self.coords = coords

        for zone in self.contenu:
            # on force les valeurs a null pour toutes les recalculer
            zone.x = None
            zone.y = None
            zone.width = None
            zone.height = None

            new_zone = self.calc_coords(zone)
            new_zone.recalc_zones()

    def mouse_enter(self):
        # fprint("mouse_enter")
        pass

    def mouse_exit(self):
        # fprint("mouse_exit")
        pass

    def check_mouse(self, mouse_position):
        mx, my = mouse_position
        zx, zy, zw, zh = self.get_rect()

        if zx <= mx <= zx+zw and zy <= my <= zy+zh:
            if not self.mouse_over:
                self.mouse_over = True
                self.mouse_enter()
        else:
            if self.mouse_over:
                self.mouse_over = False
                self.mouse_exit()

        for zone in self.contenu:
            zone.check_mouse(mouse_position)


    def draw(self, screen):
        color = (255, 250, 250
            ) if self.parent and self.mouse_over and Variable.is_tick_actif() else self.color
        pygame.draw.rect(screen, color, self.get_rect(), 1)
        for zone in self.contenu:
            zone.draw(screen)


def main():

    root = Zone("root", color=(0, 250, 250))
    fprint(0, root)

    top = root.add(Zone(color=(150, 150, 0), side="top", padx=15, pady=(15, 10), relheight=0.25))
    top.add(Zone(side="left", padx=(5, 3), pady=5, relwidth=0.25))
    top.add(Zone(side="left", padx=(3, 22), pady=5, relx=0.25, relwidth=0.75))
    # Ascenseur
    top.add(Zone(color=(20, 150, 100), side="right", padx=(0, 3), pady=5, x=20, width=20))
    fprint(1, root)

    middle = root.add(Zone(color=(150, 150, 0), side="top", 
        padx=15, pady=(0, 50), rely=0.25, relheight=0.75))
    fprint(2, root)

    bottom = root.add(Zone(color=(50, 50, 50), side="BOTTOM", pad=15, height=55, relwidth=1))
    bottom.add(Zone(color=(20, 200, 200), relwidth=1/3, padx=(0, 5)))
    bottom.add(Zone(color=(20, 200, 200), relx=1/3, relwidth=1/3))
    bottom.add(Zone(color=(20, 200, 200), side="RIGHT", relwidth=1/3, padx=(5, 0)))
    # fprint(3, root)

    screen = pygame.display.set_mode(root.get_size(), pygame.RESIZABLE, 24)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.KEYUP:
                    running = not event.key == 27

                case pygame.KMOD_LGUI:
                    root.check_mouse(event.pos)

                case pygame.QUIT:
                    running = False

                case pygame.VIDEORESIZE:
                    root.recalc_zones([0, 0, event.w, event.h])

                case default:
                    pass
                    # fprint("event:", default)


        root.draw(screen)
        pygame.display.update()

        clock.tick(60)
        Variable.update_tick()



if __name__ == "__main__":
    pygame.init()
    try:
        main()
    finally:
        pygame.quit()

