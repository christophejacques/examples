import pygame
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

    def alpha_color(self,):
        pct = self.life / self.max_life
        return [int(x*pct) for x in self.color]

    def to_draw(self):
        return (self.pos.x, self.pos.y)


class Firework(Application):
    MIN_SIZE = (300, 200)
    VEL_MAX = 0

    DEFAULT_CONFIG = ("Feu d'artifice", Colors.MIDDLE_BLUE)
    WINDOW_PROPERTIES = ["SOUND(12)", "RESIZABLE"]

    def __init__(self, parent, screen, args):
        self.set_parent(parent)
        self.resize(screen)
        self.nombre = self.screen.get_size()[0]//300 

        self.action = ""
        self.fusees = []
        self.particles = []
        self.load_sounds()

    def load_sounds(self):
        self.sounds = {"LAUNCH": [], "EXPLODE": []}
        self.sound_channels = []
        self.max_channels = 32
        if not self.parent: return 
        for i in range(3):
            sound = self.parent.load_sound(make_path("sounds", f"fusee{1+i}.mp3"), 0.2)
            self.sounds["LAUNCH"].append(sound)
        for i in range(5):
            sound = self.parent.load_sound(make_path("sounds", f"Petard{1+i}.mp3"), 0.4)
            self.sounds["EXPLODE"].append(sound)

    def close(self):
        # print("Stopping sound channels.")
        if self.parent:
            self.parent.stop_channels()

    def set_parent(self, parent):
        self.parent = parent

    def resize(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        Firework.VEL_MAX = int(0.3*math.sqrt(self.height*4/5))

    def get_action(self):
        return self.action

    def explosion(self, fusee):
        for _ in range(fusee.nombre*20):
            p = StaticVector.random2D().mult(fusee.nombre*random.random()).add(Vector(0, -1))
            self.particles.append(Particle(fusee.pos.x, fusee.pos.y, p.x, p.y, fusee.color, 1, fusee.nombre))

    def play_sound(self, type_sound, rand):
        if self.parent and len(self.sound_channels) < self.max_channels:
            channel = self.parent.play_sound(self.sounds[type_sound][random.randint(0, rand)])
            if channel:
                self.sound_channels.append(channel)
                        
    def add_fusee(self):
        if self.parent:
            self.parent.remove_unused_channels()
            self.play_sound("LAUNCH", 2)
        self.fusees.append(
            Particle(random.randint(10, self.width-10), self.height, nombre=random.randint(2, 12)))

    def update(self):
        if self.parent and self.parent.keypressed():
            self.touche = self.parent.get_key()
            if self.touche == pygame.K_ESCAPE:
                self.action = "QUIT"

            elif self.touche == pygame.K_KP_PLUS:
                self.nombre += 1
                self.parent.set_title(f"Feu d'artifice ({self.nombre} fusées)")
            elif self.touche == pygame.K_KP_MINUS:
                if self.nombre > 1:
                    self.nombre -= 1
                    self.parent.set_title(f"Feu d'artifice ({self.nombre} fusées)")

        if len(self.fusees) < self.nombre:
            self.add_fusee()

        for i, f in enumerate(self.fusees):
            f.update()
            if f.vel.y > 0:
                self.play_sound("EXPLODE", 3)
                self.explosion(f)
                self.fusees.pop(i)

        for i, p in enumerate(self.particles):
            p.update()
            if p.life <= 0:
                self.particles.pop(i)

    def draw(self):
        self.screen.fill(Colors.BLACK)
        for f in self.fusees:
            pygame.draw.circle(self.screen, f.color, f.to_draw(), f.nombre)
        for p in self.particles:
            pygame.draw.circle(self.screen, p.alpha_color(), p.to_draw(), 2)


def run():
    pygame.init()
    running = True
    screen = pygame.display.set_mode((1400, 400), pygame.RESIZABLE)  # pygame.FULLSCREEN)
    f = Firework(None, screen, ())
    while running:
        pygame.time.Clock().tick(60)
        f.update()
        f.draw()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KMOD_LGUI:
                pass

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

            elif event.type == pygame.MOUSEBUTTONUP:
                pass

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    f.close()
                    running = False
                elif event.key == pygame.K_SPACE:
                    f.add_fusee()

            elif event.type == pygame.AUDIO_S16:
                pass

            elif event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                # print(event.type)
                f.resize(screen)

    pygame.quit()


if __name__ == '__main__':
    print("Compilation : Ok")
    run()
    print("Fin")
