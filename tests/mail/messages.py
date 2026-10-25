import pygame  # noqa: E402

from time import perf_counter
from typing import List, Tuple, Optional, Dict, Generator
from functools import partial
from threading import Thread

from textes import Texte, Lien
from outils import Ascenseur, MessageBox
from general import Mouse, fprint, Variable
from mail import Mail


class Message:
    data: Dict[str, Texte]

    def __init__(self):
        self.data = dict()

    def load(self, cle: str, texte: Texte) -> None:
        self.data[cle] = texte

    def to_draw(self) -> Generator:
        for cle in self.data:
            texte = self.data[cle]
            yield cle, texte.surface


class ListeMessages:

    hauteur_ligne: int = 28

    surface: pygame.surface.Surface
    x: int
    y: int
    w: int
    h: int
    visible: bool

    ascenseur: Ascenseur
    mouse_over: bool

    directory: str
    nb_mails: int 
    nb_lignes: int
    nb_lignes_max: int

    selected: Optional[int]
    message_over: int 

    decal: int
    debut: int

    nb_colonnes: int
    data_titres: Dict
    titres: List[Lien]

    liste_datas: List[Dict]
    liste_messages: List[Message]

    actions: Optional[str]

    def __init__(self, screen: pygame.surface.Surface, coords: Tuple):

        self.decal = 0
        self.nb_lignes = 0
        self.nb_lignes_max = 0

        self.load_titres()
        self.update_screen(screen, coords)
        self.mouse_over = False
        self.nb_mails = 0
        self.selected = None
        self.message_over = 0

        self.actions = None
        self.directory = '"INBOX"'

    def get_actions(self) -> Optional[str]:
        actions: str

        if self.actions is None:
            return None

        actions = self.actions
        self.actions = None
        return actions

    def get_texte_color(self, *args) -> Tuple:
        attr = args[1]
        if "V" in attr:
            return (150, 150, 150)

        return (200, 240, 240)

    def get_color(self, index) -> Tuple:
        if index == 1:
            return (255, 255, 255)

        elif index == 2:
            return (255, 100, 100)

        elif index == "SEEN":
            return (150, 150, 150)

        elif index == "UNSEEN":
            return (200, 240, 240)

        return (160, 240, 220)

    def load_titres(self) -> None:
        cle: str
        lien: Lien

        self.data_titres = {
            "ATT": {"lib": "Attr", "pos": 10, "col": 1},
            "NUM": {"lib": "N°", "pos": 50, "col": 1},
            "EXP": {"lib": "Expéditeur", "pos": 50, "col": 1},
            "OBJ": {"lib": "Objet", "pos": 300, "col": 1},
            "DAT": {"lib": "Date", "pos": 580, "col": 1},
            "DIR": {"lib": r"\/", "pos": 50, "col": 2},
        }
        self.titres = list()
        self.coord_x: Dict = dict()

        self.nb_colonnes = len(self.data_titres) - 1

        position: int = 0
        position_old: int = 0
        prev_key: str = ""

        for cle in self.data_titres:
            position_old = position
            position += self.data_titres[cle]["pos"]
            largeur = position - position_old
            self.data_titres[cle]["pos"] = position
            if prev_key:
                self.data_titres[prev_key]["lar"] = largeur

            prev_key = cle

            lien = Lien(Variable.SysFont3, self.data_titres[cle]["lib"],
                    position, 7, 
                    partial(self.get_color, self.data_titres[cle]["col"]), None,
                    id=cle)
            self.titres.append(lien)

            self.coord_x[cle] = lien.x

    def mouse_exit(self) -> None:
        self.mouse_over = False
        self.message_over = 0

    def mouse_move(self, mouse_pos: Tuple) -> None:
        idx: int

        self.mouse_over = True

        if mouse_pos[1] < 30:
            # ligne des titres
            self.message_over = 0
            
        else:
            # ligne des messages
            idx = mouse_pos[1] // ListeMessages.hauteur_ligne
            if idx > self.nb_mails:
                idx = 0

            self.message_over = idx

    def mouse_wheel(self, x, y) -> None: 
        if y < 0 and self.decal - y + self.nb_lignes_max > self.nb_lignes:
            return

        if self.selected is not None:
            if self.decal-y >= 0:
                self.selected += y

        self.decal += -y
        if self.decal < 0:
            self.decal = 0

        self.update_ascenseur()

    def mouse_button_up(self, mouse_pos: Tuple, button: int) -> None:
        self.selected = self.message_over
    
    def keyreleased(self, event) -> None: 
        if not self.mouse_over:
            return

        match event.key:
            case pygame.K_DELETE:
                if self.selected is None:
                    return

                self.mouse_exit()
                self.ask_for_delete_message()

            case pygame.K_UP | pygame.K_DOWN:
                shift: bool = event.mod & 1 == 1
                direction = 1 if event.key == pygame.K_UP else -1
                self.mouse_wheel(Mouse.x, direction)

            case pygame.K_HOME:
                if self.decal > 0:
                    if self.selected is not None:
                        self.selected += self.decal

                    self.decal = 0
                    self.update_ascenseur()
                    self.mouse_move(pygame.mouse.get_pos())

            case pygame.K_PAGEUP:
                if self.decal > 0:
                    dy = min(10, self.decal)
                    if self.selected is not None:
                        self.selected += dy

                    self.decal -= dy
                    self.update_ascenseur()
                    self.mouse_move(pygame.mouse.get_pos())

            case pygame.K_PAGEDOWN:
                if self.decal + self.nb_lignes_max < self.nb_lignes:
                    dy = min(10, self.nb_lignes-(self.decal + self.nb_lignes_max))
                    if self.selected is not None:
                        self.selected -= dy

                    self.decal += dy
                    self.update_ascenseur()
                    self.mouse_move(pygame.mouse.get_pos())

            case pygame.K_END:
                if self.decal + self.nb_lignes_max < self.nb_lignes:
                    if self.selected is not None:
                        self.selected -= (self.nb_lignes - self.nb_lignes_max) - self.decal

                    self.decal = self.nb_lignes - self.nb_lignes_max
                    self.update_ascenseur()
                    self.mouse_move(pygame.mouse.get_pos())

    @staticmethod
    def format_adresse(lib: str) -> str:
        if "<" in lib:
            return lib[:lib.index("<")-1]

        return lib

    def get_mails(self) -> None:
        mail: Mail
        user: str
        status: str
        response: List
        contenu: Dict

        data: str
        dossier: str
        messages: str
        unseen: str

        mail = Mail()
        user = mail.USERNAME

        try:
            mail.connect()
            mail.select(self.directory)

            status, response = mail.mail.status(self.directory, "(MESSAGES UNSEEN)")
            if status == "OK":
                # response contient une liste avec un seul élément en bytes
                data = response[0].decode("utf-8").strip("()")

                *lst_dossier, _, messages, _, unseen = data.split()
                dossier = " ".join(lst_dossier)

                self.actions = f"USER={user};DIR={dossier};ALL={messages};UNSEEN={unseen}"

                for contenu in mail.get_mails("ALL"):  # ALL, UNSEEN
                    self.liste_datas.append(contenu)

            else:
                fprint(self.directory, "Status:", status)

        except Exception as erreur:
            fprint("get_mails():", erreur)
            raise

        try:
            mail.disconnect()
        except Exception:
            pass

        if self.actions is None:
            self.actions = "LOADING=False"
        else:
            self.actions += ";LOADING=False"

    def load_mails(self) -> None:

        cle: str
        lib: str
        attr: str

        largeur_max: Dict[str, int]

        debut: float
        fin: float

        message: Message

        debut = perf_counter()

        self.get_mails()

        largeur_max = dict()
        for cle in self.data_titres:
            if cle == "DIR":
                continue

            largeur_max[cle] = self.data_titres[cle]["lar"] - 10

        for datas in reversed(sorted(self.liste_datas, key=lambda x: x["DAT"])):
            message = Message()
            attr = ""
            for cle in datas:
                if cle == "ATT":
                    attr = datas[cle]

                lib = self.format_adresse(datas[cle]) if cle == "EXP" else datas[cle]
                texte = Texte( 
                    Variable.SysFont3, 
                    lib, 
                    self.get_texte_color, attr)

                if cle != "DAT":
                    texte.set_max_width(largeur_max[cle])

                message.load(cle, texte)

            self.liste_messages.append(message)

        self.nb_mails = len(self.liste_datas)
        self.nb_lignes = self.nb_mails
        self.decal = 0

        fin = perf_counter()
        fprint(f"load messages : {fin - debut:.4f} secondes")

        self.ascenseur = Ascenseur(self.surface, self.w, self.h, self.nb_lignes, self.nb_lignes_max,
            hauteur=self.h - ListeMessages.hauteur_ligne, posy=ListeMessages.hauteur_ligne+2)

    def load(self) -> None:
        mails: Thread

        self.liste_datas = list()
        self.liste_messages = list()
        self.nb_mails = 0
        self.selected = None
        self.message_over = 0
        self.actions = "LOADING=True"

        mails = Thread(target=self.load_mails)
        mails.start()

    def delete_message(self, numero: int):

        fprint("Delete : ", end="id=")
        message = self.liste_messages[numero]
        fprint(message.data["NUM"].libelle, end=" ")
        fprint(f'{message.data["OBJ"].libelle!r}')

        del self.liste_messages[numero]
        self.nb_mails -= 1
        self.nb_lignes -= 1

        self.ascenseur = Ascenseur(self.surface, self.w, self.h, self.nb_lignes, self.nb_lignes_max,
            hauteur=self.h - ListeMessages.hauteur_ligne, posy=ListeMessages.hauteur_ligne+2)

        if self.decal + self.nb_lignes_max > self.nb_lignes and self.decal > 0:
            self.decal -= 1

        if self.selected and self.selected > self.nb_lignes:
            if self.selected > 1:
                self.selected -= 1
            else:
                self.selected = None

        self.update_ascenseur()

    def ask_for_delete_message(self):
        if not self.selected:
            return

        message = self.liste_messages[self.decal + self.selected - 1]
        MessageBox.set_message([
            "Voulez-vous supprimer le message",
            f"Numéro : {message.data["NUM"].libelle} ?"])
        
        MessageBox.bouton_oui.set_callback(self.delete_message, self.decal + self.selected - 1)
        MessageBox.activate()

    def refresh(self) -> None:
        self.load()

    def update_ascenseur(self):
        self.ascenseur.update(self.decal)

    def update_screen(self, 
            screen: pygame.surface.Surface, coords: Optional[Tuple] = None) -> None:
        hauteur: int
        h: int

        if coords is not None:
            self.coords = pygame.Rect(coords)

        self.surface = screen.subsurface(self.coords)
        self.x, self.y, self.w, h = self.coords
        self.h = h - 1

        # nombre maximal de messages à afficher
        hauteur = h // ListeMessages.hauteur_ligne
        self.nb_lignes_max = hauteur - 1

        if self.decal + self.nb_lignes_max > self.nb_lignes:
            self.decal = max(0, self.nb_lignes - self.nb_lignes_max)

        self.ascenseur = Ascenseur(self.surface, self.w, self.h, self.nb_lignes, self.nb_lignes_max,
            hauteur=self.h - ListeMessages.hauteur_ligne, posy=ListeMessages.hauteur_ligne+2)
        self.update_ascenseur()

    def draw(self) -> None:
        coord_y: int
        ligne: int
        color: Tuple
        cle: str
        message: Message
        surface: pygame.surface.Surface

        self.surface.fill((10, 20, 20))

        # fond d'une ligne de message
        selected = self.selected if self.selected else 0
        for ligne in range(1, 1+min(self.nb_mails, self.nb_lignes_max)):
            if ligne == selected:
                color = (13, 64, 13)
            elif ligne == self.message_over:
                color = (20, 50, 50)
            else:
                color = (20, 30, 30)

            if ligne % 2 and ligne not in (self.selected, self.message_over):
                continue

            pygame.draw.rect(self.surface, color, 
                (0, ListeMessages.hauteur_ligne * ligne, 
                    self.coords.w, ListeMessages.hauteur_ligne))

        # Ligne des titres
        self.surface.blits([titre.to_draw() for titre in self.titres])
        pygame.draw.line(self.surface, (50, 200, 150), (0, 30), (self.coords.w, 30))

        # tableau des messages
        coord_y = 6
        for message in self.liste_messages[self.decal:self.decal+self.nb_lignes_max]:
            coord_y += ListeMessages.hauteur_ligne
            for cle, surface in message.to_draw():
                self.surface.blit(surface, (self.coord_x[cle], coord_y))

        if self.nb_lignes <= self.nb_lignes_max:
            return

        self.ascenseur.draw()
