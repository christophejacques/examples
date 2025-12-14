import os
import platform


class PathException(Exception):
    pass


class Path:
    __path: str
    __filename: str

    def __init__(self, path: str = None, filename: str = "", controle: bool = True):
        self.__filename = filename
        self.__path = ""
        self.controle = controle
        if path:
            self.goto(path)
        else:
            self.goto(os.path.curdir)

    def to_parent(self):
        self.__path = os.path.abspath(os.path.join(self.__path, os.path.pardir))
        return self

    def to_root(self):
        self.__path = os.path.join(os.path.splitdrive(self.__path)[0], os.path.sep)
        return self

    @property
    def root(self):
        return Path(os.path.join(os.path.splitdrive(self.__path)[0], os.path.sep), self.__filename)

    @property
    def parent(self):
        return Path(os.path.abspath(os.path.join(self.__path, os.path.pardir)), self.__filename)

    def goto(self, *paths):
        for path in paths:
            new_path = os.path.join(self.__path, path)
            if not self.controle or os.path.exists(new_path):
                self.__path = os.path.abspath(new_path)
            else:
                raise PathException(f"Path: {new_path} does not exists.")            

    def set_filename(self, filename: str):
        self.__filename = filename
        return self

    def __str__(self):
        if self.__filename:
            return os.path.join(self.__path, self.__filename)
        else:
            return self.__path

    def __repr__(self):
        return f"'{self}'"


filename = "test.txt"
directory = Path(filename=filename)
print(directory)

directory.to_parent()
directory.goto("..", "..")
print(directory)

directory.to_root()
print(f"{directory}")
print(f"{directory!r}")
