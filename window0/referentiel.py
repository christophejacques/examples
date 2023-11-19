import pygame
import random
import os

from abc import ABCMeta, abstractmethod


black = (0, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
light_grey = (200, 200, 200)
grey = (128, 128, 128)
dark_grey = (64, 64, 64)
zone_color = (200, 100, 50)

pygame.init()


class GetFilesDirectory:

    def __init__(self, directory: str):
        if not os.path.isdir(directory):
            raise Exception(f"Le repertoire '{directory}' n'existe pas")
        self.directory = directory
        self.file = None

    def parcours(self):
        for f in os.scandir(self.directory):
            yield f

    def next_file(self):
        if self.file is None:
            self.file = self.parcours()

        return next(self.file)


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Position:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def in_zone(self, zone) -> bool:
        res = (zone[1][0] >= self.x >= zone[0][0]) and (zone[1][1] >= self.y >= zone[0][1])
        return res

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class RegisterException(Exception):
    pass


class PG:
    def init(self, screen):
        self.screen = None

    def is_display_active(self) -> bool:
        return pygame.display.get_active()

    def draw_line(self, couleur, pointa, pointb) -> None:
        pygame.draw.line(self.screen, couleur, pointa, pointb)

    def draw_rect(self, color, zone, size) -> None:
        pygame.draw.rect(self.screen, color, zone, size)

    def draw_circle(self, couleur, centre, rayon) -> None:
        pygame.draw.circle(self.screen, couleur, centre, rayon)

    def SysFont(self, font: str, taille: int) -> pygame.font.Font:
        return pygame.font.SysFont(font, taille, 0, 0)


class AbstractZoneContent(PG, metaclass=ABCMeta):

    def __init__(self):
        self.methods: dict = {}

    @abstractmethod
    def set_zone(self): pass

    def set_screen(self, screen) -> None:
        self.screen = screen

    @abstractmethod
    def update(self): pass

    @abstractmethod
    def draw(self): pass

    def register(self, methods: list) -> None:
        for method in methods:
            if type(method) == dict:
                self.methods.update(method)
            else:
                self.methods.update({method: None})

        for method in self.methods:
            if not hasattr(self, method):
                raise RegisterException(
                    f"Le methode '{method}' n'existe pas dans la classe: {self.__class__.__name__}")

    def has_registered(self, method) -> bool:
        return method in self.methods

    def on_mouse_enter(self, mouse_position) -> list:
        self.mouse_entered = True
        return []

    def on_mouse_move(self, mouse_position) -> list:
        return []

    def on_mouse_exit(self) -> list:
        self.mouse_entered = False
        return []


class AbstractZone(AbstractZoneContent, metaclass=ABCMeta):

    @abstractmethod
    def add(self): pass
