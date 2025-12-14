import random

from colors import Colors
from classes import Application


class Cellule:
    updated = False
    bas = True
    droite = True


class Pile:

    def __init__(self, val):
        self.data = [val]

    def copy(self):
        return self.data.copy()

    def is_empty(self):
        return len(self.data) == 0

    def push(self, val):
        self.data.append(val)

    def pop(self):
        return self.data.pop()


DIRECTION = {
    1: (1, 0),
    2: (0, 1),
    3: (-1, 0),
    4: (0, -1)
}


class Laby(Application):

    DEFAULT_CONFIG = ("Labyrinthe 10", Colors.MIDDLE_ORANGE, 10)

    MIN_SIZE = (400, 300)
    
    def __init__(self, args):  # args = cell_size
        self.title = self.DEFAULT_CONFIG[0]
        self.cell_size = args[0]
        self.chemin = None
        self.show_soluce = False
        self.touche = ""
        self.action = ""

    def post_init(self):
        w, h = self.tools.get_size()
        self.set_size(w, h)
        self.generate()
        self.get_theme()

    def get_theme(self):
        self.fore_color = self.theme.get("FORE_COLOR")
        self.back_color = self.theme.get("BACKGROUND_COLOR")

    def set_size(self, w, h):
        self.w = w
        self.h = h
        self.prepare_board()        

    def resize(self):
        self.set_size(*self.tools.get_size())
        self.generate()

    def prepare_board(self):
        self.train = []
        self.coord = None
        self.width = self.w // self.cell_size
        self.height = self.h // self.cell_size
        print(f"prepare board : {self.width}x{self.height}")
        self.debut = random.randint(0, self.width-1)
        self.fin = random.randint(0, self.width-1)
        self.generated = False
        self.cells = []
        for _ in range(self.width):
            colonne = [Cellule() for _ in range(self.height)]
            self.cells.append(colonne)

    def get_action(self):
        return self.action

    def is_done(self, i, j):
        res = self.cells[i-1][j].updated if i > 0 else True
        if res and j > 0: 
            res = self.cells[i][j-1].updated
        if res and i < self.width-1: 
            res = self.cells[i+1][j].updated
        if res and j < self.height-1: 
            res = self.cells[i][j+1].updated

        return res

    def update_cell(self, x, y, i, j):
        if i == -1: 
            self.cells[x-1][y].droite = False
        elif i == 1: 
            self.cells[x][y].droite = False
        elif j == -1: 
            self.cells[x][y-1].bas = False
        elif j == 1: 
            self.cells[x][y].bas = False

        self.cells[x][y].updated = True

    def next(self, x, y):
        i, j = DIRECTION[random.randint(1, 4)]
        while x+i < 0 or x+i >= self.width or y+j < 0 or y+j >= self.height:
            i, j = DIRECTION[random.randint(1, 4)]

        while self.cells[x+i][y+j].updated:
            i, j = DIRECTION[random.randint(1, 4)]
            while x+i < 0 or x+i >= self.width or y+j < 0 or y+j >= self.height:
                i, j = DIRECTION[random.randint(1, 4)]
        return i, j

    def generate(self):
        self.generated = False
        self.chemin = None
        pile = Pile((self.debut, 0))

        while not pile.is_empty():
            x, y = pile.pop()
            if self.is_done(x, y):
                continue

            while True:
                # recherche de la prochaine cellule non traitee
                i, j = self.next(x, y)
                self.update_cell(x, y, i, j)
                pile.push((x, y))

                x += i
                y += j

                if y == self.height-1 and x == self.fin and not self.chemin:
                    # chemin trouve
                    self.chemin = pile.copy()
                    self.chemin.append((x, y))
                    print(f"Chemin de {len(self.chemin)} cases", flush=True)

                if self.is_done(x, y):
                    self.cells[x][y].updated = True
                    break

            # self.draw()

        self.generated = True
        return True

    def follow_chemin(self):
        for coord in self.chemin:
            yield coord

    def draw_cell(self, x, y, bg_color):
        self.tools.rect(bg_color, ((x*self.cell_size, y*self.cell_size), 
            (self.cell_size, self.cell_size)))

    def draw_train(self):
        if self.chemin:
            if len(self.train) == 0 or self.coord is None:
                self.coord = iter(self.follow_chemin())
            try:
                self.train.append(next(self.coord))
                if len(self.train) > 50: 
                    self.train.pop(0)
            except StopIteration:
                if len(self.train) > 0:
                    self.train.pop(0)

            for cell in self.train:
                self.draw_cell(*cell, (80, 70, 200))

    def keyreleased(self, event):
        self.touche = self.keys.get_key()
        if self.touche == 27:
            self.action = "QUIT"
        elif self.touche == self.keys.K_F1:
            self.show_soluce = not self.show_soluce

        elif self.touche == self.keys.K_SPACE:
            self.prepare_board()
            self.generate()

    def update(self):
        pass

    def draw(self):
        if self.generated:
            self.tools.fill(self.back_color)
        else:
            self.tools.fill((60, 30, 20))

        bg_color = (10, 80, 20)

        pos1 = (0, 0)
        pos2 = (self.width*self.cell_size, 0)

        # Chemin : Debut -> Fin
        if self.show_soluce and self.chemin:
            for x, y in self.chemin:
                self.draw_cell(x, y, bg_color)

        self.draw_train()

        # Ligne Top fenetre
        self.tools.line(self.fore_color, pos1, pos2)
        # Cellule Debut
        self.draw_cell(self.debut, 0, bg_color)
        pos2 = (0, self.height*self.cell_size)
        # Ligne Bottom fenetre
        self.tools.line(self.fore_color, pos1, pos2)
        # Cellule Fin
        self.draw_cell(self.fin, self.height-1, bg_color)

        # Labyrinthe
        for j in range(self.height):
            for i in range(self.width):
                if i == self.fin and j == self.height-1:
                    continue
                pos2 = ((i+1)*self.cell_size, (j+1)*self.cell_size)
                if self.cells[i][j].bas:
                    pos1 = (i*self.cell_size, (j+1)*self.cell_size)
                    self.tools.line(self.fore_color, pos1, pos2)

                if self.cells[i][j].droite:
                    pos1 = ((i+1)*self.cell_size, j*self.cell_size)
                    self.tools.line(self.fore_color, pos1, pos2)


if __name__ == '__main__':
    from exec import run
    run(locals())
