from abc import abstractmethod, ABCMeta
from classes import Application, fprint
from typing import Self, Optional, Callable, List, Tuple, Any
from colors import Colors, darker
from functools import partial


class CheckForme(metaclass=ABCMeta):
    SPACE: int = 4
    tools: object
    rect: object
    isActif: Callable
    getColor: Callable
    getMaxColor: Callable

    def __init__(self, parent: Self):
        self.tools = parent.tools
        self.rect = parent.rect
        self.isActif = parent.isActif
        self.getColor = parent.getColor
        self.getMaxColor = parent.getMaxColor
        self.__post_init__()

    @abstractmethod
    def __post_init__(self):
        pass

    @abstractmethod
    def draw_form(self):
        pass

    def set_tools(self, parent):
        self.tools = parent.tools

    def draw(self):
        self.draw_form()


class Carre(CheckForme):
    x: int
    y: int
    w: int
    h: int

    def __post_init__(self):
        self.x = self.rect.x + self.SPACE
        self.y = self.rect.y + self.SPACE
        self.w = self.rect.w - 2*self.SPACE
        self.h = self.rect.h - 2*self.SPACE

    def draw_form(self):
        self.tools.rect(self.getMaxColor(), self.rect, 1)
        if self.isActif():
            self.tools.rect(self.getColor(), (self.x, self.y, self.w, self.h))


class Tiret(CheckForme):

    def __post_init__(self):
        self.x = self.rect.x + self.SPACE
        self.y = self.rect.y + self.SPACE
        self.w = self.rect.w - 2*self.SPACE
        self.h = self.rect.h - 2*self.SPACE
        self.y1 = self.rect.y + self.rect.h // 2 - self.SPACE // 2
        self.h1 = self.SPACE

    def draw_form(self):
        self.tools.rect(self.getColor(), (self.x, self.y1, self.w, self.h1))


class Cible(CheckForme):
    RADIUS: int = 8
    SPACE: int = 4
    DELTA: int = 2
    cx: int
    cy: int
    x1: int
    x2: int
    y1: int
    y2: int

    def __post_init__(self):
        self.cx, self.cy = self.rect.center

        self.x1  = self.rect.x + self.DELTA
        self.x1p = self.x1+self.SPACE
        self.y1  = self.rect.y  + self.DELTA
        self.y1p = self.y1+self.SPACE
        self.x2  = self.rect.x + self.rect.w - self.DELTA
        self.x2p = self.x2-self.SPACE
        self.y2  = self.rect.y + self.rect.h - self.DELTA
        self.y2p = self.y2-self.SPACE

    def draw_form(self):
        if self.isActif():
            self.tools.circle(self.getMaxColor(), (self.cx, self.cy), self.RADIUS)
        else:
            color = self.getMaxColor()
            self.tools.line(color, (self.x1, self.y1), (self.x1p, self.y1))
            self.tools.line(color, (self.x1, self.y1), (self.x1, self.y1p))
            self.tools.line(color, (self.x2, self.y1), (self.x2p, self.y1))
            self.tools.line(color, (self.x2, self.y1), (self.x2, self.y1p))

            self.tools.line(color, (self.x1, self.y2), (self.x1p, self.y2))
            self.tools.line(color, (self.x1, self.y2), (self.x1, self.y2p))
            self.tools.line(color, (self.x2, self.y2), (self.x2p, self.y2))
            self.tools.line(color, (self.x2, self.y2), (self.x2, self.y2p))


class Rond(CheckForme):
    RADIUS: int = 10
    x: int
    y: int
    radius: int

    def __post_init__(self):
        self.x, self.y = self.rect.center
        self.radius = self.RADIUS - self.SPACE

    @classmethod
    def set_class_radius(cls, radius):
        cls.RADIUS = radius

    def set_radius(self, radius):
        self.RADIUS = radius

    def draw_form(self):
        self.tools.circle(self.getMaxColor(), (self.x, self.y), self.RADIUS, 1)
        if self.isActif():
            self.tools.circle(self.getColor(), (self.x, self.y), self.radius)


class ButtonStyle:

    def __init__(self, parent, forme: type, texte: str, coords: Tuple, 
            default: bool=False, couleur: Optional[Tuple]=None, callback: Optional[Callable]=None):
        
        self.on = default
        self.mouse_over = False
        self.clicked = False

        self.callback = callback
        self.tools = parent.tools

        self.rect = self.tools.Rect(coords)
        self.forme = forme(self)

        self.set_tools(parent)

        self.texte = texte
        self.FONT = self.tools.font("courrier", 24)
        self.set_color(couleur)

        _, _, self.texte_w, self.texte_h = self.texte_surf_min.get_rect()
        self.texte_rect = self.tools.Rect(
            self.rect.x+24, self.rect.y+3, self.texte_w, self.texte_h)

    def set_color(self, color):
        couleur = color if color else (0, 0, 0)
        self.max_color = couleur
        self.min_color = darker(couleur, 0.6)
        self.color = self.min_color
        self.texte_surf_min = self.FONT.render(self.texte, False, self.min_color)
        self.texte_surf_max = self.FONT.render(self.texte, False, self.max_color)

    def set_tools(self, parent: Application):
        self.tools = parent.tools
        self.forme.set_tools(parent)

    def isActif(self):
        return self.on

    def check(self):
        self.on = True

    def uncheck(self):
        self.on = False

    def getColor(self):
        return self.color

    def getMaxColor(self):
        return self.max_color

    def mouse_move(self, mouseX: int, mouseY: int):
        mouse_over = self.mouse_over
        self.mouse_over = self.rect.collidepoint((mouseX, mouseY)) or (
            self.texte_rect.collidepoint((mouseX, mouseY)))
        if mouse_over == self.mouse_over:
            return

        if self.mouse_over:
            self.color = self.max_color
        else:
            self.color = self.min_color

    def mouse_button_down(self, mouseX: int, mouseY: int, button: int):
        self.clicked = button == 1 and self.mouse_over

    def mouse_button_up(self, mouseX: int, mouseY: int, button: int):
        pass

    def update_position(self, x: int, y: int):
        self.rect.x += x
        self.rect.y += y
        self.texte_rect.x, self.texte_rect.y = self.rect.x+24, self.rect.y+3
        self.forme.__post_init__()

    def draw(self):
        self.forme.draw()
        if self.on or self.mouse_over:
            self.tools.blit(self.texte_surf_max, self.texte_rect)
        else:
            self.tools.blit(self.texte_surf_min, self.texte_rect)


class Liste(ButtonStyle):
    pass


class Radio(ButtonStyle):

    def mouse_button_up(self, mouseX: int, mouseY: int, button: int):
        if button == 1 and self.mouse_over and self.clicked:
            self.on = True
            if self.on and self.callback:
                self.callback()
        self.clicked = False


class Check(ButtonStyle):

    def mouse_button_up(self, mouseX: int, mouseY: int, button: int):
        if button == 1 and self.mouse_over and self.clicked:
            self.on = not self.on
            if self.on and self.callback:
                self.callback()
        self.clicked = False


class ListBoutons:

    def __init__(self, style: type[ButtonStyle], coords: tuple, default: int=-1, 
            visible: bool=True, color: Optional[tuple]=None, callback: Optional[Callable]=None):

        self.style = style
        self.x, self.y = coords
        self.mouse_over: bool = False
        self.boutons: list[ButtonStyle] = list()
        self.index: int = default
        self.visible: bool = visible
        self.color = color

    def set_tools(self, parent: Application):
        for bouton in self.boutons:
            bouton.set_tools(parent)

    def set_visible(self, valeur):
        self.visible = valeur

    def add(self, bouton: ButtonStyle):
        if not isinstance(bouton, self.style):
            raise TypeError(
                f"Le bouton est de type '{bouton.__class__.__name__}' au lieu de type '{self.style.__name__}'")

        bouton.update_position(self.x, self.y)
        if self.color:
            bouton.set_color(self.color)
        self.boutons.append(bouton)

    def select(self, select_index):
        if self.style == Radio:
            for index, bouton in enumerate(self.boutons):
                if select_index == index:
                    bouton.on = True
                    self.index = index
                else:
                    bouton.on = False

        elif self.style == Check:
            for index, bouton in enumerate(self.boutons):
                if index in select_index:
                    bouton.on = True
                else:
                    bouton.on = False

    def get(self):
        if self.style == Radio:
            return self.index
            
        elif self.style != Check:
            return None

        lst_index: list = list()
        for index, btn in enumerate(self.boutons):
            if btn.on:
                lst_index.append(index)
        return lst_index

    def mouse_move(self, mouseX: int, mouseY: int):
        if not self.visible:
            return
            
        self.mouse_over = False
        for bouton in self.boutons:
            bouton.mouse_move(mouseX, mouseY)
            if bouton.mouse_over:
                self.mouse_over = True

    def mouse_button_down(self, mouseX: int, mouseY: int, button: int):
        if not self.visible:
            return
            
        for bouton in self.boutons:
            bouton.mouse_button_down(mouseX, mouseY, button)

    def mouse_button_up(self, mouseX: int, mouseY: int, button: int):
        if not self.visible:
            return

        clicked_btn = None
        for index, bouton in enumerate(self.boutons):
            if bouton.mouse_over:
                bouton.mouse_button_up(mouseX, mouseY, button)
                if bouton.on:
                    clicked_btn = bouton
                    self.index = index

        if self.style == Radio and not clicked_btn or self.style == Check:
            return

        for bouton in self.boutons:
            if bouton != clicked_btn:
                bouton.on = False

    def draw(self):
        if not self.visible:
            return

        for bouton in self.boutons:
            bouton.draw()


class Switch:
    SPACE: int = 4

    def __init__(self, parent, couleur: tuple, coords: tuple, size: tuple,
            default: bool=False, callback: Optional[Callable]=None, *params):
        self.on = default
        self.min_color = darker(couleur, 0.6)
        self.color = self.min_color
        self.max_color = couleur
        self.mouse_over = False
        self.clicked = False
        self.set_callback(callback, *params)
        self.coords = coords
        self.size = size

        self.set_tools(parent)
        self.rect = self.tools.Rect(self.coords)
        self.w = (self.rect.w-3) // 2
        self.h = self.rect.h-2*self.SPACE
        self.y = self.rect.y+self.SPACE
        self.x2 = self.rect.x + self.rect.w - self.w - self.SPACE

    def set_tools(self, parent: Application):
        self.tools = parent.tools

    def set_callback(self, callback, *params):
        if callback:
            self.callback = partial(callback, *params)
        else:
            self.callback = None

    def mouse_move(self, mouseX: int, mouseY: int):
        self.mouse_over = self.rect.collidepoint((mouseX, mouseY))
        if self.mouse_over:
            self.color = self.max_color
        else:
            self.color = self.min_color

    def mouse_button_down(self, mouseX: int, mouseY: int, button: int):
        self.clicked = button == 1 and self.mouse_over

    def mouse_button_up(self, mouseX: int, mouseY: int, button: int):
        if button == 1 and self.mouse_over and self.clicked:
            self.on = not self.on
            if self.callback:
                self.callback(self.on)

        self.clicked = False

    def draw(self):
        if self.on:
            self.tools.rect(self.max_color, (self.rect.x-20, self.rect.y+10, *self.size), 1)
            self.tools.rect((0, 0, 0), (self.rect.x-5, self.rect.y-5, self.rect.w+10, self.rect.h+10))
            self.tools.rect(self.color, (self.x2, self.y, self.w, self.h))
        else:
            self.tools.rect((0, 0, 0), self.rect)
            self.tools.rect(self.color, (self.rect.x+self.SPACE, self.y, self.w, self.h))

        self.tools.rect(self.max_color, self.rect, 1)


class Librairie(Application):

    DEFAULT_CONFIG: tuple = ("Switch", (50, 150, 150))
    MIN_SIZE: tuple = (810, 300)
    WINDOW_PROPERTIES: list = ["CENTER"]

    def __init__(self, *args):
        self.title = self.DEFAULT_CONFIG[0]
        self.action = ""
        self.objets: list = list()

    def post_init(self):
        self.get_theme()
        self.set_title(self.title)

        visible1 = self.registre.load("RadioBoutons.visible0", True)
        visible2 = self.registre.load("RadioBoutons.visible1", False)
        visible3 = self.registre.load("RadioBoutons.visible2", True)

        selected1 = self.registre.load("RadioBoutons.selected0", 0)
        selected2 = self.registre.load("RadioBoutons.selected1", [])
        selected3 = self.registre.load("RadioBoutons.selected2", [])

        rbs = ListBoutons(Radio, (40, 70), visible=visible1)
        rbs.add(Radio(self, Rond, "Un", (0, 0, 20, 20), couleur=(50, 200, 100)))
        rbs.add(Radio(self, Rond, "Deux", (0, 30, 20, 20), couleur=(100, 200, 50)))
        rbs.add(Radio(self, Rond, "Trois", (0, 60, 20, 20), couleur=(50, 200, 200)))
        rbs.add(Radio(self, Rond, "Quatre", (0, 90, 20, 20), couleur=(200, 200, 50)))
        rbs.add(Radio(self, Rond, "Cinq", (0, 120, 20, 20), couleur=(200, 100, 50)))
        rbs.add(Radio(self, Rond, "Six", (0, 150, 20, 20), couleur=(200, 50, 100)))
        rbs.select(selected1)

        self.objets.append(rbs)

        sw1: Switch = Switch(self, Colors.GREEN, (40, 30, 50, 20), (160, 220), visible1)
        sw1.set_callback(rbs.set_visible)
        self.objets.append(sw1)

        rbs = ListBoutons(Check, (240, 70), visible=visible2)
        rbs.add(Check(self, Carre, "One", (0, 0, 20, 20), couleur=(50, 200, 100)))
        rbs.add(Check(self, Carre, "Two", (0, 30, 20, 20), couleur=(100, 200, 50)))
        rbs.add(Check(self, Carre, "Three", (0, 60, 20, 20), couleur=(50, 200, 200)))
        rbs.add(Check(self, Carre, "Four", (0, 90, 20, 20), couleur=(200, 200, 50)))
        rbs.add(Check(self, Carre, "Five", (0, 120, 20, 20), couleur=(200, 100, 50)))
        rbs.add(Check(self, Carre, "Six", (0, 150, 20, 20), couleur=(200, 50, 100)))
        rbs.select(selected2)

        self.objets.append(rbs)

        sw2: Switch = Switch(self, Colors.CYAN, (240, 30, 50, 20), (160, 220), visible2)
        sw2.set_callback(rbs.set_visible)
        self.objets.append(sw2)

        sw3: Switch = Switch(self, Colors.ORANGE, (440, 30, 50, 20), (160, 220), visible3)

        rbs = ListBoutons(Check, (440, 70), visible=visible3, color=sw3.max_color)
        rbs.add(Check(self, Cible, "Uno", (0, 0, 20, 20)))
        rbs.add(Check(self, Cible, "Dos", (0, 30, 20, 20)))
        rbs.add(Check(self, Cible, "Tres", (0, 60, 20, 20)))
        rbs.add(Check(self, Cible, "Quatro", (0, 90, 20, 20)))
        rbs.add(Check(self, Cible, "Cinco", (0, 120, 20, 20)))
        rbs.add(Check(self, Cible, "Seise", (0, 150, 20, 20)))
        rbs.select(selected3)

        sw3.set_callback(rbs.set_visible)
        self.objets.append(sw3)
        self.objets.append(rbs)

        sw4: Switch = Switch(self, Colors.RED, (640, 30, 50, 20), (160, 220), True)

        rbs = ListBoutons(Liste, (640, 70), visible=True, color=(250, 20, 20))
        rbs.add(Liste(self, Tiret, "First", (0, 0, 20, 20)))
        rbs.add(Liste(self, Tiret, "Second", (0, 30, 20, 20)))
        rbs.add(Liste(self, Tiret, "Third", (0, 60, 20, 20)))
        rbs.add(Liste(self, Tiret, "Fourth", (0, 90, 20, 20)))

        sw4.set_callback(rbs.set_visible)
        self.objets.append(sw4)
        self.objets.append(rbs)

        self.win_resize("BOTTOM RIGHT", 0, 0, *self.MIN_SIZE)


    def save_registres(self):
        index: int = -1
        for obj in self.objets:
            if not isinstance(obj, ListBoutons):
                continue
            index += 1
            if obj.visible != self.registre.load(f"RadioBoutons.visible{index}", True):
                self.registre.save(f"RadioBoutons.visible{index}", obj.visible)

            rb_index = obj.get()
            if rb_index != self.registre.load(f"RadioBoutons.selected{index}", 0):
                self.registre.save(f"RadioBoutons.selected{index}", rb_index)

    def resize(self):
        for obj in self.objets:
            obj.set_tools(self)

    def get_theme(self):
        pass
        # print(self.theme.get_theme())

    def mouse_enter(self, mouseX, mouseY):
        pass

    def mouse_exit(self):
        pass

    def keypressed(self, event):
        touche = self.keys.get_key()            

    def keyreleased(self, event):
        if event.key == 27:
            self.action = "QUIT"
            self.keys.clear_key_buffer()

    def close(self):
        self.save_registres()

    def mouse_move(self, mouseX: int, mouseY: int):
        for objet in self.objets:
            objet.mouse_move(mouseX, mouseY)

    def mouse_button_down(self, mouseX: int, mouseY: int, button: int):
        for objet in self.objets:
            objet.mouse_button_down(mouseX, mouseY, button)

    def mouse_button_up(self, mouseX: int, mouseY: int, button: int):
        for objet in self.objets:
            objet.mouse_button_up(mouseX, mouseY, button)

    def get_action(self):
        return self.action

    def update(self):
        pass

    def draw(self):
        self.tools.fill(0)
        for objet in self.objets:
            objet.draw()


if __name__ == '__main__':
    from exec import run
    run(locals())
