import pygame, random, math

max_vel = 5
max_star_dist = 500


def signe_int(x):
    return x / abs(x)


class Etoiles:

    def __init__(self, maximum, zone):
        self.maximum = maximum
        self.liste = []
        self.zone = zone
        self.center = ((zone[1][0]+zone[0][0])//2, (zone[1][1]+zone[0][1])//2)
        print("Center :", self.center)

    def update(self):
        # creation d'un nouveau point
        if len(self.liste) < self.maximum:
            au_centre = False
            retrecicement = 10
            while not au_centre:
                x = random.randint(self.zone[0][0]+retrecicement, self.zone[1][0]-retrecicement)
                y = random.randint(self.zone[0][1]+retrecicement, self.zone[1][1]-retrecicement)
                z = random.randint(10, max_star_dist)
                au_centre = math.sqrt( \
                    (self.center[0]-x)*(self.center[0]-x) + (self.center[1]-y)*(self.center[1]-y)) > 10
            self.liste.append([x, \
                               y, \
                               z, \
                               random.randint(1, 10),
                               self.center[0] + int(2 * (x - self.center[0])) // z,
                               self.center[1] + int(2 * (y - self.center[1])) // z, \
                               self.zone[0][0] // z // 2
                              ])

        # animation des points
        for i, e in enumerate(self.liste):
            e[2] -= e[3]
            if e[2] < 1:
                self.liste.pop(i)
            else:
                e[4] = self.center[0] + int(100 * (e[0] - self.center[0])) // e[2]
                e[5] = self.center[1] + int(100 * (e[1] - self.center[1])) // e[2]
                e[6] = self.zone[0][0] // e[2] // 2
                if e[4] - e[6] < self.zone[0][0] or e[5] - e[6] < self.zone[0][1] or \
                   e[4] + e[6] > self.zone[1][0] or e[5] + e[6] > self.zone[1][1]:
                    self.liste.pop(i)

    def get_coords(self):
        color = lambda z : 255 * (max_star_dist - z) // max_star_dist
        l = [(
              nx, \
              ny, \
              nz,
              (color(z), color(z), color(z))
             ) \
            for x, y, z, t, nx, ny, nz in self.liste]

        #print(l)
        return l


class Ligne:

    def __init__(self, deb, fin, boite, color):
        self.deb = deb
        self.fin = fin
        self.boite = boite
        self.color = color

        self.veld = [0, 0]
        self.velf = [0, 0]
        while self.veld[0] == 0 or self.veld[1] == 0:
            self.veld = [random.randint(-max_vel, max_vel), random.randint(-max_vel, max_vel)]
        while self.velf[0] == 0 or self.velf[1] == 0:
            self.velf = [random.randint(max_vel, max_vel), random.randint(-max_vel, max_vel)]

    def update(self):
        for i in range(2):
            if self.deb[i] + self.veld[i] > self.boite[1][i] or self.deb[i] + self.veld[i] < self.boite[0][i]:
                self.veld[i] *= -1
            self.deb[i] += self.veld[i]

            if self.fin[i] + self.velf[i] > self.boite[1][i] or self.fin[i] + self.velf[i] < self.boite[0][i]:
                self.velf[i] *= -1
            self.fin[i] += self.velf[i]

    def get_coords(self):
        return (self.deb, self.fin)


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def init_vars():
    ballet = []
    if False:
        for i in range(100):
            ballet.append(Ligne([random.randint(zone[0], window_size[0]), random.randint(0, window_size[1])], \
                            [random.randint(zone[0], window_size[0]), random.randint(0, window_size[1])], \
                            ((zone[0], 0), window_size), (random.randint(0,255), random.randint(0,255), random.randint(0,255))))

    for i in range(100):
        ballet.append(Ligne([random.randint(0, zone[0]), random.randint(0, zone[1])], \
                        [random.randint(0, zone[0]), random.randint(0, zone[1])], \
                        ((0, 0), zone), (random.randint(0,255), random.randint(0,255), random.randint(0,255))))
    return ballet


pygame.init()

try:
  #pygame.mixer_music.load("D:\\Mes Documents\\Musique\\Youtube Compilation\\DJ RN SR MEGA DANCE Vol 17 TRN DJ.mp3")
  print("")

except:
  print("Error loading music")
  
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 500)

pygame.display.set_caption("Ma fenêtre pygame")
window_size = (1280, 600)
zone = (window_size[0] // 2, window_size[1])

screen = pygame.display.set_mode(window_size, pygame.RESIZABLE, 8)

Application_launched = True
Application_active = True

black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
color = (75, 150, 255)
grey = (200, 200, 200)
white = (255, 255, 255)

ballet = []
etoiles = Etoiles(0, [zone,window_size])

mouse_pos = (window_size[0]//2, window_size[1]//2)
mouse_cursor_circle_size = 40
mouse_button_pressed = False
user_event = True

font = pygame.font.SysFont("Arial", 12, 0, 0)
text_font = font.render(f"{clock.get_fps():3.1f} FPS", 0, white)
nbstars_font = font.render(f"{len(etoiles.liste)} FPS", 0, white)

# pygame.mixer_music.play()

while Application_launched:

    # 60 images/s
    clock.tick(60)
    # pygame.time.wait(10)

    if Application_active:
        screen.fill(black)
        pygame.draw.rect(screen, white, [(0, 0), window_size], 1)
        pygame.draw.line(screen, white, (zone[0], 0), (zone[0], window_size[1]), 1)
        for l in ballet:
            l.update()
            pygame.draw.line(screen, l.color, *l.get_coords())

        etoiles.update()
        for e in etoiles.get_coords():
            pygame.draw.circle(screen, e[3], e[:2], e[2])
            # print(f"({x}, {y})", end=" ")

        if mouse_button_pressed:
            pass
            #pygame.draw.circle(screen, random_color(), mouse_pos, mouse_cursor_circle_size)
        else:
            pass
            #pygame.draw.circle(screen, random_color(), mouse_pos, mouse_cursor_circle_size, 2)

        # affichage des modifications
        screen.blit(text_font, (10, 10))
        screen.blit(nbstars_font, (zone[0]+10, 10))


        pygame.display.flip()

    # print(f"busy ? {pygame.mixer_music.get_busy()}")

    # gestion des evennements
    for event in pygame.event.get():
        # - Croix "X" de la fenetre ------------------------------------------------------------------------
        if event.type == pygame.QUIT:
            Application_launched = False

        # - touche clavier relachée ------------------------------------------------------------------------
        elif event.type == pygame.KEYUP:
            key_code = event.dict.get("key", 0)
            key_mode = event.dict.get("mod", 0)

            if key_mode == pygame.KMOD_LALT and key_code == pygame.K_F4 or key_code == pygame.K_ESCAPE :
                Application_launched = False

            if key_code == pygame.K_SPACE:
                pass

            elif key_code == pygame.K_F11:
                pass

            elif key_code == pygame.K_p:
                pygame.mixer_music.play()

        # - touche souris enfoncée ------------------------------------------------------------------------
        elif event.type in [pygame.MOUSEBUTTONDOWN]:
            mouse_button_pressed = True

        # - touche souris relachée ------------------------------------------------------------------------
        elif event.type in [pygame.MOUSEBUTTONUP]:
            mouse_button_pressed = False
            button = event.dict.get("button", 0)
            if button == pygame.BUTTON_WHEELUP:
                mouse_cursor_circle_size -= 5
                if mouse_cursor_circle_size < 10:
                    mouse_cursor_circle_size = 10
            elif button == pygame.BUTTON_WHEELDOWN:
                mouse_cursor_circle_size += 5
                if mouse_cursor_circle_size > 100:
                    mouse_cursor_circle_size = 100

        # - souris déplacée -------------------------------------------------------------------------------
        elif event.type in [pygame.MOUSEMOTION]:
            mouse_pos = event.dict.get("pos")

        # - fenetre ?????????????? ------------------------------------------------------------------------
        elif event.type == pygame.VIDEOEXPOSE:
            pass

        # - fenetre redimensionnée ------------------------------------------------------------------------
        elif event.type == pygame.VIDEORESIZE:
            w = event.dict.get('w')
            h = event.dict.get('h')
            print(f"change Screen Resolution = {w}x{h}")
            window_size = (w, h)
            zone = (window_size[0] // 2, window_size[1])

            ballet = init_vars()
            etoiles = Etoiles(150, [(zone[0], 0), window_size])

            screen = pygame.display.set_mode(window_size, pygame.RESIZABLE, 8)

        # - souris active dans la fenetre -----------------------------------------------------------------
        elif event.type == pygame.ACTIVEEVENT:
            # Application_active = event.dict.get("gain", 0) == 1
            pass

        # - USEREVENT activé toutes les 500ms -------------------------------------------------------------
        elif event.type == pygame.USEREVENT:
            text_font = font.render(f"{clock.get_fps():.1f} FPS", 0, white)
            nbstars_font = font.render(f"{len(etoiles.liste)} étoiles", 0, white)

        else:
            print(event.dict, event.type)

