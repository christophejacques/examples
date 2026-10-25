from os import getcwd, chdir, sep as separator
from typing import Tuple, Optional, List

from general import pygame, Variable, Mouse, fprint, get_pygame_const_name
from outils import MessageBox
from headers import Headers
from footers import Footers
from repertoires import Repertoires
from messages import ListeMessages


class Lecteur:

    clock: pygame.time.Clock
    screen: pygame.surface.Surface
    screen_width: int
    screen_height: int

    dirs_size: int 
    line_height: int
    block_size: int

    nb_lines: int
    nb_cols: int
    color_diff: int

    idxx: int
    idxy: int

    mouse: Mouse
    mouse_button_down_pos: Tuple
    running: bool

    nb_messages: int
    messages_non_vu: int

    headers: Headers
    liste_messages: ListeMessages
    repertoires: Repertoires
    footers: Footers

    def __init__(self):

        # change le repertoire courant afin de trouver 
        # toutes les applications et le parametrage
        directory: str = separator.join(__file__.split(separator)[:-1])
        if directory != getcwd():
            fprint(f"change current directory to : {directory}")
            chdir(directory)

        # Récupération de la liste des noms de polices disponibles
        # polices = pygame.font.get_fonts()

        # Affichage des polices
        # print(f"Nombre total de polices disponibles : {len(polices)}")
        # for police in polices:
        #     print(f"{police:40}", end="")

    def init_fonts(self) -> None:
        Variable.SysFont1 = pygame.font.SysFont("couriernew", 18)
        Variable.SysFont2 = pygame.font.SysFont("dejavuserif", 16)
        Variable.SysFont3 = pygame.font.SysFont(["segoeuiemoji"], 17)
        Variable.SysFont4 = pygame.font.SysFont("linuxlibertineg", 18, bold=False, italic=True)

    def initialize(self) -> None:
        self.clock = pygame.time.Clock()
        self.running = True

        desktops: List[Tuple] = pygame.display.get_desktop_sizes()
        disp_size: Tuple

        if desktops[0][1] > 1000:
            # Full HD max resolution
            disp_size = (1600, 788)
        else:
            disp_size = desktops[0]
            
        # self.screen = pygame.display.set_mode(desktops[0], pygame.FULLSCREEN, 24)
        self.screen = pygame.display.set_mode(disp_size, pygame.RESIZABLE, 24)
        self.screen_width, self.screen_height = self.screen.get_size()

        MessageBox(self.screen)

        self.mouse = Mouse(*pygame.mouse.get_pos())
        self.mouse_button_down_pos = (0, 0)

        # Initialisation du cadrillage
        self.block_size = 40

        self.nb_lines = (self.screen_height-20) // self.block_size 
        self.nb_cols = (self.screen_width-20) // self.block_size 
        self.color_diff = 255 // (self.nb_lines + self.nb_cols)

        self.idxx = (self.mouse.x-10) // self.block_size
        self.idxy = (self.mouse.y-10) // self.block_size

    def init_draw(self) -> None:
        self.dirs_size = 300
        self.line_height = 30

        self.nb_messages = 0
        self.messages_non_vu = 0

        self.headers = Headers(self.screen, (0, 0, self.screen_width, self.line_height))
        self.headers.load({
            "Adresse : ": ("ADDR", "", 10),
            "Messages : ": ("ALL", "0", 500),
            "Non lus : ": ("UNSEEN", "0", 680)
        })

        self.repertoires = Repertoires(self.screen,
            (0, self.line_height, self.dirs_size, 
                self.screen_height-2*self.line_height))
        self.repertoires.load()

        self.liste_messages = ListeMessages(self.screen, 
            (
                self.dirs_size, 
                self.line_height, 
                self.screen_width-self.dirs_size, 
                self.screen_height-2*self.line_height))
        self.liste_messages.load()

        self.footers = Footers(self.screen,
            (0, self.screen_height-self.line_height, 
                self.screen_width, self.line_height))
        self.footers.load({
            " Dossiers ": (10, "DIR", self.toggle_repertoire),
            " Rafraichir ": (100, "REF", self.refresh_mails),
            " Loading ... ": (300, "LOD", None, True)
        })

    def quit(self):
        self.running = False

    def boot(self) -> None:
        pygame.init()
        self.init_fonts()
        self.initialize()
        self.init_draw()

    def shutdown(self) -> None:
        pygame.quit()

    def mouse_enter_leave(self) -> None: 
        self.liste_messages.mouse_exit()
        self.repertoires.mouse_exit()
    
    def mouse_move(self, pos) -> None:
        self.mouse = Mouse(*pos)

        if MessageBox.show:
            MessageBox.mouse_move(pos)
            return

        if self.repertoires.visible and self.repertoires.coords.collidepoint(pos):
            self.repertoires.mouse_move((pos[0], pos[1]-self.repertoires.y))

        elif self.repertoires.mouse_over:
            self.repertoires.mouse_exit()

        if self.liste_messages.coords.collidepoint(pos):
            dx = self.repertoires.w if self.repertoires.visible else 0
            self.liste_messages.mouse_move(
                (pos[0]-dx, pos[1]-self.liste_messages.y))

        elif self.liste_messages.mouse_over:
            self.liste_messages.mouse_exit()

        if self.footers.coords.collidepoint(pos):
            self.footers.mouse_move((pos[0], pos[1]-self.footers.y))

        elif self.footers.mouse_over:
            self.footers.mouse_exit()

    def mouse_button_down(self, pos, button): 
        if MessageBox.show:
            MessageBox.mouse_button_down(pos, button)
            return
        
        self.mouse_button_down_pos = pos
        mouse_pos = pos[0], pos[1]-self.screen_height+30

        if self.footers.coords.collidepoint(pos):
            self.footers.mouse_button_down(mouse_pos, button)

        elif (self.repertoires.visible and self.repertoires.coords.collidepoint(pos) and 
                self.repertoires.coords.collidepoint(self.mouse_button_down_pos)):
            self.repertoires.mouse_button_down((pos[0], pos[1]-self.repertoires.y), button)

    def mouse_button_up(self, pos, button) -> None:
        if MessageBox.show:
            MessageBox.mouse_button_up(pos, button)
            self.mouse_move(pygame.mouse.get_pos())
            return

        if button != 1:
            return

        mouse_pos = pos[0], pos[1]-self.screen_height+30
        if (self.footers.coords.collidepoint(pos) and 
                self.footers.coords.collidepoint(self.mouse_button_down_pos)):
            self.footers.mouse_button_up(mouse_pos, button)

        elif (self.repertoires.visible and self.repertoires.coords.collidepoint(pos) and 
                self.repertoires.coords.collidepoint(self.mouse_button_down_pos)):
            self.repertoires.mouse_button_up((pos[0], pos[1]-self.repertoires.y), button)

        elif self.liste_messages.coords.collidepoint(pos):
            self.liste_messages.mouse_button_up((pos[0], pos[1]-self.liste_messages.y), button)

    def mouse_wheel(self, x: int, y: int) -> None: 
        if MessageBox.show:
            MessageBox.mouse_move((x, y))
            return

        if self.liste_messages.coords.collidepoint(Mouse.x, Mouse.y):
            self.liste_messages.mouse_wheel(x, y)

        elif self.repertoires.visible and self.repertoires.coords.collidepoint(Mouse.x, Mouse.y):
            self.repertoires.mouse_wheel(x, y)

    def ask_for_quit(self):
        MessageBox.set_message(["Voulez-vous fermer l'application ?"])
        MessageBox.bouton_oui.set_callback(self.quit)
        MessageBox.activate()

    def keypressed(self, event): ...

    def keyreleased(self, event) -> None: 
        if event.key == pygame.K_ESCAPE:
            if MessageBox.show:
                MessageBox.deactivate()
                self.mouse_move(pygame.mouse.get_pos())
            else:
                self.ask_for_quit()
            return

        if self.liste_messages.mouse_over:
            self.liste_messages.keyreleased(event)

        elif self.repertoires.visible and self.repertoires.mouse_over:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                direction = 1 if event.key == pygame.K_UP else -1
                self.repertoires.mouse_wheel(Mouse.x, direction)

    def update_screen(self) -> None: 
        decal_x: int

        self.screen_width, self.screen_height = self.screen.get_size()

        self.headers.update_screen(self.screen, 
            (0, 0, self.screen_width, self.line_height))
        
        self.repertoires.update_screen(self.screen,
            (0, self.line_height, self.dirs_size, self.screen_height-2*self.line_height))

        if self.repertoires.visible:
            decal_x = self.dirs_size
        else:
            decal_x = 0

        self.liste_messages.update_screen(self.screen, 
            (decal_x, self.line_height, self.screen_width-decal_x, 
                self.screen_height-2*self.line_height))

        self.footers.update_screen(self.screen,
            (0, self.screen_height-self.line_height, self.screen_width, self.line_height))

        MessageBox.update_screen(self.screen)

    def get_pygame_events(self) -> None:
        is_mouse_scrolling: bool = False
        for event in pygame.event.get(pygame.MOUSEWHEEL):
            is_mouse_scrolling = True
            self.mouse_wheel(event.x, event.y)
            break

        for event in pygame.event.get():
            match event.type:
                case pygame.KMOD_LGUI:
                    self.mouse_move(event.pos)

                case pygame.MOUSEBUTTONDOWN:
                    if is_mouse_scrolling:
                        continue

                    if event.button != 2:
                        self.mouse_button_down(event.pos, event.button)

                case pygame.MOUSEBUTTONUP:
                    if is_mouse_scrolling:
                        continue
                    
                    self.mouse_button_up(event.pos, event.button)

                case pygame.MOUSEWHEEL:
                    fprint("Event mouse wheel")
                    self.mouse_wheel(event.x, event.y)

                case pygame.KEYDOWN:
                    self.keypressed(event)

                case pygame.KEYUP:
                    self.keyreleased(event)

                case (pygame.AUDIO_S8 | 
                        pygame.AUDIO_S16 | 
                        pygame.WINDOWENTER | 
                        pygame.ACTIVEEVENT):
                    self.mouse_enter_leave()

                case (pygame.WINDOWMAXIMIZED |
                        pygame.WINDOWSIZECHANGED |
                        pygame.WINDOWRESIZED |
                        pygame.WINDOWRESTORED):
                    pass

                case pygame.VIDEORESIZE:
                    self.update_screen()

                case pygame.QUIT:
                    self.running = False

                case (pygame.WINDOWSHOWN | 
                        pygame.WINDOWMOVED |
                        pygame.VIDEOEXPOSE | 
                        pygame.WINDOWCLOSE | 
                        pygame.WINDOWFOCUSGAINED):
                    pass

                case pygame.TEXTEDITING:
                    pass

                case pygame.JOYDEVICEADDED | pygame.AUDIODEVICEADDED:
                    pass

                case _:
                    fprint(event.type, get_pygame_const_name(event.type))
                    pass

    def update_repertoires(self) -> None:
        actions: Optional[str]
        
        actions = self.repertoires.get_actions()
        if actions is None:
            return

        key: str
        value: str

        for action in actions.split(";"):
            key, value = action.split("=")
            match key:
                case "DIR":
                    if value != self.liste_messages.directory:
                        self.liste_messages.directory = f'"{value}"'
                        self.liste_messages.load()

                case _:
                    raise Exception(f"Paramètre {key} inconnu.")

    def update_liste_messages(self) -> None:
        actions: Optional[str]
        
        actions = self.liste_messages.get_actions()
        if actions is None:
            return

        key: str
        value: str
        repertoire: str = ""

        for action in actions.split(";"):
            key, value = action.split("=")
            match key:
                case "USER":
                    if value != self.headers.liens[1].libelle:
                        # compte connecte
                        self.headers.get("ADDR").set_libelle(value)

                case "DIR":
                    repertoire = value
                    repertoire = repertoire

                case "ALL":
                    self.nb_messages = int(value)

                case "UNSEEN":
                    self.messages_non_vu = int(value)

                case "LOADING":
                    loading = eval(value)
                    self.footers.get("LOD").set_visible(loading)
                    self.mouse_move(pygame.mouse.get_pos())

        if self.nb_messages != int(self.headers.liens[3].libelle):
            # nb total de messages
            self.headers.get("ALL").set_libelle(str(self.nb_messages))

        if self.messages_non_vu != int(self.headers.liens[5].libelle):
            # nb de messages non lu
            self.headers.get("UNSEEN").set_libelle(str(self.messages_non_vu))

    def update(self) -> None:
        self.update_repertoires()
        self.update_liste_messages()

    def draw(self) -> None:
        self.clock.tick(60)

        self.headers.draw()
        self.repertoires.draw()
        self.liste_messages.draw()
        self.footers.draw()

        MessageBox.draw()

        pygame.display.update()

    def refresh_mails(self) -> None:
        self.liste_messages.refresh()

    def toggle_repertoire(self) -> None: 
        self.repertoires.toggle()

        if self.repertoires.visible:
            self.liste_messages.update_screen(self.screen, 
                (self.dirs_size, self.line_height, 
                self.screen_width-self.dirs_size, self.screen_height-2*self.line_height))
        else:
            self.liste_messages.update_screen(self.screen, 
                (0, self.line_height, self.screen_width, 
                    self.screen_height-2*self.line_height))

    def run(self) -> None:
        self.boot()
        while self.running:
            self.update()
            self.draw()
            self.get_pygame_events()

        self.shutdown()


def main() -> None:
    lect: Lecteur

    lect = Lecteur()
    lect.run()


if __name__ == '__main__':
    main()
