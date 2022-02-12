import random, math
from __init__ import background, createCanvas, stroke, fill, circle, rect, square, rectMode
from __init__ import P5, strokeWeight, noStroke, map, Vector, line, push, pop
from __init__ import *


rotationX = lambda angle: [[1, 0, 0], [0, math.cos(angle), -math.sin(angle)], [0, math.sin(angle), math.cos(angle)]]


def multiplicationMatrice(m1, m2):
    resultat = []
    for i in range(len(m1)):
        enCours = 0
        for j in range(len(m1[0])):
            enCours += m1[i][j] * m2[j] 
        resultat.append(enCours)
    return resultat


sizeX = 800
sizeY = 600

z_max = 30
z_min = -z_max

coef = 6
angle = 1.46

total = 0
decalX = sizeX
decalY = 200
decalX2 = decalX//2
decalY2 = decalY//2


class VAR:
    size = 40
    n = 0
    deb = 0
    fin = 0
    rotx = None
    data = []
    draw = []
    a_min, a_max = 0, 0


def make2Darray(n):
    if n % 2 == 1:
        deb = -(n-1)//2
        fin = 1+n//2
    else:
        deb = -n//2
        fin = n//2
    # VAR.a_min = 10*z_min // n
    # VAR.a_max = 10*z_max // n
    VAR.a_min = z_min 
    VAR.a_max = z_max 
    VAR.deb = deb
    VAR.fin = fin
    print("n, deb, fin =", n, deb, fin)
    lst = []
    for i in range(VAR.deb, VAR.fin):
        lst.append([[i*VAR.size, j*VAR.size, 
            random.randint(VAR.a_min, VAR.a_max) if j == 0 else 0] for j in range(coef*n)])

    # adoucissement de la différence de hauteur des points voisins sur l'axe des X (moyenne)
    for i in range(0, n-1):
        lst[i][0][2] = (lst[i][0][2] + lst[i+1][0][2])/2

    lst[n-1][0][2] = (lst[n-1][0][2] + lst[n-2][0][2])/2
    return lst


def copy(table):
    copie = []
    for col in table:
        copie.append([val.copy() for val in col])
    return copie


def set_profondeur(x, y):
    # simulation de la notion de profondeur
    if y >= 0:
        x = x * map(y, 0, sizeY, 1, 1.5)
    else:
        x = x * map(y, -sizeY, 0, 0.5, 1)
    return x


def preload():
    createCanvas(sizeX, sizeY)
    VAR.n = 1 + P5.WIDTH // VAR.size 
    # VAR.n = 19
    VAR.data = make2Darray(VAR.n)
    translate(int(decalX2), decalY2)

    VAR.rotX = rotationX(angle)

    VAR.draw = []
    for i in range(VAR.n):
        VAR.draw.append([[x for x in VAR.data[i][j]] for j in range(coef*VAR.n)])


def setup():
    fill(0, 50, 50)
    noStroke()


def update():
    if True and P5.frameCount % 2 == 0:
        # decalage d'une ligne de toutes les valeurs
        for j in range(coef*VAR.n-1, 0, -1):
            for i in range(VAR.n):
                VAR.draw[i][j][2] = VAR.draw[i][j-1][2]

        # Ajout d'une nouvelle premiere ligne
        for i in range(VAR.n):
            VAR.draw[i][0][2] = (
                 constrain(VAR.draw[i][1][2]+random.randint(VAR.a_min, VAR.a_max), 2*z_min, 2*z_max))

        # lissage de la hauteur de 2 points voisins sur l'axe des Y (moyenne)
        for i in range(0, VAR.n-1):
            VAR.draw[i][0][2] = (VAR.draw[i][0][2] + VAR.draw[i+1][0][2])/2

        VAR.draw[VAR.n-1][0][2] = (VAR.draw[VAR.n-1][0][2] + VAR.draw[VAR.n-2][0][2])/2

    # Rotation sur l'axe des X
    for j in range(coef*VAR.n):
        for i in range(VAR.n):
            VAR.data[i][j] = multiplicationMatrice(VAR.rotX, VAR.draw[i][j])


def draw():
    background(0, 100, 200)
    update()
    for j in range(coef*VAR.n-1):
        # print(j)
        for i in range(VAR.n-1):
            v1_x, v1_y, v1_z = VAR.data[i][j]
            v2_x, v2_y, v2_z = VAR.data[i][j+1]
            v3_x, v3_y, v3_z = VAR.data[i+1][j]
            v4_x, v4_y, v4_z = VAR.data[i+1][j+1]

            v1_x = set_profondeur(v1_x, v1_y)
            v2_x = set_profondeur(v2_x, v2_y)
            v3_x = set_profondeur(v3_x, v3_y)
            v4_x = set_profondeur(v4_x, v4_y)

            if False:
                diff = VAR.draw[i][j][2]-VAR.draw[i+1][j][2]
                color = map(diff, z_min/2, z_max/2, 0, 255)
            else:
                color = map(VAR.draw[i][j][2], 2*z_min, 2*z_max, 0, 255)
            fill(10, color, 10)
            triangle((v1_x, v1_y), (v2_x, v2_y), (v3_x, v3_y))

            color = map(VAR.draw[i+1][j+1][2], 2*z_min, 2*z_max, 0, 255)
            fill(10, color, 10)
            triangle((v4_x, v4_y), (v2_x, v2_y), (v3_x, v3_y))
