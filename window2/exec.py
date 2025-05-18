import pygame
import traceback

from mouse import Mouse
from audio import Audio
from keyboard import Keyboard
from classes import Tools, Variable



def get_pygame_const_name(index):
    for c in dir(pygame):
        if c[1] in "AZERTYUIOPMLKJHGFDSQWXCVBN":
            if type(getattr(pygame, c)) == int and getattr(pygame, c) == index:
                return c


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


class Window:

    ICONE_WIDTH = 30
    ICONE_HEIGHT = 20
    WINDOW_BORDER_SIZE = 5

    THEME_ACTIVE_COLOR = (10, 130, 170, 50)
    THEME_INACTIVE_COLOR = (130, 130, 150, 50)
    THEME_ERROR_COLOR = (200, 20, 20)

    def __init__(self, full_screen, x, y, w, h, text, colour, app, *args):
        self.app = app
        self.full_screen = full_screen
        self.sound_id = None
        self.active = True
        self.mouse_over = False
        self.properties = self.app.WINDOW_PROPERTIES
        sound_property = self.search_for_in("SOUND", self.properties)
        if sound_property:
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
        self.tools = Tools(full_screen)

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

        self.window_surf = self.full_screen
        self.window_draw_surf = self.window_surf
        self.window_draw_surf.fill(self.colour)

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
        pass

    def set_win_buttons_surface_color(self):
        pass

    def set_title(self, title):
        self.title = title
        pygame.display.set_caption(title)

    def set_error(self):
        self.on_error = True

    def theme_color(self, active_color=THEME_ACTIVE_COLOR, inactive_color=THEME_INACTIVE_COLOR, check_error=False):
        return active_color

    def last_statut(self):
        return None

    def keypressed(self):
        if self.active:
            return Keyboard.keypressed()
        else:
            return False

    def clear_key_buffer(self):
        if self.active:
            return Keyboard.clear_buffer()

    def get_key(self):
        if self.active:
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
        pass

    def minimize(self):
        pass

    def maximize(self):
        pass

    def move(self, x=0, y=0):
        pass

    def resize(self, direction, dx=0, dy=0, width=None, height=None):
        self.instance.resize(self.instance.tools.screen)

    def update(self):
        pass

    def draw(self, screen_surf):
        pass

    def close(self):
        pass


def run(application):
    pygame.init()
    running = True
    
    screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)
    window = Window(screen, 0, 0, 1200, 600, "", (0, 0, 0), application, *application.DEFAULT_CONFIG[2:])
    
    instance = window.instance
    
    while running:
        pygame.time.Clock().tick(60)
        instance.update()
        instance.draw()

        for action in instance.get_action().split(";"):
            match action:
                case "QUIT":
                    instance.registre.save_file()
                    running = False

        pygame.display.update()
        for event in pygame.event.get():
            # print(event, get_pygame_const_name(event.type), flush=True)

            if event.type == pygame.KEYDOWN:
                instance.keypressed(event)

            elif event.type == pygame.KEYUP:
                Keyboard.add_key_to_buffer(event.key)
                instance.keyreleased(event)

            elif event.type == pygame.TEXTINPUT:
                pass

            elif event.type == pygame.KMOD_LGUI:
                Mouse.set_pos(event.pos)
                instance.mouse_move(*Mouse.get_pos())

            elif event.type == pygame.MOUSEWHEEL:
                instance.mouse_wheel(event.x, event.y)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                Mouse.set_pos(event.pos) 
                Mouse.save_pos()
                instance.mouse_button_down(*event.pos, event.button)
                # instance.mouse_button_down(*window.get_mouse_pos(), event.button)

            elif event.type == pygame.MOUSEBUTTONUP:
                instance.mouse_button_up(*event.pos, event.button)

            elif event.type == pygame.WINDOWENTER:
                instance.mouse_enter(0, 0)

            elif event.type == pygame.ACTIVEEVENT:
                if event.gain == 0:
                    instance.mouse_exit()

            elif event.type == pygame.QUIT:
                running = False
                instance.registre.save_file()
                instance.close()

            elif event.type in (
                    pygame.TEXTEDITING,
                    pygame.AUDIODEVICEADDED, 
                    pygame.AUDIO_S8, 
                    pygame.AUDIO_S16,
                    pygame.JOYDEVICEADDED,
                    pygame.WINDOWSHOWN,
                    pygame.WINDOWFOCUSGAINED,
                    pygame.WINDOWMOVED,
                    pygame.WINDOWRESIZED,
                    pygame.WINDOWMAXIMIZED,
                    pygame.WINDOWRESTORED,
                    pygame.WINDOWCLOSE,
                    pygame.WINDOWSIZECHANGED,
                    pygame.VIDEOEXPOSE):
                pass

            elif event.type == pygame.VIDEORESIZE:
                instance.resize(screen)

            else:
                print(event.type, get_pygame_const_name(event.type), flush=True)

    pygame.quit()
