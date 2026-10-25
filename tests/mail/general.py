from os import environ

# Supprime l'affichage du chargement de pygame
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame  # noqa: E402


class Variable:

    DEBUG: bool = False

    SysFont1: pygame.font.Font
    SysFont2: pygame.font.Font
    SysFont3: pygame.font.Font
    SysFont4: pygame.font.Font


class Mouse:

    x: int
    y: int

    @classmethod
    def __init__(cls, x, y):
        cls.x = x
        cls.y = y

    @classmethod
    def update(cls):
        cls.x, cls.y = pygame.mouse.get_pos()


def fprint(*args, **kwargs) -> None:
    print(*args, **kwargs, flush=True)


def get_pygame_const_name(index):
    for c in dir(pygame):
        if c[0] in "AZERTYUIOPMLKJHGFDSQWXCVBN":
            if type(getattr(pygame, c)) == int and getattr(pygame, c) == index:
                return c
