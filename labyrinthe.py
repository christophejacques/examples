import pygame
import random


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


class Laby:
    def __init__(self, cell_size, w, h):
        self.cell_size = cell_size
        self.chemin = None
        self.show_soluce = False

        self.set_size(w, h)

    def set_size(self, w, h):
        self.w = w
        self.h = h
        # flags=pygame.NOFRAME
        self.screen = pygame.display.set_mode((1+w, 1+h), flags=pygame.SHOWN, vsync=1)
        self.prepare_board()        

    def prepare_board(self):
        self.train = []
        self.coord = None
        self.width = self.w // self.cell_size
        self.height = self.h // self.cell_size
        self.debut = random.randint(0, self.width-1)
        self.fin = random.randint(0, self.width-1)
        self.generated = False
        self.cells = []
        for _ in range(self.width):
            colonne = [Cellule() for _ in range(self.height)]
            self.cells.append(colonne)

    def is_done(self, i, j):
        res = self.cells[i-1][j].updated if i > 0 else True
        if res and j > 0: 
            res = self.cells[i][j-1].updated
        if res and i < self.width-1: 
            res = self.cells[i+1][j].updated
        if res and j < self.height-1: 
            res = self.cells[i][j+1].updated

        return res

    def update(self, x, y, i, j):
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
                self.update(x, y, i, j)
                pile.push((x, y))

                x += i
                y += j

                if y == self.height-1 and x == self.fin and not self.chemin:
                    # chemin trouve
                    self.chemin = pile.copy()
                    self.chemin.append((x, y))
                    print(f"Chemin de {len(self.chemin)} cases")

                if self.is_done(x, y):
                    self.cells[x][y].updated = True
                    break

            self.draw()

        self.generated = True
        return True

    def follow_chemin(self):
        for coord in self.chemin:
            yield coord

    def draw_cell(self, x, y, bg_color):
        pygame.draw.rect(self.screen, bg_color, ((x*self.cell_size, y*self.cell_size), 
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

    def draw(self):
        if self.generated:
            self.screen.fill((20, 20, 20))
        else:
            self.screen.fill((60, 30, 20))

        bg_color = (10, 80, 20)

        pos1 = (0, 0)
        pos2 = (self.width*self.cell_size, 0)

        # Chemin : Debut -> Fin
        if self.show_soluce and self.chemin:
            for x, y in self.chemin:
                self.draw_cell(x, y, bg_color)

        self.draw_train()

        # Ligne Top fenetre
        pygame.draw.line(self.screen, (255, 255, 255), pos1, pos2)
        # Cellule Debut
        self.draw_cell(self.debut, 0, bg_color)
        pos2 = (0, self.height*self.cell_size)
        # Ligne Bottom fenetre
        pygame.draw.line(self.screen, (255, 255, 255), pos1, pos2)
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
                    pygame.draw.line(self.screen, (255, 255, 255), pos1, pos2)

                if self.cells[i][j].droite:
                    pos1 = ((i+1)*self.cell_size, j*self.cell_size)
                    pygame.draw.line(self.screen, (255, 255, 255), pos1, pos2)

        pygame.display.update()


def main():
    running = True
    pygame.display.init()

    laby = Laby(20, 1600, 800)
    laby.generate()
    clock = pygame.time.Clock()
    
    while running:
        clock.tick(60)
        laby.draw()

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F1:
                    laby.show_soluce = not laby.show_soluce

                elif event.key == pygame.K_KP_PLUS: 
                    if event.mod & pygame.KMOD_LALT == pygame.KMOD_LALT:
                        laby.set_size(laby.w, laby.h+laby.cell_size)
                        laby.generate()
                    elif event.mod & pygame.KMOD_LCTRL == pygame.KMOD_LCTRL:
                        laby.set_size(laby.w+laby.cell_size, laby.h)
                        laby.generate()
                    else:
                        laby.cell_size += 10 
                        laby.prepare_board()
                        laby.generate()
                elif event.key == pygame.K_KP_MINUS and laby.cell_size > 10: 
                    if event.mod & pygame.KMOD_LALT == pygame.KMOD_LALT:
                        laby.set_size(laby.w, laby.h-laby.cell_size)
                        laby.generate()
                    elif event.mod & pygame.KMOD_LCTRL == pygame.KMOD_LCTRL:
                        laby.set_size(laby.w-laby.cell_size, laby.h)
                        laby.generate()
                    else:
                        laby.cell_size -= 10 
                        laby.prepare_board()
                        laby.generate()

                elif event.key == pygame.K_SPACE:
                    laby.prepare_board()
                    laby.generate()

            elif event.type == pygame.QUIT:
                running = False

        pygame.display.update()


if __name__ == '__main__':
    main()
    pygame.display.quit()
