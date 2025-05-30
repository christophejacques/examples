import pygame
import json
import traceback

from audio import Audio
from mouse import Mouse
from keyboard import Keyboard
from colors import Colors
from classes import Variable, Tools, get_all_classes, Theme, Registres


def get_pygame_const_name(index):
    for c in dir(pygame):
        if c[1] in "AZERTYUIOPMLKJHGFDSQWXCVBN":
            if type(getattr(pygame, c)) == int and getattr(pygame, c) == index:
                return c


pygame.init()

# SYS_FONT = pygame.font.SysFont(pygame.font.get_default_font(), 16)
# SYS_FONT = pygame.font.SysFont("comicsans", 12)
SYS_FONT = pygame.font.SysFont("courier", 12)


class Icone:
    ICONE_WIDTH = 80
    ICONE_HEIGHT = 60
    ICONE_DECAL = 50

    def __init__(self, screen, title, couleur, x, y, app, *args):
        self.title = title
        self.couleur = couleur
        self.app = app
        self.args = args
        self.icone_rect = pygame.Rect(x, y, self.ICONE_WIDTH, self.ICONE_HEIGHT)
        self.dest_rect = self.icone_rect
        
        self.update_screen(screen)
        self.icone_surf.fill(self.couleur)
        self.title = title

        self.update_theme()
        self.title_rect = pygame.Rect(x, Icone.ICONE_HEIGHT+y, Icone.ICONE_WIDTH, Icone.ICONE_HEIGHT)
        self.mouse_over = False

    def update_screen(self, screen):
        self.screen_surf = screen
        self.icone_surf = self.screen_surf.subsurface(self.icone_rect)

    def update_theme(self):
        self.text_surf = SYS_FONT.render(self.title, False, Theme.get("FORE_COLOR"))

    def move(self, dx=0, dy=0, liste_icones=None):
        if dx or dy:
            w, h = self.screen_surf.get_size()
            if self.icone_rect[0] + dx < 0:
                dx = -self.icone_rect[0]
            if self.icone_rect[1] + dy < 0:
                dy = -self.icone_rect[1]
            if dx + self.icone_rect[0] + self.icone_rect[2] > w:
                dx = w - self.icone_rect[0] - self.icone_rect[2] 
            if dy + self.icone_rect[1] + self.icone_rect[3] > h:
                dy = h - self.icone_rect[1] - self.icone_rect[3] 

            self.icone_rect = self.icone_rect.move(dx, dy)
            self.title_rect = self.title_rect.move(dx, dy)
            
            self.icone_surf = self.screen_surf.subsurface(self.icone_rect)
            midx, midy = (
                self.icone_rect.midtop[0]+Icone.ICONE_DECAL//2, 
                self.icone_rect.midleft[1]+Icone.ICONE_DECAL//2)
            posx = (midx // (Icone.ICONE_WIDTH+Icone.ICONE_DECAL)) * (Icone.ICONE_WIDTH+Icone.ICONE_DECAL) + 10
            posy = (midy // (Icone.ICONE_HEIGHT+Icone.ICONE_DECAL)) * (Icone.ICONE_HEIGHT+Icone.ICONE_DECAL) + 10

            dest_rect = pygame.Rect(posx, posy, Icone.ICONE_WIDTH, Icone.ICONE_HEIGHT)
            mouse_on_ico = dest_rect.collidelist([ico.icone_rect for ico in liste_icones if ico != self])
            if mouse_on_ico < 0:
                # Pas de collision avec les autres icones sur le bureau
                self.dest_rect = dest_rect

    def move_ip(self, x, y):
        self.icone_rect = pygame.Rect(x, y, Icone.ICONE_WIDTH, Icone.ICONE_HEIGHT)
        self.dest_rect = self.icone_rect
        self.title_rect = pygame.Rect(x, Icone.ICONE_HEIGHT+y, Icone.ICONE_WIDTH, Icone.ICONE_HEIGHT)
        self.icone_surf = self.screen_surf.subsurface(self.icone_rect)

    def draw(self):
        self.icone_surf.fill(self.couleur)
        if self.mouse_over:
            pygame.draw.rect(self.screen_surf, Colors.GREY, self.dest_rect, 1)
            pygame.draw.rect(self.icone_surf, Colors.WHITE, (0, 0, self.ICONE_WIDTH, self.ICONE_HEIGHT), 1)
        self.screen_surf.blit(self.text_surf, self.title_rect)


class Tache:
    TASK_HEIGHT = 0
    TASK_WIDTH_MAX = 200
    TASK_WIDTH = TASK_WIDTH_MAX
    TASK_SELECT_HEIGHT = 3
    TASK_ICONE_SIZE = 20
    TASK_TITLE_BORDER = 5

    TASK_BUTTON_BACK_COLOR = (80, 80, 80)
    TASK_SELECTED_BUTTON_BACK_COLOR = (50, 50, 50)
    TASK_ERROR_BUTTON_BACK_COLOR = (250, 50, 50)

    def __init__(self, screen, title, couleur, x, window):
        self.update_screen(screen)
        self.title = title
        self.window = window
        self.mouse_over = False
        self.set_pos(x)
        self.get_theme()

    def get_theme(self):
        self.text_surf = SYS_FONT.render(self.title, False, Theme.get("FORE_COLOR"))
        if self.window.on_error:
            self.couleur = Window.THEME_ERROR_COLOR
        else:
            self.couleur = Tache.TASK_BUTTON_BACK_COLOR

    def update_screen(self, screen):
        self.screen_surf = screen

    def set_pos(self, x):
        self.posx = x
        self.tache_rect = pygame.Rect(self.posx, 0, Tache.TASK_WIDTH, Tache.TASK_HEIGHT)
        self.tache_button_rect = self.tache_rect.clip(
            (self.posx, 0), (Tache.TASK_WIDTH, Tache.TASK_HEIGHT-Tache.TASK_SELECT_HEIGHT))
        self.title_rect = self.tache_button_rect.clip(
            (self.posx+Tache.TASK_ICONE_SIZE, Tache.TASK_TITLE_BORDER), 
            (Tache.TASK_WIDTH-Tache.TASK_ICONE_SIZE, Tache.TASK_HEIGHT-Tache.TASK_SELECT_HEIGHT))
        self.tache_select_rect = self.tache_rect.clip(
            (self.posx, Tache.TASK_HEIGHT-Tache.TASK_SELECT_HEIGHT), (Tache.TASK_WIDTH, Tache.TASK_SELECT_HEIGHT))

        self.tache_button_surf = self.screen_surf.subsurface(self.tache_button_rect)
        self.tache_select_surf = self.screen_surf.subsurface(self.tache_select_rect)

    def set_title(self, title):
        self.title = title
        self.text_surf = SYS_FONT.render(self.title, False, Theme.get("FORE_COLOR"))

    def update(self):
        if self.window.on_error and self.couleur != Window.THEME_ERROR_COLOR:
            self.couleur = Window.THEME_ERROR_COLOR
    
    def draw(self):
        if self.window.active:
            if self.window.on_error:
                self.tache_button_surf.fill(Tache.TASK_ERROR_BUTTON_BACK_COLOR)
            else:
                self.tache_button_surf.fill(Tache.TASK_SELECTED_BUTTON_BACK_COLOR)
        else:
            self.tache_button_surf.fill(self.couleur)

        if self.mouse_over:
            self.tache_select_surf.fill(Colors.CYAN)
        self.screen_surf.blit(self.text_surf, self.title_rect)


class Window:

    ICONE_WIDTH = 30
    ICONE_HEIGHT = 20
    WINDOW_BORDER_SIZE = 5

    THEME_ACTIVE_COLOR = (10, 130, 170, 50)
    THEME_INACTIVE_COLOR = (130, 130, 150, 50)
    THEME_ERROR_COLOR = (200, 20, 20)

    def __init__(self, x, y, w, h, text, colour, app, *args):
        self.app = app
        self.sound_id = None
        self.active = True
        self.mouse_over = False
        self.properties = self.app.WINDOW_PROPERTIES
        sound_property = self.search_for_in("SOUND", self.properties)
        if sound_property:
            # print("Activate", sound_property)
            if "(" in sound_property and ")" in sound_property:
                nb_channels = int(sound_property[1+sound_property.index("("):sound_property.index(")")])
            else:
                nb_channels = 1
            self.sound_id = Audio.new_application()
            Audio.init_application(self.sound_id, nb_channels)
        self.statut = []
        self.on_error = False
        self.title = text
        self.colour = colour
        self.set_size(x, y, w, h, False)
        self.min_size = self.app.MIN_SIZE
        self.set_title(text)
        self.sound_index = 0
        self.sounds = {}
        try:
            Variable.window = self
            self.instance = self.app(self.window_draw_surf, args)
            self.instance.post_init()

        except Exception as e:
            self.set_error()
            print("Window.__init__() Error:", e)
            traceback.print_exc()

    def set_size(self, x, y, w, h, update_app=True):
        self.border_size = 0 if self.last_statut() == "MAXIMIZED" else self.WINDOW_BORDER_SIZE

        # creation surfaces d'affichage
        self.window_surf = pygame.Surface((w, h), 0, 24)

        self.window_draw_surf = self.window_surf.subsurface(
            pygame.Rect(self.border_size, self.ICONE_HEIGHT, w-2*self.border_size, h-self.ICONE_HEIGHT-self.border_size))
        self.window_draw_surf.fill(self.colour)

        self.top_surf = self.window_surf.subsurface(pygame.Rect(0, 0, w, self.ICONE_HEIGHT))
        self.min_surf = self.top_surf.subsurface(pygame.Rect(w-3*self.ICONE_WIDTH-self.border_size, 0, self.ICONE_WIDTH, self.ICONE_HEIGHT))
        self.max_surf = self.top_surf.subsurface(pygame.Rect(w-2*self.ICONE_WIDTH-self.border_size, 0, self.ICONE_WIDTH, self.ICONE_HEIGHT))
        self.close_surf = self.top_surf.subsurface(pygame.Rect(w-self.ICONE_WIDTH-self.border_size, 0, self.ICONE_WIDTH, self.ICONE_HEIGHT))
        self.title_surf = self.top_surf.subsurface(pygame.Rect(self.border_size+self.ICONE_WIDTH, 0, w-4*self.ICONE_WIDTH-2*self.border_size, self.ICONE_HEIGHT))

        # creation bords fenetre
        if self.last_statut() != "MAXIMIZED":
            self.bottom_surf = self.window_surf.subsurface(pygame.Rect(0, h-self.border_size, w, self.border_size))
            self.left_surf = self.window_surf.subsurface(pygame.Rect(0, 0, self.border_size, h))
            self.right_surf = self.window_surf.subsurface(pygame.Rect(w-self.border_size, 0, self.border_size, h))

        # creation rectangles
        self.window = pygame.Rect(x, y, w, h)
        self.window_draw = self.window.clip((x+self.border_size, y+self.ICONE_HEIGHT), (w-2*self.border_size, h-self.ICONE_HEIGHT-self.border_size))
        self.top_rect = self.window.clip((x, y), (w, self.ICONE_HEIGHT))
        self.icone_rect = self.top_rect.clip((x+self.border_size, y), (self.ICONE_WIDTH, self.ICONE_HEIGHT))
        self.title_rect = self.top_rect.clip((x+self.ICONE_WIDTH+self.border_size, 3+y), (w-4*self.ICONE_WIDTH-2*self.border_size, self.ICONE_HEIGHT))
        self.min_rect = self.top_rect.clip((x+w-3*self.ICONE_WIDTH-self.border_size, y), (self.ICONE_WIDTH, self.ICONE_HEIGHT))
        self.max_rect = self.top_rect.clip((x+w-2*self.ICONE_WIDTH-self.border_size, y), (self.ICONE_WIDTH, self.ICONE_HEIGHT))
        self.close_rect = self.top_rect.clip((x+w-self.ICONE_WIDTH-self.border_size, y), (self.ICONE_WIDTH, self.ICONE_HEIGHT))

        self.bottom_rect = self.window.clip((x, y+h-self.border_size), (w, self.border_size))
        self.left_rect = self.window.clip((x, y, self.border_size, h))
        self.right_rect = self.window.clip((x+w-self.border_size, y, self.border_size, h))

        if update_app and not self.on_error:
            try:
                self.instance.tools = Tools(self.window_draw_surf)
                self.instance.resize(self.window_draw_surf)
                
            except Exception as e:
                self.set_error()
                print("Window.set_size() Error:", e)

        self.set_surface_color()

    def resize(self, direction, dx=0, dy=0, width=None, height=None):
        # print(f"{dx=}, {dy=}, {width=}, {height=}", flush=True)
        x, y = self.window.topleft
        if not width is None:
            self.set_size(x, y, width, height)
            return 
            
        w, h = self.window.size
        if dy != 0 and "BOTTOM" in direction:
            if h+dy >= self.min_size[1]+self.border_size+self.top_rect.height:
                h += dy
        if dx != 0 and "LEFT" in direction:
            if w-dx >= self.min_size[0]+2*self.border_size:
                x += dx
                w -= dx
        elif dx != 0 and "RIGHT" in direction:
            if w+dx >= self.min_size[0]+2*self.border_size:
                w += dx
        
        self.set_size(x, y, w, h)

    def update_theme(self):
        if self.on_error:
            return
        self.set_surface_color()
        self.instance.get_theme()

    def search_for_in(self, value, liste):
        for val in liste:
            if value in val:
                return val
        return False

    def load_sound(self, fichier, volume):
        if not self.sound_id:
            return False
        return Audio.load_sound(self.sound_id, fichier, volume)

    def play_sound(self, index, callback=None):
        if self.sound_id:
            Audio.play_sound(self.sound_id, index, callback)
        return False

    def remove_unused_channels(self):
        if self.sound_id:
            Audio.remove_appli_unused_sound_channels(self.sound_id)

    def stop_channels(self):
        if self.sound_id:
            Audio.stop_all_channels_application(self.sound_id)

    def get_mouse_pos(self):
        mouseX, mouseY = Mouse.get_pos()
        x, y = self.window.topleft
        mouseX -= x + self.border_size
        mouseY -= y + self.top_rect.height
        return mouseX, mouseY

    def set_surface_color(self):
        color = self.theme_color(check_error=True)
        self.top_surf.fill(color)

        self.set_win_buttons_surface_color()
        if self.last_statut() != "MAXIMIZED":
            self.bottom_surf.fill(color)
            self.left_surf.fill(color)
            self.right_surf.fill(color)
        self.title_surf.fill(color)

    def set_win_buttons_surface_color(self):
        self.min_surf.fill(self.theme_color((10, 100, 140), (110, 110, 110)))
        pygame.draw.rect(self.min_surf, self.theme_color((0, 0, 0), (60, 60, 60)), (10, 11, 11, 2), 1)
        if "RESIZABLE" in self.properties:
            self.max_surf.fill(self.theme_color((50, 120, 120), (120, 120, 120)))
            pygame.draw.rect(self.max_surf, self.theme_color((0, 0, 0), (60, 60, 60)), (10, 8, 11, 5), 1)
            pygame.draw.rect(self.max_surf, self.theme_color((0, 0, 0), (60, 60, 60)), (11, 9, 9, 3), 1)
            if self.last_statut() == "MAXIMIZED":
                pygame.draw.line(self.max_surf, self.theme_color((0, 0, 0), (60, 60, 60)), (8, 14), (18, 14), 1)
                pygame.draw.line(self.max_surf, self.theme_color((0, 0, 0), (60, 60, 60)), (8, 10), (8, 14), 1)
        else:
            self.max_surf.fill((50, 120, 120))
            pygame.draw.rect(self.max_surf, (60, 60, 60), (10, 8, 11, 5), 1)
            pygame.draw.rect(self.max_surf, (60, 60, 60), (11, 9, 9, 3), 1)

        self.close_surf.fill(self.theme_color((185, 85, 85), (130, 130, 150)))
        pygame.draw.line(self.close_surf, self.theme_color((0, 0, 0), (60, 60, 60)), (12, 7), (19, 13), 3)
        pygame.draw.line(self.close_surf, self.theme_color((0, 0, 0), (60, 60, 60)), (12, 13), (19, 7), 3)

    def set_title(self, title):
        self.title = title
        self.text_surf = SYS_FONT.render(self.title, False, (255, 255, 255))

    def set_error(self):
        self.on_error = True
        self.set_surface_color()

    def theme_color(self, active_color=None, inactive_color=None, check_error=False):
        if active_color is None:
            active_color = Window.THEME_ACTIVE_COLOR
        if inactive_color is None:
            inactive_color = Window.THEME_INACTIVE_COLOR

        if check_error and self.on_error:
            return self.THEME_ERROR_COLOR
        return active_color if self.active else inactive_color

    def last_statut(self):
        if self.statut:
            return self.statut[-1]
        return None

    def keypressed(self):
        if self.active:
            return Keyboard.keypressed()
        else:
            return False

    def keyreleased(self, event):
        pass

    def clear_key_buffer(self):
        if self.active:
            return Keyboard.clear_buffer()

    def get_key(self):
        if self.active:
            # print(f"window.get_key({self.title})")
            return Keyboard.get_key()
        else:
            return None

    def view_key(self, which_one):
        if self.active:
            if which_one.lower() == "LAST":
                return Keyboard.view_last_key()
            else:
                return Keyboard.view_next_key()
        else:
            return None

    def restaure(self):
        # print(f"restaure({self.statut})", flush=True)
        if self.last_statut() == "MAXIMIZED":
            self.statut.pop()
            self.set_size(*self.old_rect_size)

    def minimize(self):
        # print(f"minimize({self.statut})", flush=True)
        if self.last_statut() != "MINIMIZED":
            self.statut.append("MINIMIZED")
            self.stop_channels()

    def maximize(self):
        # print(f"maximize({self.statut})", flush=True)
        if self.last_statut() != "MAXIMIZED":
            self.old_rect_size = self.window.copy()
            self.statut.append("MAXIMIZED")
            screen_size = pygame.display.get_window_size()
            self.set_size(0, 0, screen_size[0], screen_size[1]-OperatingSystem.TASK_BAR_HEIGHT)

    def move(self, x=0, y=0):
        if x or y:
            self.window = self.window.move(x, y)
            self.window_draw = self.window_draw.move(x, y)
            self.top_rect = self.top_rect.move(x, y)
            self.title_rect = self.title_rect.move(x, y)
            self.icone_rect = self.icone_rect.move(x, y)
            self.min_rect = self.min_rect.move(x, y)
            self.max_rect = self.max_rect.move(x, y)
            self.close_rect = self.close_rect.move(x, y)

            self.bottom_rect = self.bottom_rect.move(x, y)
            self.left_rect = self.left_rect.move(x, y)
            self.right_rect = self.right_rect.move(x, y)

    def update(self):
        if not self.on_error and self.last_statut() != "MINIMIZED":
            try:
                self.instance.update()
            except Exception as e:
                self.set_error()
                print("Window.update() Error:", e)

    def draw(self, screen_surf):
        if self.last_statut() != "MINIMIZED":
            screen_surf.blit(self.window_surf, self.window)
            # if self.mouse_over:
            screen_surf.blit(self.text_surf, self.title_rect)
            if not self.on_error:
                try:
                    self.instance.draw()
                except Exception as e:
                    self.set_error()
                    print("Window.draw() Error:", e)

    def close(self):
        if not self.on_error:
            self.instance.registre.save_file()
            self.instance.close()
        else:
            Keyboard.clear_buffer()

        if self.sound_id:
            Audio.close_application(self.sound_id)
            

class OperatingSystem:
    TASK_BAR_HEIGHT = 25
    TASK_BAR_DECAL = 1
    TASK_BAR_MENU_WIDTH = 3
    NEW_WINDOW_DECAL = 30
    TASK_BAR_COLOR = (20, 20, 20, 100)

    def __init__(self):
        self.running = True
        Tache.TASK_HEIGHT = OperatingSystem.TASK_BAR_HEIGHT
        self.registre = Registres("OS")

        Audio.init(False)
        Theme.set_theme("SOMBRE")

        desktops = pygame.display.get_desktop_sizes()
        # define display/window height based on (the first) desktop size
        self.liste_fenetres = []
        self.liste_icones = []
        self.liste_systray = []
        self.ico_posX, self.ico_posY = 10, 10-(Icone.ICONE_DECAL+Icone.ICONE_HEIGHT)
        self.icone_catched_by_mouse = None
        self.window_catch_by_mouse = None
        self.liste_taches = []
        self.clock = pygame.time.Clock()
        self.tick = 0

        if desktops[0][1] > 1000:
            # Full HD max resolution
            disp_size = (1800, 788)
        else:
            disp_size = desktops[0]
        # self.screen = pygame.display.set_mode(desktops[0], pygame.FULLSCREEN, 24)
        self.screen = pygame.display.set_mode(disp_size, pygame.RESIZABLE, 24)
        self.set_size()
        self.update_theme()

    def update_screen(self):
        self.set_size()
        for icone in self.liste_icones:
            icone.update_screen(self.screen_surf)

        for tache in self.liste_taches:
            tache.update_screen(self.barre_taches)
        self.resize_taches()
        self.update_systrays_positions()

        screen_size = pygame.display.get_window_size()
        for fenetre in self.liste_fenetres:
            if fenetre.last_statut() == "MAXIMIZED":
                fenetre.set_size(0, 0, screen_size[0], screen_size[1]-OperatingSystem.TASK_BAR_HEIGHT)

    def update_systrays_positions(self):
        total: int = 0
        width, height = self.barre_taches.get_size()
        for systray in self.liste_systray:
            systray_width = systray.get_width()

            sysapp_rect = pygame.Rect(
                width - total - systray_width, 0, 
                systray_width, height)

            systray.update_screen(self.barre_taches.subsurface(sysapp_rect))
            
            # calcul du decalage de zone pour le prochain SysTray
            total += systray_width + systray.TEXT_OFFSET

    def update_theme(self):
        for icone in self.liste_icones:
            icone.update_theme()

        Window.THEME_ACTIVE_COLOR = Theme.get("THEME_ACTIVE_COLOR")
        Window.THEME_INACTIVE_COLOR = Theme.get("THEME_INACTIVE_COLOR")
        Window.THEME_ERROR_COLOR = Theme.get("THEME_ERROR_COLOR")

        for fenetre in self.liste_fenetres:
            fenetre.update_theme()

        OperatingSystem.TASK_BAR_COLOR = Theme.get("TASK_BAR_COLOR")

        Tache.TASK_BUTTON_BACK_COLOR = Theme.get("TASK_BUTTON_BACK_COLOR")
        Tache.TASK_ERROR_BUTTON_BACK_COLOR = Theme.get("TASK_ERROR_BUTTON_BACK_COLOR")
        Tache.TASK_SELECTED_BUTTON_BACK_COLOR = Theme.get("TASK_SELECTED_BUTTON_BACK_COLOR")
        for tache in self.liste_taches:
            tache.get_theme()

        for systray in self.liste_systray:
            systray.get_theme()

    def set_size(self):
        # print(self.screen.get_size(), flush=True)
        self.width, self.height = self.screen.get_size() 
        self.last_position = (10, 10)
        self.screen_surf = self.screen.subsurface(0, 0, self.width, self.height-self.TASK_BAR_HEIGHT)
        self.barre_taches_rect = pygame.Rect(0, self.height-self.TASK_BAR_HEIGHT, self.width, self.TASK_BAR_HEIGHT)
        self.barre_taches = self.screen.subsurface(self.barre_taches_rect)
        self.load_background_image()

    def load_background_image(self):
        image_file = self.registre.load("Wallpaper", "pornstar.jpg")
        try:
            # image = pygame.image.load("wallpaper/pornstar34.jpg")
            # image = pygame.image.load("Wallpaper/Tiffany Doll/pornstar390.jpg")
            # image = pygame.image.load("Wallpaper/Lexy Belle/pornstar463.jpg")
            # image = pygame.image.load("Wallpaper/Nikita Bellucci/pornstar293.jpg")
            # image = pygame.image.load("wallpaper/wallpaper1.jpg")
            image = pygame.image.load(image_file)
            *_, img_width, img_height = image.get_rect()

            # print(self.width, self.height, img_width, img_height, flush=True)
            if self.width > img_width:
                self.background = pygame.transform.scale(image, (self.width, self.width*img_height//img_width))
            else:
                self.background = pygame.transform.scale(image, (img_width, img_height))

        except Exception as e:
            print("Error loading background:", e)
            self.background = None

    def close_all_icones(self):
        self.liste_icones.clear()

    def create_icone(self, title, couleur, app, *args):
        trouve = False
        if self.saved_icones_position.get(app.__name__, False):
            self.ico_posX, self.ico_posY = self.saved_icones_position.get(app.__name__)
            icone_position = pygame.Rect(self.ico_posX, self.ico_posY, Icone.ICONE_WIDTH, Icone.ICONE_HEIGHT)
            trouve = icone_position.collidelist([ico.icone_rect for ico in self.liste_icones]) < 0

        while not trouve:
            self.ico_posY += Icone.ICONE_DECAL+Icone.ICONE_HEIGHT
            if self.ico_posY+Icone.ICONE_HEIGHT > self.screen_surf.get_size()[1]:
                self.ico_posX += Icone.ICONE_DECAL+Icone.ICONE_WIDTH
                self.ico_posY = 10
            icone_position = pygame.Rect(self.ico_posX, self.ico_posY, Icone.ICONE_WIDTH, Icone.ICONE_HEIGHT)
            trouve = icone_position.collidelist([ico.icone_rect for ico in self.liste_icones]) < 0

        icone = Icone(self.screen_surf, title, couleur, self.ico_posX, self.ico_posY, app, *args)
        self.liste_icones.append(icone)

    def load_applications(self):
        for une_classe in get_all_classes("Application"):
            libelle, color, *args = une_classe.DEFAULT_CONFIG
            self.create_icone(libelle, color, une_classe, *args)

    def close_all_systray_apps(self):
        # Enregistrement de la base de registre des systrays
        for systray in self.liste_systray:
            # print("check:", systray.DEFAULT_CONFIG[0], end=" = ")
            # print(systray.registre.get_all())
            systray.registre.save_file()

        self.liste_systray.clear()

    def load_systray_apps(self):
        total: int = 0
        classes: list = []
        for une_classe in get_all_classes("SysTray"):
            classes.append(une_classe)

        classes.sort(key=lambda k: k.PRIORITY)
        for une_classe in classes:
            libelle, color, *args = une_classe.DEFAULT_CONFIG
            Variable.window = self.barre_taches

            # calcul de la position de la zone a affecter au SysTray
            width, height = self.barre_taches.get_size()
            sysapp_rect = pygame.Rect(
                width - total - une_classe.INITIAL_WIDTH, 0, 
                une_classe.INITIAL_WIDTH, height)

            # Initialisation dy SysTray
            systray = une_classe(self.barre_taches.subsurface(sysapp_rect), color)
            self.liste_systray.append(systray)
            
            # calcul du decalage de zone pour le prochain SysTray
            total += systray.get_width() + une_classe.TEXT_OFFSET

    def get_systrays_x(self):
        if self.liste_systray:
            return self.liste_systray[-1].get_offset()[0] 
        else:
            return self.barre_taches.get_size()[0]

    def get_systrays_width(self):
        # recupere la taille de la zone contenant tous les systrays
        if self.liste_systray:
            systrays_size = self.barre_taches.get_size()[0] - self.liste_systray[-1].tools.screen.get_offset()[0] 
            return systrays_size
        else:
            return 0

    def update_systray_pos(self):
        total = 0
        for systray in self.liste_systray:
            systray_size = systray.tools.screen.get_size()[0]
            systray_width = systray.get_width()
            if systray_size != systray_width:
                self.update_systrays_positions()
                return

    def open(self, title, couleur, app, *args):
        # Check si la fenetre est unique
        if "UNIQUE" in app.WINDOW_PROPERTIES:
            for fenetre in self.liste_fenetres:
                if fenetre.app == app:
                    self.activate_window(fenetre)
                    return

        self.last_position = self.last_position[0]+self.NEW_WINDOW_DECAL, self.last_position[1]+self.NEW_WINDOW_DECAL
        largeur = self.width//2
        hauteur = self.height//2
        if self.last_position[0]+largeur > self.width or (
           self.last_position[1]+hauteur > self.height-self.TASK_BAR_HEIGHT):
            self.last_position = (self.NEW_WINDOW_DECAL+10, 10)

        if "CENTER" in app.WINDOW_PROPERTIES:
            print(self.width, "x", self.height)
            x = largeur - app.MIN_SIZE[0] // 2
            y = hauteur - app.MIN_SIZE[1] // 2
            fenetre = Window(x, y, largeur, hauteur, title, couleur, app, *args)
        else:
            fenetre = Window(*self.last_position, largeur, hauteur, title, couleur, app, *args)
        
        systrays_width = self.get_systrays_width()
        if len(self.liste_taches) == 0:
            Tache.TASK_WIDTH = Tache.TASK_WIDTH_MAX
        else:
            if (1+len(self.liste_taches))*(Tache.TASK_WIDTH+self.TASK_BAR_DECAL) > \
                self.barre_taches_rect[2] - self.TASK_BAR_MENU_WIDTH - systrays_width:

                Tache.TASK_WIDTH = (self.barre_taches_rect[2] - self.TASK_BAR_MENU_WIDTH - systrays_width) // \
                                   (1+len(self.liste_taches)) - self.TASK_BAR_DECAL
        
        self.resize_taches()
        tache = Tache(self.barre_taches, title, couleur, 
            self.TASK_BAR_MENU_WIDTH+len(self.liste_taches)*(Tache.TASK_WIDTH+self.TASK_BAR_DECAL), fenetre)
        self.liste_taches.append(tache)

        if self.liste_fenetres:
            self.liste_fenetres[-1].active = False
            self.liste_fenetres[-1].set_surface_color()
        self.liste_fenetres.append(fenetre)

        mouse_position = Mouse.get_pos()
        if fenetre.window.collidepoint(mouse_position):
            fenetre.mouse_over = True
            if not fenetre.on_error:
                try:
                    fenetre.instance.mouse_enter(*fenetre.get_mouse_pos())
                except Exception as e:
                    fenetre.set_error()
                    print("mouse_move Error:", e)

    def calculate_tache_position(self, index):
        for i, tache in enumerate(self.liste_taches[index:]):
            tache.set_pos(self.TASK_BAR_MENU_WIDTH+(index+i)*(Tache.TASK_WIDTH+self.TASK_BAR_DECAL))

    def unselect_all_taches(self):
        for tache in self.liste_taches:
            tache.mouse_over = False

    def resize_taches(self):
        self.calculate_tache_position(0)

    def close_tache(self, fenetre):
        for i, tache in enumerate(self.liste_taches):
            if tache.window == fenetre:
                self.liste_taches.pop(i)
                if Tache.TASK_WIDTH < Tache.TASK_WIDTH_MAX:
                    systray_width = self.get_systrays_width()
                    if len(self.liste_taches) == 0:
                        Tache.TASK_WIDTH = Tache.TASK_WIDTH_MAX
                    else:
                        Tache.TASK_WIDTH = min(Tache.TASK_WIDTH_MAX, 
                            (self.barre_taches_rect[2] - self.TASK_BAR_MENU_WIDTH - systray_width) // \
                            len(self.liste_taches) - self.TASK_BAR_DECAL)
                    self.resize_taches()
                else:
                    self.calculate_tache_position(i)
                break

    def close(self, fenetre):
        if fenetre:
            fenetre.close()
            self.close_tache(fenetre)
            self.liste_fenetres.remove(fenetre)
            self.activate_last_window()

    def close_all(self):
        # Fermeture des fenetres
        while self.liste_fenetres:
            self.close(self.liste_fenetres[0])

        # Fermeture des systrays
        self.close_all_systray_apps()

    def show_all_windows(self):
        for f in self.liste_fenetres:
            if f.last_statut() == "MINIMIZED":
                f.statut.pop()
        self.activate_last_window()

    def inactive_all_windows(self):
        for f in self.liste_fenetres:
            f.active = False

    def activate_window(self, fenetre):
        for i, f in enumerate(self.liste_fenetres):
            if f == fenetre:
                if not f.active:
                    f.active = True
                    f.set_surface_color()
                    if f == self.liste_fenetres[-1]:
                        break
                    self.liste_fenetres[-1].active = False
                    self.liste_fenetres[-1].set_surface_color()
                    fen = self.liste_fenetres.pop(i)
                    self.liste_fenetres.append(fen)
                return

    def activate_last_window(self):
        for fen in reversed(self.liste_fenetres):
            if fen.last_statut() != "MINIMIZED":
                self.activate_window(fen)
                return
        self.inactive_all_windows()

    def activate_next_window(self):
        if self.liste_fenetres:
            fenetre_active = self.get_active_window()
            for fenetre in self.liste_fenetres:
                if fenetre != fenetre_active:
                    if fenetre.last_statut() != "MINIMIZED":
                        self.activate_window(fenetre)
                        break

    def load_icones(self):
        contenu = {}
        self.saved_icones_position = {}
        try:
            with open('desktop.json') as file_handle:
                contenu = json.loads(file_handle.read())
                for code_application, donnees in contenu.items():
                    if donnees.get("position"):
                        self.saved_icones_position[code_application] = donnees["position"]

        except Exception as e:
            print("load_icones Error:", e)

    def save_icones(self):
        contenu = {}
        try:
            with open('desktop.json', 'w') as file_handle:
                for icone in self.liste_icones:
                    contenu[icone.app.__name__] = {}
                    contenu[icone.app.__name__]["libelle"] = icone.title
                    contenu[icone.app.__name__]["position"] = icone.dest_rect.topleft
                    
                file_handle.write(json.dumps(contenu, indent=4))
        except Exception as e:
            print("save_icones Error:", e)

        # Sauvegarde de la base de registre de l'OS
        self.registre.save_file()
    
    def get_icone_mouse_over(self):
        for icone in self.liste_icones:
            if icone.mouse_over:
                return icone
        return None

    def get_systray_mouse_over(self):
        for systray in self.liste_systray:
            if systray.mouse_over:
                return systray
        return None

    def get_tache_mouse_over(self):
        for tache in self.liste_taches:
            if tache.mouse_over:
                return tache
        return None

    def get_active_window(self):
        for f in reversed(self.liste_fenetres):
            if f.active and f.last_statut() != "MINIMIZED":
                return f
        return None

    def get_systrays_actions(self):
        for systray in self.liste_systray:
            systray_action = systray.get_action()

            if isinstance(systray_action, tuple):
                systray_action, callback = systray_action
            else:
                callback = None

            if systray_action is None:
                continue

            match systray_action.split(":"):
                case ["CHANGE_THEME", new_theme]:
                    Theme.set_theme(new_theme)
                    self.update_theme()

                case ["UPDATE", "SYSTRAYS"]:
                    self.update_systray_pos()
                    if callback:
                        callback()

    def get_windows_actions(self):
        for fenetre in self.liste_fenetres:
            if not fenetre.on_error and fenetre.instance.get_action() is not None:
                for action in fenetre.instance.get_action().split(";"):
                    match action.split(":"):
                        case ["QUIT"]:
                            self.close(fenetre)
                        case ["SET", "WALLPAPER", filename]:
                            self.registre.save("Wallpaper", filename)
                            self.load_background_image()

    def check_keyboard_events(self):
        return

        if not Keyboard.keypressed():
            return

        if not self.liste_fenetres:
            event_key = Keyboard.get_key()
            if event_key == pygame.K_ESCAPE:
                self.running = False
        else:
            if self.get_active_window():
                event_key = Keyboard.view_last_key()
            else:
                event_key = Keyboard.get_key()

            if event_key == pygame.K_k:
                self.close(self.get_active_window())
    
            elif event_key == pygame.K_TAB:
                self.activate_next_window()

            elif event_key == pygame.K_SPACE:
                if not self.get_active_window():
                    self.show_all_windows()

    def keypressed(self, event):
        fenetre = self.get_active_window()
        if fenetre:
            fenetre.instance.keypressed(event)

    def keyreleased(self, event):
        # print(f"os.keyreleased({event.key})", flush=True)
        fenetre = self.get_active_window()
        if event.key == pygame.K_ESCAPE and not fenetre:
            self.running = False

        elif event.key == pygame.K_TAB:
            Keyboard.get_key()
            self.activate_next_window()

        elif fenetre:
            fenetre.instance.keyreleased(event)

    def update(self):
        # diminution de 33.33% de la puissance allouee aux fenetres non actives
        self.tick = 0 if (self.tick > 1000000) else self.tick+1
        self.active_time = self.tick % 3

        # fenetre ouverte non minimisee
        for fenetre in self.liste_fenetres:
            if self.active_time or fenetre.active:
                fenetre.update()

        # Barre des tache avec ses taches
        for tache in self.liste_taches:
            tache.update()

        # Barre de tache avec ses SysTray
        for systray in self.liste_systray:
            systray.update()

    def draw(self):
        # Fond d'ecran
        if self.background:
            self.screen_surf.blit(self.background, (0, 0))
        else:
            self.screen_surf.fill((30, 30, 30))

        # icone sur le bureau
        for icone in self.liste_icones:
            if icone != self.get_icone_mouse_over():
                icone.draw()
        if self.get_icone_mouse_over():
            self.get_icone_mouse_over().draw()

        # fenetre ouverte non minimisee
        for fenetre in self.liste_fenetres:
            fenetre.draw(self.screen_surf)

        # Barre de tache avec ses taches
        self.barre_taches.fill(OperatingSystem.TASK_BAR_COLOR)
        for tache in self.liste_taches:
            tache.draw()

        # Barre de tache avec ses SysTray
        for systray in self.liste_systray:
            systray.draw()
            # print(systray.registre.get_all(), flush=True)

        pygame.display.update()
        self.clock.tick(60)  # Limit the frame rate to 60 FPS.

    def mouse_button_down(self, mouse_position, mouse_button):
        window_spotted = False
        Mouse.left_button_down = True
        self.icone_catched_by_mouse = None
        self.resize_window = None
        Mouse.set_pos(mouse_position) 
        Mouse.save_pos()

        if self.liste_fenetres:
            for fen in reversed(self.liste_fenetres):
                if fen.last_statut() != "MINIMIZED" and fen.window.collidepoint(Mouse.get_pos()):
                    window_spotted = True
                    self.activate_window(fen)
                    if not fen.on_error and fen.window_draw.collidepoint(Mouse.get_pos()):
                        fen.instance.mouse_button_down(*fen.get_mouse_pos(), mouse_button)
                    break
            if not self.get_active_window():
                Mouse.left_button_down = False
            else:
                if Mouse.cursor_over in ("LEFT", "BOTTOM", "RIGHT"):
                    self.window_catch_by_mouse = self.get_active_window()
                else:
                    Mouse.left_button_down = (
                        self.get_active_window().last_statut() != "MINIMIZED" and 
                        self.get_active_window().title_rect.collidepoint(Mouse.get_pos()))
                    if Mouse.left_button_down:
                        # self.get_active_window().window_surf.set_alpha(220)
                        pass

        if not window_spotted and self.liste_icones:
            self.icone_catched_by_mouse = self.get_icone_mouse_over()

    def mouse_button_up(self, mouse_position, mouse_button):
        Mouse.left_button_down = False
        Mouse.right_button_down = False
        self.window_catch_by_mouse = None
        Mouse.click()
        if self.icone_catched_by_mouse:
            # Gestion deplacement icone du bureau
            self.icone_catched_by_mouse.move_ip(*self.icone_catched_by_mouse.dest_rect[:2])
            self.icone_catched_by_mouse = None

        if self.barre_taches_rect.collidepoint(mouse_position):
            # La souris se trouve dans la barre de taches
            systray = self.get_systray_mouse_over()
            if systray:
                systray_rect = systray.tools.screen.get_rect().move(systray.tools.screen.get_abs_offset())
                if systray_rect.collidepoint(mouse_position) and (
                   systray_rect.collidepoint(Mouse.get_saved_pos())):
                    systray.mouse_up()
                    # update all systrays position if necessary
                    # self.update_systray_pos()
            else:
                # Gestion click tache dans barre des taches
                tache = self.get_tache_mouse_over()
                if tache:
                    if tache.tache_rect.collidepoint((mouse_position[0], mouse_position[1]-self.barre_taches_rect[1])) and (
                       tache.tache_rect.collidepoint((Mouse.get_saved_pos()[0], Mouse.get_saved_pos()[1]-self.barre_taches_rect[1]))):
                        if tache.window.last_statut() == "MINIMIZED":
                            tache.window.statut.pop()
                            self.activate_window(tache.window)
                        elif tache.window.active:
                            tache.window.minimize()
                            self.activate_last_window()
                        else:
                            self.activate_window(tache.window)

        else:
            # La souris se trouve sur le bureau
            window_spotted = False
            fen_active = self.get_active_window()
            if fen_active:
                fen_active.window_surf.set_alpha(255)
                # Click sur partie haute de la fenetre
                if fen_active.top_rect.collidepoint(Mouse.get_saved_pos()) and (
                   fen_active.top_rect.collidepoint(mouse_position)):
                    # Click sur btn Fermer
                    if fen_active.close_rect.collidepoint(Mouse.get_saved_pos()) and (
                       fen_active.close_rect.collidepoint(mouse_position)):
                        self.close(fen_active)
                        window_spotted = True
                    # Click sur btn Minimiser
                    elif fen_active.min_rect.collidepoint(Mouse.get_saved_pos()) and (
                         fen_active.min_rect.collidepoint(mouse_position)):
                        fen_active.minimize()
                        self.activate_last_window()
                        window_spotted = True
                    elif "RESIZABLE" in fen_active.properties:
                        # Click sur btn Maximiser
                        if (fen_active.max_rect.collidepoint(Mouse.get_saved_pos())) and (
                            fen_active.max_rect.collidepoint(mouse_position)):
                            window_spotted = True
                            if fen_active.last_statut() == "MAXIMIZED":
                                fen_active.restaure()
                            else:
                                fen_active.maximize()
                        # Dbl Click
                        elif Mouse.has_double_clicked() and Mouse.get_saved_pos() == mouse_position:
                            window_spotted = True
                            if fen_active.last_statut() == "MAXIMIZED":
                                fen_active.restaure()
                            else:
                                fen_active.maximize()
                                
                # Click a l'interieur de la fenetre
                elif fen_active.window_draw.collidepoint(Mouse.get_saved_pos()) and (
                     fen_active.window_draw.collidepoint(mouse_position)):
                    window_spotted = True
                    if not fen_active.on_error:
                        fen_active.instance.mouse_button_up(*fen_active.get_mouse_pos(), mouse_button)

            if not window_spotted:
                # Gestion du double-click d'un icone du bureau
                icone = self.get_icone_mouse_over()
                if icone and Mouse.has_double_clicked():
                    self.open(icone.title, icone.couleur, icone.app, *icone.args)

        Mouse.set_pos(mouse_position)

    def mouse_wheel(self, dx, dy):
        fen_active = self.get_active_window()
        if fen_active:
            fen_active.instance.mouse_wheel(dx, dy)

    def mouse_move(self, mouse_position):
        window_spotted = False
        mx, my = Mouse.get_pos()
        if self.icone_catched_by_mouse:
            # deplacement des icones du bureau
            self.icone_catched_by_mouse.move(mouse_position[0]-mx, mouse_position[1]-my, self.liste_icones)

        elif self.get_active_window() and not self.barre_taches_rect.collidepoint(mouse_position):
            # la souris n'est pas dans la barre de tache
            if Mouse.left_button_down and self.window_catch_by_mouse:
                # redimensionnement de la fenetre active
                self.get_active_window().resize(Mouse.cursor_over,
                    mouse_position[0]-mx, mouse_position[1]-my)

            elif Mouse.left_button_down and self.get_active_window().last_statut() != "MINIMIZED":
                # deplacement de la fenetre active
                if self.get_active_window().window_surf.get_alpha() != 220:
                    self.get_active_window().window_surf.set_alpha(220)
                    
                self.get_active_window().move(mouse_position[0]-mx, mouse_position[1]-my)

            elif not Mouse.left_button_down:
                # Execution des methodes : mouse_enter, mouse_exit et mouse_move dans les instances
                self.mouse_enter_leave(False)
                for fenetre in reversed(self.liste_fenetres):
                    if fenetre.last_statut() != "MINIMIZED":
                        if not window_spotted and fenetre.window.collidepoint(mouse_position):
                            if not fenetre.mouse_over:
                                fenetre.mouse_over = True
                                if not fenetre.on_error:
                                    fenetre.instance.mouse_enter(*fenetre.get_mouse_pos())
                            window_spotted = True
                            if fenetre.top_rect.collidepoint(mouse_position):
                                if fenetre.min_rect.collidepoint(mouse_position):
                                    Mouse.cursor_over = "MIN"
                                    fenetre.min_surf.fill((70, 190, 220))
                                    pygame.draw.rect(fenetre.min_surf, (0, 0, 0), (10, 11, 11, 2), 1)
                                elif "RESIZABLE" in fenetre.properties and fenetre.max_rect.collidepoint(mouse_position):
                                    Mouse.cursor_over = "MAX"
                                    fenetre.max_surf.fill((70, 190, 220))
                                    pygame.draw.rect(fenetre.max_surf, (0, 0, 0), (10, 8, 11, 5), 1)
                                    pygame.draw.rect(fenetre.max_surf, (0, 0, 0), (11, 9, 9, 3), 1)
                                    if fenetre.last_statut() == "MAXIMIZED":
                                        pygame.draw.line(fenetre.max_surf, (0, 0, 0), (8, 14), (18, 14), 1)
                                        pygame.draw.line(fenetre.max_surf, (0, 0, 0), (8, 10), (8, 14), 1)

                                elif fenetre.close_rect.collidepoint(mouse_position):
                                    Mouse.cursor_over = "CLOSE"
                                    fenetre.close_surf.fill((240, 90, 90))
                                    pygame.draw.line(fenetre.close_surf, (0, 0, 0), (12, 7), (19, 13), 3)
                                    pygame.draw.line(fenetre.close_surf, (0, 0, 0), (12, 13), (19, 7), 3)

                            elif "RESIZABLE" in fenetre.properties:
                                if fenetre.bottom_rect.collidepoint(mouse_position):
                                    Mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
                                    Mouse.cursor_over = "BOTTOM"
                                elif fenetre.left_rect.collidepoint(mouse_position):
                                    Mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
                                    Mouse.cursor_over = "LEFT"
                                elif fenetre.right_rect.collidepoint(mouse_position):
                                    Mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
                                    Mouse.cursor_over = "RIGHT"

                            if fenetre.window_draw.collidepoint(mouse_position):
                                # curseur dans la fenetre pour l'application
                                if not fenetre.on_error:
                                    try:
                                        fenetre.instance.mouse_move(*fenetre.get_mouse_pos())
                                    except Exception as e:
                                        fenetre.set_error()
                                        print("move_mouse Error:", e)

                        else:
                            if fenetre.mouse_over:
                                fenetre.mouse_over = False
                                if not fenetre.on_error:
                                    fenetre.instance.mouse_exit()
        
        if not Mouse.left_button_down:

            # Gestion des taches dans la barre de tache
            if self.barre_taches_rect.collidepoint(mouse_position):
                # Mouse_Exit() sur toutes les fenetre en ayant besoin
                for fenetre in reversed(self.liste_fenetres):
                    if fenetre.mouse_over:
                        fenetre.mouse_over = False
                        if not fenetre.on_error:
                            fenetre.instance.mouse_exit()

                # Recherche systray sous curseur
                if self.liste_systray:
                    over_systray = False
                    rect = self.liste_systray[-1].tools.screen.get_offset()
                    systrays_rect = pygame.Rect(
                        rect[0], 
                        self.barre_taches_rect[1], 
                        self.barre_taches_rect[2]-rect[0], 
                        self.TASK_BAR_HEIGHT)

                    if systrays_rect.collidepoint(mouse_position):
                        over_systray = True
                        for systray in self.liste_systray:
                            systray_rect = pygame.Rect(systray.tools.screen.get_offset()+systray.tools.screen.get_size())
                            if systray_rect.collidepoint((mouse_position[0], 0)):
                                systray.mouse_over = True
                                systray.mouse_move()
                            else:
                                systray.mouse_over = False

                if not over_systray:
                    # Recherche tache sous curseur
                    for tache in self.liste_taches:
                        if tache.tache_rect.collidepoint((mouse_position[0], mouse_position[1]-self.barre_taches_rect[1])):
                            tache.mouse_over = True
                        else:
                            tache.mouse_over = False

            else:
                # Gestion des icones sur le bureau
                self.unselect_all_taches()
                for icone in self.liste_icones:
                    if not window_spotted and icone.icone_rect.collidepoint(mouse_position):
                        icone.mouse_over = True
                    else:
                        icone.mouse_over = False

        Mouse.set_pos(mouse_position)

    def mouse_enter_leave(self, check_mouse_over=True):
        Mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        Mouse.cursor_over = None
        self.unselect_all_taches()
        for fenetre in reversed(self.liste_fenetres):
            fenetre.set_win_buttons_surface_color()
            if check_mouse_over and fenetre.mouse_over:
                fenetre.mouse_over = False
                if not fenetre.on_error:
                    fenetre.instance.mouse_exit()

        for systray in self.liste_systray:
            systray.mouse_over = False

    def get_pygame_events(self):

        for event in pygame.event.get():
            if event.type == pygame.KMOD_LGUI:
                self.mouse_move(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 2:
                    self.mouse_button_down(event.pos, event.button)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_up(event.pos, event.button)

            elif event.type == pygame.MOUSEWHEEL:
                self.mouse_wheel(event.x, event.y)

            elif event.type == pygame.KEYDOWN:
                self.keypressed(event)

            elif event.type == pygame.KEYUP:
                Keyboard.add_key_to_buffer(event.key)
                self.keyreleased(event)

            elif event.type in (pygame.AUDIO_S16, pygame.WINDOWENTER, pygame.ACTIVEEVENT):
                self.mouse_enter_leave()

            elif event.type in (
                    pygame.WINDOWMAXIMIZED, 
                    pygame.WINDOWRESTORED,
                    pygame.VIDEORESIZE):
                self.update_screen()

            elif event.type == pygame.QUIT:
                self.running = False

            else:
                # print(event.type, get_pygame_const_name(event.type))
                pass

    def run(self):
        self.load_icones()
        self.load_applications()
        self.load_systray_apps()

        while self.running:
            self.get_systrays_actions()
            self.get_windows_actions()
            self.check_keyboard_events()
            self.update()
            self.draw()
            self.get_pygame_events()

        self.close_all()
        self.save_icones()
        pygame.quit()


if __name__ == "__main__":
    my_os = OperatingSystem()
    my_os.run()
