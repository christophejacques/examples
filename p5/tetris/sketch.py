import random
from __init__ import background, createCanvas, stroke, fill, circle, rect, square, rectMode
from __init__ import P5, strokeWeight, noStroke, map, Vector, line, push, pop
from __init__ import *


class VAR:
    size = 20


def get_largeur(piece):
    for i in reversed(range(4)):
        somme = 0
        for j in range(4):
            somme += piece[j][i] 
        if somme > 0:
            return i


class Piece:

    def __init__(self):
        self.rotation = 0
        self.x = Board.COLS//2-2
        self.y = Board.ROWS-4
        self.next = []
        liste = []
        liste.append([[1, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        liste.append([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        liste.append([[1, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        liste.append([[1, 1, 1, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        liste.append([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        liste.append([[0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        liste.append([[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        self.liste = liste
        self.init()

    def init(self):
        self.bloc = random.choice(self.liste)

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_down(self):
        self.y -= 1

    def rotate_right(self):
        new = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new[i][j] += self.bloc[j][3-i]
        self.next = new
        self.to_bottom()

    def rotate_left(self):
        new = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new[i][j] += self.bloc[3-j][i]
        self.next = new
        # self.to_bottom()
        self.to_left()

    def to_bottom(self):
        while sum(self.next[0]) == 0:
            for j in range(3):
                self.next[j] = self.next[j+1]
            self.next[3] = [0 for _ in range(4)]

    def to_left(self):
        while self.next[0][0]+self.next[1][0]+self.next[2][0]+self.next[3][0] == 0:
            for j in range(4):
                for i in range(3):
                    self.next[j][i] = self.next[j][i+1]
            for j in range(4):
                self.next[j][3] = 0

    def validate(self):
        self.bloc = self.next

    def update(self):
        self.y -= 1

    def draw(self, x=None, y=None):
        if x is None and y is None:
            x = self.x*VAR.size
            y = self.y*VAR.size
        stroke(60, 10, 10)
        fill(150, 50, 50)
        for j, row in enumerate((self.bloc)):
            for i, cell in enumerate(row):
                if cell:
                    fill(150, 50, 50)
                    rect(x+Board.LEFT + i*VAR.size, Board.BOTTOM - y - j*VAR.size, VAR.size, VAR.size)


class Board:
    COLS = 12
    ROWS = 27
    LEFT = 0
    BOTTOM = 0

    def __init__(self):
        self.init()
        
    def init(self):
        self.data = []
        for row in range(Board.ROWS):
            self.data.append([0 for _ in range(Board.COLS)])
        Board.LEFT = P5.WIDTH//2 - self.COLS*VAR.size//2
        Board.BOTTOM = P5.HEIGHT - 50
        self.coefficient = 10
        self.accel = self.coefficient
        self.rempli = False
        self.next_piece = Piece()
        self.new_piece()

    def new_piece(self):
        self.piece = self.next_piece
        self.next_piece = Piece()
        self.rempli = not self.position_piece_autorized(self.piece.bloc, self.piece.x, self.piece.y)

    def print(self):
        for col in b.data:
            print("[", end="")
            for row in col:
                print(row if row else " ", end=" ")
            print("]", col)

    def move_left(self):
        if self.position_piece_autorized(self.piece.bloc, self.piece.x-1, self.piece.y):
            self.piece.move_left()

    def move_right(self):
        if self.position_piece_autorized(self.piece.bloc, self.piece.x+1, self.piece.y):
            self.piece.move_right()

    def move_down(self):
        if self.rempli:
            return

        if self.position_piece_autorized(self.piece.bloc, self.piece.x, self.piece.y-1):
            self.piece.move_down()
        else:
            self.fusion_piece()
            self.new_piece()

    def rotate_left(self):
        self.piece.rotate_left()
        if self.position_piece_autorized(self.piece.next, self.piece.x, self.piece.y):
            self.piece.validate()

    def rotate_right(self):
        self.piece.rotate_right()
        if self.position_piece_autorized(self.piece.next, self.piece.x, self.piece.y):
            self.piece.validate()

    def position_piece_autorized(self, piece, x, y):
        if x < 0 or y < 0 or x+get_largeur(piece) >= Board.COLS:
            return False

        return self.can_fusion_piece(x, y)
    
    def can_fusion_piece(self, x, y):
        for j in range(4):
            for i in range(min(4, Board.COLS-x)):
                if self.data[y+j][x+i] + self.piece.bloc[j][i] > 1:
                    return False
        return True

    def fusion_piece(self):
        for j in range(4):
            for i in range(min(4, Board.COLS-self.piece.x)):
                self.data[self.piece.y+j][self.piece.x+i] += self.piece.bloc[j][i]
        self.suppression_lignes()
        self.accel = self.coefficient

    def suppression_lignes(self):
        for j, row in enumerate(self.data):
            row = self.data[j]
            while sum(row) == Board.COLS:
                self.data.pop(j)
                self.data.append([0 for _ in range(Board.COLS)])
                row = self.data[j]

    def accelerate(self):
        self.accel = 1

    def update(self):
        if not self.rempli and P5.frameCount % min(self.accel, self.coefficient) == 0:
            self.move_down()

    def draw(self):
        stroke(255, 0, 0)
        y = Board.BOTTOM - (Board.ROWS-5)*VAR.size
        line(Board.LEFT, y, Board.LEFT+Board.COLS*VAR.size, y)
        stroke(20, 200, 150)
        fill(80, 120, 80)
        rect(Board.LEFT-10, 0, 10, P5.HEIGHT)
        rect(Board.LEFT+Board.COLS*VAR.size, 0, 10, P5.HEIGHT)
        rect(0, Board.BOTTOM+VAR.size, P5.WIDTH, 10)
        stroke(60, 10, 10)
        if self.rempli:
            fill(200, 70, 50)
        else:
            fill(50, 100, 150)

        for j, col in enumerate(self.data):
            for i, row in enumerate(col):
                if row:
                    rect(Board.LEFT + i*VAR.size, Board.BOTTOM - j*VAR.size, VAR.size, VAR.size)

        if not self.rempli:                    
            self.next_piece.draw((Board.COLS+3)*VAR.size, (Board.ROWS-8)*VAR.size)
            self.piece.draw()


b = Board()


def preload():
    print("preload")
    frameRate(60)


def keyPressed():
    if P5.keyCode == pygame.K_LEFT:
        b.move_left()
    elif P5.keyCode == pygame.K_RIGHT:
        b.move_right()
    elif P5.keyCode == pygame.K_UP:
        b.rotate_right()
    elif P5.keyCode == pygame.K_DOWN:
        b.accelerate()
    elif P5.keyCode == pygame.K_SPACE:
        if b.rempli:
            b.init()
        else:
            b.move_down()
    elif P5.keyCode == pygame.K_RETURN:
        if b.rempli:
            b.init()


def setup():
    createCanvas(800, 500)
    b.init()
    stroke(20, 200, 150)


def draw():
    background(0)
    b.draw()
    b.update()
