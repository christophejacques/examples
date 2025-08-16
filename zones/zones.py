from __future__ import annotations
from typing import Optional


OPTIONS: tuple = ("side", "x", "y", "width", "height", "position", "relwidth", "relheight", "padx", "pady")


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)

class Screen:
    size: list[int] = [1200, 600]


class Zone:
    parent_size: list = [0, 0] + Screen.size
    screen: list
    parent: Optional[Zone]
    coords: list[int]
    contenu: list[Zone]

    def __init__(self, 
        position: str="", 
        **options):

        for option in options:
            if option not in OPTIONS:
                raise TypeError(f"'{option}' est un argument keyword invalide pour {self.__class__.__name__}()")

        self.parent = None
        self.contenu = list()

        self.x = None
        self.y = None
        self.width = None
        self.height = None

        self.position = position.upper()
        if self.position == "ROOT":
            self.coords = self.parent_size.copy()

        self.options = options

        # Mettre en place calcul de la zone


    def __str__(self):
        res: str = ""
        if self.contenu:
            res = " ["
            for zone in self.contenu:
                res += f"{zone}, "

            res = res[:-2]
            res += "]"

        return f"{self.position} {self.coords}" + res

    def add(self, zone: Zone):
        zone.parent = self
        side = None

        for option in zone.options:
            match option:
                case "side":
                    side = zone.options.get(option, "").upper()

                case "x":
                    zone.x = zone.options.get(option)

                case "y":
                    zone.y = zone.options.get(option)

                case "width":
                    zone.width = zone.options[option]

                case "height":
                    zone.height = zone.options[option]

                case default:
                    pass

        if zone.width is None:
            relwidth = zone.options.get("relwidth")
            if relwidth:
                zone.width = int(self.parent_size[2] * relwidth)
            else:
                zone.width = self.parent_size[2]

            if side == "RIGHT":
                zone.x = self.parent_size[2] - zone.width
            else:
                zone.x = self.parent_size[0]

        if zone.height is None:
            relheight = zone.options.get("relheight")
            if relheight:
                zone.height = int(self.parent_size[3] * relheight)
            else:
                zone.height = self.parent_size[3]

            if side == "BOTTOM":
                zone.y = self.parent_size[3] - zone.height
            else:
                zone.y = self.parent_size[1]

        if zone.x is None:
            if side == "RIGHT":
                zone.x = self.parent_size[2] - self.parent_size[0]
            else:
                zone.x = self.parent_size[0]
        if zone.y is None:
            if side == "BOTTOM":
                zone.y = self.parent_size[3] - self.parent_size[1]
            else:
                zone.y = self.parent_size[1]

        zone.coords = [zone.x, zone.y, zone.width, zone.height]

        self.contenu.append(zone)


# root = Zone(coords=[0, 0, 1200, 600])
root = Zone("root")
print(0, root)
root.add(Zone( side="top", relheight=0.2))
print(1, root)
root.add(Zone( side="bottom", relheight=0.2))
print(2, root)
root.add(Zone( height=100))
print(3, root)
