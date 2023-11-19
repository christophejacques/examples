import traceback

from referentiel import AbstractZoneContent, AbstractZone, Position
from referentiel import zone_color


class Zone(AbstractZone):
    index = 0

    def __init__(self, bg_color, zone=None):
        super().__init__()
        self.index = Zone.index
        Zone.index += 1
        self.objets = []
        self.active = True
        self.color = zone_color
        self.bg_color = bg_color
        self.screen = None
        self.mouse_entered = False
        self.mouse = Position(0, 0)
        if zone:
            self.set_zone(zone)
        else:
            self.set_zone(((0, 0), (0, 0)))

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def set_zone(self, zone):
        self.zone = zone
        for objet in self.objets:
            objet.set_zone(self.zone)

    def add(self, objet):
        objet.set_screen(self.screen)
        objet.set_zone(self.zone)
        self.objets.append(objet)

    def update(self):
        if not self.active:
            return

        for objet in self.objets:
            objet.update()

    def draw(self):
        if not self.active:
            return

        left, top = self.zone[0]
        width, height = self.zone[1]
        zone = (self.zone[0], (width-left, height-top))

        # Fond de la zone
        if self.bg_color:
            self.screen.fill(self.bg_color, rect=zone)

        for objet in self.objets:
            objet.draw()

        # Cadre de la zone
        if self.color:
            self.draw_rect(self.color, zone, 1)

    def on_click(self):
        resTotal = []
        res = self.methods.get("on_click")
        if res:
            resTotal += [res]
        for objet in self.objets:
            if objet.has_registered("on_click") and self.mouse.in_zone(objet.zone):
                res = objet.on_click()
                if res:
                    resTotal += res
        return resTotal

    def on_mouse_enter(self, mouse_position):
        cmds: list = []
        if not self.active:
            return []
        self.mouse_entered = True
        res = self.methods.get("on_mouse_enter")
        if res:
            cmds += [res]

        self.mouse = Position(*mouse_position)
        for objet in self.objets:
            if self.mouse.in_zone(objet.zone):
                if objet.has_registered("on_mouse_enter") and not objet.mouse_entered:
                    for cmd in objet.on_mouse_enter(mouse_position):
                        cmds.append(cmd)

        return cmds

    def on_mouse_move(self, mouse_position):
        cmds: list = []
        self.mouse = Position(*mouse_position)
        for objet in self.objets:
            if self.mouse.in_zone(objet.zone):
                if objet.has_registered("on_mouse_enter") and not objet.mouse_entered:
                    for cmd in objet.on_mouse_enter(mouse_position):
                        cmds.append(cmd)

                if objet.has_registered("on_mouse_move"):
                    for cmd in objet.on_mouse_move(mouse_position):
                        cmds.append(cmd)
            else:
                if objet.has_registered("on_mouse_exit") and objet.mouse_entered:
                    for cmd in objet.on_mouse_exit():
                        cmds.append(cmd)

        return cmds

    def on_mouse_exit(self):
        self.mouse_entered = False
        cmds: list = []
        res = self.methods.get("on_mouse_exit")
        if res:
            cmds += [res]

        for objet in self.objets:
            if objet.has_registered("on_mouse_exit") and objet.mouse_entered:
                for cmd in objet.on_mouse_exit():
                    cmds.append(cmd)

        return cmds


def main():
    try:
        assert isinstance(Zone(0), AbstractZoneContent), "Problème de la classe Zones"
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main()
