import pygame  # noqa: E402

from time import perf_counter
from threading import Thread
from typing import List, Tuple, Optional, Dict

from general import Variable, fprint
from outils import Ascenseur
from mail import Mail


class Repertoire:

    colors: Dict = {
        True: (50, 200, 150),
        False: (200, 200, 200)
    }

    hauteur_ligne: int = 24
    largeur_niveau: int = 12

    libelle: str
    sdir_libelle: str
    selected: bool
    niveau: int
    nb_sdir: int

    surface: pygame.surface.Surface
    sdir_surf: pygame.surface.Surface

    x: int
    w: int
    h: int
    sdir_x: int
    sdir_w: int
    sdir_h: int

    has_sdir: bool
    visible: bool

    mouse_over: bool
    sdir_mouse_over: bool
    mouse_button_pushed: bool
    sdir_mouse_button_pushed: bool

    def __init__(self, ident: str, libelle: str, affichage: str, 
            niveau: int, selected: bool = False, nb_dirs: int = 0):

        self.id = ident
        self.libelle = libelle
        self.sdir_libelle = ""
        self.affichage = affichage
        self.niveau = niveau
        self.nb_sdir = nb_dirs
        self.has_sdir = nb_dirs > 1
        self.x = Repertoire.largeur_niveau * self.niveau
        self.sdir_x = self.x - 18

        self.visible = True
        self.mouse_over = False
        self.sdir_mouse_over = False
        self.mouse_button_pushed = False
        self.sdir_mouse_button_pushed = False
        self.select(selected)

    @staticmethod
    def y(ligne: int) -> int:
        return 10 + Repertoire.hauteur_ligne * ligne
    
    def select(self, selected: bool) -> None:
        self.selected = selected
        self.set_libelle(self.libelle)
        if self.has_sdir:
            self.set_sdir_libelle("+")

    def set_visible(self, visible: bool):
        self.visible = visible

    def set_libelle(self, libelle: str):
        self.libelle = libelle
        self.surface = Variable.SysFont2.render(libelle, False, 
            Repertoire.colors.get(self.selected, (255, 0, 0)))

        self.w, self.h = self.surface.get_size()

    def set_sdir_libelle(self, libelle: str):
        self.sdir_libelle = libelle
        self.sdir_surf = Variable.SysFont2.render(libelle, False, 
            Repertoire.colors.get(self.selected, (255, 0, 0)))

        self.sdir_w, self.sdir_h = self.sdir_surf.get_size()

    def sdir_to_screen(self, ligne: int) -> Tuple:
        return (self.sdir_surf, (self.sdir_x, self.y(ligne)))

    def to_screen(self, ligne: int) -> Tuple:
        return (self.surface, (self.x, self.y(ligne)))
        

class Repertoires:

    liste: List[Repertoire]

    max: int 
    selected: str
    decal: int 
    nb_dirs: int

    surface: pygame.surface.Surface
    x: int
    y: int
    w: int
    h: int
    visible: bool
    loaded: bool
    mouse_over: bool

    mouse_over_y: int

    actions: Optional[str]

    def __init__(self, screen: pygame.surface.Surface, coords: Tuple):
        self.liste = list()

        self.decal = 0
        self.nb_dirs = 0

        self.coords = pygame.Rect(coords)
        self.update_screen(screen, coords)
        self.set_visible(True)

        self.loaded = False
        self.selected = "INBOX"
        self.mouse_over = False
        self.mouse_over_y = 0

        self.actions = None

    def update_screen(self, 
            screen: pygame.surface.Surface, coords: Optional[Tuple] = None) -> None:

        if coords is not None:
            self.coords = pygame.Rect(coords)

        self.surface = screen.subsurface(self.coords)
        self.x, self.y, w, self.h = self.coords
        self.w = w - 1
        self.max = self.h // Repertoire.hauteur_ligne

        if self.decal + self.max > self.nb_dirs:
            self.decal = max(0, self.nb_dirs - self.max)

        self.update_ascenseur()

    def update_ascenseur(self) -> None:
        liste: List[Repertoire]
        nb_dirs: int

        liste = list(filter(lambda x: x.visible, self.liste))
        nb_dirs = len(liste)

        self.ascenseur = Ascenseur(
            self.surface, self.w, self.h, nb_dirs, self.max, posy=-1, hauteur=self.h+2)
        self.ascenseur.update(self.decal)

    def get_actions(self) -> Optional[str]:
        if self.actions is None:
            return None

        actions = self.actions
        self.actions = None
        return actions

    def mouse_move(self, mouse_pos: Tuple) -> None:
        mx: int
        my: int
        liste: List[Repertoire]

        self.mouse_over = True
        self.mouse_over_y = 0
        mx, my = mouse_pos

        liste = list(filter(lambda x: x.visible, self.liste))[self.decal:self.decal+self.max]

        for idx, repertoire in enumerate(liste):
            if repertoire.id == "MAIL":
                continue

            surface, (x, y) = repertoire.to_screen(idx)

            if y < my < y + repertoire.hauteur_ligne:
                self.mouse_over_y = y - 2

                if repertoire.has_sdir:
                    repertoire.sdir_mouse_over = mx < x
                    repertoire.mouse_over = not repertoire.sdir_mouse_over
                else:
                    repertoire.mouse_over = True
                    repertoire.sdir_mouse_over = False

            else:
                repertoire.mouse_over = False
                repertoire.sdir_mouse_over = False

    def mouse_exit(self) -> None:
        self.mouse_over = False
        self.mouse_over_y = 0

    def mouse_wheel(self, x, y) -> None: 
        if y < 0 and self.decal - y + self.max > self.nb_dirs:
            return

        self.decal += -y
        if self.decal < 0:
            self.decal = 0

        self.ascenseur.update(self.decal)

    def mouse_button_down(self, mouse_pos: Tuple, button: int) -> None:
        for idx, repertoire in enumerate(self.liste[self.decal:self.decal+self.max]):
            if repertoire.id == "MAIL":
                continue

            repertoire.mouse_button_pushed = repertoire.mouse_over
            repertoire.sdir_mouse_button_pushed = repertoire.sdir_mouse_over
    
    def mouse_button_up(self, mouse_pos: Tuple, button: int) -> None:
        for idx, repertoire in enumerate(self.liste[self.decal:self.decal+self.max]):
            if repertoire.id == "MAIL" or not (
                    repertoire.mouse_button_pushed or repertoire.sdir_mouse_button_pushed):
                continue

            if repertoire.mouse_button_pushed:
                self.select(repertoire.id)
            else:
                self.toggle_sdir(repertoire.id)

            repertoire.mouse_button_pushed = False
            repertoire.sdir_mouse_button_pushed = False

    def clear(self) -> None:
        self.liste.clear()
    
    def get_repertoires(self) -> None:
        mail: Mail

        connu: bool
        num: int
        ident: str
        repertoire: str

        repertoires_connus: List[Tuple] = list()
        repertoires_autres: List[Tuple] = list()

        debut = perf_counter()

        self.liste.append(Repertoire("MAIL", "Boîte de réception", "", 1, False, 0))

        mail = Mail()

        try:
            mail.connect()
            for connu, num, ident, repertoire, true_name in mail.get_dirs():
                if connu:
                    repertoires_connus.append((num, ident, repertoire, true_name))
                else:
                    repertoires_autres.append((num, ident, repertoire, true_name))

        except Exception as erreur:
            fprint("get_dirs():", erreur)

        # tri des repertoire par id
        repertoires_connus.sort(key=lambda elt: elt[0])

        # tri des repertoire par libelle
        repertoires_autres.sort(key=lambda elt: elt[2])

        for value in repertoires_connus:
            num, ident, repertoire, true_name = value
            try:
                nombre_sous_repertoires = len(list(mail.get_dirs(true_name)))
            except Exception as erreur:
                nombre_sous_repertoires = 0
                fprint("Ss rep", true_name, ":", erreur)

            self.liste.append(Repertoire(ident, repertoire, true_name, 2, 
                ident == self.selected, nombre_sous_repertoires))

        for value in repertoires_autres:
            num, ident, repertoire, true_name = value
            try:
                nombre_sous_repertoires = len(list(mail.get_dirs(repertoire)))
            except Exception as erreur:
                nombre_sous_repertoires = 0
                fprint("Ss rep", true_name, ":", erreur)

            self.liste.append(Repertoire(ident, repertoire, true_name, 2, 
                ident == self.selected, nombre_sous_repertoires))

        try:
            mail.disconnect()
        except Exception:
            pass

        self.loaded = True

        self.nb_dirs = len(self.liste)

        self.ascenseur = Ascenseur(self.surface, self.w, self.h, self.nb_dirs, self.max)
        self.ascenseur.update(self.decal)

        fin = perf_counter()
        temps_execution = fin - debut
        fprint(f"load repertoires : {temps_execution:.4f} secondes")

    def load(self) -> None:
        thread: Thread

        self.loaded = False
        thread = Thread(target=self.get_repertoires)
        thread.start()

    def get(self, ident: str) -> Repertoire:
        for repertoire in self.liste:
            if repertoire.id == ident:
                return repertoire

        raise Exception(f"Le repertoire {ident} n'existe pas")

    def index(self, ident: str, visible_only: bool = False) -> int:
        index: int

        index = 0
        for repertoire in self.liste:
            if repertoire.id == ident:
                return index

            if visible_only:
                index += 1 if repertoire.visible else 0
            else:
                index += 1

        raise Exception(f"Le repertoire {ident} n'existe pas")

    def set_visible_sdir(self, index: int, visible: bool) -> None:
        niveau = self.liste[index].niveau

        for repertoire in self.liste[index:]:
            if repertoire.niveau < niveau:
                break

            repertoire.set_visible(visible)

    def show_sdir(self, index: int) -> None:
        self.set_visible_sdir(index, True)

    def hide_sdir(self, index: int) -> None:
        self.set_visible_sdir(index, False)

    def toggle_sdir(self, ident: str) -> None:
        repertoire = self.get(ident)

        if not repertoire.has_sdir:
            return

        libelle = " - " if repertoire.sdir_libelle == "+" else "+"
        repertoire.set_sdir_libelle(libelle)

        index = 1 + self.index(ident)
        if len(self.liste) > index and self.liste[index].niveau == 1+repertoire.niveau:
            self.set_visible_sdir(index, not self.liste[index].visible)
            self.update_ascenseur()
            return
        
        mail = Mail()
        repertoires = list()

        try:
            mail.connect()
            for connu, num, new_ident, new_repertoire, true_name in mail.get_dirs(ident):
                if new_ident == ident:
                    continue

                new_repertoire = new_repertoire.split("/")[-1]
                repertoires.append((num, new_ident, new_repertoire, new_repertoire))

        except Exception as erreur:
            fprint("get_dirs():", erreur)

        # tri des repertoire par libelle
        repertoires.sort(key=lambda elt: elt[2])

        for value in repertoires:
            num, ident, new_repertoire, true_name = value
            try:
                search_repertoire = f'"{new_repertoire}"'
                nombre_sous_repertoires = len(list(mail.get_dirs(search_repertoire)))
            except Exception as erreur:
                nombre_sous_repertoires = 0
                fprint("Ss rep", true_name, ":", erreur)

            self.liste.insert(index, Repertoire(
                ident, new_repertoire, true_name, 1+repertoire.niveau, 
                False, nombre_sous_repertoires))

            index += 1

        try:
            mail.disconnect()
        except Exception:
            pass

        self.nb_dirs = len(self.liste)
        self.ascenseur = Ascenseur(self.surface, self.w, self.h, self.nb_dirs, self.max)
        self.ascenseur.update(self.decal)

    def select(self, ident: str) -> None:
        if ident == self.selected:
            return

        # on commence à 1 car le numero 0 ne correspond à aucun répertoire
        for idx, repertoire in enumerate(self.liste[1:]):
            if ident == repertoire.id:
                repertoire.select(True)
                self.selected = repertoire.id
                self.actions = f"DIR={self.selected}"

            elif repertoire.selected:
                repertoire.select(False)

    def toggle(self) -> None:
        self.visible = not self.visible

    def set_visible(self, visible: bool) -> None:
        self.visible = visible

    def to_screen(self) -> List[Tuple]:
        dirs_texte: List[Tuple] = list()
        index: int

        index = 0
        # for repertoire in self.liste[self.decal:self.decal+self.max]:
        for repertoire in self.liste[self.decal:]:
            if not repertoire.visible:
                continue

            dirs_texte.append(repertoire.to_screen(index))
            index += 1
            if index > self.max:
                break

        return dirs_texte

    def draw(self) -> None:
        if not self.visible:
            return 

        # directories
        self.surface.fill((10, 20, 20))
        pygame.draw.line(self.surface, (50, 200, 150), (self.w, 0), (self.w, self.h))

        if not self.loaded:
            return 

        if self.mouse_over_y:
            pygame.draw.rect(self.surface, (30, 50, 50),
                (0, self.mouse_over_y, self.w, Repertoire.hauteur_ligne))                

        self.surface.blits(self.to_screen())

        liste: List[Repertoire]
        liste = list(filter(lambda x: x.visible, self.liste))[self.decal:self.decal+self.max]

        for idx, repertoire in enumerate(liste):
            if repertoire.has_sdir:
                surface, coords = repertoire.sdir_to_screen(idx)
                self.surface.blit(surface, coords)

                if repertoire.sdir_mouse_over:
                    rect_coords = (*coords, repertoire.sdir_w, repertoire.sdir_h)
                    pygame.draw.rect(self.surface, (150, 200, 130), rect_coords, 1)

        self.ascenseur.draw()

        index1 = self.index(self.selected)
        index2 = self.index(self.selected, True)
        if index2 < self.decal:
            return

        # ligne indiquant que l'option est selectionnee
        selected_repertoire = self.liste[index1]
        if not selected_repertoire.visible:
            return

        dx = selected_repertoire.x
        dy = selected_repertoire.y(index2 - self.decal) 
        dy += self.y - 10
        w = selected_repertoire.surface.get_width()

        pygame.draw.line(self.surface, (50, 200, 150), (dx, dy), (dx+w, dy))
