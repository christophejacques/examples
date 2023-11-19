from referentiel import pygame
from referentiel import black, light_grey, white, green, random_color

from window import Window
from zone import Zone
from objets import Graphical_Text, Lignes, StarField


def get_pygame_const_name(index) -> str:
    for c in dir(pygame):
        if c[1] in "AZERTYUIOPMLKJHGFDSQWXCVBN":
            if type(getattr(pygame, c)) == int and getattr(pygame, c) == index:
                return c
    return ""


def Quit() -> None:
    global Application_launched
    Application_launched = False


def key_pressed(key_code, key_mode=None) -> None:
    global Application_launched
    global Playing_music

    if key_mode == pygame.KMOD_LALT and key_code == pygame.K_F4 or key_code == pygame.K_ESCAPE:
        Quit()

    elif key_code == pygame.K_n:
        if pygame.mixer_music.get_busy():
            pygame.mixer_music.stop()

    elif key_code == pygame.K_p:
        if pygame.mixer_music.get_busy():
            Playing_music = False
            music.set_texte("Press 'p' to play music")
            pygame.mixer_music.pause()
        else:
            Playing_music = True
            music.set_texte("Press 'p' to stop music")
            if pygame.mixer_music.get_pos() > 0:
                pygame.mixer_music.unpause()
            else:
                pygame.mixer_music.play()
        music.calcul_position()

    elif key_code == pygame.K_KP1:
        # Active/desactive Lignes
        win.get_zone("lignes").active = not win.get_zone("lignes").active
        win.optimize()

    elif key_code == pygame.K_KP2:
        # Active/desactive Etoiles
        win.get_zone("étoiles").active = not win.get_zone("étoiles").active
        win.optimize()

    elif key_code == pygame.K_KP3:
        # Active/desactive Textes
        win.get_zone("textes").active = not win.get_zone("textes").active
        win.optimize()

    elif key_code == pygame.K_SPACE:
        if pygame.mixer_music.get_busy():
            pygame.mixer_music.rewind()

    elif key_code == pygame.K_KP_MINUS:
        win.get_zone("Fichier").active = False
        if ballet.maximum > 10:
            ballet.maximum -= 10
        if etoiles.maximum > 10:
            etoiles.maximum -= 10

    elif key_code == "fichier":
        match key_mode:
            case "swap":
                win.get_zone("Fichier").active = not win.get_zone("Fichier").active
            case "show":
                win.get_zone("Fichier").active = True
            case "hide":
                win.get_zone("Fichier").active = False
            case "hide_Menu":
                position = win.mouse
                zone = win.get_zone("menu")
                if not position.in_zone(zone.objets[0].zone):
                    win.get_zone("Fichier").active = False

    elif key_code == pygame.K_KP_PLUS:
        win.get_zone("Fichier").active = False
        ballet.maximum += 10
        etoiles.maximum += 10


def execute_commands(cmds: list[str]) -> None:
    for cmd in cmds:
        try:
            eval(cmd)
        except Exception as e:
            print(f"Commande *{cmd}* inconnue !")
            print("Error:", e)


clock = pygame.time.Clock()

# defini le USEREVENT devant se produire toutes les 500ms
pygame.time.set_timer(pygame.USEREVENT, 500)

pygame.display.set_caption("Démo de l'utilisation du module pygame")
# window_size: tuple[int, int] = pygame.display.get_desktop_sizes()[0]
window_size: tuple[int, int] = (1750, 900)

zballet = Zone(black)
# zetoile = Zone(black)
zetoile = Zone((0, 3, 0))
ztextes = Zone((10, 10, 100))
zmenus = Zone((64, 64, 64))
zmenu1 = Zone((64, 64, 64))

screen = pygame.display.set_mode(window_size, flags=pygame.RESIZABLE, display=0)
# screen = pygame.display.set_mode(window_size, flags=pygame.NOFRAME)  # , depth=8)

win = Window(screen, black, ((0, 0), window_size))

# MUSIC_END_EVENT = pygame.USEREVENT+1
MUSIC_END_EVENT = pygame.event.custom_type()
try:
    pygame.mixer.music.set_endevent(MUSIC_END_EVENT)
    sound_filename = win.sound_directory.next_file().path
    pygame.mixer_music.load(sound_filename)
except Exception:
    print("Error loading music")

win.add("menu", zmenus, {"bottom": "22"})

win.add("textes", ztextes, {
    "left": "0",
    "top": "height-80",
    "right": "width"})
win.add("lignes", zballet, {
    "left": "0",
    "top": "fbottom('menu')",
    "right": "iif(fisactive('étoiles'), width*0.5, width)",
    "bottom": "iif(ftop('textes')==0, height, ftop('textes'))"})
win.add("étoiles", zetoile, {
    "left": "fright('lignes')",
    "bottom": "iif(ftop('textes')==0, height, ftop('textes'))",
    "top": "fbottom('menu')"})
win.add("Fichier", zmenu1, {
    "left": "fleft('menu')",
    "top": "fbottom('menu')",
    "right": "fleft('menu')+110",
    "bottom": "fbottom('menu')+44"})

win.optimize()
win.register(["on_mouse_enter", "on_mouse_move", "on_mouse_exit", {"on_click": "key_pressed('fichier', 'hide_Menu')"}])

Application_launched = True
Application_active = True
Playing_music = False

ballet = Lignes(40)
zballet.add(ballet)
zballet.register([{"on_click": "print('zballet.click()')"}])

etoiles = StarField(40)
zetoile.add(etoiles)
zetoile.register([{"on_click": "print('zetoile.click()')"}])

mouse_pos = (-1, -1)
mouse_cursor_circle_size = 10
mouse_button_pressed = False
track_mouse_position = False

fps_font = Graphical_Text(f" {clock.get_fps():3.1f} FPS", "Arial", 16, white, None, "gauche haut")
nblignes_font = Graphical_Text(f"{len(ballet.liste)}  lignes ", "Arial", 16, white, None, "droite haut")
zballet.add(fps_font)
zballet.add(nblignes_font)

nbstars_font = Graphical_Text(f" {len(etoiles.liste)}  étoiles", "Arial", 16, white, None, "gauche haut")
zetoile.add(nbstars_font)

music = Graphical_Text(" Press 'p' key to play music", "Arial", 18, green, None, "centre Haut")
music.add_ligne("Press 'n' key for next soundtrack")

sound_file_text = Graphical_Text(sound_filename.split("\\")[-1], "Arial", 18, green, None, "centre bas")

commentaire = Graphical_Text("Press 'c' key to follow mouse cursor", "Arial", 18, green, None, "gauche bas", (300, 0))

comment_key_1 = Graphical_Text("Press '1' key to swap Ballet", "Arial", 18, green, None, "gauche haut", (300, 0))
comment_key_2 = Graphical_Text("Press '2' key to swap Starfield", "Arial", 18, green, None, "centre haut", (400, 0))

comment_gauche = Graphical_Text(" Press '-' key", "Arial", 16, green, None, "gauche haut")
comment_gauche.add_ligne(" to decrease")
comment_gauche.add_ligne(" lines numbers")
comment_droite = Graphical_Text("Press '+' key ", "Arial", 16, green, None, "Droite haut")
comment_droite.add_ligne("to rise")
comment_droite.add_ligne("lines numbers ")

ztextes.add(music)
ztextes.add(sound_file_text)
ztextes.add(comment_gauche)
ztextes.add(comment_key_1)
ztextes.add(comment_key_2)
ztextes.add(comment_droite)
ztextes.add(commentaire)

decalage = 0
menu1 = Graphical_Text("   Fichier   ", "Arial", 16, light_grey, black, "gauche Haut", (decalage, 0))
decalage += 1+menu1.get_width()
menu2 = Graphical_Text("   Lignes    ", "Arial", 16, light_grey, black, "gauche Haut", (decalage, 0))
decalage += 1+menu2.get_width()
menu3 = Graphical_Text("   Etoiles   ", "Arial", 16, light_grey, black, "gauche Haut", (decalage, 0))
decalage += 1+menu3.get_width()
menu4 = Graphical_Text("    Aide     ", "Arial", 16, light_grey, black, "gauche Haut", (decalage, 0))
decalage += 1+menu4.get_width()
menu5 = Graphical_Text("   Quitter   ", "Arial", 16, light_grey, black, "gauche Haut", (decalage, 0))

decalage = 0
menu11 = Graphical_Text("   Augmentation    ", "Arial", 16, light_grey, black, "gauche Haut", (0, decalage))
decalage += 1+menu11.get_height()
menu12 = Graphical_Text("   Diminution        ", "Arial", 16, light_grey, black, "gauche Haut", (0, decalage))

zmenus.add(menu1)
zmenus.add(menu2)
zmenus.add(menu3)
zmenus.add(menu4)
zmenus.add(menu5)

zmenu1.add(menu11)
zmenu1.add(menu12)

zmenus.register(["on_mouse_move", "on_mouse_enter", "on_click", "on_mouse_exit"])
zmenu1.register(["on_mouse_move", "on_mouse_enter", "on_click", "on_mouse_exit"])

menu1.register(["on_mouse_enter", {"on_click": "key_pressed('fichier', 'swap')"}, "on_mouse_exit"])
menu2.register(["on_mouse_enter", {"on_click": "key_pressed(pygame.K_KP1)"}, "on_mouse_exit"])
menu3.register(["on_mouse_enter", {"on_click": "key_pressed(pygame.K_KP2)"}, "on_mouse_exit"])
menu4.register(["on_mouse_enter", {"on_click": "key_pressed(pygame.K_KP3)"}, "on_mouse_exit"])
menu5.register(["on_mouse_enter", {"on_click": "Quit()"}, "on_mouse_exit"])

menu11.register(["on_mouse_enter", {"on_click": "key_pressed(pygame.K_KP_PLUS)"}, "on_mouse_exit"])
menu12.register(["on_mouse_enter", {"on_click": "key_pressed(pygame.K_KP_MINUS)"}, "on_mouse_exit"])
zmenu1.deactivate()


while Application_launched:

    # 60 images/s
    clock.tick(60)

    if Application_active:
        win.update()
        win.draw()

        if track_mouse_position:
            if mouse_button_pressed:
                pygame.draw.circle(screen, random_color(), mouse_pos, mouse_cursor_circle_size)
            else:
                pygame.draw.circle(screen, random_color(), mouse_pos, mouse_cursor_circle_size, 2)

    # gestion des evennements
    for event in pygame.event.get():
        # - Croix "X" de la fenetre -------------------------------------------
        if event.type == pygame.QUIT:
            Application_launched = False

        elif event.type == pygame.JOYDEVICEADDED:
            pass
            
        # - touche clavier enfoncée -------------------------------------------
        elif event.type == pygame.KEYDOWN:
            pass

        elif event.type in [pygame.TEXTINPUT, pygame.TEXTEDITING]:
            pass

        # - touche clavier relachée -------------------------------------------
        elif event.type == pygame.KEYUP:
            key_code = event.dict.get("key", 0)
            key_mode = event.dict.get("mod", 0)

            if key_code in [pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP_MINUS,
                    pygame.K_KP_PLUS, pygame.K_SPACE, pygame.K_p, pygame.K_n,
                    pygame.K_ESCAPE] or key_mode == pygame.KMOD_LALT and key_code == pygame.K_F4:
                key_pressed(key_code, key_mode)

            elif key_code == pygame.K_c:
                track_mouse_position = not track_mouse_position
                commentaire.set_texte("Press 'c' key")
                if track_mouse_position:
                    commentaire.set_texte("Press 'c' key to unfollow mouse cursor")
                else:
                    commentaire.set_texte("Press 'c' key to follow mouse cursor")
                commentaire.calcul_position()

        # - touche souris enfoncée ------------------------------------------------------------------------
        elif event.type in [pygame.MOUSEBUTTONDOWN]:
            mouse_button_pressed = True

        # - touche souris relachée ------------------------------------------------------------------------
        elif event.type in [pygame.MOUSEBUTTONUP]:
            mouse_button_pressed = False
            cmds = win.on_click()
            execute_commands(cmds)

            button = event.dict.get("button", 0)
            if button == pygame.BUTTON_WHEELUP:
                mouse_cursor_circle_size -= 10
                if mouse_cursor_circle_size < 10:
                    mouse_cursor_circle_size = 10
            elif button == pygame.BUTTON_WHEELDOWN:
                mouse_cursor_circle_size += 10
                if mouse_cursor_circle_size > 400:
                    mouse_cursor_circle_size = 400

        # - utilisation molette souris -------------------------------------------------------------------------------
        elif event.type in [pygame.MOUSEWHEEL]:
            pass

        # - souris déplacée -------------------------------------------------------------------------------
        elif event.type in [pygame.MOUSEMOTION]:
            mouse_pos = event.dict.get("pos", (-1, -1))
            cmds = win.on_mouse_move(mouse_pos)
            execute_commands(cmds)

        elif event.type in [pygame.WINDOWENTER, pygame.WINDOWFOCUSGAINED]:
            if not win.mouse_entered and win.has_registered("on_mouse_enter"):
                mouse_pos = event.dict.get("pos", (-1, -1))
                cmds = win.on_mouse_enter(mouse_pos)
                execute_commands(cmds)

        elif event.type == pygame.WINDOWLEAVE:
            if win.mouse_entered and win.has_registered("on_mouse_exit"):
                cmds = win.on_mouse_exit()
                execute_commands(cmds)

        elif event.type == pygame.WINDOWSHOWN:
            pass
            # print("Affichage de la fenêtre")

        # - fenetre ?????????????? ------------------------------------------------------------------------
        elif event.type == pygame.VIDEOEXPOSE:
            pass

        # - fenetre redimensionnée ------------------------------------------------------------------------
        elif event.type in [pygame.WINDOWRESIZED, pygame.WINDOWMOVED, pygame.WINDOWSIZECHANGED]:
            pass

        elif event.type == pygame.VIDEORESIZE:
            w: int = event.dict.get('w', 0)
            h: int = event.dict.get('h', 0)
            print(f"change Screen Resolution = {w}x{h}")
            window_size = (w, h)
            win.set_zone(((0, 0), window_size))

            screen = pygame.display.set_mode(window_size, pygame.RESIZABLE, 8)

        elif event.type in [pygame.AUDIODEVICEADDED, pygame.AUDIO_S8]:
            pass

        # - souris active dans la fenetre -----------------------------------------------------------------
        elif event.type == pygame.ACTIVEEVENT:
            # Application_active = event.dict.get("gain", 0) == 1
            pass

        # - USEREVENT activé toutes les 500ms -------------------------------------------------------------
        elif event.type == pygame.USEREVENT:
            # fps_font = arial18.render(f"{clock.get_fps():.1f} FPS", 0, white)
            fps_font.set_texte(f" {clock.get_fps():3.1f} FPS")
            nbstars_font.set_texte(f" {len(etoiles.liste)} étoiles")
            nblignes_font.set_texte(f"{len(ballet.liste)} lignes ")
            nblignes_font.calcul_position()
            if pygame.mixer_music.get_busy():
                minutes, secondes = divmod(pygame.mixer_music.get_pos() // 1000, 60)
                if minutes:
                    music.set_texte(f"Press 'p' to stop music ({minutes:0>2}:{secondes:0>2}s)")
                else:
                    music.set_texte(f"Press 'p' to stop music ({secondes}s)")
                music.calcul_position()

        elif event.type == MUSIC_END_EVENT:
            sound_filename = win.sound_directory.next_file().path
            pygame.mixer_music.load(sound_filename)
            sound_file_text.set_texte(sound_filename.split("\\")[-1], 2)
            sound_file_text.calcul_position()
            pygame.mixer_music.play()

        else:
            print(get_pygame_const_name(event.type), end=" > ")
            print(event.dict, event.type)

    if Application_active:
        print(end="", flush=True)
        pygame.display.update()


pygame.quit()
