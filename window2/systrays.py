from classes import SysTray, get_all_classes, Variable
from datetime import datetime
from audio import Audio


class SysTrayOff:
    pass


class SystemDateTime(SysTray):

    PRIORITY = 1
    DEFAULT_CONFIG = ("Date Time", (50, 200, 50))
    INITIAL_WIDTH = 200

    def __init__(self, screen, couleur):
        super().__init__(screen)
        self.update_screen(screen)
        self.get_theme()
        self.SYS_FONT = self.tools.font("courier", 16)

        etat_actuel = 1
        self.etat = self.registre.load("Etat", etat_actuel)

        if etat_actuel != self.etat:
            # On force la mise à jour du Format
            # pour charger la dernière valeur
            self.update_format()
        else:
            self.format = "%d/%m/%Y %H:%M:%S "
            self.systray_width = self.SYS_FONT.render(datetime.now().strftime(self.format), 
                False, self.couleur).get_size()[0]
            self.pending_action = None
        
    def get_theme(self):
        if self.theme.get_theme() == "CLAIR":
            self.couleur = (200, 200, 0)
            self.couleur = self.theme.get("FORE_COLOR")
        else:
            self.couleur = self.theme.get("FORE_COLOR")

    def get_action_callback(self):
        self.pending_action = None

    def get_action(self):
        if self.pending_action:
            return self.pending_action, self.get_action_callback
        else:
            return None

    def update_screen(self, screen):
        super().update_screen(screen)
        self.screen_width = screen.get_size()[0]

    def get_width(self):
        return self.systray_width

    def update_format(self):
        self.format = {
            1: "%d/%m/%Y %H:%M:%S ",
            2: " %d/%m/%Y ",
            3: " %H:%M:%S "
        }[self.etat]

        self.systray_width = self.SYS_FONT.render(datetime.now().strftime(self.format), 
            False, self.couleur).get_size()[0]

        self.pending_action = "UPDATE:SYSTRAYS"

    def mouse_up(self):
        self.etat += 1
        if self.etat > 3:
            self.etat = 1

        self.update_format()
        self.registre.save("Etat", self.etat)
        print("save registre:", "Etat", self.registre.get_all(), flush=True)
        
    def update(self):
        texte = datetime.now().strftime(self.format)
        self.text_surf = self.SYS_FONT.render(texte, False, self.couleur)
        self.systray_rect = self.tools.Rect(
            self.TEXT_OFFSET, self.TEXT_OFFSET, self.systray_width, 25)

    def draw(self):
        self.tools.fill((50, 10, 5))
        self.tools.fill(self.theme.get("TASK_BAR_COLOR"))
        self.tools.blit(self.text_surf, self.systray_rect)


class SoundView(SysTray):

    PRIORITY = 2
    DEFAULT_CONFIG = ("Sound", (50, 200, 50))
    INITIAL_WIDTH = 25

    def __init__(self, screen, couleur):
        super().__init__(screen)
        self.update_screen(screen)
        self.get_theme()
        self.SYS_FONT = self.tools.font("comicsans", 12)
        self.systray_width = 25
        self.etat = 1

    def get_theme(self):
        if self.theme.get_theme() == "CLAIR":
            self.couleur = (200, 200, 0)
        else:
            self.couleur = self.theme.get("FORE_COLOR")
        self.inactive_couleur = self.theme.get("INACTIVE_FORE_COLOR")

    def update_screen(self, screen):
        super().update_screen(screen)
        self.width = screen.get_size()[0]

    def get_width(self):
        return self.systray_width

    def mouse_move(self, *args):
        # print("mouse move", args)
        pass
    
    def mouse_up(self):
        self.etat += 1
        if self.etat > 2:
            self.etat = 1
        self.format, mute_unmute = {
            1: ("  <)  ", Audio.unmute_all_applications),
            2: (" <X)  ", Audio.mute_all_applications)
        }[self.etat]
        mute_unmute()

    def update(self):        
        self.systray_rect = self.tools.Rect(0, 0, self.systray_width, 25)

    def draw(self):
        self.tools.fill((10, 50, 5))
        x = 2*self.TEXT_OFFSET
        y = 10
        h = 4

        points = [(x, 12), (x+6, 7), (x+6, 17)]
        self.tools.polygon(self.couleur, points, 1)

        color = self.inactive_couleur if Audio.MUTE else self.couleur
        x += 8
        for i in range(3):
            self.tools.line(color, (x+2*i, y-2*i), (x+2*i, y+h+2*i))


class ThemeSelection(SysTray):

    PRIORITY = 2
    DEFAULT_CONFIG = ("Theme", (50, 200, 50))
    INITIAL_WIDTH = 20

    def __init__(self, screen, couleur):
        super().__init__(screen)
        self.update_screen(screen)
        self.get_theme()
        self.SYS_FONT = self.tools.font("comicsans", 12)

        theme_actuel = self.theme.get_theme()
        self.actual_theme = self.registre.load("Theme", theme_actuel)
        # print("Init Theme=", self.actual_theme, flush=True)

        if theme_actuel != self.actual_theme:
            # On force la mise à jour du Theme
            # pour charger la dernière valeur
            self.pending_action = "CHANGE_THEME:" + self.actual_theme
        else:
            self.pending_action = None
        
        self.systray_width = screen.get_size()[0]
        self.systray_height = screen.get_size()[1]

    def get_theme(self):
        # self.couleur = self.theme.get("FORE_COLOR")
        self.couleur = (200, 200, 200)
        self.pending_action = None

    def update_screen(self, screen):
        super().update_screen(screen)
        self.screen_width = screen.get_size()[0]

    def get_width(self):
        return self.systray_width

    def get_action(self):
        return self.pending_action

    def mouse_up(self):
        if self.actual_theme == "CLAIR":
            self.actual_theme = "SOMBRE"
        else:
            self.actual_theme = "CLAIR"

        self.registre.save("Theme", self.actual_theme)
        self.pending_action = "CHANGE_THEME:" + self.actual_theme

    def update(self):
        self.systray_rect = self.tools.Rect(
            self.TEXT_OFFSET, self.TEXT_OFFSET, self.systray_width, self.systray_height)

    def draw(self):
        self.tools.fill((10, 5, 50))

        x = 8
        y = 12
        r = 6
        points = (x+2, y)
        if self.actual_theme == "SOMBRE":
            self.tools.circle(self.couleur, points, r, 1)
        else:
            self.tools.circle(self.couleur, points, r)


if __name__ == '__main__':
    for cls in get_all_classes("SysTray"):
        print(cls)
