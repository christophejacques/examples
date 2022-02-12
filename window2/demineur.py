import pygame
import random
from mouse import Mouse
from colors import Colors

from classes import Application


class Cell:
    width = 48
    decal = 2
    size = width+decal

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bee = False
        self.revealed = False
        self.marked = False
        self.nb_bees = 0

    def draw_rect(self):
        return (self.x)*(Cell.decal+Cell.width), self.y*(Cell.decal+Cell.width), Cell.width, Cell.width

    def draw_square(self):
        return (self.x)*(Cell.decal+Cell.width), self.y*(Cell.decal+Cell.width), Cell.width, Cell.width

    def draw_circle(self):
        return (int(Cell.width//2+(self.x)*(Cell.decal+Cell.width)), int(Cell.width//2+self.y*(Cell.decal+Cell.width))), int(Cell.width/2.5)

    def draw_text(self):
        return 4+Cell.width//4+(self.x)*(Cell.decal+Cell.width), self.y*(Cell.decal+Cell.width), Cell.width


class Demineur(Application):

    DEFAULT_CONFIG = ("Démineur", Colors.LIGHT_BLUE)

    MIN_SIZE = (200, 200)
    TAILLE = 10

    MARKED = (100, 100, 20)

    x = 0
    y = 0

    def __init__(self, parent, screen, *args):
        self.grid = []
        self.parent = parent
        self.screen = screen
        self.SYS_FONT = pygame.font.SysFont("comicsans", 30)
        self.cursor_cell_over = None

    def post_init(self):
        w, h = self.screen.get_size()
        longueur = min(w, h)//Cell.size * Cell.size
        self.parent.resize("BOTTOM RIGHT", -(w-longueur), -(h-longueur))

    def resize(self, screen):
        self.screen = screen
        self.initialize()

    def initialize(self):
        self.action = ""
        # initialisation du tableau 2D
        self.TAILLE = min(self.screen.get_size())//50
        self.parent.set_title(f"Demineur taille: {self.TAILLE}")
        self.grid.clear()
        for row in range(self.TAILLE):
            colonne = []
            for col in range(self.TAILLE):
                colonne.append(Cell(row, col))
            self.grid.append(colonne)

        # ajout des bombes
        for _ in range(self.TAILLE*self.TAILLE//5):
            lx = random.randint(0, self.TAILLE-1)
            ly = random.randint(0, self.TAILLE-1)
            while self.grid[lx][ly].bee:
                lx = random.randint(0, self.TAILLE-1)
                ly = random.randint(0, self.TAILLE-1)
            self.grid[lx][ly].bee = True

        # comptage des bombes
        for row in range(self.TAILLE):
            for col in range(self.TAILLE):
                self.grid[col][row].nb_bees = self.get_bee_numbers(col, row)

    def get_action(self):
        return self.action

    def get_bee_numbers(self, x, y):
        nb = 0
        for row in range(max(0, y-1), min(self.TAILLE, y+2)):
            for col in range(max(0, x-1), min(self.TAILLE, x+2)):
                if self.grid[col][row].bee:
                    nb += 1
        return nb

    def graph_print(self, x, y, color):
        trect = self.grid[x][y].draw_text()
        trect += (trect[-1],)
        texte_surf = self.SYS_FONT.render("{}".format(self.grid[x][y].nb_bees), False, color)
        self.screen.blit(texte_surf, trect)

    def grid_resolved(self):
        for row in range(self.TAILLE):
            for col in range(self.TAILLE):
                if not (self.grid[col][row].marked and self.grid[col][row].bee or self.grid[col][row].revealed):
                    return False
        self.parent.set_title("Demineur terminé")
        return True

    def reveal_zeros(self, x, y):
        if not self.grid[x][y].revealed:
            self.grid[x][y].revealed = True
            self.grid[x][y].marked = False
            if self.grid[x][y].nb_bees == 0:
                for row in range(max(0, y-1), min(self.TAILLE, y+2)):
                    for col in range(max(0, x-1), min(self.TAILLE, x+2)):
                        self.reveal_zeros(col, row)

    def show_all(self):
        for row in range(self.TAILLE):
            for col in range(self.TAILLE):
                self.grid[col][row].revealed = True

    def mouse_move(self, mouseX, mouseY):
        col = mouseX // 50
        row = mouseY // 50
        if 0 <= col < self.TAILLE and 0 <= row < self.TAILLE:
            lrect = pygame.Rect(*self.grid[col][row].draw_rect())
            self.cursor_cell_over = lrect
        else:
            self.cursor_cell_over = None

    def mouse_enter(self, mouseX, mouseY):
        # print("mouse_enter()")
        self.mouse_move(mouseX, mouseY)

    def mouse_exit(self):
        self.cursor_cell_over = None

    def mouse_button_up(self, mouseX, mouseY, button):
        x = mouseX // 50
        y = mouseY // 50
        if 0 <= x < self.TAILLE and 0 <= y < self.TAILLE:
            if button == 1:
                self.grid[x][y].marked = False
                if self.grid[x][y].bee:
                    self.show_all()
                else:
                    self.reveal_zeros(x, y)
                    self.grid[x][y].revealed = True

            elif button == 3:
                if not self.grid[x][y].revealed:
                    self.grid[x][y].marked = not self.grid[x][y].marked

            if self.grid_resolved():
                self.show_all()

    def update(self):
        if not self.parent.keypressed():
            return 

        self.touche = self.parent.get_key()
        if self.touche == pygame.K_ESCAPE:
            self.action = "QUIT"
        elif self.touche == pygame.K_SPACE:
            self.initialize()
        elif self.touche == pygame.K_F1:
            self.show_all()
        else:
            print("keyCode:", self.touche)

    def draw(self):
        self.screen.fill(Colors.BLACK)
        for col in range(self.TAILLE):
            for row in range(self.TAILLE):
                if self.grid[col][row].revealed:
                    if self.grid[col][row].bee:
                        if self.grid[col][row].marked:
                            couleur_fond = self.MARKED
                        else:
                            couleur_fond = (200, 200, 200)
                        pygame.draw.rect(self.screen, couleur_fond, self.grid[col][row].draw_square())
                        if self.grid[col][row].marked:
                            couleur_fond = (0, 250, 0)
                        else:
                            couleur_fond = (250, 0, 0)
                        pygame.draw.circle(self.screen, couleur_fond, *self.grid[col][row].draw_circle())
                    else:
                        if self.grid[col][row].marked:
                            couleur_fond = self.MARKED
                        else:
                            couleur_fond = (200, 200, 200)
                        pygame.draw.rect(self.screen, couleur_fond, self.grid[col][row].draw_square())
                        if self.grid[col][row].marked:
                            self.graph_print(col, row, Colors.RED)
                        else:
                            self.graph_print(col, row, Colors.GREY)
                else:
                    if self.grid[col][row].marked:
                        couleur_fond = self.MARKED
                    else:
                        couleur_fond = (10, 10, 10)
                    pygame.draw.rect(self.screen, couleur_fond, self.grid[col][row].draw_square())

        if self.cursor_cell_over:
            pygame.draw.rect(self.screen, (0, 255, 0), (*self.cursor_cell_over.topleft, self.cursor_cell_over.width-2, self.cursor_cell_over.width-2), 4)
