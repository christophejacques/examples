from abc import abstractmethod, ABCMeta
from os import path


class Application(metaclass=ABCMeta):
    MIN_SIZE = (200, 100)
    title = ""

    WINDOW_PROPERTIES = ["RESIZABLE"]
    DEFAULT_CONFIG = ("?", (0, 0, 0))

    @abstractmethod
    def __init__(self, parent, screen, *args):
        pass

    def post_init(self):
        pass

    def close(self):
        print("Application closed !")

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
        pass

    @abstractmethod
    def draw(self):
        pass


class NoApplication(Application):

    DEFAULT_CONFIG = ("No Application", (80, 80, 80))

    def __init__(self, parent, screen, *args):
        self.parent = parent
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

    def get_action(self):
        return self.action

    def update(self):
        if self.parent.keypressed():
            self.touche = self.parent.get_key()
            if self.touche == 27:
                self.action = "QUIT"

    def draw(self):
        pass


def make_path(*args):
    return path.join(*args)
