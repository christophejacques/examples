import pygame
import random
import traceback
from abc import ABCMeta, abstractmethod


black = (0, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
light_grey = (200, 200, 200)
grey = (128, 128, 128)
dark_grey = (64, 64, 64)
zone_color = (200, 100, 50)


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def in_zone(self, zone):
        return (zone[1][0] >= self.x >= zone[0][0]) and (zone[1][1] >= self.y >= zone[0][1])

    def __str__(self):
        return f"({self.x}, {self.y})"


class RegisterException(Exception):
    pass


class AbstractZoneContent(metaclass=ABCMeta):

    @abstractmethod
    def set_zone(self): pass

    def set_screen(self, screen):
        self.screen = screen

    @abstractmethod
    def update(self): pass

    @abstractmethod
    def draw(self): pass

    def register(self, methods):
        self.methods = {}
        for method in methods:
            if type(method) == dict:
                self.methods.update(method)
            else:
                self.methods.update({method: None})

        for method in self.methods:
            if not hasattr(self, method):
                raise RegisterException(
                    f"Le méthode '{method}' n'existe pas dans la classe: {self.__class__.__name__}")

    def has_registered(self, method):
        return method in self.methods

    def on_mouse_enter(self):
        self.mouse_entered = True

    def on_mouse_move(self):
        pass

    def on_mouse_exit(self):
        self.mouse_entered = False


class AbstractZone(AbstractZoneContent, metaclass=ABCMeta):

    @abstractmethod
    def add(self): pass


class Window(AbstractZone):

    def __init__(self, screen, bg_color, zone):
        self.screen = screen
        self.bg_color = bg_color
        self.zone = zone
        self.zones = []
        self.rules = []
        self.methods = []
        self.mouse_entered = False
        self.mouse = Position(0, 0)

    def set_zone(self, zone):
        self.zone = zone
        self.optimize()

    def add(self, nom, zone, rules):
        zone.set_screen(self.screen)
        zone.nom = nom
        self.zones.append(zone)
        self.rules.append(rules)

    def get_zone(self, nom):
        for zone in self.zones:
            if zone.nom == nom:
                return zone

    def optimize(self):

        def iif(condition, si_vrai, si_faux):
            return si_vrai if condition else si_faux

        def nfz(fonction, valeur, si_null_ou_erreur):
            try:
                return eval(f"{fonction}({valeur})")
            except Exception as e:
                print("Error:", e)
                return si_null_ou_erreur

        def wait(formule):
            return formule

        def fisactive(nom_zone):
            return self.get_zone(nom_zone).active

        def ftop(nom_zone):
            if self.get_zone(nom_zone).active:
                return self.get_zone(nom_zone).zone[0][1]
            else:
                return 0

        def fbottom(nom_zone):
            if self.get_zone(nom_zone).active:
                return self.get_zone(nom_zone).zone[1][1]
            else:
                return 0

        def fleft(nom_zone):
            if self.get_zone(nom_zone).active:
                return self.get_zone(nom_zone).zone[0][0]
            else:
                return 0

        def fright(nom_zone):
            if self.get_zone(nom_zone).active:
                return self.get_zone(nom_zone).zone[1][0]
            else:
                return 0

        width, height = self.zone[1]
        left, top, right, bottom = 0, 0, 0, 0

        for i, zone in enumerate(self.zones):
            if zone.active:
                # print(f"optimize {zone.nom}", end=": ")
                left = int(eval(self.rules[i].get("left", "0")))
                top = int(eval(self.rules[i].get("top", "0")))
                right = int(eval(self.rules[i].get("right", "width")))
                bottom = int(eval(self.rules[i].get("bottom", "height")))

                new_zone = ((left, top), (right, bottom))
                # print(new_zone, end=" ")
                zone.set_zone(new_zone)
                # print("OK")

    def update(self):
        if pygame.display.get_active():
            for zone in self.zones:
                zone.update()

    def draw(self):
        if pygame.display.get_active():
            self.screen.fill(self.bg_color, rect=self.zone)
            for zone in self.zones:
                zone.draw()

    def on_click(self):
        resTotal = []
        for zone in self.zones:
            if zone.has_registered("on_click") and self.mouse.in_zone(zone.zone):
                res = zone.on_click()
                if res:
                    resTotal += res
        return resTotal

    def on_mouse_enter(self):
        self.mouse_entered = True

    def on_mouse_move(self, mouse_position):
        self.mouse = Position(*mouse_position)
        for zone in self.zones:
            if self.mouse.in_zone(zone.zone):
                if zone.has_registered("on_mouse_enter") and not zone.mouse_entered:
                    zone.on_mouse_enter()
                if zone.has_registered("on_mouse_move"):
                    zone.on_mouse_move(mouse_position)
            else:
                if zone.has_registered("on_mouse_exit") and zone.mouse_entered:
                    zone.on_mouse_exit()

    def on_mouse_exit(self):
        self.mouse_entered = False
        for zone in self.zones:
            if zone.has_registered("on_mouse_exit") and zone.mouse_entered:
                zone.on_mouse_exit()


class Zone(AbstractZone):
    index = 0

    def __init__(self, bg_color, zone=None):
        self.index = Zone.index
        Zone.index += 1
        self.objets = []
        self.active = True
        self.color = zone_color
        self.bg_color = bg_color
        self.screen = None
        self.mouse_entered = False
        self.mouse = Position(0, 0)
        self.methods = []
        if zone:
            self.set_zone(zone)
        else:
            self.set_zone(((0, 0), (0, 0)))

    def set_zone(self, zone):
        self.zone = zone
        for objet in self.objets:
            objet.set_zone(self.zone)

    def add(self, objet):
        objet.set_screen(self.screen)
        objet.set_zone(self.zone)
        self.objets.append(objet)

    def update(self):
        if not self.active:
            return

        for objet in self.objets:
            objet.update()

    def draw(self):
        if not self.active:
            return

        left, top = self.zone[0]
        width, height = self.zone[1]
        zone = (self.zone[0], (width-left, height-top))

        if self.bg_color:
            self.screen.fill(self.bg_color, rect=zone)
        if self.color:
            pygame.draw.rect(self.screen, self.color, zone, 1)
        for objet in self.objets:
            objet.draw()

    def on_click(self):
        resTotal = []
        for objet in self.objets:
            if objet.has_registered("on_click") and self.mouse.in_zone(objet.zone):
                res = objet.on_click()
                if res:
                    resTotal += res
        return resTotal

    def on_mouse_enter(self):
        self.mouse_entered = True

    def on_mouse_move(self, mouse_position):
        self.mouse = Position(*mouse_position)
        for objet in self.objets:
            if self.mouse.in_zone(objet.zone):
                if objet.has_registered("on_mouse_enter") and not objet.mouse_entered:
                    objet.on_mouse_enter()
                if objet.has_registered("on_mouse_move"):
                    objet.on_mouse_move(mouse_position)
            else:
                if objet.has_registered("on_mouse_exit") and objet.mouse_entered:
                    objet.on_mouse_exit()

    def on_mouse_exit(self):
        for objet in self.objets:
            if objet.has_registered("on_mouse_exit") and objet.mouse_entered:
                objet.on_mouse_exit()

        self.mouse_entered = False


def main():
    pygame.init()
    screen = None
    try:
        assert isinstance(Window(screen, 0, 0), AbstractZoneContent), "Problème de la classe StarField"
        assert isinstance(Zone(0), AbstractZoneContent), "Problème de la classe Zones"
    except Exception:
        traceback.print_exc()

    pygame.quit()


if __name__ == '__main__':
    main()
