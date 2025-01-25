import os
import platform

from typing import Self, Generator


class PathException(Exception):
    pass


# Liste des types d'entrees pour la fonction scandir
TYPE_ENTREE: dict = {"FILE": "is_file",
             "DIRECTORY": "is_dir",
             "ALL": "__str__"}


class Path:
    __path: str
    __filename: str

    def __init__(self, path: str = ".", filename: str = "", controle: bool = True):
        """
        path : chemin
        filename : fichier avec extension
        controle : permet d'indiquer si l'on controle l'existance du chemin
        """
        self.__filename = filename
        self.__path = ""
        self.controle: bool = controle
        if path:
            self.goto(path)
        else:
            self.goto(os.path.curdir)

    def to_parent(self) -> Self:
        self.__path = os.path.abspath(os.path.join(self.__path, os.path.pardir))
        return self

    def to_root(self) -> Self:
        self.__path = os.path.join(os.path.splitdrive(self.__path)[0], os.path.sep)
        return self

    def to_home(self) -> Self:
        self.__path = os.path.abspath(os.environ["USERPROFILE"])
        return self

    @property
    def root(self):
        return Path(os.path.join(os.path.splitdrive(self.__path)[0], os.path.sep), self.__filename)

    @property
    def parent(self):
        return Path(os.path.abspath(os.path.join(self.__path, os.path.pardir)), self.__filename)

    def goto(self, *paths) -> None:
        for path in paths:
            if path == "~":
                self.to_home()
                continue

            new_path = os.path.join(self.__path, path)
            if not self.controle or os.path.exists(new_path):
                self.__path = os.path.abspath(new_path)
            else:
                raise PathException(f"Path: {new_path} does not exists.")            

    def set_filename(self, filename: str) -> Self:
        self.__filename = filename
        return self

    def get_drive(self) -> str:
        return os.path.splitdrive(self.__path)[0]

    def get_directory(self) -> str:
        return self.__path

    def get_filename(self) -> str:
        return self.__filename

    def scandir(self, type_entree: str = "ALL") -> Generator:
        if not TYPE_ENTREE.get(type_entree):
            raise ValueError(f"Le parametre 'type d'entree' ({type_entree}) doit etre FILE, DIRECTORY ou ALL (defaut)")

        for file_or_dir in os.scandir(self.__path):
            if getattr(file_or_dir, TYPE_ENTREE[type_entree])():
                yield file_or_dir

    def __str__(self) -> str:
        if self.__filename:
            return os.path.join(self.__path, self.__filename)
        else:
            return self.__path

    def __repr__(self) -> str:
        return f"'{self}'"


if __name__ == "__main__":
    print("plateforme:", platform.system())

    filename = "test.txt"
    directory = Path(filename=filename)
    print(directory)

    directory.to_parent()
    directory.goto("..", "..")
    print(directory)

    directory.to_root()
    print(f"{directory}")
    print(f"{directory!r}")

    directory.goto("D:")
    print(f"{directory}")
    directory.to_parent()
    print(directory.get_drive())

    directory.goto("~")
    print(f"{directory}")
    print(directory.get_drive())
    directory.to_root()
    print(list(directory.scandir("FILE")))
    