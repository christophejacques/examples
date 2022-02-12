import random
from __init__ import background, createCanvas, stroke, fill, circle, rect, square, rectMode
from __init__ import P5, strokeWeight, noStroke, map, Vector, line
from __init__ import *


SIZE = 10
ROWS, COLS = 0, 0
grid = []
updating = True
olds = 0
compteur = 0


def nbVoisins(x, y):
    somme = 0
    for i in range(max(0, x-1), min(COLS, x+2)):
        for j in range(max(0, y-1), min(ROWS, y+2)):
            somme += grid[i][j]
    return somme


def init(grid, rand=True):
    grid.clear()
    for _ in range(COLS):
        grid.append([random.randint(0, 1) if rand else 0 for _ in range(ROWS)])


def update():
    global grid
    newgrid = []
    init(newgrid, False)
    for i, col in enumerate(grid):
        for j, c in enumerate(col):
            nb = nbVoisins(i, j)
            if grid[i][j] == 1 and nb in (3, 4) or grid[i][j] == 0 and nb == 3:
                newgrid[i][j] = 1
            else:
                newgrid[i][j] = 0
    grid = newgrid.copy()


def keyReleased():
    global updating
    if P5.keyCode == pygame.K_SPACE:
        updating = not updating
    elif P5.keyCode in (pygame.K_KP_ENTER, pygame.K_RETURN):
        init(grid)


def mousePressed():
    x = P5.mouseX // SIZE
    y = P5.mouseY // SIZE
    grid[y][x] = 1


def setup():
    global COLS, ROWS
    createCanvas(600, 400)
    ROWS = P5.WIDTH // SIZE
    COLS = P5.HEIGHT // SIZE
    init(grid)
    fill(0, 50, 50)
    stroke(0)


def draw():
    global olds, compteur

    if P5.mouseIsPressed:
        mousePressed()

    s = sum([sum(x) for x in grid])
    if olds == s:
        compteur += 1
    else:
        compteur = 0
        olds = s
    if compteur > 100:
        init(grid)

    background(0)
    for i, col in enumerate(grid):
        for j, c in enumerate(col):
            if c == 1:
                fill(200, 200, 200)
            else:
                fill(0, 50, 50)
            square(j*SIZE, i*SIZE, SIZE)
    if not P5.mouseIsPressed and updating:
        update()


__import__("run")
