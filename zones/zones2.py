from __future__ import annotations
from typing import Optional, Self

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


class Page:
    parent: Optional[Pages]
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
        self.position = position
        self.contenu = list()

        if options.get("root", False):
            self.set_rect([0, 0] + Screen.size)
        else:
            self.set_rect(coords)

        self.mouse_over = False
        self.options = options

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

    def set_rect(self, coords: list[int]) -> None:
        self.coords = coords.copy()
        if coords:
            self.x, self.y, self.width, self.height = self.coords

    def create_group(self, nom_pages: str) -> Pages: 
        pages = Pages(nom_pages)
        pages.parent = self

        self.contenu.append(pages)
        self.current = nom_pages

        return pages

    def has_pages(self) -> bool:
        return len(self.contenu) > 0

    def add(self, page: Page, nom_pages: Optional[str]=None) -> None:
        if nom_pages is None:
            nom_pages = self.current

        pages: Pages = self.get(nom_pages)
        page.parent = pages
        pages.add(page)

    def delete(self) -> None:
        if not self.parent:
            return

        pages = self.parent
        for page in pages.liste:
            if self.nom != page.nom:
                continue

            pages.liste.remove(page)
            if len(pages.liste) == 0:
                self.current = ""
            else:
                self.current = pages.liste[0].nom
            break

    def delete_pages(self, nom_pages: str) -> None:
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

    def get(self, nom_pages: Optional[str] = None) -> Pages:
        if nom_pages is None:
            nom_pages = self.current

        for pages in self.contenu:
            if pages.nom == nom_pages:
                return pages

        raise Exception(f"Le groupe de pages {nom_pages!r} n'existe pas.")

    def activate_pages(self, nom_pages: str) -> Pages:
        for pages in self.contenu:
            if pages.nom == nom_pages:
                self.current = pages.nom
                return pages

        raise IndexError(f"Le groupe de pages {nom_pages!r} n'existe pas.")

    def goto_previous_pages(self) -> None:
        previous_nom: str = self.contenu[-1].nom

        for pages in self.contenu:
            if self.current == pages.nom:
                self.current = previous_nom
                return

            previous_nom = pages.nom

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

    def draw(self) -> None:
        if len(self.contenu) > 0:
            print(self.nom, self.get())
        else:
            print(self)


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

    def add(self, page: Page) -> None: 
        page.parent = self
        self.liste.append(page)
        self.current = page.nom
        if self.parent is None:
            return

        fprint("calcul coords", self.parent.coords, page.options)
        if page.position == "Gauche":
            page.set_rect(self.parent.coords[:2])

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

    def draw(self) -> None:
        for page in self.liste:
            page.draw()


pr = Page("root", root=True)
# print(pr)

h = pr.create_group("Horizontal")
h.add(Page("Gauche", pad=(15, 0)))
h.add(Page("Droite", pad=(0, 15)))
# h.add(Page("Right", pad=(0, 15)))
# h.delete("Right")

# for pages in pr:
#     for page in pages:
#         print(pages.nom, page)

# pr.create_group("Vertical")
# pr.add(Page("Haut"))
# pr.add(Page("Bas"))
# print(pr)

# unique = pr.create_group("Unique")
# pr.add(Page("Centre"))
# unique.add(Page("Cotés"))
# print(pr)

# pr.delete_pages("Vertical")
print(pr)


exit()


class Zone:
    nom: str

    parent: Optional[Zone]
    pages: Pages

    color: Optional[tuple]

    coords: list[int]

    x: Optional[int]
    y: Optional[int]
    width: Optional[int]
    height: Optional[int]

    mouse_over: bool

    def __init__(self, 
        nom: str = "",
        position: str = "", 
        **options):

        for option in options:
            if option not in OPTIONS:
                raise TypeError(f"'{option}' est un argument keyword invalide pour {self.__class__.__name__}()")

        self.nom = nom
        self.parent = None
        
        self.current_zone = "default"
        self.pages = Pages()

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
        return f"{self.position} {self.get_rect()}".strip() 

        res: str = ""
        if self.contenu:  # ToDo
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


    def add(self, zone: Zone, nom_page: Optional[str] = None) -> Zone:
        zone.parent = self
        zone.color = zone.options.get("color", self.color)

        if nom_page is None:
            nom_page = self.current_zone

        # calcul les coordonnees a partir des options
        zone_calculee = self.calc_coords(zone)

        self.pages.add(Page(nom_page, zone_calculee))

        return zone_calculee

    def add_page(self, nom_page: str, goto: bool = True):
        if self.pages.get(nom_page) is not None:
            raise Exception(f"la page '{nom_page}' existe deja.")

        self.pages[nom_page] = list()
        if goto:
            self.goto_page(nom_page)

    def rename_page(self, new_name: str):
        if self.pages.get(new_name) is not None:
            raise Exception(f"la page '{new_name}' existe deja.")

        self.pages[new_name] = self.pages.pop(self.current_zone)
        self.current_zone = new_name


    def del_page(self, nom_page: str):
        if self.pages.get(nom_page) is None:
            raise Exception(f"la page '{nom_page}' n'existe pas.")

        del self.pages[nom_page]

    def previous_page(self):
        liste_pages = list(self.pages)
        index = liste_pages.index(self.current_zone)

        index -= 1
        if index < 0:
            self.current_zone = liste_pages[len(liste_pages)-1]
        else:
            self.current_zone = liste_pages[index]

        fprint(self.current_zone, "affichee")

    def next_page(self):
        liste_pages = list(self.pages)
        index = liste_pages.index(self.current_zone)

        index += 1
        if index >= len(liste_pages):
            self.current_zone = liste_pages[0]
        else:
            self.current_zone = liste_pages[index]

        fprint(self.current_zone, "affichee")

    def goto_page(self, nom_page: str):
        if self.pages.get(nom_page) is None:
            raise Exception(f"la page '{nom_page}' n'existe pas.")

        self.current_zone = nom_page

    def recalc_zones(self, coords: Optional[list]=None):
        if not coords is None:
            self.set_rect(coords)

        for page in self.pages:
            for zone in self.pages[page]:
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

    def mouse_button_up(self, mouse_position, button):
        
        def check_contenu(zone) -> Optional[Zone]:
            if not zone.mouse_over:
                return None

            for z in zone.pages[zone.current_zone]:
                if z.mouse_over:
                    return check_contenu(z)

            return zone

        zone = check_contenu(self)
        fprint("Zone clicked:", zone)
        if zone:
            if zone.parent:
                zone = zone.parent
            if button == 1:
                zone.next_page()
            else:
                zone.previous_page()

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

        for zone in self.pages[self.current_zone]:
            zone.check_mouse(mouse_position)
    
    def draw(self, screen):
        color = (255, 250, 250
            ) if self.parent and self.mouse_over and Variable.is_tick_actif() else self.color
        pygame.draw.rect(screen, color, self.get_rect(), 1)
        for zone in self.pages[self.current_zone]:
            zone.draw(screen)


def load_zone(page: str) -> Zone:

    zone = Zone("root", color=(0, 250, 250))

    match page:
        case "accueil":
            zone.rename_page("accueil")
            zone.add(Zone(color=(150, 150, 0), pad=15))
            
            zone.add_page("informations")
            zone.add(Zone(color=(50, 100, 200), pad=25))

            zone.add_page("credits")
            zone.add(Zone(color=(50, 200, 100), pad=35))
            
            zone.add_page("fin")
            zone.add(Zone(color=(200, 100, 40), pad=45))
            
            zone.goto_page("accueil")

        case "main":
            zone.rename_page("main")
            top = zone.add(Zone(color=(150, 150, 0), side="top", padx=15, pady=(15, 10), relheight=0.25))
            top.add(Zone(side="left", padx=(5, 3), pady=5, relwidth=0.25))
            top.add(Zone(side="left", padx=(3, 22), pady=5, relx=0.25, relwidth=0.75))
            # Ascenseur
            top.add(Zone(color=(20, 150, 100), side="right", padx=(0, 3), pady=5, x=20, width=20))

            middle = zone.add(Zone(color=(150, 150, 0), side="top", 
                padx=15, pady=(0, 50), rely=0.25, relheight=0.75))

            bottom = zone.add(Zone(color=(50, 50, 50), side="BOTTOM", pad=15, height=55, relwidth=1))
            bottom.add(Zone(color=(20, 200, 200), relwidth=1/3, padx=(0, 5)))
            bottom.add(Zone(color=(20, 200, 200), relx=1/3, relwidth=1/3))
            bottom.add(Zone(color=(20, 200, 200), side="RIGHT", relwidth=1/3, padx=(5, 0)))

        case "page1":
            zone.rename_page("boite_outil")
            zone.add(Zone(color=(50, 200, 50), relwidth=0.25, padx=(15,0), pady=15))
            zone.add(Zone(color=(50, 250, 50), relx=0.25, relwidth=0.75, pad=15))

            zone.add_page("detail")
            zone.add(Zone(color=(50, 200, 50), width=35, padx=(15,0), pady=15))
            zone.add(Zone(color=(50, 250, 50), padx=(50, 15), pady=15))

        case "page2":
            zone.rename_page("detail2")
            left = zone.add(Zone(color=(50, 200, 50), relwidth=0.75, padx=(15,0), pady=15))
            right = zone.add(Zone(color=(50, 250, 50), relx=0.75, relwidth=0.25, pad=15))

    fprint("Zone", zone.current_zone, "chargee", end=": ")
    fprint(list(map(lambda z: z.coords, zone.pages[zone.current_zone])))

    return zone


def next_page(page: str) -> str:

    match [page[:4], page[4:]]:
        case ["accu", _]:
            page = "main"

        case ["main", _]:
            page = "page1"

        case ["page", x]:
            if x == "2":
                page = "accueil"
            else:
                page = "page" + str(1+int(x))

    return page


def main():
    page_str: str = "accueil"
    mouse_position_save: tuple = (-1, -1)
    page = load_zone(page_str)

    screen = pygame.display.set_mode(page.get_size(), pygame.RESIZABLE, 24)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.KEYUP:
                    running = not event.key == 27

                    if event.key in (pygame.K_PAGEDOWN, pygame.K_PAGEUP):
                        page.next_page()

                    elif event.key in (pygame.K_BACKSPACE, ):
                        page.previous_page()

                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        page_str = next_page(page_str)
                        page = load_zone(page_str)
                        page.check_mouse(mouse_position_save)

                case pygame.KMOD_LGUI:
                    page.check_mouse(event.pos)
                    mouse_position_save = event.pos

                case pygame.MOUSEBUTTONUP:
                    page.mouse_button_up(event.pos, event.button)

                case pygame.QUIT:
                    running = False

                case pygame.VIDEORESIZE:
                    Screen.size = [event.w, event.h]
                    page.recalc_zones([0, 0, event.w, event.h])

                case default:
                    pass
                    # fprint("event:", default)


        screen.fill(0)
        page.draw(screen)
        pygame.display.update()

        clock.tick(60)
        Variable.update_tick()


# zr= Zone("ROOT")
# ps = Pages("0")
# ps.add(Page("p1", zr.add(Zone(x=0, width=20, y=0, height=20))))
# ps.add(Page("p2", zr.add(Zone(x=10, width=20, y=10))))
# for nom, z in ps:
#     print(nom, z)
# exit()



if __name__ == "__main__":
    pygame.init()
    try:
        main()
    finally:
        pygame.quit()
        fprint("Fin")

