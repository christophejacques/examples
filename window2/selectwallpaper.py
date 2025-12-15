import time
import os

from classes import Application, fprint
from functools import partial
from threading import Thread


class Box:

    def __init__(self, parent, color, coords):
        self.tools = parent.tools.get_subtools(coords)
        self.rect = self.tools.Rect(coords)
        self.mouse = parent.mouse

        self.backcolor = color
        self.has_mouse_on = False
        self.keep_mouse_events = False
        self.action = None

    def resize(self, parent, new_size=None, **options):
        if len(options) > 0:
            if "dx" in options: self.rect.x += options["dx"]
            if "dwidth" in options: self.rect.width += options["dwidth"]
        elif new_size:
            self.rect = self.tools.Rect(new_size)

        self.tools = parent.tools.get_subtools((*self.rect.topleft, *self.rect.size))

    def set_backcolor(self, backcolor):
        self.backcolor = backcolor

    def set_theme(self, theme):
        pass

    def get_action(self):
        action = self.action
        self.action = None
        return action

    def mouse_move(self, position):
        pass

    def mouse_enter(self):
        self.has_mouse_on = True

    def mouse_exit(self):
        self.has_mouse_on = False

    def mouse_button_down(self, posX, posY, button):
        pass

    def mouse_button_up(self, posX, posY, button):
        pass

    def collide_mouse(self, position):
        is_mouse_on = self.rect.collidepoint(position)
        if is_mouse_on and not self.has_mouse_on:
            self.mouse_enter()

        elif not is_mouse_on and self.has_mouse_on:
            self.mouse_exit()

        elif not is_mouse_on and not self.has_mouse_on:
            self.has_mouse_on = False

        return is_mouse_on

    def draw(self):
        self.tools.fill(self.backcolor)


class Separation(Box):

    def __init__(self, *args):
        super().__init__(*args)
        self.theme = args[0].theme
        self.mouse_is_clicked = False
        self.posX = 0
        self.cx = self.rect.width // 2

    def set_theme(self, theme):
        self.backcolor = self.theme.get("LIST_BACK_COLOR")

    def mouse_enter(self):
        super().mouse_enter()
        self.mouse.set_cursor(7)

    def mouse_exit(self):
        super().mouse_exit()
        self.mouse.set_cursor(0)

    def set_action(self, posX):
        dx = posX - self.posX
        if dx == 0:
            return 
        self.action = "MOVE:" + str(dx)

    def mouse_move(self, position):
        if self.mouse_is_clicked:
            self.set_action(position[0])

    def mouse_button_down(self, posX, posY, button):
        self.keep_mouse_events = True
        self.mouse_is_clicked = True
        self.posX = posX

    def mouse_button_up(self, posX, posY, button):
        self.keep_mouse_events = False
        self.mouse_is_clicked = False
        self.set_action(posX)

    def draw(self):
        self.tools.line(self.backcolor, (self.cx, 0), (self.cx, self.rect.height), width=3)


class Bouton(Box):
    BORDER_SIZE: int = 2

    def __init__(self, parent, texte: str, coords, callback=None, *params):
        # la couleur de fond est mise a jour par la methode update
        super().__init__(parent, None, coords)

        self.font = self.tools.font("courier bold", 30)
        self.texte = texte
        self.font_color = "black"
        self.set_callback(callback, *params)

        self.texte_font = self.font.render(self.texte, False, self.font_color)
        self.delta = (self.rect.width - self.texte_font.get_size()[0]) // 2
        
        self.enable = True
        self.has_mouse_on = False
        self.is_clicked = False
        self.hidden = False

        self.x2 = coords[2] - 1
        self.y2 = coords[3] - 1

        self.update()

    def resize(self, parent, new_size=None, **options):
        super().resize(parent, new_size, **options)
        # fprint(self.texte, self.rect)
        self.x2 = self.rect.width - 1
        self.delta = (self.rect.width - self.texte_font.get_size()[0]) // 2

        self.update()

    def set_callback(self, callback, *params):
        if callback:
            self.callback = partial(callback, *params)
        else:
            self.callback = None

    def show(self):
        self.hidden = False

    def hide(self):
        self.hidden = True

    def is_visible(self) -> bool:
        return not self.hidden

    def activate(self):
        self.enable = True
        self.update()

    def deactivate(self):
        self.enable = False
        self.font_color = (200, 200, 200)
        self.texte_font = self.font.render(self.texte, False, self.font_color)
        self.update()

    def mouse_enter(self):
        self.has_mouse_on = True
        if self.enable:
            self.backcolor = (180, 180, 180)

            self.font_color = "blue"
            self.texte_font = self.font.render(self.texte, False, self.font_color)

    def mouse_exit(self):
        self.has_mouse_on = False
        if self.enable:
            self.backcolor = (150, 150, 150)

            self.font_color = "black"
            self.texte_font = self.font.render(self.texte, False, self.font_color)

    def mouse_button_down(self, posX, posY, button):
        self.is_clicked = self.has_mouse_on and self.enable and button == 1
        self.update()

    def mouse_button_up(self, posX, posY, button):
        was_clicked = self.is_clicked
        self.is_clicked = False
        self.update()
        if self.enable and was_clicked and self.callback:
            self.callback()

    def collide_mouse(self, position):
        res = super().collide_mouse(position)
        self.update()
        return res

    def update(self):
        if not self.enable:
            # bouton desactive
            self.dx = self.delta
            self.dy = 10
            self.light_color = "lightgrey"
            self.shadow_color = (20, 40, 40)
            self.backcolor = (110, 110, 110)

        elif self.is_clicked and self.has_mouse_on:
            # bouton clique avec souris dessus
            self.dx = self.delta + self.BORDER_SIZE
            self.dy = 10 + self.BORDER_SIZE
            self.light_color = (50, 70, 70)
            self.shadow_color = "white"
            self.backcolor = (150, 150, 150)

        elif self.has_mouse_on:
            # bouton non clique avec souris dessus
            self.dx = self.delta 
            self.dy = 10 
            self.light_color = "white"
            self.shadow_color = (50, 70, 70)
            self.backcolor = (165, 165, 165)

        else:
            self.dx = self.delta
            self.dy = 10
            self.light_color = "white"
            self.shadow_color = (50, 70, 70)
            self.backcolor = (180, 180, 180)

    def draw(self):
        if self.hidden:
            return

        super().draw()
        # Affichage du texte
        self.tools.blit(self.texte_font, (self.dx, self.dy))

        # Affichage des bords
        for decal in range(self.BORDER_SIZE):
            self.tools.line(self.light_color, (0, decal), (self.x2, decal))
            self.tools.line(self.light_color, (decal, 0), (decal, self.y2))
        for decal in range(self.BORDER_SIZE):
            self.tools.line(self.shadow_color, (decal, self.y2-decal), (self.x2, self.y2-decal))
            self.tools.line(self.shadow_color, (self.x2-decal, decal), (self.x2-decal, self.y2))


class TextBox(Box):

    def __init__(self, parent, color, coords, texte: str):
        super().__init__(parent, color, coords)
        self.theme = parent.theme
        self.font = self.tools.font("courier", 18)
        self.set_texte(texte)

    def set_texte(self, texte):
        self.texte_font = self.font.render(texte, False, self.theme.get("FORE_COLOR"))
        self.texte = texte

    def set_theme(self, theme):
        fprint("set TB theme", theme)
        self.set_texte(self.texte)
        self.backcolor = self.theme.get("LIST_BACK_COLOR")

    def draw(self):
        if self.backcolor:
            super().draw()

        self.tools.blit(self.texte_font, (10, 10))


class ListDirectoryFile(Box):

    BORDER_SIZE: int = 8
    MAX_FILES: int = 17

    def __init__(self, parent, color, coords, directory: str):
        super().__init__(parent, color, coords)
        self.directory = directory
        self.font = self.tools.font("courier", 18)
        self.theme = parent.theme

        self.liste: dict = dict()
        self.decal: int

        self.scan()

        # recherche de l'image dans la liste afin de la pre selectionner
        filename = parent.registre.load("fichier", "")
        try:
            self.selected_index = (
                self.liste["files"].index(filename[1+filename.rindex(os.path.sep):]) +
                self.len_dirs)

            if self.selected_index > self.MAX_FILES:
                self.decal = self.selected_index - self.MAX_FILES 
                self.selected_index -= self.decal 

            self.index = self.selected_index 

        except Exception as error:
            fprint(error)

    def scan(self):
        self.liste["dirs"] = list()
        self.liste["files"] = list()
        self.decal = 0
        self.index = -1
        self.selected_index = -1
        self.is_clicked = False
        self.ascenseur_is_clicked = False
        self.mouse_over_ascenseur = False
        self.action = "CD:" + self.directory

        for file in os.scandir(self.directory):
            if file.is_dir() and file.name[0] not in (".", "_"): 
                self.liste["dirs"].append(f"[{file.name}]")
            elif file.is_file() and file.name.lower().endswith(".jpg"):
                self.liste["files"].append(file.name)

        self.liste["dirs"].sort()
        self.len_dirs = len(self.liste["dirs"])
        self.liste["files"].sort()
        self.len_files = len(self.liste["files"])
        self.recalc_size()

    def recalc_size(self):
        new_max = -1 + (self.tools.get_size()[1] - 2 * self.BORDER_SIZE) // 21
        self.MAX_FILES = new_max

        nombre_total = self.len_dirs + self.len_files

        self.ascenseur = nombre_total > self.MAX_FILES
        self.largeur_ascenseur = 12 if self.ascenseur else 0
        if nombre_total > 0:
            self.hauteur_ascenseur = int(self.rect.height * self.MAX_FILES / nombre_total)
        else:
            self.hauteur_ascenseur = 0

        if nombre_total - self.decal < self.MAX_FILES:
            self.decal -= self.MAX_FILES - nombre_total + self.decal + 1
            if self.decal < 0:
                self.decal = 0

    def resize(self, *args, **options):
        super().resize(*args, **options)
        self.recalc_size()

    def mouse_exit(self):
        super().mouse_exit()
        self.index = -1
        self.mouse_over_ascenseur = False

    def update_ascenseur(self, position):
        if self.ascenseur_is_clicked:
            pourcentage_decal = position[1] / self.rect.height

            pourcentage_decal = pourcentage_decal + (
                self.hauteur_ascenseur*(pourcentage_decal-0.5) / self.rect.height)
            if pourcentage_decal < 0:
                pourcentage_decal = 0
            elif pourcentage_decal > 1:
                pourcentage_decal = 1

            decal = self.decal
            self.decal = int(round((self.len_dirs+self.len_files-self.MAX_FILES-1) * pourcentage_decal, 0))
            self.selected_index += decal - self.decal
            return

        self.mouse_over_ascenseur = position[0] >= self.rect.width - self.largeur_ascenseur    

    def mouse_move(self, position):
        self.update_ascenseur(position)

        index = (position[1] - self.BORDER_SIZE) // 21 
        if index < 0 or index >= self.len_dirs+self.len_files or index > self.MAX_FILES or (
            position[0] >= self.rect.width-self.largeur_ascenseur):
            self.index = -1
            return

        self.index = index

    def mouse_button_down(self, posX, posY, button):
        if posX < self.rect.width-self.largeur_ascenseur:
            self.is_clicked = self.has_mouse_on and button == 1
            self.ascenseur_is_clicked = False
        else:
            self.ascenseur_is_clicked = button == 1
            if self.ascenseur_is_clicked:
                self.keep_mouse_events = True

    def mouse_button_up(self, posX, posY, button):
        self.keep_mouse_events = False
        self.mouse_action((posX, posY))

    def mouse_action(self, position):
        self.is_clicked = False
        if self.index < 0 or self.ascenseur_is_clicked:
            self.update_ascenseur(position)
            self.ascenseur_is_clicked = False
            return

        if self.decal + self.index < self.len_dirs:
            directory = self.liste["dirs"][self.decal + self.index].strip("[]")
            self.directory = os.path.join(self.directory, directory)
            self.scan()
            return

        self.selected_index = self.index
        self.action = "LOAD:" + (
            os.path.join(
                self.directory,
                self.liste["files"][self.decal + self.index - self.len_dirs]))

    def set_action(self, action):
        match action:
            case "INIT":
                pass

            case "PARENT":
                if os.path.sep in self.directory:
                    self.directory = self.directory[:self.directory.rindex(os.path.sep)]
                    self.scan()

            case "SELECT":
                self.mouse_action(None)

            case "HOME":
                self.selected_index += self.decal
                self.index = 0
                self.decal = 0            

            case "END":
                if self.len_dirs+self.len_files >= self.MAX_FILES:
                    self.index = self.MAX_FILES
                    decal = self.decal
                    self.decal = self.len_dirs+self.len_files - self.MAX_FILES - 1
                    self.selected_index += decal - self.decal 
                else:
                    self.index = self.len_dirs+self.len_files - 1

            case "PAGEUP":
                if self.index > 0:
                    self.index = 0

                elif self.decal > self.MAX_FILES:
                    self.decal -= self.MAX_FILES
                    self.selected_index += self.MAX_FILES
                else:
                    self.selected_index += self.decal
                    self.decal = 0

            case "SCROLLUP":
                if self.decal > 0:
                    if self.decal > 1:
                        self.decal -= 2
                        self.selected_index += 2
                    else:
                        self.decal -= 1
                        self.selected_index += 1

            case "SCROLLDOWN":
                if self.decal+self.MAX_FILES+1 < self.len_dirs+self.len_files:
                    if self.decal+self.MAX_FILES+2 < self.len_dirs+self.len_files:
                        self.decal += 2
                        self.selected_index -= 2
                    else:
                        self.decal += 1
                        self.selected_index -= 1

            case "UP":
                if self.index > 0:
                    self.index -= 1
                elif self.decal > 0:
                    self.decal -= 1
                    self.selected_index += 1

            case "DOWN":
                if self.decal+self.index +1 < self.len_dirs + self.len_files:
                    if self.index < self.MAX_FILES:
                        self.index += 1
                    else:
                        self.decal += 1
                        self.selected_index -= 1

            case "PAGEDOWN":
                if self.index < self.MAX_FILES:
                    if self.MAX_FILES < self.len_dirs+self.len_files:
                        self.index = self.MAX_FILES 
                    else:
                        self.index = self.len_dirs+self.len_files -1

                elif self.index+self.decal < self.len_dirs+self.len_files:
                    if self.decal+self.index+self.MAX_FILES < self.len_dirs+self.len_files:
                        self.decal += self.MAX_FILES
                        self.selected_index -= self.MAX_FILES
                    else:
                        decal = self.decal
                        self.decal = self.len_dirs+self.len_files - self.MAX_FILES - 1
                        self.selected_index += decal - self.decal

    def set_theme(self, theme):
        fprint("set theme", theme)
        self.backcolor = self.theme.get("LIST_BACK_COLOR")

    def draw(self):
        super().draw()
        rech_index: int = 0
        index: int = 0

        largeur_dirfile: int = self.rect.width - 4 - self.largeur_ascenseur

        # affichage des repertoires et fichiers
        for dirfile in (self.liste["dirs"] + self.liste["files"]):
            if rech_index-self.decal < 0 or index > self.MAX_FILES:
                rech_index += 1
                continue

            if self.selected_index == index:
                color = self.theme.get("LIST_SELECTED_TEXT_COLOR")
                self.tools.rect((100, 100, 250), (
                    2, self.BORDER_SIZE+(index)*21, largeur_dirfile, 21))
                self.tools.rect((0, 0, 250), (
                    2, self.BORDER_SIZE+(index)*21, largeur_dirfile, 21), 1)

            elif self.index == index and not self.ascenseur_is_clicked:
                color = self.theme.get("LIST_MOUSEOVER_TEXT_COLOR")
                self.tools.rect((10, 250, 250), (
                    2, self.BORDER_SIZE+(index)*21, largeur_dirfile, 21))
                self.tools.rect((10, 200, 200), (
                    2, self.BORDER_SIZE+(index)*21, largeur_dirfile, 21), 1)

            else:
                color = self.theme.get("LIST_TEXT_COLOR")

            texte_font = self.font.render(dirfile, False, color)
            self.tools.blit(texte_font, (self.BORDER_SIZE, self.BORDER_SIZE+21*(index)))
            index += 1

        # Affichage de l'ascenseur si besoin
        if self.ascenseur:
            ascenseur_color: tuple = (200, 200, 200)
            x1: int = self.rect.width - self.largeur_ascenseur
            x2: int = self.rect.width-2

            # cadre de l'ascenseur
            self.tools.rect(ascenseur_color, (x1, 0, self.largeur_ascenseur, self.rect.height))

            total: int = self.len_dirs+self.len_files
            diff: int = self.rect.height
            y1: int = 2 + (diff * self.decal) // total
            y2: int = min(self.rect.height-2, y1 + (diff * self.MAX_FILES) // total)
            
            # Ascenseur
            if self.ascenseur_is_clicked or self.mouse_over_ascenseur:
                ascenseur_color = (100, 100, 100)
            else:
                ascenseur_color = (150, 150, 150)
            self.tools.rect(ascenseur_color, (x1, y1, self.largeur_ascenseur, y2-y1))


class Image(Box):

    def __init__(self, parent, color, coords, filename: str):
        super().__init__(parent, color, coords)
        self.w = 0
        self.h = 0
        self.size = self.tools.get_size()
        self.set_filename(filename)
        self.FONT = self.tools.font("comicsans", 18)

    def resize(self, *args, **options):
        super().resize(*args, **options)

        if "dwidth" in options:
            self.size = self.tools.get_size()
        else:
            self.size = tuple(args[1][2:])

        self.calc_rapport()
        self.image = self.tools.scale_image(self.img, *self.img_size)

    def calc_rapport(self):
        self.w, self.h = self.img.get_size()
        rap_img = self.w / self.h
        rap_ref = self.size[0] / self.size[1]

        if rap_img < rap_ref:
            img_w = self.size[0] * rap_img / rap_ref
            img_h = self.size[1]
        else:
            img_w = self.size[0] 
            img_h = self.size[1] * rap_ref / rap_img

        self.img_size = img_w, img_h

    def set_filename(self, filename):
        if filename is None:
            self.image = None
            return

        self.filename = filename.split("\\")[-1]
        self.img = self.tools.load_image(filename)
        self.calc_rapport()
        self.image = self.tools.scale_image(self.img, *self.img_size)

    def printscreen(self, texte: str, position: tuple[int, int]):
        ombre = self.FONT.render(texte, False, (5, 5, 5))
        texte = self.FONT.render(texte, False, (20, 255, 20))
        x, y = position
        self.tools.blit(ombre, [x-1, y-1])
        self.tools.blit(ombre, [x-1, y+1])
        self.tools.blit(ombre, [x+1, y-1])
        self.tools.blit(ombre, [x+1, y+1])
        self.tools.blit(ombre, [x-1, y])
        self.tools.blit(ombre, [x+1, y])
        self.tools.blit(texte, [x, y])

    def draw(self):
        super().draw()
        if self.image:
            w, h = self.tools.get_size()
            dx = (w - self.image.get_width()) // 2
            dy = (h - self.image.get_height()) // 2
            self.tools.blit(self.image, (dx, dy))

            self.printscreen(self.filename, (10, 2))
            self.printscreen(f"{self.w}x{self.h}", (10, h-32))


class SelectWallpaper(Application):

    DEFAULT_CONFIG: tuple = ("SelectWallpaper", (150, 150, 150))
    MIN_SIZE: tuple = (1200, 545)
    WINDOW_PROPERTIES: list = ["CENTER", "UNIQUE"]

    def __init__(self, *args):
        self.title = self.DEFAULT_CONFIG[0]
        self.action = ""

        self.ecrans = list()
        self.boutons = list()

        self.focused_bouton = None
        self.compteur_tache = 0

    @property
    def directory(self):
        if self.img_filename is None:
            return ""
        elif len(self.img_filename) > 1:
            return self.img_filename[:self.img_filename.rindex(os.path.sep)]
        return self.img_filename

    def post_init(self):
        self.set_title(self.title)
        self.win_resize("CENTER", 0, 0, *self.MIN_SIZE)

        nombre = self.registre.load("Utilisation", 0)
        self.registre.save("Utilisation", 1+nombre)
        self.get_theme()
        self.img_filename = self.registre.load("fichier", None)
        self.decal_sep_x = self.registre.load("decal_sep_x", 410)

        # couleur_fond = (220, 220, 220)
        couleur_fond = self.theme.get("LIST_BACK_COLOR")

        # Definition des zones
        self.liste_dirs_files = ListDirectoryFile(
            self, couleur_fond, (10, 60, self.decal_sep_x-10, 400), self.directory)
        self.ecrans.append(self.liste_dirs_files)
        self.separation = Separation(self, couleur_fond, (self.decal_sep_x, 10, 10, 500))
        self.ecrans.append(self.separation)
        self.image = Image(self, "black", (self.decal_sep_x+10, 10, 1200-(self.decal_sep_x+30), 500), self.img_filename)
        self.ecrans.append(self.image)
        self.textDirectory = TextBox(self, couleur_fond, (55, 10, self.decal_sep_x-55, 40), "")
        self.ecrans.append(self.textDirectory)

        self.width, self.height = self.tools.get_size()
        self.check_actions()


        cx = self.liste_dirs_files.rect.centerx

        # Bouton Valider
        self.valider = Bouton(self, "Valider", (cx+10, 470, cx-20, 40), 
            self.check_action, "SET:WALLPAPER")
        self.boutons.append(self.valider)

        # Bouton Annuler
        self.annuler = Bouton(self, "Annuler", (10 , 470, cx-20, 40), self.close)
        self.boutons.append(self.annuler)

        # Bouton Parent
        self.parent = Bouton(self, "Par", (10 , 10, 40, 40), 
            self.liste_dirs_files.set_action, "PARENT")
        self.boutons.append(self.parent)

    def load_image(self):
        self.image.set_filename(self.img_filename)

    def toggle(self, *boutons):
        for bouton in boutons:
            if bouton.hidden:
                bouton.show()
            else:
                bouton.hide()

    def resize(self):
        if not self.ecrans:
            return

        self.width, self.height = self.tools.get_size()
        
        self.liste_dirs_files.resize(self, 
            (self.liste_dirs_files.rect.x, 60, self.liste_dirs_files.rect.width, self.height-127))
        self.separation.resize(self, (self.separation.rect.x, 10, 10, self.height-20))

        self.image.resize(self, 
            (self.image.rect.x, 10, self.width-self.image.rect.x-10, self.height-20))

        self.textDirectory.resize(self)
    
        self.annuler.resize(self, 
            (self.annuler.rect.x, self.height - 52, 
                self.annuler.rect.width, self.annuler.rect.height))
        self.valider.resize(self, 
            (self.valider.rect.x, self.height - 52, 
                self.valider.rect.width, self.valider.rect.height))
        self.parent.resize(self)

    def get_theme(self):
        active_theme = self.theme.get_theme()

        if active_theme == "CLAIR":
            self.background = (100, 190, 200)
        else:
            self.background = (30, 55, 60)

        for ecran in self.ecrans:
            ecran.set_theme(active_theme)

    def mouse_enter(self, mouseX, mouseY):
        pass

    def mouse_exit(self):
        pass


    def set_action_keypressed(self, action, delay):
        self.liste_dirs_files.set_action(action)
        time.sleep(delay)

    def until_keyreleased(self, action):
        # delay initial
        delay = 0.5
        self.compteur_tache += 1
        compteur = self.compteur_tache
        while not self.anykey_released and compteur == self.compteur_tache:
            tache = Thread(target=self.set_action_keypressed, args=(action, delay))
            tache.start()
            tache.join()
            # delay post delay initial (plus rapide)
            delay = 0.05

    def keypressed(self, event):
        touche = self.keys.get_key()

        if event.key == self.keys.K_UP:
            self.anykey_released = False
            Thread(target=self.until_keyreleased, args=("UP",)).start()

        elif event.key == self.keys.K_DOWN:
            self.anykey_released = False
            Thread(target=self.until_keyreleased, args=("DOWN",)).start()

    def keyreleased(self, event):
        # touche = self.keys.get_key()
        self.anykey_released = True

        if event.key == self.keys.K_ESCAPE:
            self.close()

        elif event.key in (self.keys.K_KP_ENTER, self.keys.K_RETURN):
            self.liste_dirs_files.set_action("SELECT")
            self.check_action(self.liste_dirs_files.get_action())

        elif event.key == self.keys.K_HOME:
            self.liste_dirs_files.set_action("HOME")
        elif event.key == self.keys.K_END:
            self.liste_dirs_files.set_action("END")
        elif event.key == self.keys.K_UP:
            pass
        elif event.key == self.keys.K_DOWN:
            pass
        elif event.key == self.keys.K_PAGEUP:
            self.liste_dirs_files.set_action("PAGEUP")
        elif event.key == self.keys.K_PAGEDOWN:
            self.liste_dirs_files.set_action("PAGEDOWN")
        else:
            fprint(event)
                
    def mouse_move(self, mouseX, mouseY):

        self.focused_bouton = None
        self.focused_ecran = None

        # n'execute que les mouvements sur l'ecran qui le demande
        for ecran in self.ecrans:
            if ecran.keep_mouse_events:
                ecran.mouse_move((mouseX-ecran.rect.left, mouseY-ecran.rect.top))

                # mise a jour de l'affichage pour la gestion du separateur
                if ecran == self.separation:
                    self.check_actions()
                return

        for bouton in self.boutons:
            # activation des events enter & exit
            if bouton.is_visible() and bouton.collide_mouse((mouseX, mouseY)):
                self.focused_bouton = bouton

        for ecran in self.ecrans:
            # activation des events enter & exit
            if ecran.collide_mouse((mouseX, mouseY)):
                ecran.mouse_move((mouseX-ecran.rect.left, mouseY-ecran.rect.top))
                self.focused_ecran = ecran

    def mouse_wheel(self, dx, dy):
        if dy > 0:
            self.liste_dirs_files.set_action("SCROLLUP")
        elif dy < 0:
            self.liste_dirs_files.set_action("SCROLLDOWN")

    def mouse_button_down(self, mouseX, mouseY, button):
        if button in (4, 5):
            return

        if self.focused_bouton:
            self.focused_bouton.mouse_button_down(mouseX, mouseY, button)
            return

        if self.focused_ecran:
            self.focused_ecran.mouse_button_down(
                mouseX-self.focused_ecran.rect.left, 
                mouseY-self.focused_ecran.rect.top, button)

    def mouse_button_up(self, mouseX, mouseY, button):
        if button in (4, 5):
            return

        if self.focused_bouton:
            if self.focused_bouton.collide_mouse((mouseX, mouseY)):
                self.focused_bouton.mouse_button_up(mouseX, mouseY, button)
                self.check_actions()

        elif self.focused_ecran:
            if self.focused_ecran.collide_mouse((mouseX, mouseY)):
                self.focused_ecran.mouse_button_up(
                    mouseX-self.focused_ecran.rect.left, 
                    mouseY-self.focused_ecran.rect.top, button)
                self.check_actions()

        if self.separation.mouse_is_clicked and self.focused_ecran != self.separation:
            self.separation.mouse_button_up(
                mouseX-self.separation.rect.left, 
                mouseY-self.separation.rect.top, button)
            self.check_actions()

        if self.focused_ecran != self.liste_dirs_files:
            # gestion de l'ascenseur
            if self.liste_dirs_files.ascenseur_is_clicked:
                self.liste_dirs_files.mouse_button_up(
                    mouseX-self.liste_dirs_files.rect.left, 
                    mouseY-self.liste_dirs_files.rect.top, button)

        for bouton in self.boutons:
            bouton.is_clicked = False

    def check_actions(self):
        for ecran in self.ecrans:
            action = ecran.get_action()
            self.check_action(action)

    def check_action(self, action):
        if action is None or action == "":
            return

        match action.split(":"):
            case ["MOVE", dx]:
                dx = int(dx)
                if dx < 0 and self.textDirectory.tools.get_size()[0] < 200-dx:
                    return
                if dx > 0 and self.textDirectory.tools.get_size()[0] > 600-dx:
                    return
                self.liste_dirs_files.resize(self, dwidth=dx)
                self.separation.resize(self, dx=dx)
                self.image.resize(self, dx=dx, dwidth=-dx)
                self.textDirectory.resize(self, dwidth=dx)

                cx = self.liste_dirs_files.rect.centerx
                self.valider.resize(self, (cx+10, self.valider.rect.y, cx-20, 40))
                self.annuler.resize(self, (10 , self.annuler.rect.y, cx-20, 40))

            case ["CD", repertoire]:                
                self.textDirectory.set_texte(repertoire)

            case ["LOAD", params]:
                self.img_filename = params
                self.load_image()

            case ["SET", "WALLPAPER"]:
                self.action = f"{action}:{self.img_filename};QUIT"
                self.registre.save("fichier", self.img_filename)
                
                if self.decal_sep_x != self.separation.rect.x:
                    self.registre.save("decal_sep_x", self.separation.rect.x)


    def close(self):
        self.action = "QUIT"
        if self.decal_sep_x != self.separation.rect.x:
            self.registre.save("decal_sep_x", self.separation.rect.x)

    def get_action(self):
        action = self.action
        self.action = None
        return action

    def update(self):
        pass

    def draw(self):
        self.tools.fill(self.background)
        for ecran in self.ecrans:
            ecran.draw()

        for bouton in self.boutons:
            bouton.draw()


if __name__ == '__main__':
    from exec import run
    run(locals())
