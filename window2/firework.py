import random
import math

from classes import Application, make_path
from colors import Colors
from p5 import Vector, StaticVector


class Particle:

    def __init__(self, x, y, vx=0, vy=None, color=(0, 0, 0), nombre=1, parent_size=0):
        self.color = color
        self.nombre = nombre
        self.max_life = 20 * parent_size
        self.life = self.max_life
        while sum(self.color) < 200:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.pos = Vector(x, y)
        rand = random.randint(Firework.VEL_MAX, Firework.VEL_MAX+5)
        self.vel = Vector(vx, vy if vy else -rand)
        self.acc = Vector(0, 0.15)

    def update(self):
        if self.nombre == 1:
            self.life -= 1
        self.vel.add(self.acc)
        self.pos.add(self.vel)

    def alpha_color(self):
        pct = self.life / self.max_life
        return [int(x*pct) for x in self.color]

    def to_draw(self):
        return (self.pos.x, self.pos.y)


class Firework(Application):
    MIN_SIZE = (300, 200)
    VEL_MAX = 0

    DEFAULT_CONFIG = ("Feu d'artifice", Colors.MIDDLE_BLUE)
    WINDOW_PROPERTIES = ["SOUND(60)", "RESIZABLE"]

    def __init__(self, screen, args):
        
        super().__init__(screen)
        self.resize(screen)
        self.nombre = self.screen.get_size()[0]//300 

        self.action = ""
        self.fusees = []
        self.particles = []
        self.load_sounds()
        self.get_theme()

    def get_theme(self):
        if self.theme.get_theme() == "CLAIR":
            self.back_color = (200, 200, 200)
        else:
            self.back_color = (0, 0, 0)

    def keyreleased(self, event):
        # print("Firework", event, flush=True)
        touche = self.keys.get_key()
        if touche == self.keys.K_ESCAPE:
            self.action = "QUIT"
            return

        if touche == self.keys.K_KP_PLUS:
            self.nombre += 1
            self.set_title(f"Feu d'artifice ({self.nombre} fusées)")

        elif touche == self.keys.K_KP_MINUS:
            if self.nombre > 1:
                self.nombre -= 1
                self.set_title(f"Feu d'artifice ({self.nombre} fusées)")

    def load_sounds(self):
        self.sounds = {"LAUNCH": [], "EXPLODE": []}
        self.sound_channels = []
        self.max_channels = 32

        for i in range(3):
            sound = self.sound.load_sound(make_path("sounds", f"fusee{1+i}.mp3"), 0.2)
            self.sounds["LAUNCH"].append(sound)
        for i in range(5):
            sound = self.sound.load_sound(make_path("sounds", f"Petard{1+i}.mp3"), 0.4)
            self.sounds["EXPLODE"].append(sound)

    def close(self):
        self.sound.stop_channels()

    def set_parent(self, parent):
        self.parent = parent

    def resize(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        Firework.VEL_MAX = int(0.35*math.sqrt(self.height*4/5))

    def get_action(self):
        return self.action

    def explosion(self, fusee):
        for _ in range(fusee.nombre*20):
            p = StaticVector.random2D().mult(fusee.nombre*random.random()).add(Vector(0, -1))
            self.particles.append(Particle(fusee.pos.x, fusee.pos.y, p.x, p.y, fusee.color, 1, fusee.nombre))

    def play_sounds(self, type_sound, rand):
        if len(self.sound_channels) < self.max_channels:
            channel = self.sound.play_sound(self.sounds[type_sound][random.randint(0, rand)])
            if channel:
                self.sound_channels.append(channel)
                        
    def add_fusee(self):
        self.sound.remove_unused_channels()
        self.play_sounds("LAUNCH", 2)
        self.fusees.append(
            Particle(random.randint(10, self.width-10), self.height, nombre=random.randint(2, 12)))

    def update(self):
        if len(self.fusees) < self.nombre:
            self.add_fusee()

        for i, f in enumerate(self.fusees):
            f.update()
            if f.vel.y > 0:
                self.play_sounds("EXPLODE", 3)
                self.explosion(f)
                self.fusees.pop(i)

        for i, p in enumerate(self.particles):
            p.update()
            if p.life <= 0:
                self.particles.pop(i)

    def draw(self):
        self.screen.fill(self.back_color)
        for f in self.fusees:
            self.tools.circle(f.color, f.to_draw(), f.nombre)
        for p in self.particles:
            self.tools.circle(p.alpha_color(), p.to_draw(), 2)


if __name__ == '__main__':
    from exec import run
    run(Firework)
