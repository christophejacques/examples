from classes import Application, fprint


class Modele(Application):

    DEFAULT_CONFIG: tuple = ("Modele", (150, 150, 150))
    MIN_SIZE: tuple = (600, 400)
    WINDOW_PROPERTIES: list = []

    def __init__(self, screen, *args):
        # super().__init__(screen)
        self.title = self.DEFAULT_CONFIG[0]
        self.action = ""

    def post_init(self):
        self.get_theme()
        self.set_title(self.title)
        self.win_resize("BOTTOM RIGHT", 0, 0, *self.MIN_SIZE)

    def resize(self, screen):
        pass

    def get_theme(self):
        print(self.theme.get_theme())

    def mouse_enter(self, mouseX, mouseY):
        pass

    def mouse_exit(self):
        pass

    def keypressed(self, event):
        # print(event, flush=True)
        touche = self.keys.get_key()            

    def keyreleased(self, event):
        # print(event, flush=True)
        # touche = self.keys.get_key()
        if event.key == 27:
            self.action = "QUIT"
                
    def mouse_move(self, mouseX, mouseY):
        pass

    def mouse_button_down(self, mouseX, mouseY, button):
        pass

    def mouse_button_up(self, mouseX, mouseY, button):
        pass

    def get_action(self):
        return self.action

    def update(self):
        pass

    def draw(self):
        pass


if __name__ == '__main__':
    from exec import run
    run(locals())
