from classes import Application


class NoApplication(Application):

    DEFAULT_CONFIG = ("No Application", (80, 80, 80))
    WINDOW_PROPERTIES = []

    def __init__(self, *args):
        self.title = self.DEFAULT_CONFIG[0]
        self.action = ""

    def post_init(self):
        # self.resize(screen)
        self.get_theme()

    def get_theme(self):
        self.fore_color = self.theme.get("FORE_COLOR")
        self.back_color = self.theme.get("BACKGROUND_COLOR")
        self.draw_once()

    def resize(self):
        self.set_title(self.title + " Resize({}x{})".format(*self.tools.get_size()))

    def mouse_enter(self, mouseX, mouseY):
        self.set_title(self.title + " Mouse_Enter()")

    def mouse_exit(self):
        self.set_title(self.title + " Mouse_Exit()")

    def mouse_move(self, mouseX, mouseY):
        self.set_title(self.title + f" Mouse_Move({mouseX}, {mouseY})")
        if mouseX > 200 and mouseY > 200:
            a = 1 / 0

    def mouse_button_up(self, mouseX, mouseY, button):
        self.set_title(self.title + f" Mouse_button_up({button})")

    def get_action(self):
        return self.action

    def update(self):
        pass

    def draw_once(self):
        w, h = self.tools.get_size()
        self.tools.fill(self.back_color)
        self.tools.line(self.fore_color, (200, 200), (200, h))
        self.tools.line(self.fore_color, (200, 200), (w, 200))

    def draw(self):
        pass

if __name__ == '__main__':
    from exec import run
    run(locals())
