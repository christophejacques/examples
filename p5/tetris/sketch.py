import random
import pygame
from __init__ import background, createCanvas, resizeCanvas, stroke, fill, rect
from __init__ import P5, line
from __init__ import textSize, text, frameRate
from __init__ import *


function_keys_list = [pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, 
  pygame.K_F6, pygame.K_F7, pygame.K_F8, pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12, ]
reserved_keys_list = function_keys_list + [
  pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_KP_ENTER, pygame.K_KP_PLUS, pygame.K_KP_MINUS]


class VAR:
    size = 20


class Board:
    COLS = 12
    ROWS = 27
    BOTTOM = 0


class Player:
    ID = 0

    def __init__(self, xpos):
        Player.ID += 1
        self.ID = Player.ID
        self.LEFT = xpos
        self.pret = False
        self.waiting_keys = False
        self.waiting_key = []
        self.keys = {}
        self.joys = {}
        self.init()

    def ask_keys(self):
        self.waiting_keys = True
        self.pret = False
        self.waiting_key = [("Gauche", "LEFT"), ("Droite", "RIGHT"), (" Haut", "UP"), (" Bas", "DOWN")]

    def set_joy(self, button):
        self.joys[self.waiting_key.pop(0)[1]] = button
        self.waiting_keys = len(self.waiting_key) > 0
        # print(self.joys)

    def set_joys(self, left=-1, right=-1, up=-1, down=-1):
        if left: self.joys["LEFT"] = left
        if right: self.joys["RIGHT"] = right
        if up: self.joys["UP"] = up
        if down: self.joys["DOWN"] = down

    def set_key(self, key):
        if key not in reserved_keys_list:
            self.keys[self.waiting_key.pop(0)[1]] = key
            self.waiting_keys = len(self.waiting_key) > 0
            # self.pret = not self.waiting_keys

    def set_keys(self, left=None, right=None, up=None, down=None):
        if left: self.keys["LEFT"] = left
        if right: self.keys["RIGHT"] = right
        if up: self.keys["UP"] = up
        if down: self.keys["DOWN"] = down

    def init(self):
        self.data = []
        self.score = 0
        for row in range(Board.ROWS):
            self.data.append([0 for _ in range(Board.COLS)])

        self.rempli = False
        self.next_piece = Piece(self.LEFT)
        self.new_piece()
        self.update_speed()

    def update_speed(self):
        self.coefficient = max(1, 40 - Game.level)
        self.accel = self.coefficient

    def ready(self):
        self.pret = True

    def new_piece(self):
        self.piece = self.next_piece
        self.next_piece = Piece(self.LEFT)
        for _ in range(random.randint(0, 2)):
            self.next_piece.rotate_left()
            self.next_piece.validate()
        self.rempli = self.highest_row() >= 24

    def print(self):
        for col in self.data:
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

    def add_ligne(self):
        self.move_down()
        total = len(self.data)-2
        for j, row in enumerate(reversed(self.data[:-1])):
            self.data[1+total-j] = self.data[total-j].copy()

        self.data[0] = [1 for _ in range(Board.COLS)]
        for _ in range(2):
            self.data[0][random.randint(0, Board.COLS-1)] = 0

    def highest_row(self):
        for j, row in enumerate(self.data):
            if sum(row) == 0:
                break
        return j

    def suppression_lignes(self):
        nb_lignes = 0
        for j, row in enumerate(self.data):
            row = self.data[j]
            while sum(row) == Board.COLS:
                self.data.pop(j)
                self.data.append([0 for _ in range(Board.COLS)])
                row = self.data[j]
                nb_lignes += 1

        if nb_lignes > 0:
            Game.total_lignes += nb_lignes
            self.score += nb_lignes * nb_lignes * Board.COLS
            Game.lines_finished[self] = Game.lines_finished.get(self, 0) + nb_lignes

    def accelerate(self):
        self.accel = 1

    def update(self):
        if not self.rempli and P5.frameCount % min(self.accel, self.coefficient) == 0:
            self.move_down()

    def draw(self):
        y = Board.BOTTOM - (Board.ROWS-5)*VAR.size

        # Ligne à ne pas dépasser sinon on perd
        stroke(255, 0, 0)
        line(self.LEFT, y, self.LEFT+Board.COLS*VAR.size, y)

        #  Bord gauche et Droit de la plage de déplacement
        stroke(20, 200, 150)
        fill(80, 120, 80)
        rect(self.LEFT-10, 0, 10, P5.HEIGHT)
        fill(0, 60, 60)
        rect(self.LEFT+Board.COLS*VAR.size, 0, 10, P5.HEIGHT - 30)

        stroke(30, 30, 30)
        if self.rempli:
            fill(50, 15, 15)
        elif Game.statut == "RUNNING":
            fill(50, 100, 150)
        elif Game.statut == "PAUSED":
            fill(15, 30, 45)
        else:
            fill(15, 50, 15)

        # Cases occupées dans le plan
        for j, col in enumerate(self.data):
            for i, row in enumerate(col):
                if row:
                    rect(self.LEFT + i*VAR.size, Board.BOTTOM - j*VAR.size, VAR.size, VAR.size)

        if not self.rempli and Game.running:
            # Piece en cours et prochaine piece
            self.next_piece.draw((Board.COLS+1)*VAR.size, (Board.ROWS-7)*VAR.size)
            self.piece.draw()

        # Score
        stroke(200)
        textSize(20)
        text("Score :", self.LEFT + (Board.COLS+1)*VAR.size, 7*VAR.size)
        text(self.score, self.LEFT + (Board.COLS+1)*VAR.size, 8*VAR.size)

        # Niveau
        text("Niveau :", self.LEFT + (Board.COLS+1)*VAR.size, 10*VAR.size)
        text(Game.level, self.LEFT + (Board.COLS+1)*VAR.size, 11*VAR.size)

        decal = 2
        textSize(20)
        if Game.statut in ("WAITING_PLAYERS", "FINISHED"):
            # Indicateur de changement de touches
            text(f"F{self.ID}: set keys", self.LEFT-decal + 3*(Board.COLS//5)*VAR.size, Board.ROWS*VAR.size-36)
        else:
            # Numero du Joueur
            text(f"Joueur n°{self.ID}", self.LEFT-decal + 3*(Board.COLS//5)*VAR.size, Board.ROWS*VAR.size-36)
            
        # Attente, Debut (decompte), Pret
        if Game.statut in ("WAITING_PLAYERS", "READY"):
            if Game.statut == "READY":
                texte = "Début " + str(Game.decompte)
                couleur = 50, 255, 50
            elif self.waiting_keys:
                texte = self.waiting_key[0][0]
                couleur = 50, 200, 200
            elif self.pret:
                texte = " Prêt !"
                couleur = 50, 250, 50
            else:
                texte = "Attente"
                couleur = 200, 200, 50

            decal = 2
            textSize(40)
            stroke(10)
            text(texte, self.LEFT-decal + (Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size-decal)
            text(texte, self.LEFT-decal + (Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size+decal)
            text(texte, self.LEFT+decal + (Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size-decal)
            text(texte, self.LEFT+decal + (Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size+decal)
            stroke(*couleur)
            text(texte, self.LEFT + (Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size)

        # Fin : Gagné / Perdu
        elif self.rempli and Game.statut == "RUNNING" or Game.statut == "FINISHED":
            if self.rempli:
                texte = "Perdu !"
                couleur = 250, 50, 50
            else:
                texte = "Gagné !"
                couleur = 50, 250, 50

            if self.waiting_keys:
                texte = self.waiting_key[0][0]
                couleur = 50, 200, 200

            textSize(40)
            stroke(10)
            decal = 2
            text(texte, self.LEFT-decal + (1+Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size-decal)
            text(texte, self.LEFT-decal + (1+Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size+decal)
            text(texte, self.LEFT+decal + (1+Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size-decal)
            text(texte, self.LEFT+decal + (1+Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size+decal)
            stroke(*couleur)
            text(texte, self.LEFT + (1+Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size)

        # Jeu en Pause
        elif Game.statut == "PAUSED":
            if self.rempli:
                texte = "Perdu !"
                couleur = 250, 50, 50
            else:
                # Activation du clignotement
                if P5.frameCount % 60 > 30:
                    return
                texte = "PAUSE "
                couleur = 255, 255, 100

            textSize(40)
            stroke(10)
            decal = 2
            text(texte, self.LEFT-decal + (1+Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size-decal)
            text(texte, self.LEFT-decal + (1+Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size+decal)
            text(texte, self.LEFT+decal + (1+Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size-decal)
            text(texte, self.LEFT+decal + (1+Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size+decal)
            stroke(*couleur)
            text(texte, self.LEFT + (1+Board.COLS//5)*VAR.size, 2*Board.ROWS//5*VAR.size)
            

class Game:
    NB_MAX_PLAYERS: int = 5
    running: bool = False
    statut = "WAITING_PLAYERS"
    lines_finished: dict[Player, int] = {}
    total_lignes: int = 0
    level: int = 0

    def __init__(self, nb_players):
        self.nb_players: int = 0
        self.num_player: int = 0
        self.players: list[Player] = []
        for num_player in range(nb_players):
            self.create_player()
        self.resize()

    def resize(self):
        resizeCanvas(self.nb_players * 1450//4, 530)
        Board.BOTTOM = P5.HEIGHT - 50

    def init(self):
        Game.running = True
        Game.statut = "RUNNING"
        Game.level = 0
        Game.total_lignes = 0
        for player in self.players:
            player.init()

    def remove_player(self):
        if self.num_player > 1:
            self.players.pop()
            self.num_player -= 1
            self.nb_players -= 1
            Player.ID -= 1
            self.resize()

    def add_player(self):
        if self.nb_players < Game.NB_MAX_PLAYERS:
            self.create_player()
            self.resize()
            Game.statut = "WAITING_PLAYERS"

    def create_player(self):
        if self.nb_players < Game.NB_MAX_PLAYERS:
            player = Player(self.num_player * (Board.COLS+6)*VAR.size + VAR.size)
            player.set_joys()
            player.set_keys(
                *{ 
                    0: (pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_s),
                    1: (pygame.K_j, pygame.K_l, pygame.K_i, pygame.K_k),
                    2: (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN),
                    3: (pygame.K_KP_4, pygame.K_KP_6, pygame.K_KP_8, pygame.K_KP_5),
                    4: (pygame.K_a, pygame.K_a, pygame.K_a, pygame.K_a)

                }[self.num_player])

            self.players.append(player)
            self.nb_players += 1
            self.num_player += 1

    def all_players_ready(self):
        for player in self.players:
            if not player.pret:
                return False
        return True

    def ask_player_keys(self, key):
        idx = function_keys_list.index(key)
        if idx < self.nb_players:
            Game.statut = "WAITING_PLAYERS"
            VAR.game.players[idx].ask_keys()

    def joy_button_up(self, button):
        # En attente des joueurs
        if Game.statut in ("WAITING_PLAYERS", "FINISHED"):
            for index in range(self.nb_players):
                if self.players[index].waiting_keys:
                    self.players[index].set_joy(button)
                    return
                else:
                    {
                        self.players[index].joys["LEFT"]:   self.players[index].ready,
                        self.players[index].joys["RIGHT"]:  self.players[index].ready,
                        self.players[index].joys["UP"]:     self.players[index].ready,
                        self.players[index].joys["DOWN"]:   self.players[index].ready,
                    }.get(button, nada)()

        # En jeu
        elif Game.statut == "RUNNING":
            for index in range(self.nb_players):
                if not self.players[index].rempli:
                    {
                        self.players[index].joys["LEFT"]:   self.players[index].move_left,
                        self.players[index].joys["RIGHT"]:  self.players[index].move_right,
                        self.players[index].joys["UP"]:     self.players[index].rotate_right,
                        self.players[index].joys["DOWN"]:   self.players[index].accelerate,
                    }.get(button, nada)()

    def highest_player_by_score(self, other):
        highest_score = -1
        highest_player = []
        for player in self.players:
            if player != other and not player.rempli:
                if player.score == highest_score:
                    highest_player.append(player)
                elif player.score > highest_score:
                    highest_score = player.score
                    highest_player = [player]

        if highest_player:
            return random.choice(highest_player)
        else:
            return None

    def get_lines(self, other):
        total = 0
        for player in self.players:
            if player != other:
                total += Game.lines_finished.get(player, 0)
        return total

    def pause(self):
        if Game.statut != "PAUSED":
            Game.statut = "PAUSED"
        else:
            Game.statut = "RUNNING"

    def update(self):
        # print(Game.statut, end=" : ")
        # for player in self.players:
        #     print(player.pret, end=", ")
        # print()
        if Game.statut == "PAUSED":
            return

        if Game.statut == "WAITING_PLAYERS":
            nb_pret = 0
            for player in self.players:
                nb_pret += 1 if player.pret else 0

            waiting_players = len(self.players) != nb_pret
            if not waiting_players:
                Game.statut = "READY"
                Game.decompte = 5
                P5.frameCount = 1

        elif Game.statut == "READY":
            if Game.decompte > 0:
                if P5.frameCount % 60 == 0:
                    Game.decompte -= 1
            else:
                Game.statut == "RUNNING"
                self.init()

        elif Game.running and Game.statut == "RUNNING":
            for player in self.players:
                player.update()

            if Game.lines_finished:
                for player in self.players:
                    if Game.lines_finished.get(player):
                        nb_lignes = Game.lines_finished.get(player)
                        # print(nb_lignes, "ligne(s) finie par Joueur", player.ID, end=". ")
                        highest_player = self.highest_player_by_score(player)
                        # print("Ajout", nb_lignes, "ligne(s) au Joueur", highest_player.ID)
                        if highest_player:
                            for ligne in range(nb_lignes):
                                highest_player.add_ligne()
                        del Game.lines_finished[player]

                Game.lines_finished.clear()

            if Game.total_lignes % 11 == 0:
                Game.level += 1
                Game.total_lignes += 1

            nb_active_players = 0
            for player in self.players:
                nb_active_players += 0 if player.rempli else 1

            Game.running = nb_active_players > 1 or \
                (self.num_player == 1 and nb_active_players == 1)
            if not Game.running:
                Game.statut = "FINISHED"

    def draw(self):
        background(0)
        fill(80, 120, 80)
        stroke(255)
        rect(0, Board.BOTTOM+VAR.size, P5.WIDTH, 10)

        for player in self.players:
            player.draw()


def get_largeur(piece):
    for i in reversed(range(4)):
        somme = 0
        for j in range(4):
            somme += piece[j][i] 
        if somme > 0:
            return i


class Piece:

    def __init__(self, xpos):
        self.LEFT = xpos
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
        fill(150)
        for j, row in enumerate((self.bloc)):
            for i, cell in enumerate(row):
                if cell:
                    rect(x+self.LEFT + i*VAR.size, Board.BOTTOM - y - j*VAR.size, VAR.size, VAR.size)


def preload():
    frameRate(60)


def nada():
    pass


mon_joy: dict = {}
mon_hat: list[int] = [0, 0]


def JoyMotion():
    for joy in P5.joysticks:
        button = 0
        for j in range(joy.get_numhats()):
            x, y = joy.get_hat(j)
            if x == 0 and mon_hat[0] != 0:
                button = {
                    -1: 1001,  # "GAUCHE",
                    1: 1002,   # "DROITE",
                    }[mon_hat[0]]

            elif y == 0 and mon_hat[1] != 0:
                button = {
                    -1: 1003,  # "BAS",
                    1: 1004,   # "HAUT",
                    }[mon_hat[1]]

            mon_hat[0] = x
            mon_hat[1] = y

        if button:
            Game.joy_button_up(button)


def JoyButtonPressed():
    for joy in P5.joysticks:
        for x in range(joy.get_numbuttons()):
            if joy.get_button(x):
                if mon_joy.get(joy):
                    mon_joy[joy].add(x)
                else:
                    mon_joy[joy] = set()
                    mon_joy[joy].add(x)


def JoyButtonReleased():
    for joy in mon_joy:
        to_del = []
        for button in mon_joy[joy]:
            if not joy.get_button(button):
                to_del.append(button)

    for button in to_del:
        mon_joy[joy].remove(button)

        VAR.game.joy_button_up(button)


def keyPressed():
    # En attente des joueurs
    if Game.statut == "WAITING_PLAYERS":
        for index in range(VAR.game.nb_players):
            if VAR.game.players[index].waiting_keys:
                VAR.game.players[index].set_key(P5.keyCode)
                return
            else:
                {
                    VAR.game.players[index].keys["LEFT"]:   VAR.game.players[index].ready,
                    VAR.game.players[index].keys["RIGHT"]:  VAR.game.players[index].ready,
                    VAR.game.players[index].keys["UP"]:     VAR.game.players[index].ready,
                    VAR.game.players[index].keys["DOWN"]:   VAR.game.players[index].ready,
                }.get(P5.keyCode, nada)()

        if P5.keyCode in function_keys_list:
            VAR.game.ask_player_keys(P5.keyCode)
        else:
            {
                pygame.K_KP_PLUS:   VAR.game.add_player,
                pygame.K_KP_MINUS:  VAR.game.remove_player,
            }.get(P5.keyCode, nada)()
            
    # Pret ou Fini
    elif Game.statut in ("READY", "FINISHED"):
        if Game.statut == "FINISHED":
            # FINISHED
            for index in range(VAR.game.nb_players):
                if VAR.game.players[index].waiting_keys:
                    VAR.game.players[index].set_key(P5.keyCode)
                    return

            if P5.keyCode in function_keys_list:
                VAR.game.ask_player_keys(P5.keyCode)
            elif VAR.game.all_players_ready():
                {
                    pygame.K_KP_PLUS:   VAR.game.add_player,
                    pygame.K_KP_MINUS:  VAR.game.remove_player,
                    pygame.K_RETURN:    VAR.game.init,
                    pygame.K_SPACE:     VAR.game.init,
                }.get(P5.keyCode, nada)()
            else:
                for index in range(VAR.game.nb_players):
                    {
                        VAR.game.players[index].keys["LEFT"]:   VAR.game.players[index].ready,
                        VAR.game.players[index].keys["RIGHT"]:  VAR.game.players[index].ready,
                        VAR.game.players[index].keys["UP"]:     VAR.game.players[index].ready,
                        VAR.game.players[index].keys["DOWN"]:   VAR.game.players[index].ready,
                    }.get(P5.keyCode, nada)()

                {
                    pygame.K_KP_PLUS:   VAR.game.add_player,
                    pygame.K_KP_MINUS:  VAR.game.remove_player,
                }.get(P5.keyCode, nada)()

        else:
            # READY
            {
                pygame.K_KP_PLUS:   VAR.game.add_player,
                pygame.K_KP_MINUS:  VAR.game.remove_player,
                pygame.K_RETURN:    VAR.game.init,
                pygame.K_SPACE:     VAR.game.init,
            }.get(P5.keyCode, nada)()

    # Jeu en cours
    elif Game.running and Game.statut == "RUNNING":
        for index in range(VAR.game.nb_players):
            if not VAR.game.players[index].rempli:
                {
                    VAR.game.players[index].keys["LEFT"]:   VAR.game.players[index].move_left,
                    VAR.game.players[index].keys["RIGHT"]:  VAR.game.players[index].move_right,
                    VAR.game.players[index].keys["UP"]:     VAR.game.players[index].rotate_right,
                    VAR.game.players[index].keys["DOWN"]:   VAR.game.players[index].accelerate,
                }.get(P5.keyCode, nada)()

        {
            pygame.K_SPACE:     VAR.game.pause,
        }.get(P5.keyCode, nada)()

    # Pause
    elif Game.statut == "PAUSED":
        {
            pygame.K_RETURN:    VAR.game.pause,
            pygame.K_SPACE:     VAR.game.pause,
        }.get(P5.keyCode, nada)()

    # check Erreur
    else:
        print("Statut inconnu:", Game.statut)


def setup():
    VAR.game = Game(2)
    createCanvas(VAR.game.nb_players * 1450//4, 530)
    pygame.display.set_caption("Tetris multiplayer")


def draw():
    VAR.game.update()
    VAR.game.draw()
