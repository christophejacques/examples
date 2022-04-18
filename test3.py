import pygame


def get_pygame_type_name(index):
    for constante in dir(pygame):
        if constante[0] in "AZERTYUIOPMLKJHGFDSQWXCVBN":
            if getattr(pygame, constante) == index:
                return constante


class VAR:
    running = True


def Quitter(*args):
    VAR.running = False


def mouse_button_up(event, *args):
    if event.button == 1:
        print(event, args)


def exec_keyup(event):
    if event.key == pygame.K_ESCAPE:
        VAR.running = False


fonctions = {
    pygame.KEYDOWN: {},
    pygame.KEYUP: {
        "EXEC": exec_keyup,
    },
    pygame.MOUSEBUTTONDOWN: {},
    pygame.MOUSEBUTTONUP: {
        "EXEC": mouse_button_up,
    },
    pygame.KMOD_LGUI: {},
    pygame.ACTIVEEVENT: {},
    pygame.AUDIO_S8: {},
    pygame.AUDIO_S16: {},
    pygame.TEXTEDITING: {},
    pygame.VIDEOEXPOSE: {},
    pygame.WINDOWCLOSE: {},
    pygame.WINDOWFOCUSGAINED: {},
    pygame.WINDOWENTER: {},
    pygame.WINDOWFOCUSLOST: {},
    pygame.WINDOWMINIMIZED: {},
    pygame.WINDOWMOVED: {},
    pygame.WINDOWRESTORED: {},
    pygame.WINDOWSHOWN: {},
    pygame.QUIT: {
        "EXEC": Quitter,
    },
}


screen = pygame.display.set_mode((400, 200), flags=0)
pygame.display.set_caption("Dico pour event pygame")

while VAR.running:
    for event in pygame.event.get():
        fonction = fonctions.get(event.type, None)
        if fonction is not None:
            if fonction.get("EXEC"):
                fonction["EXEC"](event)
        else:
            print(get_pygame_type_name(event.type))

pygame.quit()
