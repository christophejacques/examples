import pygame

from abc import abstractmethod, ABCMeta
from os import path
# from os.path import sep as separateur


class Variable:

    DEBUG: bool = False
    window: object


class Theme:
    theme: str = "CLAIR"

    data = {
        "CLAIR": {
            "FORE_COLOR": (0, 0, 0),
            "BACKGROUND_COLOR": (255, 255, 255),
            "INACTIVE_FORE_COLOR": (250, 250, 250),
            "GRAY_COLOR": (50, 50, 250),
            "BOUTON_COLOR": (180, 180, 180),
            "PUSH_COLOR": (255, 255, 255),
            "MOUSE_OVER_COLOR": (210, 210, 210),
            "THEME_ACTIVE_COLOR": (10, 130, 170, 50),
            "THEME_INACTIVE_COLOR": (130, 130, 150, 50),
            "THEME_ERROR_COLOR": (200, 20, 20),
            "TASK_BUTTON_BACK_COLOR": (180, 180, 180),
            "TASK_SELECTED_BUTTON_BACK_COLOR": (150, 150, 150),
            "TASK_ERROR_BUTTON_BACK_COLOR": (180, 20, 20),
            "TASK_BAR_COLOR": (200, 200, 200, 100)

        },
        "SOMBRE": {
            "FORE_COLOR": (250, 250, 250),
            "BACKGROUND_COLOR": (0, 0, 0),
            "INACTIVE_FORE_COLOR": (15, 15, 15),
            "GRAY_COLOR": (200, 200, 100),
            "BOUTON_COLOR": (70, 70, 70),
            "PUSH_COLOR": (0, 0, 0),
            "MOUSE_OVER_COLOR": (40, 40, 40),
            "THEME_ACTIVE_COLOR": (10, 80, 120, 50),
            "THEME_INACTIVE_COLOR": (100, 100, 120, 50),
            "THEME_ERROR_COLOR": (170, 20, 20),
            "TASK_BUTTON_BACK_COLOR": (80, 80, 80),
            "TASK_SELECTED_BUTTON_BACK_COLOR": (50, 50, 50),
            "TASK_ERROR_BUTTON_BACK_COLOR": (250, 50, 50),
            "TASK_BAR_COLOR": (20, 20, 20, 100)
        }    
    }

    @classmethod
    def get_theme(self):
        return Theme.theme

    @classmethod
    def set_theme(self, theme):
        Theme.theme = theme.upper()

    @classmethod
    def get(self, type_color):
        return Theme.data[Theme.theme][type_color]


class Sound:

    def __init__(self):
        if Variable.DEBUG:
            print(f"Sound.__init__({Variable.window.title})", flush=True)

        self.load_sound = Variable.window.load_sound
        self.play_sound = Variable.window.play_sound
        self.stop_channels = Variable.window.stop_channels
        self.remove_unused_channels = Variable.window.remove_unused_channels


class Keys:

    def __init__(self):
        if Variable.DEBUG:
            print(f"Keys.__init__({Variable.window.title})", flush=True)

        for attrib in filter(lambda a: a[:2] == "K_", dir(pygame)):
            setattr(self, attrib, getattr(pygame, attrib))

        self.get_key = Variable.window.get_key
        self.view_key = Variable.window.view_key
        self.clear_key_buffer = Variable.window.clear_key_buffer            


class Tools:

    def __init__(self, screen):
        if Variable.DEBUG:
            print(f"Tools.__init__({screen})", flush=True)
        self.update_screen(screen)

    def update_screen(self, screen):
        self.screen = screen

    def font(self, police, taille):
        return pygame.font.SysFont(police, taille)

    def line(self, couleur, *coords):
        pygame.draw.line(self.screen, couleur, *coords)

    def Rect(self, *coords):
        return pygame.Rect(*coords)

    def rect(self, couleur, *coords):
        pygame.draw.rect(self.screen, couleur, *coords)

    def circle(self, couleur, *coords):
        pygame.draw.circle(self.screen, couleur, *coords)

    def polygon(self, couleur, liste_points, taille):
        pygame.draw.polygon(self.screen, couleur, liste_points, taille)

    def pixels3d(self):
        return pygame.surfarray.pixels3d(self.screen)

    def get_ticks(self):
        return pygame.time.get_ticks()

    def blit(self, surface, rect):
        self.screen.blit(surface, rect)


class SysTray(metaclass=ABCMeta):
    tools: Tools

    PRIORITY = 99
    DEFAULT_CONFIG = ("?", (0, 0, 0))
    TEXT_OFFSET = 3

    mouse_over = False

    @abstractmethod
    def __init__(self, screen):
        self.tools = Tools(screen)
        self.theme = Theme()
        # self.sound = Sound()

    @abstractmethod
    def update_screen(self, screen, posx=0):
        self.tools = Tools(screen)

    @abstractmethod
    def set_posx(self, x):
        pass

    @abstractmethod
    def get_width(self):
        pass

    def get_action(self):
        return None

    def get_theme(self):
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
    tools: Tools
    sound: Sound
    keys: Keys

    WINDOW_PROPERTIES = ["RESIZABLE"]
    DEFAULT_CONFIG: tuple = ("?", (0, 0, 0))

    @abstractmethod
    def __init__(self, screen, *args):
        self.tools = Tools(screen)
        self.keys = Keys()
        self.sound = Sound()
        self.theme = Theme()
        window = Variable.window
        self.set_title = window.set_title
        self.win_resize = window.resize

    def post_init(self):
        pass

    def close(self):
        pass

    @abstractmethod
    def resize(self, screen):
        pass

    def get_theme(self):
        pass

    def get_action(self):
        return None

    def keypressed(self, event):
        pass

    def keyreleased(self, event):
        touche = self.keys.get_key()
        if touche == 27:
            self.action = "QUIT"

    def load_sound(self, fichier, volume):
        print("version initiale")

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
        pass

    @abstractmethod
    def draw(self):
        pass


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


def get_all_classes(type_classe: str):
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
    for cls in get_all_classes("Application"):
        print(cls)
