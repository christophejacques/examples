from __init__ import P5, noLoop, background, line, createCanvas, textSize, strokeWeight
from __init__ import noFill, circle
from __init__ import *

board = [
    ['', '', ''],
    ['', '', ''],
    ['', '', '']
]


class VAR:
    w = 0
    h = 0

    ai = 'X'
    human = 'O'
    currentPlayer = human


def bestMove():
    global board
    # AI to make its turn
    bestScore = -99
    move = None
    for i in range(3):
        for j in range(3):
            # Is the spot available?
            if (board[i][j] == ''):
                board[i][j] = VAR.ai
                score = minimax(board, 0, False)
                board[i][j] = ''
                if (score > bestScore):
                    bestScore = score
                    move = (i, j)

    board[move[0]][move[1]] = VAR.ai
    VAR.currentPlayer = VAR.human


scores = {
    "X": 10,
    "O": -10,
    "tie": 0}


def minimax(board, depth, isMaximizing):
    result = checkWinner()
    if (result is not None):
        return scores[result]

    if (isMaximizing):
        bestScore = -99
        for i in range(3):
            for j in range(3):
                # Is the spot available?
                if (board[i][j] == ''):
                    board[i][j] = VAR.ai
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    bestScore = max(score, bestScore)
        return bestScore

    else:
        bestScore = 99
        for i in range(3):
            for j in range(3):
                # Is the spot available?
                if (board[i][j] == ''):
                    board[i][j] = VAR.human
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    bestScore = min(score, bestScore)

        return bestScore


def setup():
    createCanvas(400, 400)
    VAR.w = P5.WIDTH // 3
    VAR.h = P5.HEIGHT // 3
    bestMove()


def equals3(a, b, c):
    return a == b and b == c and a != ''


def checkWinner():
    winner = None

    # horizontal
    for i in range(3):
        if (equals3(board[i][0], board[i][1], board[i][2])):
            winner = board[i][0]

    # Vertical
    for i in range(3):
        if (equals3(board[0][i], board[1][i], board[2][i])):
            winner = board[0][i]

    # Diagonal
    if (equals3(board[0][0], board[1][1], board[2][2])):
        winner = board[0][0]

    if (equals3(board[2][0], board[1][1], board[0][2])):
        winner = board[2][0]

    openSpots = 0
    for i in range(3):
        for j in range(3):
            if (board[i][j] == ''):
                openSpots += 1

    if (winner is None and openSpots == 0):
        return 'tie'
    else:
        return winner


def mousePressed():
    if (VAR.currentPlayer == VAR.human):
        # Human make turn
        i = (P5.mouseX // VAR.w)
        j = (P5.mouseY // VAR.h)
        # If valid turn
        if (board[i][j] == ''):
            board[i][j] = VAR.human
            VAR.currentPlayer = VAR.ai
            bestMove()


def draw():
    background(255)
    strokeWeight(4)

    line(VAR.w, 0, VAR.w, P5.HEIGHT)
    line(VAR.w * 2, 0, VAR.w * 2, P5.HEIGHT)
    line(0, VAR.h, P5.WIDTH, VAR.h)
    line(0, VAR.h * 2, P5.WIDTH, VAR.h * 2)

    for j in range(3):
        for i in range(3):
            x = VAR.w * i + VAR.w / 2
            y = VAR.h * j + VAR.h / 2
            spot = board[i][j]
            textSize(32)
            r = VAR.w / 4
            if (spot == VAR.human):
                noFill()
                circle(x, y, r)
            elif (spot == VAR.ai):
                line(x - r, y - r, x + r, y + r)
                line(x + r, y - r, x - r, y + r)

    result = checkWinner()
    if (result is not None):
        noLoop()
        if (result == 'tie'):
            print('Tie!')
        else:
            print(f"{result} wins!")
