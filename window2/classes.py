import pygame
import json

from abc import abstractmethod, ABCMeta
from os import path

from mouse import Mouse
# from os.path import sep as separateur


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)
    

class Registres:
    __filename: str = "registres.json"
    __data: dict
    __modified: bool

    def __init__(self, application: str):
        # print("load registres:", application, flush=True)
        self.clear()
        self.__application = application
        self.load_file()

    def is_modified(self) -> bool:
        return self.__modified

    def load_file(self) -> None:
        # Lecture des registres de l'application
        # print("chargement du registre :", self.__application, flush=True)
        self.__modified = False
        try:
            with open(self.__filename, encoding="utf-8") as reg:
                self.__data = json.load(reg).get(self.__application, None)

            if self.__data is None:
                print("Initialisation de l'application dans la base de registres", flush=True)
                self.__modified = True
                self.__data = dict()

        except FileNotFoundError as fnfe:
            print("Initialisation de la base de registres", flush=True)
            self.__modified = True
            with open(self.__filename, "w", encoding="utf-8") as reg:
                json.dump({}, reg)
                self.__data = dict()

    def save_file(self) -> None:
        # Sauvegarde des registres de l'application
        if not self.__modified:
            return

        print("save registres:", self.__application, flush=True)
        with open(self.__filename, encoding="utf-8") as reg:
            self.__reg = json.load(reg)

        self.__reg[self.__application] = self.__data
        with open(self.__filename, "w", encoding="utf-8") as reg:
            json.dump(self.__reg, reg)

    def clear(self) -> None:
        self.__modified = True
        self.__data = dict()

    def get_all(self) -> dict:
        return self.__data

    def load(self, chemin_registre, default=None) -> object:
        res : dict = self.__data
        # Recuperation des informations du chemin_registre
        for registre in chemin_registre.split("."):
            res = res.get(registre, None)
            if res is None:
                self.save(chemin_registre, default)
                return default

        # Lecture de la cle de registre finale
        return res

    def save(self, chemin_registre, valeur) -> None:
        res : dict = self.__data
        self.__modified = True

        # Creation / Recuperation des informations du chemin_registre
        for registre in chemin_registre.split(".")[:-1]:
            temp = res.get(registre, None)
            if temp is None:
                res[registre] = dict()
                res = res.get(registre, {})
            else:
                res = temp

        # Creation / Mise a jour de la cle de registre finale
        registre = chemin_registre.split(".")[-1]
        res[registre] = valeur


class Variable:

    DEBUG: bool = False
    window: object


class Theme:
    theme: str = "SOMBRE"

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
            "TASK_BAR_COLOR": (200, 200, 200, 100),
            "LIST_TEXT_COLOR": (0, 0, 0),
            "LIST_SELECTED_TEXT_COLOR": (0, 250, 0),
            "LIST_MOUSEOVER_TEXT_COLOR": (50, 50, 250),
            "LIST_BACK_COLOR": (220, 220, 220),

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
            "TASK_BAR_COLOR": (20, 20, 20, 100),
            "LIST_TEXT_COLOR": (220, 220, 220),
            "LIST_SELECTED_TEXT_COLOR": (200, 200, 200),
            "LIST_MOUSEOVER_TEXT_COLOR": (50, 50, 50),
            "LIST_BACK_COLOR": (30, 30, 30),
        }    
    }

    @classmethod
    def get_theme(cls):
        return cls.theme

    @classmethod
    def set_theme(cls, theme):
        cls.theme = theme.upper()

    @classmethod
    def get(cls, type_color):
        return cls.data[Theme.theme][type_color]


class Sound:

    def __init__(self, window=None):
        if not window:
            window = Variable.window

        if Variable.DEBUG:
            print(f"Sound.__init__({window.title})", flush=True)

        self.load_sound = window.load_sound
        self.play_sound = window.play_sound
        self.stop_channels = window.stop_channels
        self.remove_unused_channels = window.remove_unused_channels


class Keys:

    def __init__(self, window=None):
        if not window:
            window = Variable.window

        if Variable.DEBUG:
            print(f"Keys.__init__({window.title})", flush=True)

        for attrib in filter(lambda a: a[:2] == "K_", dir(pygame)):
            setattr(self, attrib, getattr(pygame, attrib))

        self.get_key = window.get_key
        self.view_key = window.view_key
        self.clear_key_buffer = window.clear_key_buffer            


class Tools:

    def __init__(self, screen):
        if Variable.DEBUG:
            print(f"Tools.__init__({screen})", flush=True)
        self.update_screen(screen)

    def get_subtools(self, coords):
        return Tools(self.screen.subsurface(self.Rect(*coords)))

    def update_screen(self, screen):
        self.screen = screen

    def fill(self, color, rect=None):
        if rect:
            self.screen.fill(color, rect)
        else:
            self.screen.fill(color)

    def font(self, police, taille):
        return pygame.font.SysFont(police, taille)

    def load_image(self, image):
        return pygame.image.load(image)

    def scale_image(self, image, img_width, img_height):
        return pygame.transform.scale(image, (img_width, img_height))

    def line(self, couleur, *coords, width=1):
        pygame.draw.line(self.screen, couleur, *coords, width)

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

    def get_locked(self):
        return self.screen.get_locked()

    def get_rect(self):
        return self.screen.get_rect()

    def get_size(self):
        return self.screen.get_size()

    def get_ticks(self):
        return pygame.time.get_ticks()

    def blit(self, surface, rect):
        self.screen.blit(surface, rect)

    def unlock(self):
        self.screen.unlock()


class SysTray(metaclass=ABCMeta):
    tools: Tools
    theme: Theme
    registre: Registres

    PRIORITY = 99
    DEFAULT_CONFIG = ("?", (0, 0, 0))
    TEXT_OFFSET = 3
    INITIAL_WIDTH = 15

    mouse_over = False

    @abstractmethod
    def __init__(self, color):
        self.theme = Theme()
        self.registre = Registres(self.DEFAULT_CONFIG[0])

    def __init_screen__(self, screen):
        self.tools = Tools(screen)

    @abstractmethod
    def update_screen(self):
        pass

    def post_init(self):
        pass
        
    def get_width(self):
        return self.tools.screen.get_size()[0]

    # 
    # Permet d'envoyer des actions a faire par l'OS
    # 
    # return None : None
    # return str  : action
    # return tuple: action, callback
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
    MIN_SIZE = (400, 200)
    title = ""
    tools: Tools
    theme: Theme
    sound: Sound
    keys: Keys
    registre: Registres
    mouse: Mouse

    WINDOW_PROPERTIES = ["RESIZABLE"]
    DEFAULT_CONFIG: tuple = ("?", (0, 0, 0))

    @abstractmethod
    def __init__(self, screen, window):
        if hasattr(self, "__is_initialized"):
            return

        if Variable.DEBUG:
            print(f"Initialisation de l'application {self.DEFAULT_CONFIG[0]}", flush=True)
        self.__is_initialized = True

        self.tools = Tools(screen)
        self.keys = Keys(window)
        self.sound = Sound(window)
        self.theme = Theme()
        self.registre = Registres(self.DEFAULT_CONFIG[0])
        self.mouse = Mouse()

        # window = Variable.window
        self.set_title = window.set_title
        self.win_resize = window.resize

    def post_init(self):
        pass

    def close(self):
        pass

    @abstractmethod
    def resize(self):
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

    def mouse_wheel(self, dx, dy):
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
