import os
from msvcrt import getch
from utils.colors import *
import traceback
updt = []

DEBUG = False

def mygetch():
    if DEBUG:
        return getch()
    else:
        return 0 # getch()

def initbool(table):
    table.clear()
    for x in range(9):
        table.append([False]*9)

grid0 = [[0,0,0, 0,5,0, 0,0,9], [4,0,0, 0,0,9, 0,2,0], [7,0,0, 0,0,0, 4,0,6], 
        [0,3,0, 0,6,4, 0,0,0], [0,6,0, 8,0,0, 0,0,1], [0,0,7, 0,0,1, 5,0,0], 
        [3,0,2, 0,4,0, 0,7,8], [0,0,0, 0,0,0, 0,1,0], [9,0,8, 3,0,0, 0,0,0]]
       
grid0= [[5,3,0, 6,0,0, 0,9,8], [0,7,0, 1,9,5, 0,0,0], [0,0,0, 0,0,0, 0,6,0], 
        [8,0,0, 4,0,0, 7,0,0], [0,6,0, 8,0,3, 0,2,0], [0,0,3, 0,0,1, 0,0,6], 
        [0,6,0, 0,0,0, 0,0,0], [0,0,0, 4,1,9, 0,8,0], [2,8,0, 0,0,5, 0,7,9]]

grid0 = [[3,0,0, 0,7,5, 0,9,0], [0,0,0, 0,0,0, 0,0,0], [7,0,1, 0,2,4, 0,0,0], 
        [0,0,0, 0,0,0, 0,0,0], [0,0,8, 0,0,9, 5,4,0], [0,0,0, 0,1,0, 8,0,9], 
        [2,0,0, 0,3,0, 1,8,0], [0,0,1, 0,6,0, 0,0,2], [0,6,8, 1,5,0, 4,0,0]]
# difficile
grid= [[0,6,0, 3,0,2, 1,0,0], [7,0,0, 5,0,0, 0,0,0], [0,0,0, 8,0,0, 0,2,4], 
        [0,0,0, 8,0,1, 0,0,0], [0,2,0, 0,0,4, 1,0,7], [9,0,0, 2,7,0, 0,0,0], 
        [0,0,0, 7,0,0, 0,0,0], [0,0,0, 8,5,0, 0,0,0], [3,0,0, 6,0,0, 0,4,9]]
#Expert
grid0 = [[3,0,5, 0,0,0, 0,9,0], [0,7,1, 3,4,0, 2,0,0], [0,0,9, 0,0,0, 0,0,0], 
        [0,3,0, 0,6,0, 0,0,0], [0,0,4, 0,0,0, 0,0,2], [0,0,0, 0,0,7, 8,5,0], 
        [0,0,0, 0,5,4, 0,0,7], [0,0,0, 0,0,0, 0,0,0], [0,8,0, 9,0,1, 4,0,0]]

gridetail = [[0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]

def initdetail(grille, grilledetail):
    for y in range(9):
        for x in range(9):
            val = grille[y][x]
            if val == 0:
                grilledetail[y][x] = list(range(1, 10))
            else:
                grilledetail[y][x] = [val]

def printdetail(param = 0):
    try:
        chiffre = int(param)
    except:
        chiffre = 0
        
    for y in range(9):
        if y % 2:
            lignecolor = fcolors.GVERT
        else:
            lignecolor = fcolors.GJAUNE
            
        for x in range(9):
            res = gridetail[y][x]
            if chiffre in res:
                print(fcolors.GMAGENTA, end="")
            else:
                print(lignecolor, end="")
                
            printXY(1+(3*(y%3)+x%3)*22,31+(3*(y//3)+x//3)+y//3, res)

    print(fcolors.GVERT)
    printXY(1, 34, "─", end="")
    for colonne in range(21*9): print( "─", end="")
    printXY(1, 38, "─", end="")
    for colonne in range(21*9): print( "─", end="")

    for ligne in range(11):
        if (ligne+1) % 4 == 0:
            printXY( 66, 31+ligne, "┼")
            printXY(132, 31+ligne, "┼")
        else:
            printXY( 66, 31+ligne, "│")
            printXY(132, 31+ligne, "│")

    

    return mygetch()
       
def lprint(*args, **kw):
    pass
    #print(*args, **kw)

def is_sudoku_resolved(grille):
    res = True
    n = 0
    while n<8 and res:
        n += 1
        res = is_box_ok(grille, n)
    
    return res

def is_box_ok(grille, n):
    test = [1,2,3,4,5,6,7,8,9]
    for x in range(9):
        try:
            index = test.index(grille[n][x])
        except:
            return False
            
        test.pop(index)
        
    return len(test) == 0

def purificationBy2Vert(grille):
    dico = {}
    nombre = 0
    for box in range(9):
        dico[box] = {}
        for pos in range(9):
            if grille[box][pos] == 0:
                vals = gridetail[box][pos]
                for val in vals:
                    # test vertical
                    dico[box][val] = [pos % 3]
                    for oldpos in range(9):
                        if (oldpos % 3) not in dico[box][val]:
                            recherche = gridetail[box][oldpos]
                            if val in recherche:
                                dico[box][val].append(oldpos % 3)
                                dico[box][val].sort()
    
    # suppression des tuples n'etant pas des couples 
    dicop = {}
    for box in dico:
        for val in dico[box]:
            if len(dico[box][val]) == 2:
                if dicop.get(box) == None:
                    dicop[box] = {}
                dicop[box][val] = dico[box][val]
    
    # suppression des couples non en double
    ddico = {}
    for i in range(3):
        for box in range(i%3, 9, 3):
            if dicop.get(box) != None:
                for val in dicop[box]:
                    colonnes = dicop[box][val]
                    for oldbox in range(i%3, 9, 3):
                        if box != oldbox:
                            if dicop.get(oldbox) != None:
                                if dicop[oldbox].get(val) == colonnes:
                                    if ddico.get(oldbox) == None:
                                        ddico[oldbox] = {}
                                    ddico[oldbox][val] = colonnes
        
    # decouverte de la boite non indiquée
    dicof = {}
    for box in ddico:
        for val in ddico[box]:
            liste = [x for x in range(box % 3, 9, 3)]
            liste.pop(liste.index(box))
            for oldbox in range(box % 3, 9, 3):
                if box != oldbox:
                    if ddico.get(oldbox) != None:
                        if ddico[oldbox].get(val) == None:
                            if dicof.get(oldbox) == None:
                                dicof[oldbox] = {}
                            dicof[oldbox][val] = ddico[box][val]
                    else:
                        if dicof.get(oldbox) == None:
                            dicof[oldbox] = {}
                        dicof[oldbox][val] = ddico[box][val]
    
    # suppression des elements trouves
    for box in dicof: 
        for val in dicof[box]:
            for colonnes in dicof[box][val]:
                for indice in range(3*colonnes, 3*colonnes+3):
                    if val in gridetail[box][indice] and len(gridetail[box][indice])>1:
                        gridetail[box][indice].remove(val)
                        nombre += 1
                        if len(gridetail[box][indice]) == 1:
                            grille[box][indice] = gridetail[box][indice][0]
                            updt[box][indice] = 4

    return nombre


def purificationBy2Horiz(grille):
    dico = {}
    nombre = 0
    for box in range(9):
        dico[box] = {}
        for pos in range(9):
            if grille[box][pos] == 0:
                vals = gridetail[box][pos]
                for val in vals:
                    # test horizontal
                    dico[box][val] = [pos // 3]
                    for oldpos in range(9):
                        if (oldpos // 3) not in dico[box][val]:
                            recherche = gridetail[box][oldpos]
                            if val in recherche:
                                dico[box][val].append(oldpos // 3)
                                dico[box][val].sort()

    # suppression des tuples n'etant pas des couples 
    dicop = {}
    for box in dico:
        for val in dico[box]:
            if len(dico[box][val]) == 2:
                if dicop.get(box) == None:
                    dicop[box] = {}
                dicop[box][val] = dico[box][val]

    # suppression des couples non en double
    ddico = {}
    for i in range(3):
        for box in range(i*3, (i+1)*3):
            if dicop.get(box) != None:
                for val in dicop[box]:
                    lignes = dicop[box][val]
                    for oldbox in range(i*3, (i+1)*3):
                        if box != oldbox:
                            if dicop.get(oldbox) != None:
                                if dicop[oldbox].get(val) == lignes:
                                    if ddico.get(oldbox) == None:
                                        ddico[oldbox] = {}
                                    ddico[oldbox][val] = lignes

    # decouverte de la boite non indiquée
    dicof = {}
    for box in ddico:
        for val in ddico[box]:
            liste = [x for x in range((box//3)*3, ((box//3)+1)*3)]
            liste.pop(liste.index(box))
            for oldbox in range((box//3)*3, ((box//3)+1)*3):
                if box != oldbox:
                    if ddico.get(oldbox) != None:
                        if ddico[oldbox].get(val) == None:
                            if dicof.get(oldbox) == None:
                                dicof[oldbox] = {}
                            dicof[oldbox][val] = ddico[box][val]
                    else:
                        if dicof.get(oldbox) == None:
                            dicof[oldbox] = {}
                        dicof[oldbox][val] = ddico[box][val]

    # suppression des elements trouves
    for box in dicof: 
        for val in dicof[box]:
            for ligne in dicof[box][val]:
                for indice in range(3*ligne, 3*ligne+3):
                    if val in gridetail[box][indice] and len(gridetail[box][indice])>1:
                        gridetail[box][indice].remove(val)
                        nombre += 1
                        if len(gridetail[box][indice]) == 1:
                            grille[box][indice] = gridetail[box][indice][0]
                            updt[box][indice] = 4

    return nombre

def purification(grille):
    nombre = 0
    for box in range(9):
        for pos in range(9):
            if grille[box][pos] == 0:
                vals = gridetail[box][pos]
                for val in vals:
                    # test horizontal
                    trouve = False
                    for oldpos in range(9):
                        if not (pos // 3 == oldpos // 3):
                            recherche = gridetail[box][oldpos]
                            trouve = trouve or (val in recherche)
                    
                    if not trouve:
                        # suppression des autres boites sur la meme ligne
                        for oldbox in range(3*(box // 3), 3*(box // 3) + 3):
                            if oldbox != box:
                                for oldpos in range(3*(pos // 3), 3*(pos // 3) + 3):
                                    if grille[oldbox][oldpos] == 0:
                                        try:
                                            gridetail[oldbox][oldpos].pop(gridetail[oldbox][oldpos].index(val))
                                            nombre += 1
                                            if len(gridetail[oldbox][oldpos]) == 1:
                                                grille[oldbox][oldpos] = gridetail[oldbox][oldpos][0]
                                                updt[oldbox][oldpos] = 3
                                        except:
                                            pass
                                            
                    # test vertical
                    trouve = False
                    for oldpos in range(9):
                        if not (pos % 3 == oldpos % 3):
                            recherche = gridetail[box][oldpos]
                            trouve = trouve or (val in recherche)
                    
                    if not trouve:
                        # suppression des autres boites sur la meme ligne
                        for oldbox in range(box % 3, 9, 3):
                            if oldbox != box:
                                for oldpos in range(pos % 3, 9, 3):
                                    if grille[oldbox][oldpos] == 0:
                                        try:
                                            gridetail[oldbox][oldpos].pop(gridetail[oldbox][oldpos].index(val))
                                            nombre += 1
                                            if len(gridetail[oldbox][oldpos]) == 1:
                                                grille[oldbox][oldpos] = gridetail[oldbox][oldpos][0]
                                                updt[oldbox][oldpos] = 3
                                        except:
                                            pass
                                            
    return nombre

def find_next_unique(grille):
    #return 0
    nombre = 0
    for box in range(9):
        for pos in range(9):
            if grille[box][pos] == 0:
                vals = gridetail[box][pos]
                for val in vals:
                    trouve = False
                    for oldbox in range(9):
                        if box // 3 == oldbox // 3:
                            # test valeur horizontale
                            for oldpos in range(3*(pos//3), 3+3*(pos//3)):
                                if not (oldbox == box and oldpos == pos):
                                    recherche = gridetail[oldbox][oldpos]
                                    trouve = trouve or (val in recherche)
                            
                        if not trouve and box % 3 == oldbox % 3:
                            # test valeur verticale
                            for oldpos in range(pos%3, 9, 3):
                                if not (oldbox == box and oldpos == pos):
                                    recherche = gridetail[oldbox][oldpos]
                                    trouve = trouve or (val in recherche)

                        if trouve: 
                            break
                    
                    if trouve:
                        # test de la boite
                        trouve = False
                        for oldpos in range(9):
                            if oldpos != pos:
                                recherche = gridetail[box][oldpos]
                                trouve = trouve or (val in recherche)
                                
                    
                    if not trouve:
                        grille[box][pos] = val
                        gridetail[box][pos] = [val]
                        updt[box][pos] = 2
                        nombre += 1
                
    return nombre
    

def find_next_direct(grille):

    print(end=fcolors.BLANC)
    trouve = 0
    for box in range(9):
        lprint("boite:", box, end="")
        for pos in range(9):
            val = grille[box][pos]
            if val == 0:
                """Valeur a trouver"""
                # recherche dans la boite en cours
                # ----------------------------------
                lprint("\n+ boite({}):".format(pos), end=" (")
                # reste = [1,2,3,4,5,6,7,8,9]
                reste = gridetail[box][pos]
                for oldpos in range(9):
                    if len(reste) == 1: break
                    if oldpos != pos:
                        oldval = grille[box][oldpos]
                        if oldval != 0:
                            try:
                                tmp = reste.pop(reste.index(oldval))
                                lprint(fcolors.VERT + str(tmp) + ",", end=fcolors.BLANC)
                            except:
                                pass
                            
                lprint(") reste:", reste, end=",")
                        
                # print("Valeur =", reste )
                if len(reste) == 1:
                    lprint(fcolors.GVERT +" Ok:", reste, end=fcolors.BLANC)
                    grille[box][pos] = reste[0]
                    updt[box][pos] = 1
                    trouve += 1
                    continue
                
                # recherche dans la ligne en cours
                # ----------------------------------
                num_ligne = pos // 3
                lprint("\n  ligne({}):".format(num_ligne),end=" ")
                for oldbox in range(9):
                    if len(reste) == 1: break
                    if oldbox // 3 == box // 3:
                        lprint("b{}.(".format(oldbox), end="")
                        for col in range(3):
                            checkval = grille[oldbox][num_ligne*3 + col]
                            if checkval != 0:
                                try:
                                    tmp = reste.pop(reste.index(checkval))
                                    lprint(fcolors.VERT + str(tmp) + ",", end=fcolors.BLANC)
                                except:
                                    pass
                                    
                        lprint(") reste:", reste, end=", ")
                        
                if len(reste) == 1:
                    lprint(fcolors.GVERT +" Ok:", reste, end=fcolors.BLANC)
                    grille[box][pos] = reste[0]
                    updt[box][pos] = 1
                    trouve += 1
                    continue
                                                
                # recherche dans la colonne en cours
                # ----------------------------------
                num_col = pos % 3
                lprint("\n  colon({}):".format(num_col), end=" ")
                for oldbox in range(9):
                    if oldbox % 3 == box % 3:
                        lprint("b{}.(".format(oldbox), end="")
                        for ligne in range(3):
                            checkval = grille[oldbox][num_col + ligne*3]
                            if checkval != 0:
                                try:
                                    tmp = reste.pop(reste.index(checkval))
                                    lprint(fcolors.VERT + str(tmp) + ",", end=fcolors.BLANC)
                                except:
                                    pass
                                
                        lprint(") reste:", reste, end=", ")
                        
                if len(reste) == 1:
                    lprint(fcolors.GVERT +" Ok:", reste, end=fcolors.BLANC)
                    grille[box][pos] = reste[0]
                    updt[box][pos] = 1
                    trouve += 1
                    continue
                
        lprint()
        
    return trouve
    

def show(grille, x, y):
    ligne = y
    for line in range(9):
        # ligne supérieure  # ¬│┤ ╣║ ╗╝ ┐└┴ ┬├ ─ ┼ ╚╔ ╩╦╠ ═ ╬ 
        if line % 3 == 0:
            ligne += 1
            printXY(x, ligne,"", end="")
            if line == 0:
                print(fcolors.GVERT, end=" ╔═")
            else:
                print(fcolors.GVERT, end=" ╠═")
            
            for c in range(3):
                for l in range(3):
                    if line == 0:
                        print("═══", end="")
                    else:
                        print("───", end="")
                if c == 2:
                    if line == 0:
                        print(end="═╗ ") 
                    else:
                        print(end="═╣") 
                    
                else:
                    if line == 0:
                        print(end="═╦═") 
                    else:
                        print(end="═┼═") 
                
        
        # ligne de données
        ligne += 1
        printXY(x, ligne,"", end="")
        for box in range(3):
            if box == 0:
                print(fcolors.GVERT, end=" ║ ")
            else:
                print(fcolors.GVERT, end=" │ ")
            
            num_boite = 3*(line//3)+box
            if is_box_ok(grille, num_boite):
                color = fcolors.VERT
            else:
                color = fcolors.GROUGE
            
            for col in range(3):
                index = 3*(line % 3)+col
                val = grille[num_boite][index]
                if updt[num_boite][index] == 1:
                     print(fcolors.GJAUNE + "{:2}".format(val), end=" ")
                elif updt[num_boite][index] == 2:
                     print(fcolors.GCYAN + "{:2}".format(val), end=" ")
                elif updt[num_boite][index] == 3:
                     print(fcolors.GMAGENTA + "{:2}".format(val), end=" ")
                elif updt[num_boite][index] == 4:
                     print(fcolors.GVERT + "{:2}".format(val), end=" ")
                else:
                    if val < 1:
                        print(color + "  ", end=" ")
                    else:
                        print(color + "{:2}".format(val), end=" ")
            
        print(fcolors.GVERT + " ║")

    # ligne inférieure       
    ligne += 1
    printXY(x, ligne,fcolors.GVERT, end=" ╚═")
    for col in range(3):
        for line in range(3):
            print("═══", end="")
        if col == 2:
            print(end="═╝ ") 
        else:
            print(end="═╩═") # ╩╦╠ ═

    printXY(x-1,y+7, ">")


class Add:
    total = 0
    def __init__(self, x):
        Add.total += sum([1 for i in x if i >0])


def main():
    nba = nbb = nbc = nbd = nbe = 1
    t = ""
    if DEBUG: 
        x = 67
        y = 15
    else:
        x = 1
        y = 1
            
    initdetail(grid, gridetail)

    initbool(updt)
    show(grid, x, y)
    if DEBUG: t = printdetail()
    
    while nba+nbb+nbc+nbd+nbe>0 and t!=b"\x1b" and not is_sudoku_resolved(grid):
        if DEBUG: os.system("cls")
        initbool(updt)
        Add.total = 0
        list(map(Add, grid))
        nba = find_next_direct(grid)
        nbb = find_next_unique(grid)
        nbc = purification(grid)
        nbd = purificationBy2Horiz(grid)
        nbe = purificationBy2Vert(grid)
        
        if not DEBUG: 
            x += 40
            if x > 150:
                x = 1
                y += 14
        
        printXY(x+2 , y+14, "Old:{:2}".format(Add.total))
        printXY(x+12, y+14, "Add:{}+{} ({},{},{})".format(nba, nbb, nbc, nbd, nbe))
        printXY(x+31, y+14, "Rst:{:2}".format(81-(Add.total+nba+nbb)))
        
        show(grid, x, y)
        if DEBUG:
            t = printdetail()

try:
    t=""
    if DEBUG: t = mygetch()
    if t!=b"\x1b": main()
    
except Exception as e:
    print("Exception :")
    print(e)
    print(traceback.print_exc())
    
    
if DEBUG: 
    while t != b"\x1b":
        t = printdetail(t)
else:
    #getch()
    pass

