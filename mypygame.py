import pygame


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


def get_pygame_type_name(index):
    for constante in dir(pygame):
        if constante[0] in "AZERTYUIOPMLKJHGFDSQWXCVBN":
            if getattr(pygame, constante) == index:
                return constante


class VAR:
    running = True


def Quitter(*args):
    fprint(args)
    VAR.running = False


def mouse_move(event):
    fprint(event)


def mouse_button_up(event):
    if event.button == 1:
        pass
    fprint(event)


def exec_keyup(event):
    if event.key == pygame.K_ESCAPE:
        Quitter(event)
    else:
        fprint(event)


event2fonction = {
    pygame.KEYDOWN: 0,
    pygame.KEYUP: exec_keyup,
    pygame.MOUSEBUTTONDOWN: 0,
    pygame.MOUSEBUTTONUP: mouse_button_up,
    pygame.TEXTINPUT: 0,
    pygame.KMOD_LGUI: mouse_move,
    pygame.ACTIVEEVENT: 0,
    pygame.AUDIO_S8: 0,
    pygame.AUDIO_S16: 0,
    pygame.TEXTEDITING: 0,
    pygame.VIDEOEXPOSE: 0,
    pygame.WINDOWCLOSE: 0,
    pygame.WINDOWFOCUSGAINED: 0,
    pygame.WINDOWENTER: 0,
    pygame.WINDOWFOCUSLOST: 0,
    pygame.WINDOWMINIMIZED: 0,
    pygame.WINDOWMOVED: 0,
    pygame.WINDOWRESTORED: 0,
    pygame.WINDOWSHOWN: 0,
    pygame.QUIT: Quitter,
}


screen = pygame.display.set_mode((400, 200), flags=0)
pygame.display.set_caption("Dico pour event pygame")

while VAR.running:
    for event in pygame.event.get():
        # fonction = fonctions.get(event.type, None)
        fonction = event2fonction.get(event.type, None)
        if fonction is not None:
            if callable(fonction):
                fonction(event)
        else:
            fprint(get_pygame_type_name(event.type))

pygame.quit()
