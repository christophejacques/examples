import json

from _io import TextIOWrapper
from os import environ
from typing import Dict, Any

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


class Unique:

    __instance: Dict = dict()

    def __new__(self, *args):
        if self.__name__ in Unique.__instance:
            return Unique.__instance.get(self.__name__)

        new_instance = super().__new__(self)
        Unique.__instance[self.__name__] = new_instance
        return new_instance


class Sauvegarde(Unique):

    __content: Dict = dict()
    __updated: bool = False
    __loaded: bool = False

    def __enter__(self, *args):
        self.load()
        return self

    def __exit__(self, *args):
        self.save()
        return self

    def load(self) -> None:
        fhandle: TextIOWrapper

        if self.__loaded:
            return

        # fprint("Sauvegarde chargée")
        try:
            with open("save.json", encoding="utf-8") as fhandle:
                self.__content = json.load(fhandle)
                self.__updated = False
                self.__loaded = True

        except FileNotFoundError as erreur:
            self.__content = {}
            self.__updated = True
            self.__loaded = True
            fprint("Sauvegarde.load(): FileNotFoundError", erreur)

        except json.decoder.JSONDecodeError as erreur:
            fprint("Sauvegarde.load(): JSONDecodeError", erreur)

    def save(self) -> None:
        if not self.__updated:
            return

        fhandle: TextIOWrapper

        try:
            with open("save.json", "w", encoding="utf-8") as fhandle:
                json.dump(self.__content, fhandle)
                self.__updated = False
                # fprint("Sauvegarde enregistrée.")

        except Exception as erreur:
            fprint("Sauvegarde.save():", erreur)

    def reset(self) -> None:
        self.__content = dict()
        self.__updated = True

    def set(self, variable: str, contenu: Any) -> None:
        self.__content[variable] = contenu
        self.__updated = True

    def get(self, variable: str, default: Any = None) -> Any:
        return self.__content.get(variable, default)

    def get_content(self, chemin_registre: str, default: Any = None) -> Any:
        content: dict = self.__content
        # fprint("load >", chemin_registre, end=" = ")

        # Recuperation des informations du chemin_registre
        for registre in chemin_registre.split("."):
            if registre not in content:
                self.set_content(chemin_registre, default)
                # fprint("default: ", default)
                return default

            content = content.get(registre, {})

        # Lecture de la cle de registre finale
        # fprint("return", content)
        return content

    def set_content(self, chemin_registre: str, valeur: Any) -> None:
        content: dict = self.__content

        # Creation / Recuperation des informations du chemin_registre
        for registre in chemin_registre.split(".")[:-1]:
            temp = content.get(registre, None)
            if temp is None:
                content[registre] = dict()
                content = content.get(registre, {})
                self.__updated = True
            else:
                content = temp

        # Creation / Mise a jour de la cle de registre finale
        registre = chemin_registre.split(".")[-1]
        
        # fprint("registre:", registre, "- valeur:", valeur, "- actuel:", 
        #     content.get(registre, "?"))

        if not self.__updated and registre not in content:
            self.__updated = True
            content[registre] = valeur

        elif content[registre] != valeur:
            self.__updated = True
            content[registre] = valeur


def fprint(*args, **kwargs) -> None:
    print(*args, **kwargs, flush=True)


def get_pygame_const_name(index):
    for c in dir(pygame):
        if c[0] in "AZERTYUIOPMLKJHGFDSQWXCVBN":
            if type(getattr(pygame, c)) == int and getattr(pygame, c) == index:
                return c


if __name__ == "__main__":

    with Sauvegarde() as save:
        save.set_content("Lecteur.Version", "1.0")
        fprint("Version Lecteur:", end="")
        fprint(save.get_content("Lecteur.Version", "0.0"))

        save.set_content("Messages.Version", "1.0")
        fprint("Version Messages:", end="")
        fprint(save.get_content("Messages.Version", "0.0"))
