import pygame

from audio import Audio
from abc import abstractmethod, ABCMeta
from os import path
# from os.path import sep as separateur
from datetime import datetime


class SysTray(metaclass=ABCMeta):

    PRIORITY = 99
    DEFAULT_CONFIG = ("?", (0, 0, 0))
    TEXT_OFFSET = 3

    mouse_over = False

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def update_screen(self, screen):
        pass

    @abstractmethod
    def set_posx(self, x):
        pass

    @abstractmethod
    def get_width(self):
        pass

    def mouse_move(self):
        pass

    def mouse_up(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass


class Application(metaclass=ABCMeta):
    MIN_SIZE = (200, 100)
    title = ""

    WINDOW_PROPERTIES = ["RESIZABLE"]
    DEFAULT_CONFIG: tuple = ("?", (0, 0, 0))

    @abstractmethod
    def __init__(self, parent, screen, *args):
        pass

    def post_init(self):
        pass

    def close(self):
        pass

    @abstractmethod
    def resize(self, screen):
        pass

    def get_action(self):
        return None

    def mouse_enter(self, mouseX, mouseY):
        pass

    def mouse_exit(self):
        pass
        
    def mouse_move(self, mouseX, mouseY):
        pass
        
    def mouse_button_down(self, mouseX, mouseY, button):
        pass

    def mouse_button_up(self, mouseX, mouseY, button):
        pass

    @abstractmethod
    def update(self):
        if self.parent and self.parent.keypressed():
            self.touche = self.parent.get_key()
            if self.touche == 27:
                self.action = "QUIT"

    @abstractmethod
    def draw(self):
        pass


class NoApplication(Application):

    DEFAULT_CONFIG = ("No Application", (80, 80, 80))

    def __init__(self, parent, screen, *args):
        self.parent = parent
        if self.parent:
            self.title = self.parent.title
        self.touche = ""
        self.action = ""

    def resize(self, screen):
        self.parent.set_title(self.title + " Resize({}x{})".format(*screen.get_size()))

    def mouse_enter(self, mouseX, mouseY):
        self.parent.set_title(self.title + " Mouse_Enter()")

    def mouse_exit(self):
        self.parent.set_title(self.title + " Mouse_Exit()")

    def mouse_move(self, mouseX, mouseY):
        self.parent.set_title(self.title + f" Mouse_Move({mouseX}, {mouseY})")
        if mouseX > 200 and mouseY > 200:
            a = 1 / 0

    def mouse_button_up(self, mouseX, mouseY, button):
        self.parent.set_title(self.title + f" Mouse_button_up({button})")

    def get_action(self):
        return self.action

    def update(self):
        super().update()

    def draw(self):
        pass


class SystemDateTime(SysTray):

    PRIORITY = 1
    DEFAULT_CONFIG = ("Date Time", (50, 200, 50))

    def __init__(self, screen, couleur, x):
        self.update_screen(screen)
        self.couleur = (100, 100, 100)
        self.posx = x
        # self.SYS_FONT = pygame.font.SysFont("comicsans", 12)
        self.SYS_FONT = pygame.font.SysFont("courier", 16)
        self.systray_width = self.SYS_FONT.render(" 99/99/9999 99:99:99 ", False, (255, 255, 255)).get_size()[0]
        self.etat = 1
        self.format = "%d/%m/%Y %H:%M:%S"

    def update_screen(self, screen):
        self.screen = screen
        self.width = screen.get_size()[0]

    def set_posx(self, x):
        self.posx = x

    def get_width(self):
        return self.systray_width

    def mouse_up(self):
        self.etat += 1
        if self.etat > 3:
            self.etat = 1
        self.format = {
            1: "%d/%m/%Y %H:%M:%S ",
            2: " %d/%m/%Y ",
            3: " %H:%M:%S "
        }[self.etat]
        self.systray_width = self.SYS_FONT.render(datetime.now().strftime(self.format), 
            False, (255, 255, 255)).get_size()[0]
        
    def update(self):
        texte = datetime.now().strftime(self.format)
        self.text_surf = self.SYS_FONT.render(texte, False, (255, 255, 255))
        self.systray_rect = pygame.Rect(self.width - self.systray_width - self.posx, self.TEXT_OFFSET, self.systray_width, 25)

    def draw(self):
        self.screen.blit(self.text_surf, self.systray_rect)


class SoundView(SysTray):

    PRIORITY = 2
    DEFAULT_CONFIG = ("Sound", (50, 200, 50))

    def __init__(self, screen, couleur, x):
        self.update_screen(screen)
        self.couleur = (100, 100, 100)
        self.posx = x
        self.SYS_FONT = pygame.font.SysFont("comicsans", 12)
        self.systray_width = 25
        self.etat = 1

    def update_screen(self, screen):
        self.screen = screen
        self.width = screen.get_size()[0]

    def set_posx(self, x):
        self.posx = x

    def get_width(self):
        return self.systray_width

    def mouse_up(self):
        self.etat += 1
        if self.etat > 2:
            self.etat = 1
        self.format, mute_unmute = {
            1: ("  <)  ", Audio.unmute_all_applications),
            2: (" <X)  ", Audio.mute_all_applications)
        }[self.etat]
        mute_unmute()

    def update(self):
        self.systray_rect = pygame.Rect(self.width - self.systray_width - self.posx, 0, self.systray_width, 25)

    def draw(self):
        x = self.width - self.systray_width - self.posx + self.TEXT_OFFSET
        y = 10
        h = 4
        color1 = (240, 240, 240)
        color2 = (80, 80, 80)
        color = color2 if Audio.MUTE else color1

        points = [(x, 12), (x+6, 7), (x+6, 17)]
        pygame.draw.polygon(self.screen, color1, points, 1)

        x += 8
        for i in range(3):
            pygame.draw.line(self.screen, color, (x+2*i, y-2*i), (x+2*i, y+h+2*i))


def make_path(*args):
    return path.join(*args)


def get_classes_from_file(type_classe, fichier):
    mon_app = __import__(fichier)
    for classe_name in dir(mon_app):
        if not hasattr(mon_app, type_classe): continue
        classe = getattr(mon_app, classe_name)
        if not callable(classe): continue
        if not classe.__class__.__name__ == "ABCMeta": continue
        lookup_classe = getattr(mon_app, type_classe)
        if not issubclass(classe, lookup_classe): continue
        if classe == lookup_classe: continue
        yield classe


def get_all_classes(type_classe):
    import os
    liste_classes = []
    # Recherche d'une classe Application dans les fichiers .py
    for file in os.scandir("."):
        fichier = file.name.lower()
        # if file.is_file() and fichier.endswith(".py") and fichier != __file__[1+__file__.rindex(separateur):]:
        if file.is_file() and fichier.endswith(".py") and fichier != "app.py":
            fichier = fichier[:-3]
            for classe in get_classes_from_file(type_classe, fichier):
                if classe not in liste_classes:
                    # print("CONFIG=", classe.DEFAULT_CONFIG)
                    liste_classes.append(classe)
    return liste_classes


if __name__ == '__main__':
    from exec import run
    run(NoApplication)
