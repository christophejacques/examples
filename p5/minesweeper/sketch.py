import random
from __init__ import background, createCanvas, stroke, noFill, fill, circle, square
from __init__ import P5, strokeWeight, pygame
from __init__ import *
from cell import Cell


pygame.init()

SYS_FONT = pygame.font.SysFont("comicsans", 30)
TAILLE = 10

GREY = (10, 50, 50)
RED = (255, 0, 0)
MARKED = (100, 100, 20)

grid = []
x = 0
y = 0


def get_bee_numbers(x, y):
    nb = 0
    for row in range(max(0, y-1), min(TAILLE, y+2)):
        for col in range(max(0, x-1), min(TAILLE, x+2)):
            if grid[col][row].bee:
                nb += 1
    return nb


def initialize():
    # initialisation du tableau 2D
    grid.clear()
    for row in range(TAILLE):
        colonne = []
        for col in range(TAILLE):
            colonne.append(Cell(row, col))
        grid.append(colonne)

    # ajout des bombes
    for _ in range(TAILLE*TAILLE//5):
        lx = random.randint(0, TAILLE-1)
        ly = random.randint(0, TAILLE-1)
        while grid[lx][ly].bee:
            lx = random.randint(0, TAILLE-1)
            ly = random.randint(0, TAILLE-1)
        grid[lx][ly].bee = True

    # comptage des bombes
    for row in range(TAILLE):
        for col in range(TAILLE):
            grid[col][row].nb_bees = get_bee_numbers(col, row)


def keyReleased():
    if P5.keyCode == 32:
        initialize()
    elif P5.keyCode == 1073741882:
        show_all()
    else:
        print("keyCode:", P5.keyCode)


def graph_print(x, y, color):
    trect = grid[x][y].draw_text()
    trect += (trect[-1],)
    texte_surf = SYS_FONT.render("{}".format(grid[x][y].nb_bees), False, color)
    P5.CANVAS.blit(texte_surf, trect)


def grid_resolved():
    for row in range(TAILLE):
        for col in range(TAILLE):
            if not (grid[col][row].marked and grid[col][row].bee or grid[col][row].revealed):
                return False
    return True


def reveal_zeros(x, y):
    if not grid[x][y].revealed:
        grid[x][y].revealed = True
        grid[x][y].marked = False
        if grid[x][y].nb_bees == 0:
            for row in range(max(0, y-1), min(TAILLE, y+2)):
                for col in range(max(0, x-1), min(TAILLE, x+2)):
                    reveal_zeros(col, row)


def show_all():
    for row in range(TAILLE):
        for col in range(TAILLE):
            grid[col][row].revealed = True


def mouseReleased():
    x = P5.mouseX // (2+Cell.width)
    y = P5.mouseY // (2+Cell.width)
    # print("click:", x, y)
    if P5.mouseIsPressed == 1:
        grid[x][y].marked = False
        if grid[x][y].bee:
            show_all()
        else:
            reveal_zeros(x, y)
            grid[x][y].revealed = True

    elif P5.mouseIsPressed == 3:
        if not grid[x][y].revealed:
            grid[x][y].marked = not grid[x][y].marked

    if grid_resolved():
        show_all()
    

def setup():
    createCanvas(50*TAILLE, 50*TAILLE)
    stroke(255)
    initialize()


def draw():
    background(0)
    for col in range(TAILLE):
        for row in range(TAILLE):
            if grid[col][row].revealed:
                if grid[col][row].bee:
                    if grid[col][row].marked:
                        fill(*MARKED)
                    else:
                        fill(200)
                    square(*grid[col][row].draw_square())
                    if grid[col][row].marked:
                        fill(0, 250, 0)
                    else:
                        fill(250, 0, 0)
                    circle(*grid[col][row].draw_circle())
                else:
                    if grid[col][row].marked:
                        fill(*MARKED)
                    else:
                        fill(200)
                    square(*grid[col][row].draw_square())
                    if grid[col][row].marked:
                        graph_print(col, row, RED)
                    else:
                        graph_print(col, row, GREY)
            else:
                if grid[col][row].marked:
                    fill(*MARKED)
                else:
                    fill(10)
                square(*grid[col][row].draw_square())

            lrect = pygame.Rect(*grid[col][row].draw_rect())
            if lrect.collidepoint(P5.mouseX, P5.mouseY):
                stroke(0, 255, 0)
                strokeWeight(4)
                noFill()
                square(*lrect.topleft, lrect.width-2)
                strokeWeight(1)
                stroke(255)


__import__("run")
