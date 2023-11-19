import traceback
from referentiel import AbstractZoneContent, AbstractZone, Position
from referentiel import GetFilesDirectory


class Window(AbstractZone):

    def __init__(self, screen, bg_color, zone):
        super().__init__()
        self.screen = screen
        self.bg_color = bg_color
        self.zone = zone
        self.zones = []
        self.rules = []
        self.mouse_entered = False
        self.mouse = Position(0, 0)
        self.sound_directory = GetFilesDirectory(r"D:\Mes Documents\Musique\Jeux\Chrono Trigger")

    def set_zone(self, zone):
        self.zone = zone
        self.optimize()

    def add(self, nom, zone, rules):
        zone.set_screen(self.screen)
        zone.nom = nom
        self.zones.append(zone)
        self.rules.append(rules)

    def get_zone(self, nom):
        for zone in self.zones:
            if zone.nom == nom:
                return zone

    def optimize(self):

        def iif(condition, si_vrai, si_faux):
            return si_vrai if condition else si_faux

        def nfz(fonction, valeur, si_null_ou_erreur):
            try:
                return eval(f"{fonction}({valeur})")
            except Exception as e:
                print("Error:", e)
                return si_null_ou_erreur

        def wait(formule):
            return formule

        def fisactive(nom_zone):
            return self.get_zone(nom_zone).active

        def ftop(nom_zone):
            if self.get_zone(nom_zone).active:
                return self.get_zone(nom_zone).zone[0][1]
            else:
                return 0

        def fbottom(nom_zone):
            if self.get_zone(nom_zone).active:
                return self.get_zone(nom_zone).zone[1][1]
            else:
                return 0

        def fleft(nom_zone):
            if self.get_zone(nom_zone).active:
                return self.get_zone(nom_zone).zone[0][0]
            else:
                return 0

        def fright(nom_zone):
            if self.get_zone(nom_zone).active:
                return self.get_zone(nom_zone).zone[1][0]
            else:
                return 0

        width, height = self.zone[1]
        left, top, right, bottom = 0, 0, 0, 0

        for i, zone in enumerate(self.zones):
            if zone.active:
                left = int(eval(self.rules[i].get("left", "0")))
                top = int(eval(self.rules[i].get("top", "0")))
                right = int(eval(self.rules[i].get("right", "width")))
                bottom = int(eval(self.rules[i].get("bottom", "height")))

                new_zone = ((left, top), (right, bottom))
                zone.set_zone(new_zone)

    def update(self):
        if self.is_display_active():
            for zone in self.zones:
                zone.update()

    def draw(self):
        if self.is_display_active():
            self.screen.fill(self.bg_color, rect=self.zone)
            for zone in self.zones:
                zone.draw()

    def on_click(self):
        resTotal = []
        if self.has_registered("on_click") and self.mouse.in_zone(self.zone):
            res = self.methods.get("on_click")
            if res:
                resTotal.append(res)

        for zone in self.zones:
            if zone.has_registered("on_click") and self.mouse.in_zone(zone.zone):
                res = zone.on_click()
                if res:
                    resTotal += res
        return resTotal

    def on_mouse_enter(self, mouse_position) -> list:
        cmds: list = []
        if self.has_registered("on_mouse_enter") and not self.mouse_entered:
            super().on_mouse_enter(mouse_position)

            self.mouse = Position(*mouse_position)
            for zone in self.zones:
                if self.mouse.in_zone(zone.zone):
                    if zone.has_registered("on_mouse_enter") and not zone.mouse_entered:
                        for cmd in zone.on_mouse_enter(mouse_position):
                            cmds.append(cmd)

        return cmds

    def on_mouse_move(self, mouse_position):
        cmds: list = []
        self.mouse = Position(*mouse_position)
        for zone in self.zones:
            if self.mouse.in_zone(zone.zone):
                if self.has_registered("on_mouse_enter") and zone.has_registered("on_mouse_enter") and not zone.mouse_entered:
                    for cmd in zone.on_mouse_enter(mouse_position):
                        cmds.append(cmd)

                if self.has_registered("on_mouse_move") and zone.has_registered("on_mouse_move"):
                    for cmd in zone.on_mouse_move(mouse_position):
                        cmds.append(cmd)
            else:
                if self.has_registered("on_mouse_exit") and zone.has_registered("on_mouse_exit") and zone.mouse_entered:
                    for cmd in zone.on_mouse_exit():
                        cmds.append(cmd)
        return cmds

    def on_mouse_exit(self):
        cmds: list = []
        if self.has_registered("on_mouse_exit") and self.mouse_entered:
            super().on_mouse_exit()
            for zone in self.zones:
                if zone.has_registered("on_mouse_exit") and zone.mouse_entered:
                    for cmd in zone.on_mouse_exit():
                        cmds.append(cmd)
        return cmds


def main():
    try:
        assert isinstance(Window(None, 0, 0), AbstractZoneContent), "Problème de la classe StarField"
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main()
