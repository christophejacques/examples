import pygame
import json
from windowz import Window, Animation, Zone, Position, Couleur
from raccourci import Tache_Icone, Raccourci
from mouse import Mouse


class Ecran:

    def __init__(self, titre: str):
        self.windows = []
        self.icones = []
        self.raccourcis = []
        self.active_window = None
        self.active_icone = None
        pygame.init()

        self.theme_bg = Couleur(10, 130, 170).to_tuple()
        self.barre_color = Couleur(20, 20, 20, 100).to_tuple()
        self.image = pygame.image.load(r".\wallpaper.jpg")
        # self.image = pygame.image.load(r"D:\Mes Documents\Images\Wallpaper\Blacked_5_092.jpg")
        # self.image = pygame.image.load(r"D:\Mes Documents\Images\Wallpaper\Blue-and-Purple-Background-for-PC.jpg")
        *_, img_width, img_height = self.image.get_rect()
        self.img_coef = img_width / img_height
        
        self.set_zone((1600, 800))
        self.screen = pygame.display.set_mode(self.zone_barre_taches.p2.to_tuple(), flags=pygame.HWSURFACE+pygame.RESIZABLE, depth=32, display=0)

        pygame.display.set_caption(titre)
        Mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        # Mouse().set_cursor(pygame.SYSTEM_CURSOR_WAIT)
        
    @property
    def active_raccourci(self):
        for raccourci in self.raccourcis:
            if raccourci.is_under_cursor:
                return raccourci
        return None

    def shutdown(self):
        self.save_raccourcis()
        self.windows = []
        self.icones = []
        self.raccourcis = []
        self.active_window = None
        self.active_icone = None

    def set_zone(self, zone):
        self.background = pygame.transform.scale(self.image, (zone[0], zone[0]//self.img_coef))
        self.zone = Zone(Position(0, 0), Position(zone[0], zone[1]-30))
        self.zone_barre_taches = Zone(
            Position(self.zone.p1.x, self.zone.p2.y), 
            Position(self.zone.p2.x, self.zone.p2.y+30))
        Tache_Icone.zoneb = self.zone_barre_taches
        for window in self.windows:
            if window.etat[-1] == "maximized":
                window.set_zone(self.zone)
        if self.active_window:
            if self.active_window.etat[-1] == "maximized":
                self.active_window.set_zone(self.zone)
        if self.active_icone:
            for icone in (self.icones+[self.active_icone]):
                icone.generate()

    def get_window_by_idx(self, index):
        for window in (self.windows + [self.active_window]):
            if window.index == index:
                return window
        return None

    def get_icone_by_idx(self, index):
        for icone in (self.icones + [self.active_icone]):
            if icone.idx_window == index:
                return icone
        return None

    def open_all_raccourcis(self):
        for raccourci in self.raccourcis:
            self.create_new_window(raccourci.get_window())

    def add_raccourci(self, window, zone=None):
        if not isinstance(window, Window):
            raise TypeError("Le paramètre n'est pas de type Window")
        raccourci = Raccourci(window, zone)
        if not zone:
            if self.raccourcis:
                px = self.raccourcis[-1].zone.p2.x + 10
                py = self.raccourcis[-1].zone.p1.y
                if px > self.zone.p2.x:
                    px = 10
                raccourci.zone = Zone(
                    Position(px, py),
                    Position(px+80, py+60))
            else:
                raccourci.zone = Zone(
                    Position(10, 10), 
                    Position(90, 70))
        raccourci.screen = self.screen
        self.raccourcis.append(raccourci)
    
    def create_new_window(self, window: Window):
        if not isinstance(window, Window):
            raise TypeError(f"La fenêtre {window} n'est pas de type Window.")

        if window == self.active_window and self.active_window.etat[-1] == "minimized":
            self.active_window_by_index(window.index)
            return 
        if window in self.windows:
            self.active_window_by_index(window.index)
            return

        self.add(window)

    def add(self, window: Window):
        if not isinstance(window, Window):
            raise TypeError(f"La fenêtre {window} n'est pas de type Window.")

        if self.active_window:
            self.windows.append(self.active_window)
            self.icones.append(self.active_icone)

        window.screen = self.screen
        self.active_window = window
        icone = Tache_Icone(window.index, window.title)
        icone.screen = self.screen
        self.active_icone = icone

    def check_win_buttons(self, mouse_position: Position):
        if self.active_window is None:
            return False

        for window in reversed(self.windows + [self.active_window]):
            window.cursor_zone = None

        window_spoted = False
        for window in reversed(self.windows + [self.active_window]):
            if window.etat[-1] == "minimized":
                continue
            if window.zone_title.contains(mouse_position):
                if mouse_position.in_zone(window.zone_close):
                    window_spoted = True
                    window.cursor_zone = window.zone_close
                    break
                elif mouse_position.in_zone(window.zone_maximize):
                    window_spoted = True
                    window.cursor_zone = window.zone_maximize
                    break
                elif mouse_position.in_zone(window.zone_minimize):
                    window_spoted = True
                    window.cursor_zone = window.zone_minimize
                    break

            if window.zone.contains(mouse_position) and not window_spoted:
                window_spoted = True
                if Zone(
                    (window.zone_title.p1.x, window.zone_title.p2.y), (
                     window.zone.p1.x+window.zone.decal, window.zone.p2.y)).contains(mouse_position):
                    window.cursor_zone = "LEFT"
                    Mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
                elif Zone(
                    (window.zone_title.p2.x-window.zone.decal, window.zone_title.p2.y), (
                     window.zone.p2.x, window.zone.p2.y)).contains(mouse_position):
                    window.cursor_zone = "RIGHT"
                    Mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
                elif Zone(
                    (window.zone.p1.x, window.zone.p2.y-window.zone.decal), (
                     window.zone.p2.x, window.zone.p2.y)).contains(mouse_position):
                    window.cursor_zone = "BOTTOM"
                    Mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
                else:
                    Mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                break

            elif not window_spoted:
                Mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        return window_spoted

    def get_raccourci_clicked(self):
        for raccourci in (self.raccourcis):
            if raccourci.is_under_cursor:
                return raccourci
        return None

    def check_mouse_over_raccourcis(self, mouse_position: Position, window_spoted):
        for raccourci in (self.raccourcis):
            raccourci.is_under_cursor = False
        if window_spoted:
            return False

        if not mouse_position.in_zone(self.zone):
            return False

        for raccourci in (self.raccourcis):
            if mouse_position.in_zone(raccourci.zone):
                raccourci.is_under_cursor = True

    def check_mouse_over_icones(self, mouse_position: Position):
        if self.active_window is None:
            return False
        for icone in (self.icones + [self.active_icone]):
            icone.is_under_cursor = False

        if not mouse_position.in_zone(self.zone_barre_taches):
            return False

        for icone in (self.icones + [self.active_icone]):
            if mouse_position.in_zone(icone.zone):
                icone.is_under_cursor = True

    def select_raccourci(self, mouse_position: Position):
        for raccourci in self.raccourcis:
            if raccourci.contains(mouse_position):
                return True
        return False

    def select_window(self, mouse_position: Position):
        if self.active_window:
            if self.active_window.etat[-1] == "minimized" or not self.active_window.contains(mouse_position):
                for window in reversed(self.windows):
                    if window.etat[-1] != "minimized" and window.contains(mouse_position):
                        self.add(self.active_window)
                        self.active_window = window
                        self.windows.remove(window)

                        self.active_icone = self.get_icone_by_idx(window.index)
                        self.icones.remove(self.get_icone_by_idx(window.index))
                        Tache_Icone.nombre -= 1
                        break
            return mouse_position.in_zone(
                Zone(self.active_window.zone_title.p1, Position(
                        self.active_window.zone_minimize.p1.x, self.active_window.zone_minimize.p2.y)))
        return False

    def active_last_window(self):
        for window in reversed(self.windows):
            if window.etat[-1] != "minimized":
                self.add(self.active_window)
                self.active_window = window
                self.windows.remove(window)

                self.active_icone = self.get_icone_by_idx(window.index)
                self.icones.remove(self.get_icone_by_idx(window.index))
                Tache_Icone.nombre -= 1
                break

    def active_window_by_index(self, index):
        if self.get_window_by_idx(index) == self.active_window:
            if self.active_window.etat[-1] == "minimized":
                self.active_window.etat.pop()
                self.active_window.animation = Animation(
                    self.active_icone.zone,
                    self.active_window.zone_title)
            return

        for window in self.windows:
            if window.index == index:
                window_was_minimized = False
                if window.etat[-1] == "minimized":
                    window.etat.pop()
                    window_was_minimized = True

                self.add(self.active_window)
                self.active_window = window
                self.windows.remove(window)

                self.active_icone = self.get_icone_by_idx(window.index)
                self.icones.remove(self.get_icone_by_idx(window.index))
                Tache_Icone.nombre -= 1

                if window_was_minimized:
                    self.active_window.animation = Animation(
                        self.active_icone.zone,
                        self.active_window.zone_title)
                break

    def active_window_by_icone(self):
        if self.active_icone:
            if self.active_icone.is_under_cursor and self.active_window.etat[-1] != "minimized":
                self.active_window.etat.append("minimized")
                self.active_window.animation = Animation(
                    self.active_window.zone_title, 
                    self.active_icone.zone)
                
                self.active_last_window()
                return

        for icone in self.icones:
            if icone.is_under_cursor:
                window = self.get_window_by_idx(icone.idx_window)
                # print("select window ID:", icone.idx_window, window.index)
                self.add(self.active_window)
                self.active_window = window
                self.windows.remove(window)
                self.active_icone = self.get_icone_by_idx(window.index)
                self.icones.remove(self.get_icone_by_idx(window.index))
                Tache_Icone.nombre -= 1
                break

        if self.active_icone:
            if self.active_icone.is_under_cursor and self.active_window.etat[-1] == "minimized":
                self.active_window.etat.pop()
                self.active_window.animation = Animation(
                    self.active_icone.zone,
                    self.active_window.zone_title)
                return

    def update_window_index(self):
        index_max = -1
        for window in self.windows:
            if window.index > index_max:
                index_max = window.index
        Window.cindex = index_max+1

    def kill(self):
        if self.active_window:
            Tache_Icone.nombre -= 1
            deleted_index = self.active_icone.index
            self.active_window = None
            self.active_icone = None
            self.update_window_index()
            if self.windows:
                self.active_window = self.windows.pop()
                self.active_icone = self.get_icone_by_idx(self.active_window.index)

            if self.active_window:
                if self.get_icone_by_idx(self.active_window.index) in self.icones:
                    self.icones.remove(self.get_icone_by_idx(self.active_window.index))
                    for icone in self.icones:
                        if icone.index > deleted_index:
                            icone.set_index(icone.index-1)

                if self.active_icone.index > deleted_index:
                    self.active_icone.set_index(self.active_icone.index-1)

    def load_raccourcis(self):
        contenu = {}
        # self.add_raccourci(Window("Sublime Text", Zone(Position(100, 20), Position(500, 300)), Couleur(50, 70, 100)))
        # self.add_raccourci(Window("Mozilla Firefox", Zone(Position(140, 60), Position(540, 340)), Couleur(50, 70, 100)))
        # self.add_raccourci(Window("Ce PC", Zone(Position(180, 100), Position(580, 380)), Couleur(50, 70, 100)))
        # self.add_raccourci(Window("Microsoft Edge", Zone(Position(220, 140), Position(620, 420)), Couleur(50, 70, 100)))

        with open('desktop.json') as file_handle:
            contenu = json.loads(file_handle.read())
            for nom, donnees in contenu.items():
                self.add_raccourci(Window(
                    nom, Zone(*donnees["window"]), 
                    Couleur(*donnees["couleur"])), 
                    Zone(*donnees["raccourci"]))
        
    def save_raccourcis(self):
        contenu = {}
        with open('desktop.json', 'w') as file_handle:
            for raccourci in self.raccourcis:
                contenu[raccourci.title] = {}
                contenu[raccourci.title]["raccourci"] = raccourci.zone.p1.to_tuple(), raccourci.zone.p2.to_tuple()
                contenu[raccourci.title]["window"] = raccourci.window.zone.p1.to_tuple(), raccourci.window.zone.p2.to_tuple()
                contenu[raccourci.title]["couleur"] = raccourci.window.bg_color.to_tuple()
            file_handle.write(json.dumps(contenu))

    def refresh(self):
        # self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        for raccourci in self.raccourcis:
            raccourci.draw()
        for win in self.windows:
            win.draw(False)
        if self.active_window:
            self.active_window.draw(True)

        self.screen.fill(self.barre_color, rect=self.zone_barre_taches.to_tuple())
        if self.active_icone:
            for tache_icone in (self.icones+[self.active_icone]):
                tache_icone.draw(False)
            self.active_icone.draw(True)

        pygame.display.update()


if __name__ == "__main__":
    print("Compilation: OK")
