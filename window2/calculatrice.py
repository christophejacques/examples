from classes import Application


class Ecran:

    def __init__(self, parent, display_bg=True, fore_color=None, coords=None):
        self.set_tools(parent)
        self.initial_fore_color = fore_color
        self.texte = ""

        if display_bg:
            self.ecran_rect = self.tools.Rect((
                10, 10, 4*Touche.LARGUEUR_BTN+3*Calculatrice.ESPACE_BTN, 80))
            self.we, self.he = self.ecran_rect.size
            self.FONT = self.tools.font("comicsans", 30)
        else:
            self.coords = coords
            self.FONT = self.tools.font("comicsans", 20)

        self.get_theme(parent)
        self.display_bg = display_bg
        self.set_display("")

    def get_theme(self, parent):
        self.theme = parent.theme
        if self.initial_fore_color is None:
            self.fore_color = self.theme.get("FORE_COLOR")
        else:
            self.fore_color = self.theme.get(self.initial_fore_color)

        self.texte_surf = self.FONT.render(self.texte, False, self.fore_color)

    def set_tools(self, parent):
        self.tools = parent.tools

    def get_texte(self):
        return self.texte

    def add_texte(self, texte):
        self.texte += texte

    def set_display(self, texte):
        self.texte = texte[:15]
        texte_surf = self.FONT.render(self.texte, False, self.fore_color)
        wt, ht = texte_surf.get_size()
        self.texte_surf = texte_surf

        if self.display_bg:
            self.texte_rect = (self.we - wt, 20+(self.he - ht)//2, wt, ht)
        else:
            self.texte_rect = self.coords

    def draw(self):
        if self.display_bg:
            self.tools.rect(self.theme.get("BOUTON_COLOR"), self.ecran_rect)

        self.tools.blit(self.texte_surf, self.texte_rect)

class Touche:

    LARGUEUR_BTN: int = 70
    HAUTEUR_BTN: int = 50

    def __init__(self, parent, texte, coords, deltas=(0, 0)):

        self.ligne, self.col = coords
        dx, dy = deltas
        self.texte = texte
        self.set_tools(parent)
        self.get_theme(parent)
        width, height = self.texte_surf.get_size()
        self.is_mouse_over = False

        self.touche_rect = self.tools.Rect(
            (10+(Touche.LARGUEUR_BTN+Calculatrice.ESPACE_BTN)*self.col, 
            100+(Touche.HAUTEUR_BTN+Calculatrice.ESPACE_BTN)*self.ligne, 
            Touche.LARGUEUR_BTN+dx*(Touche.LARGUEUR_BTN+Calculatrice.ESPACE_BTN), 
            Touche.HAUTEUR_BTN+dy*(Touche.HAUTEUR_BTN+Calculatrice.ESPACE_BTN), 
        ))

        self.texte_rect = self.tools.Rect(
            (( (Touche.LARGUEUR_BTN-width) + dx*(Touche.LARGUEUR_BTN+Calculatrice.ESPACE_BTN) )//2+10+
                (Touche.LARGUEUR_BTN+Calculatrice.ESPACE_BTN)*self.col, 
            102+(Touche.HAUTEUR_BTN+Calculatrice.ESPACE_BTN)*self.ligne, 
            dx, 20))

    def get_theme(self, parent):
        self.theme = parent.theme
        color: str = self.theme.get("BOUTON_COLOR")
        self.back_color(color)

        texte_surf = self.tools.font("comicsans", 30).render(self.texte, False, self.theme.get("FORE_COLOR"))
        self.texte_surf = texte_surf


    def set_tools(self, parent):
        self.tools = parent.tools

    def get_texte(self):
        return self.texte

    def has_mouse_over(self, mouse):
        self.is_mouse_over = self.touche_rect.collidepoint(mouse)
        return self.is_mouse_over

    def back_color(self, color):
        self.bgcolor = color

    def get_color(self, color):
        return self.bgcolor

    def draw(self):
        self.tools.rect(self.bgcolor, self.touche_rect)
        self.tools.blit(self.texte_surf, self.texte_rect)


class Calculatrice(Application):

    DEFAULT_CONFIG = ("Calculatrice", (150, 150, 150))
    MIN_SIZE = (325, 405)
    WINDOW_PROPERTIES = []
    ESPACE_BTN: int = 5

    def __init__(self, screen, *args):
        super().__init__(screen)
        self.title = self.DEFAULT_CONFIG[0]
        self.action = ""
        self.mouse_over = None
        self.mouse_btn_down = None
        self.result = "0"
        self.old_operator = ""
        self.operator = ""

        self.touches: list = list()
        self.ecran = Ecran(self)
        self.memory = Ecran(self, False, "GRAY_COLOR", (20, 10, 200, 70))
        self.get_theme()
        nombre = self.registre.load("Utilisation", 0)
        self.registre.save("Utilisation", 1+nombre)

        for ligne, valeur in enumerate(["CE","C", "<"]):
            touche = Touche(self, valeur, (0, ligne))
            self.touches.append(touche)

        for ligne in range(1, 4):
            for col in range(3):
                touche = Touche(self, f"{1+col+3*(3-ligne)}", (ligne, col))
                self.touches.append(touche)
        
        self.touches.append(Touche(self, "0", (4, 0), (1, 0)))
        self.touches.append(Touche(self, ".", (4, 2)))

        for ligne, valeur in enumerate(["/","*", "-", "+", "="]):
            touche = Touche(self, valeur, (ligne, 3))
            self.touches.append(touche)

    def post_init(self):
        self.set_title(self.title)
        self.win_resize("BOTTOM RIGHT", 0, 0, *self.MIN_SIZE)
        self.draw_init()

    def resize(self, screen):
        for touche in self.touches:
            touche.set_tools(self)

        self.ecran.set_tools(self)
        self.memory.set_tools(self)

    def get_theme(self):
        # print("get_theme:", self.theme.get_theme(), flush=True)

        self.ecran.get_theme(self)
        self.memory.get_theme(self)

        for touche in self.touches:
            touche.get_theme(self)

        self.draw_init()

    def mouse_enter(self, mouseX, mouseY):
        pass

    def mouse_exit(self):
        for touche in self.touches:
            if touche.get_color == self.theme.get("BOUTON_COLOR"):
                continue

            touche.back_color(self.theme.get("BOUTON_COLOR"))
            touche.draw()

    def keypressed(self, event):
        # print(event, flush=True)
        touche = self.keys.get_key()
        for touche in self.touches:
            if touche.get_texte() == event.unicode and event.unicode in ("/*-+1234567890."):
                touche.back_color(self.theme.get("PUSH_COLOR"))
                touche.draw()

            elif touche.get_texte() == "=" and event.unicode == "\r":
                touche.back_color(self.theme.get("PUSH_COLOR"))
                touche.draw()

            elif touche.get_texte() == "<" and event.unicode == "\x08":
                touche.back_color(self.theme.get("PUSH_COLOR"))
                touche.draw()

            elif touche.get_texte() == "C" and event.unicode == "\x1b":
                touche.back_color(self.theme.get("PUSH_COLOR"))
                touche.draw()
                

    def keyreleased(self, event):
        # print(event, flush=True)
        # touche = self.keys.get_key()
        if event.key == 27 and self.ecran.get_texte() == "":
            self.action = "QUIT"

        self.compute_touche(event.unicode)

        for touche in self.touches:
            if touche.get_texte() == event.unicode:
                touche.back_color(self.theme.get("BOUTON_COLOR"))
                touche.draw()

            elif touche.get_texte() == "=" and event.unicode == "\r":
                touche.back_color(self.theme.get("BOUTON_COLOR"))
                touche.draw()

            elif touche.get_texte() == "<" and event.unicode == "\x08":
                touche.back_color(self.theme.get("BOUTON_COLOR"))
                touche.draw()

            elif touche.get_texte() == "C" and event.unicode == "\x1b":
                touche.back_color(self.theme.get("BOUTON_COLOR"))
                touche.draw()
                
    def compute_touche(self, touche):

        match touche:
            case "CE":
                self.result = "0"
                self.ecran.set_display("")
                self.memory.set_display("")
                self.operator = ""

            case "C" | "\x1b":
                self.ecran.set_display("")

            case "<" | "\x08":
                self.ecran.set_display(self.ecran.get_texte()[:-1])

            case car if car in "123456789":
                if self.operator == "=":
                    self.ecran.set_display("")
                    self.operator = ""

                self.ecran.add_texte(car)
                self.ecran.set_display(self.ecran.get_texte())

            case "0":
                if self.operator == "=":
                    self.ecran.set_display("0")
                    self.operator = ""

                elif self.ecran.get_texte() != "0":
                    self.ecran.add_texte("0")
                    self.ecran.set_display(self.ecran.get_texte())

            case ".":
                if self.ecran.get_texte() == "":
                    self.ecran.add_texte("0.")
                    self.ecran.set_display(self.ecran.get_texte())

                elif "." not in self.ecran.get_texte():
                    if self.operator == "=":
                        self.ecran.set_display("0.")
                        self.operator = ""
                    else:
                        self.ecran.add_texte(".")
                        self.ecran.set_display(self.ecran.get_texte())

            case car if car in "/*-+":
                self.old_operator = ""
                if self.operator in ("", "="):
                    self.result = self.ecran.get_texte()
                    self.memory.set_display(self.result+" "+car)
                    self.ecran.set_display("")

                elif self.ecran.get_texte() != "":
                    self.memory.set_display(f"{self.result}{self.operator}{self.ecran.get_texte()}")
                    try:
                        self.result = str(eval(f"{self.result}{self.operator}{self.ecran.get_texte()}"))
                        if self.result[-2:] == ".0":
                            self.result = self.result[:-2]
                        self.ecran.set_display("")
                    except Exception as erreur:
                        print(erreur, flush=True)
                        self.result = "0"
                        self.ecran.set_display("#N/A")

                self.operator = car
                self.old_operator = self.operator

            case "=" | "\r":
                valeur = self.ecran.get_texte()
                if self.operator not in ("", "=") and valeur:
                    self.old_operator = self.operator
                    # print(f"=> {self.result}{self.operator}{valeur}", flush=True)
                    self.memory.set_display(f"{self.result}{self.operator}{valeur}")
                    try:
                        self.result = str(eval(f"{self.result}{self.operator}{valeur}"))
                        if self.result[-2:] == ".0":
                            self.result = self.result[:-2]
                        self.ecran.set_display(self.result)
                    except Exception as erreur:
                        print(erreur, flush=True)
                        self.ecran.set_display("#N/A")

                else:
                    # appui une 2eme fois de suite sur "="
                    index = self.memory.get_texte().find(self.old_operator)
                    if index >= 0:
                        try:
                            resultat_precedent = self.result
                            self.result = str(eval(f"{self.result}{self.memory.get_texte()[index:]}"))
                            self.memory.set_display(f"{resultat_precedent}{self.memory.get_texte()[index:]}")
                            if self.result[-2:] == ".0":
                                # Supression des chiffres après la virgule quand 
                                # il s'agit d'un nombre entier
                                self.result = self.result[:-2]
                            self.ecran.set_display(self.result)

                        except Exception as erreur:
                            print(erreur, flush=True)
                            self.ecran.set_display("#N/A")
                    
                self.operator = "="

        self.ecran.draw()
        self.memory.draw()

    def mouse_move(self, mouseX, mouseY):
        self.mouse_over = None
        for touche in self.touches:
            was_mouse_over = touche.is_mouse_over
            if touche.has_mouse_over((mouseX, mouseY)):
                self.mouse_over = touche

            if touche.is_mouse_over:
                if self.mouse_btn_down is None:
                    touche.back_color(self.theme.get("MOUSE_OVER_COLOR"))
                elif self.mouse_btn_down == self.mouse_over:
                    touche.back_color(self.theme.get("PUSH_COLOR"))
                else:
                    touche.back_color(self.theme.get("BOUTON_COLOR"))
            else:
                touche.back_color(self.theme.get("BOUTON_COLOR"))

            if touche.is_mouse_over != was_mouse_over:
                touche.draw()

    def mouse_button_down(self, mouseX, mouseY, button):
        if self.mouse_over:
            self.mouse_btn_down = self.mouse_over
            self.mouse_btn_down.back_color(self.theme.get("PUSH_COLOR"))
            self.mouse_btn_down.draw()
        else:
            self.mouse_btn_down = None

    def mouse_button_up(self, mouseX, mouseY, button):
        if not (self.mouse_over and self.mouse_btn_down == self.mouse_over):
            return

        # print(self.mouse_over.texte, flush=True)
        self.mouse_btn_down.back_color(self.theme.get("MOUSE_OVER_COLOR"))
        self.mouse_btn_down.draw()

        self.compute_touche(self.mouse_over.texte)
        self.mouse_btn_down = None


    def get_action(self):
        return self.action

    def update(self):
        pass

    def draw_init(self):
        self.ecran.draw()
        self.memory.draw()

        for touche in self.touches:
            touche.draw()

    def draw(self):
        pass


if __name__ == '__main__':
    from exec import run
    run(locals())
