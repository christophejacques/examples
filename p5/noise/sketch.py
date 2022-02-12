import random
from __init__ import background, createCanvas, stroke, fill, circle, rect, square, rectMode, text, textSize
from __init__ import noFill
from __init__ import P5, strokeWeight, noStroke, map, StaticVector, Vector, line, point, noLoop
from __init__ import *


grid = []
class VAR:
    tour = "X"


def mousePressed():
    res = isResolved("X") + isResolved("O") + isTie()
    if res:
        initialisation()

    else:
        x, y = 3*P5.mouseX // P5.WIDTH, 3*P5.mouseY // P5.HEIGHT
        if grid[x][y] == "":
            grid[x][y] = VAR.tour

        VAR.tour = "O" if VAR.tour == "X" else "X"


def keyPressed():
    if P5.keyCode == pygame.K_SPACE:
        initialisation()


def isTie():
    for i in range(3):
        for j in range(3):
            if grid[i][j] == "":
                return ""
    return "TT"


def isResolved(by):
    res = ""
    for i, col in enumerate(grid):
        totalc = sum([1 if x == by else 0 for x in col])
        if totalc >= 3:
            res += f"C{i}"
    total = [0, 0, 0]
    totalc1, totalc2 = 0, 0
    for j in range(3):
        for i in range(3):
            total[j] += 1 if grid[i][j] == by else 0
        if total[j] >= 3:
            res += f"R{j}"

        totalc1 += 1 if grid[j][j] == by else 0
        totalc2 += 1 if grid[2-j][j] == by else 0

    if totalc1 >= 3:
        res += "/1"
    if totalc2 >= 3:
        res += "/2"

    return res


def initialisation():
    grid.clear()
    for _ in range(3):
        grid.append(["" for _ in range(3)])


def setup():
    createCanvas(400, 400)
    initialisation()


def draw():
    background(0)

    stroke(255)
    strokeWeight(2)
    noFill()
    line(P5.WIDTH // 3, 0, P5.WIDTH // 3, P5.HEIGHT)
    line(2*P5.WIDTH // 3, 0, 2*P5.WIDTH // 3, P5.HEIGHT)
    line(0, P5.HEIGHT // 3, P5.WIDTH, P5.HEIGHT // 3)
    line(0, 2*P5.HEIGHT // 3, P5.WIDTH, 2*P5.HEIGHT // 3)
    square(0, 0, P5.WIDTH-1)
    textSize(100)
    sol = isResolved("X") + isResolved("O") + "  "
    sol = sol if sol.strip() != "" else isTie() + "  "

    for i in range(3):
        for j in range(3):
            decode = sol
            while len(decode) > 2:
                if (decode[0] == "R" and int(decode[1]) == j) or (
                    decode[0] == "C" and int(decode[1]) == i) or (
                    decode[0] == "/" and int(decode[1]) == 1 and i == j) or (
                    decode[0] == "/" and int(decode[1]) == 2 and i == 2-j):
                    stroke(0, 255, 0)
                    break
                elif decode[0] == "T":
                    stroke(200, 50, 50)
                    break
                else:
                    stroke(255, 255, 255)
                decode = decode[2:]

            text(grid[i][j], 30+i*130, 130*j)
