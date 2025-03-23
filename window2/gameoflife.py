import random
from classes import Application
from colors import Colors


class GameOfLife(Application):

    DEFAULT_CONFIG = ("Jeu de la vie", Colors.BLUE)

    MIN_SIZE = (300, 200)

    SIZE = 10
    ROWS, COLS = 0, 0
    updating = True  # True
    olds = 0
    compteur = 0

    def __init__(self, screen, args):
        super().__init__(screen)
        self.grid = []
        self.resize(screen)
        self.action = ""
        self.mouse_button_state = 0

    def initialisation(self, grid, rand=True):
        grid.clear()
        for _ in range(self.COLS):
            grid.append([random.randint(0, 1) if rand else 0 for _ in range(self.ROWS)])

    def resize(self, screen):
        self.screen = screen
        width, height = self.screen.get_size()
        self.ROWS = width // self.SIZE
        self.COLS = height // self.SIZE
        self.initialisation(self.grid)
        self.mouse_button_state = 0

    def get_action(self):
        return self.action

    def nbVoisins(self, x, y):
        somme = 0
        for i in range(max(0, x-1), min(self.COLS, x+2)):
            for j in range(max(0, y-1), min(self.ROWS, y+2)):
                somme += self.grid[i][j]
        return somme

    def new_frame(self):
        newgrid = []
        self.initialisation(newgrid, False)
        for i, col in enumerate(self.grid):
            for j, c in enumerate(col):
                nb = self.nbVoisins(i, j)
                if self.grid[i][j] == 1 and nb in (3, 4) or self.grid[i][j] == 0 and nb == 3:
                    newgrid[i][j] = 1
                else:
                    newgrid[i][j] = 0
        self.grid = newgrid.copy()

    def keyreleased(self, event):
        self.touche = self.keys.get_key()
        if self.touche == 27:
            self.action = "QUIT"

        elif self.touche in (self.keys.K_KP_ENTER, self.keys.K_RETURN):
            self.initialisation(self.grid)

        elif self.touche == self.keys.K_SPACE:
            self.updating = not self.updating

    def update(self):
        pass

    def mouse_button_down(self, mouseX, mouseY, button):
        self.mouse_button_state = button

    def mouse_button_up(self, mouseX, mouseY, button):
        self.mouse_button_state = 0
        x = mouseX // self.SIZE
        y = mouseY // self.SIZE
        if y < self.COLS and x < self.ROWS:
            self.grid[y][x] = 1

    def mouse_move(self, mouseX, mouseY):
        x = mouseX // self.SIZE
        y = mouseY // self.SIZE
        if self.mouse_button_state > 0:
            if y < self.COLS and x < self.ROWS:
                try:
                    self.grid[y][x] = 1
                except IndexError:
                    print("x:", x, " y:", y, " ROWS:", self.ROWS, " COLS:", self.COLS)

    def draw(self):
        self.screen.fill(Colors.BLACK)
        s = sum([sum(x) for x in self.grid])
        if self.olds == s:
            self.compteur += 1
        else:
            self.compteur = 0
            self.olds = s
        if self.compteur > 100:
            self.initialisation(self.grid)

        for i, col in enumerate(self.grid):
            for j, c in enumerate(col):
                if c == 1:
                    color = (200, 200, 200)
                else:
                    color = (0, 50, 50)
                self.tools.rect(color, (j*self.SIZE, i*self.SIZE, self.SIZE, self.SIZE))
                
        self.update()
        if self.mouse_button_state == 0 and self.updating:
            self.new_frame()


if __name__ == '__main__':
    from exec import run
    run(GameOfLife)
