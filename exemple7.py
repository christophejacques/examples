import pygame

from functools import partial
from typing import Optional, Callable, Tuple


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


class Constante:

    FONT22: pygame.font.Font

    @classmethod
    def __init__(cls):
        pygame.init()
        cls.FONT22 = pygame.font.SysFont("arial", 18)

    @classmethod
    def close(cls):
        pygame.quit()


class Commande:

    callback: Callable

    def __init__(self, label: str, callback: Callable, *params, **kwparams):

        self.label = label
        self.callback = partial(callback, *params, *kwparams)

        self.surface = Constante.FONT22.render(label, False, (40, 40, 200))
        self.width, self.height = self.surface.get_size()


class Bouton:

    def __init__(self, screen: pygame.surface.Surface, 
            back_color: Tuple, coords: Tuple, commande: Commande):
        self.screen = screen

        self.mouse_over = False
        self.mouse_button_pushed = False
        self.commande = commande

        self.back_color = back_color
        self.actual_back_color = self.back_color
        self.color_light = 3*(200,)
        self.color_shadow = 3*(0,)

        self.set_coords(coords)

    def set_coords(self, coords: Tuple):
        self.coords = pygame.Rect(*coords)

        self.coords_h1 = coords[:2], (coords[0]+coords[2], coords[1])
        self.coords_h2 = (coords[0], coords[1]+coords[3]), (coords[0]+coords[2], coords[1]+coords[3])

        self.coords_v1 = coords[:2], (coords[0], coords[1]+coords[3])
        self.coords_v2 = (coords[0]+coords[2], coords[1]), (coords[0]+coords[2], coords[1]+coords[3])

        self.texte_coords = (
            self.coords.x + (self.coords.width//2) - self.commande.width//2, 
            self.coords.y + (self.coords.height//2) - self.commande.height//2)

    def clicked(self):
        fprint("Commande:", self.commande.label)
        self.commande.callback()

    def mouse_button_down(self):
        self.mouse_button_pushed = self.mouse_over

        if self.mouse_button_pushed:
            self.color_light = 3*(0,)
            self.color_shadow = 3*(200,)
        else:
            self.color_light = 3*(200,)
            self.color_shadow = 3*(0,)

    def mouse_button_up(self):
        if self.mouse_button_pushed and self.mouse_over:
            self.clicked()
        self.mouse_button_pushed = False

        self.color_light = 3*(200,)
        self.color_shadow = 3*(0,)

    def mouse_move(self, position: Tuple):
        if self.coords.collidepoint(position):
            self.mouse_over = True
            self.actual_back_color = tuple(
                min(255, int(color*1.2)) for color in self.back_color)
        else:
            self.mouse_over = False
            self.actual_back_color = self.back_color
            
    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.screen, self.actual_back_color, self.coords)

        pygame.draw.line(self.screen, self.color_light, *self.coords_h1, 2)
        pygame.draw.line(self.screen, self.color_light, *self.coords_v1, 2)

        pygame.draw.line(self.screen, self.color_shadow, *self.coords_h2, 2)
        pygame.draw.line(self.screen, self.color_shadow, *self.coords_v2, 2)

        self.screen.blit(self.commande.surface, self.texte_coords)


class MessageBox:

    def __init__(self, screen: pygame.surface.Surface, size: Tuple):
        self.screen = screen
        self.is_open = True

        largeur_box, hauteur_box = size
        width, height = screen.get_size()
        self.coords = (width//2 - largeur_box//2, 
            height//2 - hauteur_box//2, largeur_box, hauteur_box)

        self.coords_white = (self.coords[0]+10, self.coords[1]+10, 
            self.coords[2]-20, self.coords[3]-80)
        self.coords_lineh1 = (self.coords_white[0], self.coords_white[1]), (
            self.coords_white[0]+self.coords_white[2], 
            self.coords_white[1])
        self.coords_lineh2 = (self.coords_white[0], 
            self.coords_white[1]+self.coords_white[3]), (
            self.coords_white[0]+self.coords_white[2], 
            self.coords_white[1]+self.coords_white[3])

        self.coords_linev1 = (self.coords_white[0], self.coords_white[1]), (
            self.coords_white[0], 
            self.coords_white[1]+self.coords_white[3])
        self.coords_linev2 = (
            self.coords_white[0]+self.coords_white[2], 
            self.coords_white[1]), (
            self.coords_white[0]+self.coords_white[2], 
            self.coords_white[1]+self.coords_white[3])

        self.boutons: list = list()

        footer_hauteur = self.coords[1] + self.coords[3] - self.coords_lineh2[0][1]
        largeur = 120
        hauteur = 34
        coods_btn = (self.coords[0] - largeur//2 + self.coords[2]//4,
            self.coords_lineh2[0][1] + footer_hauteur//2 - hauteur//2,
            largeur, hauteur)

        self.boutons.append(Bouton(self.screen, 3*(160,), coods_btn, 
            Commande("Annuler", self.close)))

        coods_btn = (self.coords[0] - largeur//2 + 3*self.coords[2]//4,
            self.coords_lineh2[0][1] + footer_hauteur//2 - hauteur//2,
            largeur, hauteur)

        self.boutons.append(Bouton(self.screen, (200, 160, 160), coods_btn, 
            Commande("Valider", self.close)))

    def close(self):
        self.is_open = False

    def mouse_move(self, position: tuple):
        for bouton in self.boutons:
            bouton.mouse_move(position)

    def mouse_button_down(self):
        for bouton in self.boutons:
            bouton.mouse_button_down()

    def mouse_button_up(self):
        for bouton in self.boutons:
            bouton.mouse_button_up()

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.screen, (150, 150, 150), self.coords)
        pygame.draw.rect(self.screen, (240, 240, 240), self.coords_white)

        pygame.draw.line(self.screen, (0, 0, 0), *self.coords_lineh1, 2)
        pygame.draw.line(self.screen, (0, 0, 0), *self.coords_linev1, 2)
        pygame.draw.line(self.screen, 3*(200,), *self.coords_lineh2, 2)
        pygame.draw.line(self.screen, 3*(200,), *self.coords_linev2, 2)

        [bouton.draw() for bouton in self.boutons]


def main():
    running = True
    Constante()

    screen = pygame.display.set_mode((800, 600), flags=pygame.SHOWN, vsync=1)
    clock = pygame.time.Clock()
    msg = MessageBox(screen, (400, 200))

    while msg.is_open and running:
        screen.fill((40, 40, 40))
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.KMOD_LGUI:
                msg.mouse_move(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                msg.mouse_button_down()

            elif event.type == pygame.MOUSEBUTTONUP:
                msg.mouse_button_up()

            elif event.type == pygame.QUIT:
                running = False

            # else:
            #     fprint(event)

        msg.draw()
        pygame.display.update()

    Constante.close()


if __name__ == '__main__':
    main()
