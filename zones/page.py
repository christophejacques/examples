from __future__ import annotations
from typing import Optional, Self

import pygame


OPTIONS: tuple = (
    "side", "color",
    "x", "y", 
    "relx", "rely", 
    "width", "height", 
    "relwidth", "relheight", 
    "pad", "padx", "pady", 
    "mouse_enter")


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


def zi(nombre) -> int:
    if isinstance(nombre, int):
        return nombre

    return 0


def get_pygame_const_name(index):
    for c in dir(pygame):
        if c[1] in "AZERTYUIOPMLKJHGFDSQWXCVBN":
            if type(getattr(pygame, c)) == int and getattr(pygame, c) == index:
                return c


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


class Page:
    screen: pygame.surface.Surface

    parent: Optional[Pages]
    index: int
    nom: str
    current: Optional[str]
    contenu: list[Pages]
    coords: list

    x: Optional[int]
    y: Optional[int]
    width: Optional[int]
    height: Optional[int]

    mouse_over: bool

    def __init__(self, 
        nom: str, 
        position: str="", 
        coords: list[int]=list(),
        **options): 

        self.current = None
        self.parent = None
        self.nom = nom
        self.position = position.upper()
        self.contenu = list()

        self.init_coords()

        if options.get("root", False):
            self.set_rect([0, 0] + Screen.size)
        else:
            self.set_rect(coords)

        color = options.get("color", False)
        if color:
            self.color = color
        else:
            self.color = (0, 0, 0)

        self.mouse_over = False
        self.options = options

        self.register_methode("mouse_enter")

    def register_methode(self, method_name: str):
        option_methode = self.options.get(method_name)
        if option_methode is None:
            return

        if callable(option_methode):
            setattr(self, method_name, option_methode)
        elif hasattr(self, option_methode):
            setattr(self, method_name, getattr(self, option_methode))
        else:
            raise Exception(f"La methode {option_methode!r} n'existe pas")

    def __str__(self) -> str:
        ctn: str = ""
        for p in self.contenu:
            ctn += ", " + str(p)
        ctn = ctn[2:]
        return f"{self.nom} {self.coords} [{ctn}]"

    def __iter__(self) -> Self:
        self.__index = -1
        return self

    def __next__(self) -> Pages:
        self.__index += 1
        if self.__index >= len(self.contenu):
            raise StopIteration()

        return self.contenu[self.__index]

    def __call__(self, nom_pages: Optional[str] = None) -> Pages:
        return self.get(nom_pages)

    def init_coords(self):
        self.x = None
        self.y = None
        self.width = None
        self.height = None

    def set_rect(self, coords: list[int]) -> None:
        self.coords = coords.copy()
        if coords:
            self.x, self.y, self.width, self.height = self.coords

    def recalc_zones(self, coords: Optional[list]=None):
        if not coords is None:
            self.set_rect(coords)

        for pages in self.contenu:
            for page in pages.liste:
                # on force les valeurs a null pour toutes les recalculer
                page.init_coords()
                new_zone = pages.calc_coords(page)
                new_zone.recalc_zones()

    def create_group(self, nom_pages: str) -> Pages: 
        pages = Pages(nom_pages)
        pages.parent = self

        self.contenu.append(pages)
        self.current = nom_pages

        return pages

    def has_pages(self) -> bool:
        return len(self.contenu) > 0

    def add(self, page: Page, nom_pages: Optional[str]=None) -> Page:
        if nom_pages is None:
            if self.current is None:
                # fprint(f"Add group: {page.nom} -> [{self.nom}]")
                self.create_group(self.nom)

            nom_pages = self.current

        pages: Pages = self.get(nom_pages)
        page.parent = pages
        pages.add(page)

        return page

    def delete(self) -> None:
        if not self.parent:
            return

        pages = self.parent
        trouve: bool = False
        for page in pages.liste:
            if not trouve:
                if self.nom != page.nom:
                    continue

                trouve = True
                pages.liste.remove(page)
                if len(pages.liste) == 0:
                    self.current = ""
                else:
                    self.current = pages.liste[0].nom

            else:
                page.index -= 1
                

    def delete_pages(self, nom_pages: Optional[str]=None) -> None:
        if nom_pages is None:
            self.contenu.clear()
            self.current = None
            return

        for pages in self.contenu:
            if pages.nom == nom_pages:
                self.contenu.remove(pages)

                if self.current == nom_pages:                    
                    if len(self.contenu) == 0:
                        self.current = ""
                    else:
                        self.current = self.contenu[0].nom
                return

    def rename(self, nom_page: str) -> None: 
        self.nom = nom_page

    def get_size(self) -> tuple[int, int]:
        if self.width is None:
            raise Exception("La largeur de la page est indéfinie")

        if self.height is None:
            raise Exception("La hauteur de la page est indéfinie")

        return self.width, self.height

    def get(self, nom_pages: Optional[str] = None) -> Pages:
        if nom_pages is None:
            nom_pages = self.current

        for pages in self.contenu:
            if pages.nom == nom_pages:
                return pages

        raise IndexError(f"Le groupe de pages {nom_pages!r} n'existe pas.")

    def goto_pages(self, nom_pages: str) -> None:
        for pages in self.contenu:
            if nom_pages != pages.nom:
                continue

            self.current = nom_pages
            return

        raise IndexError(f"Le groupe de pages {nom_pages!r} n'existe pas.")

    def goto_previous_pages(self) -> None:
        previous_nom: str = self.contenu[-1].nom

        for pages in self.contenu:
            if self.current == pages.nom:
                self.current = previous_nom
                return

            previous_nom = pages.nom

        fprint(self.nom, f"({self.current})")

    def goto_next_pages(self) -> None:
        trouve: bool = False
        updated: bool = False
        for pages in self.contenu:
            if trouve:
                self.current = pages.nom
                updated = True
                break

            if self.current == pages.nom:
                trouve = True

        if not updated:
            self.current = self.contenu[0].nom

        fprint(self.nom, f"({self.current})")

    def mouse_enter(self):
        # fprint(f"mouse_enter({self.nom})")
        pass

    def print_name(self):
        fprint(f"{self.index}-{self.nom}")

    def mouse_exit(self):
        # fprint(f"mouse_exit({self.nom})")
        pass

    def mouse_button_up(self, mouse_position, mouse_button):
        if mouse_button == 1:
            self.goto_next_pages()
        else:
            self.goto_previous_pages()

        self.check_mouse(mouse_position)
        
    def check_mouse(self, mouse_position):
        mx, my = mouse_position
        zx, zy, zw, zh = self.coords

        if zx <= mx <= zx+zw and zy <= my <= zy+zh:
            if not self.mouse_over:
                self.mouse_over = True
                self.mouse_enter()
        else:
            if self.mouse_over:
                self.mouse_over = False
                self.mouse_exit()

        
        if not self.has_pages():
            return

        for page in list(self.get()):
            page.check_mouse(mouse_position)
    
    def draw(self) -> None:
        if False:
            if self.mouse_over and Variable.is_tick_actif():
                color = (0, 255, 0)
            else:
                color = self.color
            pygame.draw.rect(Page.screen, color, self.coords, 1)

        if self.mouse_over and self.options.get("drawbg", True):
            pygame.draw.rect(Page.screen, self.color, self.coords)
        else:
            pygame.draw.rect(Page.screen, self.color, self.coords, 1)

        if not self.has_pages():
            return

        for page in self.get():
            page.draw()


class Pages:
    parent: Optional[Page]
    nom: str
    current: str
    liste: list[Page]

    def __init__(self, nom: str): 
        self.parent = None
        self.current = ""
        self.nom = nom
        self.liste = list()

    def __iter__(self) -> Self:
        self.__index = -1
        return self

    def __next__(self) -> Page:
        self.__index += 1
        if self.__index >= len(self.liste):
            raise StopIteration()

        return self.liste[self.__index]

        nom = self.liste[self.__index].nom
        page = self.liste[self.__index]

        return nom, page

    def __str__(self) -> str:
        ctn: str = ""
        for p in self.liste:
            ctn += ", " + str(p)
        ctn = ctn[2:]
        return f"{self.nom} ({ctn})"

    def __call__(self, nom_page: Optional[str] = None) -> Page:
        return self.get(nom_page)

    def has_page(self) -> bool:
        return len(self.liste) > 0

    @staticmethod
    def update_size(
        option_str, 
        debut_zone, taille_zone, 
        ref_debut, ref_size, 
        side, direction, 
        options) -> tuple[int, int]:

        if taille_zone is None:
            relwidth = options.get("rel" + option_str, 1)
            taille_zone = int(ref_size * relwidth)

            if debut_zone is None:
                if side == direction:
                    debut_zone = ref_debut + ref_size - taille_zone
                else:
                    debut_zone = ref_debut
                
        return debut_zone, taille_zone

    @staticmethod
    def update_to_end(option_str, debut_zone, taille_zone, ref_debut, ref_size, options) -> int:

        endsize = options.get("end" + option_str, False)
        if endsize:
            fprint("\n=>", debut_zone, taille_zone, ref_debut, ref_size)
            taille_zone = ref_size - (debut_zone - ref_debut)
            fprint("=>", debut_zone, taille_zone, ref_debut, ref_size)
                
        return taille_zone

    @staticmethod
    def update_padding(
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

    def calc_coords(self, page: Page) -> Page:

        update_options: Optional[dict] = None
        side: str
        pcoords: list[int]

        if self.parent:
            pcoords = self.parent.coords
        else:
            pcoords = [0, 0, 0, 0]

        px, py, pwidth, pheight = pcoords
        side = page.position
        fprint(side, page.options, pcoords, end= "")

        for option in page.options:
            match option:
                case "pad":
                    if page.options.get("padx") is not None:
                        raise Exception("Option 'pad' incompatible avec 'padx'")

                    if page.options.get("pady") is not None:
                        raise Exception("Option 'pad' incompatible avec 'pady'")

                    valeur = page.options.get(option, 0)
                    if isinstance(valeur, tuple):
                        pad = valeur
                    else:
                        pad = (valeur, valeur)

                    update_options = {
                        "padx": pad,
                        "pady": pad}

                case "x":
                    if page.options.get("relx") is not None:
                        raise Exception("Option 'x' incompatible avec 'relx'")
                    elif side in ("LEFTTO", "RIGHTTO"):
                        raise Exception(f"Option 'x' incompatible avec {side!r}")

                    if side == "RIGHT":
                        page.x = px + pwidth - page.options.get(option, 0)
                    else:
                        page.x = px + page.options.get(option, 0)

                case "relx":
                    if page.options.get("x") is not None:
                        raise Exception("Option 'relx' incompatible avec 'x'")
                    elif side in ("LEFTTO", "RIGHTTO"):
                        raise Exception(f"Option 'relx' incompatible avec {side!r}")

                    relx = page.options.get(option, 0)
                    if side == "RIGHT":
                        page.x = px + int(pwidth * (1-relx))
                    else:
                        page.x = px + int(pwidth * relx)

                case "y":
                    if page.options.get("rely") is not None:
                        raise Exception("Option 'y' incompatible avec 'rely'")
                    elif side in ("UNDER", "OVER"):
                        raise Exception(f"Option 'y' incompatible avec {side!r}")

                    if side == "BOTTOM":
                        page.y = py + pheight - page.options.get(option, 0)
                    else:
                        page.y = py + page.options.get(option, 0)

                case "rely":
                    if page.options.get("y") is not None:
                        raise Exception("Option 'rely' incompatible avec 'y'")
                    elif side in ("UNDER", "OVER"):
                        raise Exception(f"Option 'rely' incompatible avec {side!r}")

                    rely = page.options.get(option, 0)
                    if side == "BOTTOM":
                        page.y = py + int(pheight * (1-rely))
                    else:
                        page.y = py + int(pheight * rely)

                case "width":
                    if page.options.get("relwidth") is not None:
                        raise Exception("Option 'width' incompatible avec 'relwidth'")

                    page.width = page.options[option]

                case "height":
                    if page.options.get("relheight") is not None:
                        raise Exception("Option 'height' incompatible avec 'relheight'")

                    page.height = page.options.get(option, 0)

                case default:
                    pass

        if update_options:
            page.options.pop("pad")
            page.options.update(update_options)

        page.x, page.width = self.update_size("width", 
            page.x, page.width, px, pwidth, 
            side, "RIGHT", page.options)

        page.y, page.height = self.update_size("height", 
            page.y, page.height, py, pheight, 
            side, "BOTTOM", page.options)

        match side:
            case "UNDER":
                page.y = zi(self.liste[page.index-2].y) + zi(self.liste[page.index-2].height) + \
                    self.liste[page.index-2].options.get("pady",(0, 0))[1]

            case "OVER":
                page.y = zi(self.liste[page.index-2].y) - page.height - \
                    self.liste[page.index-2].options.get("pady",(0, 0))[0]

            case "RIGHTTO":
                page.x = zi(self.liste[page.index-2].x) + zi(self.liste[page.index-2].width) + \
                    self.liste[page.index-2].options.get("padx",(0, 0))[1]

            case "LEFTTO":
                page.x = zi(self.liste[page.index-2].x) - page.width - \
                    self.liste[page.index-2].options.get("padx",(0, 0))[0]

        page.width = self.update_to_end("width", page.x, page.width, px, pwidth, page.options)
        page.height = self.update_to_end("height", page.y, page.height, py, pheight, page.options)

        page.x, page.width = self.update_padding( "padx", 
            page.x, page.width, side, "RIGHT",
            pwidth, px, page.options)

        page.y, page.height = self.update_padding( "pady", 
            page.y, page.height, side, "BOTTOM",
            pheight, py, page.options)

        page.coords = [page.x, page.y, page.width, page.height]

        fprint("=> Result:", page.coords)
        return page

    def add(self, page: Page) -> None: 
        page.parent = self
        self.liste.append(page)
        self.current = page.nom
        page.index = len(self.liste)

        # calcul les coordonnees a partir des options
        zone_calculee = self.calc_coords(page)

    def get(self, nom_page: Optional[str] = None) -> Page:
        if nom_page is None:
            nom_page = self.current

        for page in self.liste:
            if page.nom == nom_page:
                return page

        raise Exception(f"La page {nom_page!r} n'existe pas.")

    def delete(self, nom_pages: str) -> bool:
        for page in self.liste:
            if page.nom == nom_pages:
                self.liste.remove(page)
                if self.current == nom_pages:                    
                    if len(self.liste) == 0:
                        self.current = ""
                    else:
                        self.current = self.liste[0].nom

                return True

        return False


class Ecrans:
    ecrans: list[Page] = list()
    total: int = 0
    index: int = -1

    @classmethod
    def resize(cls, size: list[int]):
        # fprint("---------------")
        Screen.size = size
        for page in cls.ecrans:
            page.recalc_zones([0, 0, *size])

    @classmethod
    def add_ecran(cls, ecran: Page):
        cls.ecrans.append(ecran)
        cls.total += 1

    @classmethod
    def previous_ecran(cls):
        cls.index -= 1
        if cls.index < 0:
            cls.index = cls.total - 1

        return cls.ecrans[cls.index]

    @classmethod
    def next_ecran(cls):
        cls.index += 1
        if cls.index >= cls.total:
            cls.index = 0

        return cls.ecrans[cls.index]


def initialize_test():
    dx = 2
    page = Page("root", "ROOT", color=(0, 250, 250), root=True, drawbg=False)
    menu = page.add(Page("Menu", "TOP", color=(150, 50, 0), height=30, pad=2, drawbg=False))

    # menu.add(Page("File", "LEFT", color=(50, 250, 0), width=80, padx=(dx,0), 
    #     mouse_enter="print_name"))
    # menu.add(Page("Edit", "RIGHTTO", color=(50, 50, 0), width=80, padx=(dx,0), 
    #     mouse_enter="print_name"))
    # menu.add(Page("Selection", "RIGHTTO", color=(250, 50, 0), relwidth=0.05, padx=(dx,0), 
    #     mouse_enter="print_name"))
    # menu.add(Page("Find", "RIGHTTO", color=(150, 150, 250), width=80, padx=(dx,0), mouse_enter="print_name"))
    # menu.add(Page("View", "RIGHTTO", color=(50, 150, 0), width=80, padx=(dx,0), mouse_enter="print_name"))
    # menu.add(Page("Goto", "RIGHTTO", color=(50, 250, 0), width=80, padx=(dx,0), mouse_enter="print_name"))
    # menu.add(Page("Tools", "RIGHTTO", color=(50, 150, 0), width=80, padx=(dx,0), mouse_enter="print_name"))
    # menu.add(Page("Project", "RIGHTTO", color=(50, 250, 0), width=80, padx=(dx,0), 
    #     mouse_enter="print_name"))
    # menu.add(Page("Preferences", "RIGHTTO", color=(50, 150, 0), width=100, padx=(dx,0), 
    #     mouse_enter="print_name"))
    # menu.add(Page("Help", "RIGHTTO", color=(50, 250, 0), width=80, padx=(dx,0), mouse_enter="print_name"))

    content = page.add(Page("Contenu", "UNDER", color=(150, 50, 0), 
        drawbg=False, endheight=True))
    content.add(Page("Left1", "LEFT", color=(150, 150, 0), width=100, pad=10))
    content.add(Page("Left2", "RIGHTTO", color=(150, 150, 0), width=200, pady=10))
    content.add(Page("Left3", "RIGHTTO", color=(150, 150, 0), endwidth=True, pad=10))

    Ecrans.add_ecran(page)
    return

    page = Page("root", "ROOT", color=(0, 250, 250), root=True, drawbg=False)
    menu = page.add(Page("Menu", "TOP", color=(150, 50, 0), height=30, pad=2, drawbg=False))

    menu.add(Page("File", "RIGHT", color=(50, 250, 0), width=80, padx=(dx,0), 
        mouse_enter="print_name"))
    menu.add(Page("Edit", "LEFTTO", color=(50, 50, 0), width=80, padx=(dx,0), 
        mouse_enter="print_name"))
    menu.add(Page("Selection", "LEFTTO", color=(250, 50, 0), relwidth=0.05, padx=(dx,0), 
        mouse_enter="print_name"))
    menu.add(Page("Find", "LEFTTO", color=(150, 150, 250), width=80, padx=(dx,0), mouse_enter="print_name"))
    menu.add(Page("View", "LEFTTO", color=(50, 150, 0), width=80, padx=(dx,0), mouse_enter="print_name"))
    menu.add(Page("Goto", "LEFTTO", color=(50, 250, 0), width=80, padx=(dx,0), mouse_enter="print_name"))
    menu.add(Page("Tools", "LEFTTO", color=(50, 150, 0), width=80, padx=(dx,0), mouse_enter="print_name"))
    menu.add(Page("Project", "LEFTTO", color=(50, 250, 0), width=80, padx=(dx,0), 
        mouse_enter="print_name"))
    menu.add(Page("Preferences", "LEFTTO", color=(50, 150, 0), width=100, padx=(dx,0), 
        mouse_enter="print_name"))
    menu.add(Page("Help", "LEFTTO", color=(50, 250, 0), width=80, padx=(dx,0), mouse_enter="print_name"))

    content = page.add(Page("Contenu", "UNDER", color=(150, 50, 0), 
        relheight=0.8, drawbg=False, endheight=True))
    content.add(Page("Left1", "RIGHT", color=(150, 150, 0), width=100, pad=15))
    content.add(Page("Left2", "LEFTTO", color=(150, 150, 0), width=200, pady=15))

    Ecrans.add_ecran(page)

    page = Page("root", "ROOT", color=(0, 250, 250), root=True, drawbg=False)
    page.add(Page("Line1", "TOP", color=(150, 150, 0), height=100, pad=15))
    page.add(Page("Line2", "UNDER", color=(150, 150, 0), padx=15, pady=(0, 15), endheight=True))

    Ecrans.add_ecran(page)

    page = Page("root", "ROOT", color=(0, 250, 250), root=True, drawbg=False)
    page.add(Page("Line1", "BOTTOM", color=(150, 150, 0), height=100, pad=15))
    page.add(Page("Line2", "OVER", color=(150, 150, 0), height=200, padx=15))

    Ecrans.add_ecran(page)
    # Ecrans.index = 1


def initialize():
    # Page 1
    page = Page("root", "ROOT", color=(0, 250, 250), root=True)
    page.create_group("accueil")
    page.add(Page("Accueil", "FULL", color=(150, 150, 0), pad=15))

    page.create_group("informations")
    page.add(Page("Informations", "FULL", color=(50, 100, 200), pad=25))

    page.create_group("credits")
    page.add(Page("Credits", "FULL", color=(50, 200, 100), pad=35))

    page.create_group("route")
    page.add(Page("Fin", "FULL", color=(200, 100, 40), pad=45))

    page.create_group("about")
    page.add(Page("Fin", "FULL", color=(200, 100, 40), pad=65))

    page.create_group("fin")
    page.add(Page("Fin", "FULL", color=(200, 100, 40), pad=85))

    page.goto_pages("accueil")
    Ecrans.add_ecran(page)

    # Page 2
    page = Page("root", "ROOT", color=(0, 250, 250), root=True)
    page.create_group("main")

    # Top
    top = page.add(Page("Top", "TOP", color=(150, 150, 0), padx=15, pady=(15, 10), relheight=0.25))
    top.add(Page("Left", "LEFT", color=(150, 150, 0), padx=(5, 3), pady=5, relwidth=0.25))
    top.add(Page("right", "LEFT", color=(150, 150, 0), padx=(3, 23), pady=5, relx=0.25, relwidth=0.75))
    top.add(Page("Ascenseur", "RIGHT", color=(20, 150, 100), padx=(0, 3), pady=5, x=20, width=20))

    # Middle
    middle = page.add(Page("Middle", "TOP", color=(150, 150, 0), 
        padx=15, pady=(0, 50), rely=0.25, relheight=0.75))

    # Bottom
    bottom = page.add(Page("Bottom", "BOTTOM", color=(50, 50, 50), pad=15, height=55, relwidth=1))
    bottom.add(Page("Gauche", "", color=(20, 200, 200), relwidth=1/3, padx=(0, 5)))
    bottom.add(Page("Milieu", "", color=(20, 200, 200), relx=1/3, relwidth=1/3))
    bottom.add(Page("Droite", "RIGHT", color=(20, 200, 200), relwidth=1/3, padx=(5, 0)))
    Ecrans.add_ecran(page)

    # Page 3
    page = Page("root", "ROOT", color=(0, 250, 250), root=True)
    page.create_group("boite_outil")
    page.add(Page("Gauche", "", color=(50, 20, 200), relwidth=0.25, padx=(15,0), pady=15))
    page.add(Page("Droite", "RIGHT", color=(50, 50, 250), relwidth=0.75, pad=15))

    page.create_group("detail")
    page.add(Page("35w", "", color=(50, 20, 250), width=35, padx=(15,0), pady=15))
    page.add(Page("50p", "", color=(50, 50, 250), padx=(50, 15), pady=15))

    page.goto_pages("boite_outil")
    Ecrans.add_ecran(page)

    # Page 4
    page = Page("root", "ROOT", color=(0, 250, 250), root=True)
    page.create_group("boite_outil2")
    page.add(Page("75w", "", color=(50, 20, 250), relwidth=0.75, padx=(15,0), pady=15))
    page.add(Page("75p", "RIGHT", color=(50, 50, 250), relwidth=0.25, pad=15))

    page.create_group("detail2")
    page.add(Page("75w", "", color=(50, 20, 250), padx=(15,50), pady=15))
    page.add(Page("75p", "RIGHT", color=(50, 50, 250), width=35, padx=(15, 0), pady=15))

    page.goto_pages("boite_outil2")
    Ecrans.add_ecran(page)


def main():
    # initialize()
    initialize_test()

    page: Page = Ecrans.next_ecran()
    mouse_position_save: tuple[int, int] = (-1, -1)

    Page.screen: pygame.surface.Surface = pygame.display.set_mode(
        page.get_size(), 
        pygame.RESIZABLE, 
        24)
    clock: pygame.time.Clock = pygame.time.Clock()

    running: bool = True
    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.KEYUP:
                    if event.key in (pygame.K_ESCAPE, ):
                        running = False

                    elif event.key in (pygame.K_PAGEDOWN, ):
                        page.goto_next_pages()

                    elif event.key in (pygame.K_PAGEUP, ):
                        page.goto_previous_pages()

                    elif event.key in (pygame.K_BACKSPACE, ):
                        page = Ecrans.previous_ecran()
                        page.check_mouse(mouse_position_save)

                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        page = Ecrans.next_ecran()
                        page.check_mouse(mouse_position_save)
                        
                case pygame.WINDOWENTER:
                    # fprint("Window Enter")
                    pass
                
                case pygame.KMOD_LGUI:
                    page.check_mouse(event.pos)
                    mouse_position_save = event.pos

                case pygame.ACTIVEEVENT:
                    if event.gain == 0:
                        # Souris sort de la fenetre
                        mouse_position_save = (-1, -1)
                        page.check_mouse(mouse_position_save)
                
                case pygame.MOUSEWHEEL:
                    pass

                case pygame.MOUSEBUTTONDOWN:
                    pass

                case pygame.MOUSEBUTTONUP:
                    match event.button:
                        case 1 | 3:
                            page.mouse_button_up(event.pos, event.button)
                        case 5:
                            page = Ecrans.next_ecran()
                            page.check_mouse(mouse_position_save)
                        case 4:
                            page = Ecrans.previous_ecran()
                            page.check_mouse(mouse_position_save)

                case pygame.VIDEORESIZE:
                    Ecrans.resize([event.w, event.h])

                case pygame.QUIT:
                    running = False

                case default:
                    pass
                    # fprint("event:", get_pygame_const_name(default))


        Page.screen.fill(0)
        page.draw()
        pygame.display.update()

        clock.tick(60)
        Variable.update_tick()


if __name__ == "__main__":
    pygame.init()
    try:
        main()
    finally:
        pygame.quit()
        fprint("Fin")

