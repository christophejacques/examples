import random
from classes import Application
from colors import Colors


class Apples:

    def __init__(self, maximum=1):
        self.liste = []
        self.maximum = maximum

    def init(self):
        self.liste.clear()
        for _ in range(self.maximum):
            self.create()

    def create(self):
        x = random.randint(1, SnakeGame.w-2)
        y = random.randint(1, SnakeGame.h-2)
        self.liste.append((x, y))

    def to_draw(self):
        for a in self.liste:
            yield a[0]*SnakeGame.size, a[1]*SnakeGame.size


class Snake:

    def __init__(self, tools):
        self.tail = []
        self.to_show = ""
        self.tools = tools

    def init(self):
        self.tail.clear()
        self.is_alive = True
        self.pos = (SnakeGame.w//2, SnakeGame.h//2)
        self.vel = (1, 0)
        self.key_vel = (0, 0)

    def eat(self, position, apples):
        for i, apple in enumerate(apples.liste):
            if apple == position:
                del apples.liste[i]
                apples.create()
                return True
                
    def update(self, apples):
        self.vel = self.key_vel
        
        suivant = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        if not self.tools.Rect(0, 0, SnakeGame.w, SnakeGame.h).collidepoint(*suivant):
            self.to_show = f"OUT {suivant} Taille: {len(self.tail)}"
            self.is_alive = False
            return 
        if suivant in self.tail:
            self.to_show = f"AUTO BITE {suivant} Taille: {len(self.tail)}"
            self.is_alive = False
            return 

        self.tail.append(self.pos)
        if not self.eat(suivant, apples):
            self.tail.pop(0)

        self.pos = (self.pos[0]+self.vel[0], self.pos[1]+self.vel[1])

    def to_draw(self):
        for c in self.tail:
            yield c[0]*SnakeGame.size, c[1]*SnakeGame.size

        yield self.pos[0]*SnakeGame.size, self.pos[1]*SnakeGame.size


class SnakeGame(Application):
    MIN_SIZE = (300, 300)
    VEL_MAX = 0

    WINDOW_PROPERTIES = ["RESIZABLE"]
    DEFAULT_CONFIG = ("Jeu du Serpent", Colors.GREEN)

    size = 10
    w, h = 0, 0

    def __init__(self, parent, screen, args):
        self.set_parent(parent)
        self.snake = Snake(parent.tools)
        self.apples = Apples()
        self.resize(screen)
        self.action = ""

    def set_parent(self, parent):
        print(f"parent({parent=})", flush=True)
        self.parent = parent

    def resize(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        # print("NewSize:", self.width, self.height)
        self.initialisation()

    def initialisation(self):
        self.frameCount = 0
        SnakeGame.w = self.width // SnakeGame.size
        SnakeGame.h = self.height // SnakeGame.size
        # nombre d'Apple sur 1% de la surface
        self.apples.maximum = self.w * self.h // 100
        self.snake.init()
        self.apples.init()
        # print("Board Size:", SnakeGame.w, SnakeGame.h)

    def get_action(self):
        return self.action

    def update(self):
        self.frameCount += 1
        if not self.parent:
            return

        if self.parent.keypressed():
            if self.parent.view_key("LAST") == self.parent.keys.K_ESCAPE:
                self.parent.get_key()
                self.action = "QUIT"

        if self.frameCount % 4 == 1:
            self.touche = self.parent.get_key()
            if self.touche == self.parent.keys.K_SPACE:
                self.initialisation()

            if self.snake.is_alive:
                if self.touche == self.parent.keys.K_UP:
                    if self.snake.vel[1] != 1:
                        self.snake.key_vel = (0, -1)
                elif self.touche == self.parent.keys.K_DOWN:
                    if self.snake.vel[1] != -1:
                        self.snake.key_vel = (0, 1)
                elif self.touche == self.parent.keys.K_LEFT:
                    if self.snake.vel[0] != 1:
                        self.snake.key_vel = (-1, 0)
                elif self.touche == self.parent.keys.K_RIGHT:
                    if self.snake.vel[0] != -1:
                        self.snake.key_vel = (1, 0)

                self.snake.update(self.apples)

            elif self.touche is not None:
                self.parent.clear_key_buffer()
                self.snake.init()
                self.apples.init()

        if self.snake.to_show:
            self.parent.set_title(SnakeGame.DEFAULT_CONFIG[0] + " : " + self.snake.to_show)
            self.snake.to_show = ""

    def draw(self):
        self.screen.fill(Colors.BLACK)

        for x, y in self.apples.to_draw():
            self.screen.fill(Colors.GREEN, (x, y, SnakeGame.size, SnakeGame.size))
        
        for x, y in self.snake.to_draw():
            self.screen.fill(Colors.WHITE, (x, y, SnakeGame.size, SnakeGame.size))


if __name__ == '__main__':
    from exec import run
    run(SnakeGame)
