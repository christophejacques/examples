import random
from classes import Application
from colors import Colors


class TicTacToe(Application):
    MIN_SIZE = (400, 400)
    VEL_MAX = 0

    WINDOW_PROPERTIES = ["NO_MAX"]
    DEFAULT_CONFIG = ("Tic Tac Toe", Colors.DARK_BLUE)

    def __init__(self, screen, args):
        super().__init__(screen)
        self.screen = screen
        self.nombre = screen.get_size()[0]//200 
        self.action = ""
        self.grid = []
        self.tour = "X"
        self.initialisation()
        self.get_theme()

    def get_theme(self):
        self.fore_color = self.theme.get("FORE_COLOR")
        self.back_color = self.theme.get("BACKGROUND_COLOR")

    def post_init(self):
        self.resize(self.screen)
        self.FONT = self.tools.font("comicsans", 100)

        w, h = self.screen.get_size()
        longueur = self.MIN_SIZE[0]
        self.win_resize("BOTTOM RIGHT", -(w-longueur), -(h-longueur))

    def initialisation(self):
        self.grid.clear()
        for _ in range(3):
            self.grid.append(["" for _ in range(3)])

    def resize(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.dx = self.width // 3
        self.dy = self.height // 3
        self.decalx = max(0, self.dx // 2)
        self.decaly = max(0, self.dy // 2)

    def get_action(self):
        return self.action

    def mouse_button_up(self, mouseX, mouseY, button):
        res = self.isResolved(self.grid, "X") + self.isResolved(self.grid, "O") + self.isTie(self.grid)
        if res:
            self.initialisation()

        else:
            x, y = 3*mouseX // self.width, 3*mouseY // self.height
            if self.grid[x][y] == "":
                self.grid[x][y] = self.tour
                self.tour = "O" if self.tour == "X" else "X"
                if self.tour == "O":
                    if self.isResolved(self.grid, "X") + self.isTie(self.grid):
                        self.tour = "X"
                    else:
                        x, y = self.ia(self.tour)
                        self.mouse_button_up(10+x*self.dx, 10+y*self.dy, 1)

    def isTie(self, grid):
        for i in range(3):
            for j in range(3):
                if grid[i][j] == "":
                    return ""
        return "TT"

    def isResolved(self, grid, by):
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

    def minimax(self, grille, level, isMaximizing):
        if self.isTie(grille):
            return 0
        elif self.isResolved(grille, "O"):
            return 1
        elif self.isResolved(grille, "X"):
            return -1

        if isMaximizing:
            best_score = -99
            tour = "O" 
            func = max
        else:
            best_score = 99
            tour = "X"
            func = min

        for j in range(3):
            for i in range(3):
                if grille[i][j] == "":
                    grille[i][j] = tour
                    score = self.minimax(grille, level + 1, not isMaximizing)
                    grille[i][j] = ""
                    best_score = func(best_score, score)
        return best_score

    def ia(self, tour):
        if tour == "O":
            best_score = -99
            isMaximizing = False
        else:
            best_score = 99
            isMaximizing = True

        move = None
        for j in range(3):
            for i in range(3):
                if self.grid[i][j] == "":
                    self.grid[i][j] = tour
                    score = self.minimax(self.grid, 0, isMaximizing)
                    self.grid[i][j] = ""
                    if tour == "O" and score > best_score:
                        best_score = score
                        move = (i, j)
                    elif tour == "X" and score < best_score:
                        best_score = score
                        move = (i, j)

        return move

    def keyreleased(self, event):
        self.touche = self.keys.get_key()
        if self.touche == self.keys.K_ESCAPE:
            self.action = "QUIT"
        elif self.touche == self.keys.K_SPACE:
            self.initialisation()
        elif self.touche in (self.keys.K_KP_ENTER, self.keys.K_RETURN):
            if self.isResolved(self.grid, "X") + self.isResolved(self.grid, "O") + self.isTie(self.grid):
                self.initialisation()
            else:
                x, y = self.ia(self.tour)
                self.mouse_button_up(10+x*self.dx, 10+y*self.dy, 1)

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.back_color)

        self.tools.line(self.fore_color, (self.width // 3, 0), (self.width // 3, self.height), 2)
        self.tools.line(self.fore_color, (2*self.width // 3, 0), (2*self.width // 3, self.height), 2)
        self.tools.line(self.fore_color, (0, self.height // 3), (self.width, self.height // 3), 2)
        self.tools.line(self.fore_color, (0, 2*self.height // 3), (self.width, 2*self.height // 3), 2)
        self.tools.rect(self.fore_color, (0, 0, self.width-1, self.height-1), 2)

        sol = self.isResolved(self.grid, "X") + self.isResolved(self.grid, "O") + "  "
        sol = sol if sol.strip() != "" else self.isTie(self.grid) + "  "

        for i in range(3):
            for j in range(3):
                decode = sol
                color = self.fore_color
                while len(decode) > 2:
                    if (decode[0] == "R" and int(decode[1]) == j) or (
                        decode[0] == "C" and int(decode[1]) == i) or (
                        decode[0] == "/" and int(decode[1]) == 1 and i == j) or (
                        decode[0] == "/" and int(decode[1]) == 2 and i == 2-j):
                        color = (0, 255, 0)
                        break
                    elif decode[0] == "T":
                        color = (200, 50, 50)
                        break
                        
                    decode = decode[2:]

                texte_surf = self.FONT.render("{}".format(self.grid[i][j]), False, color)
                w, h = texte_surf.get_size()
                self.screen.blit(texte_surf, (self.decalx-w//2+i*self.dx, self.decaly+self.dy*j-h//2)) 


if __name__ == '__main__':
    from exec import run
    run(TicTacToe)
