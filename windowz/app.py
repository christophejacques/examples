import pygame
import traceback
from ecran import Ecran, Animation, Mouse, Position


def get_pygame_const_name(index):
    for c in dir(pygame):
        if c[1] in "AZERTYUIOPMLKJHGFDSQWXCVBN":
            if type(getattr(pygame, c)) == int and getattr(pygame, c) == index:
                return c


def main():
    ecran = Ecran("My Windows pygame")
    ecran.load_raccourcis()

    application_affichee = True

    while application_affichee:
        ecran.refresh()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.KEYUP:
                key_code = event.dict.get("key", 0)
                # key_mode = event.dict.get("mod", 0)

                if key_code == pygame.K_ESCAPE:
                    application_affichee = False

                elif key_code == pygame.K_k:
                    ecran.kill()

                elif key_code == pygame.K_n:
                    ecran.open_all_raccourcis()

            elif event.type == pygame.QUIT:
                application_affichee = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                Mouse.left_button_down = event.button == 1
                Mouse.selected_object = None
                Mouse.down_position = event.pos
                if Mouse.left_button_down:
                    if ecran.select_window(Position(*Mouse.down_position)):
                        Mouse.selected_object = "WINDOW"
                    elif ecran.select_raccourci(Position(*Mouse.down_position)):
                        Mouse.selected_object = "RACCOURCI"
                    else:
                        window_spoted = ecran.check_win_buttons(Position(*event.pos))

            elif event.type == pygame.MOUSEBUTTONUP:
                Mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                if event.button == 1:
                    Mouse.click()
                    if Mouse.selected_object == "WINDOW" and Mouse.has_double_clicked():
                        ecran.active_window.transparent = False
                        Mouse.left_button_down = False
                        Mouse.selected_object = None
                        if ecran.active_window.etat[-1] == "maximized":
                            ecran.active_window.etat.pop()
                            ecran.active_window.set_zone(ecran.active_window.zone_backup)
                            ecran.active_window.zone_backup = None
                        else:
                            ecran.active_window.zone_backup = ecran.active_window.zone
                            ecran.active_window.etat.append("maximized")
                            ecran.active_window.set_zone(ecran.zone)
                        continue

                    raccourci_clicked = ecran.get_raccourci_clicked()
                    if Mouse.has_double_clicked() and raccourci_clicked:
                        Mouse.left_button_down = False
                        Mouse.selected_object = None
                        ecran.create_new_window(raccourci_clicked.get_window())
                        continue

                    if ecran.active_window is not None:
                        ecran.active_window.transparent = False
                        ecran.check_win_buttons(Position(*event.pos))
                        if ecran.active_window.cursor_zone is not None:
                            if ecran.active_window.cursor_zone == ecran.active_window.zone_minimize:
                                ecran.active_window.animation = Animation(
                                    ecran.active_window.zone_title, 
                                    ecran.active_icone.zone)
                                
                                ecran.active_window.etat.append("minimized")
                                ecran.active_last_window()
                            elif ecran.active_window.cursor_zone == ecran.active_window.zone_maximize:
                                if ecran.active_window.etat[-1] == "maximized":
                                    zone_title = ecran.active_window.zone_title
                                    ecran.active_window.etat.pop()
                                    ecran.active_window.set_zone(ecran.active_window.zone_backup)
                                    ecran.active_window.animation = Animation(zone_title, ecran.active_window.zone_title)
                                    ecran.active_window.zone_backup = None
                                else:
                                    zone_title = ecran.active_window.zone_title
                                    ecran.active_window.zone_backup = ecran.active_window.zone
                                    ecran.active_window.etat.append("maximized")
                                    ecran.active_window.set_zone(ecran.zone)
                                    ecran.active_window.animation = Animation(zone_title, ecran.active_window.zone_title)

                            elif ecran.active_window.cursor_zone == ecran.active_window.zone_close:
                                ecran.kill()
                        else:
                            ecran.active_window_by_icone()

                    Mouse.left_button_down = False
                    Mouse.selected_object = None

            elif event.type == pygame.KMOD_LGUI:
                if Mouse.left_button_down and Mouse.selected_object == "WINDOW":
                    ecran.active_window.transparent = True
                    Mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
                    dx = event.pos[0]-Mouse.down_position[0]
                    dy = event.pos[1]-Mouse.down_position[1]
                    Mouse.down_position = event.pos
                    if ecran.active_window.etat[-1] == "maximized":
                        ecran.active_window.move_to(Mouse.down_position)
                    ecran.active_window.move((dx, dy))
                elif Mouse.left_button_down and Mouse.selected_object == "RACCOURCI":
                    dx = event.pos[0]-Mouse.down_position[0]
                    dy = event.pos[1]-Mouse.down_position[1]
                    Mouse.down_position = event.pos
                    ecran.active_raccourci.move((dx, dy))
                elif Mouse.left_button_down and \
                 ecran.active_window.cursor_zone in ("LEFT", "RIGHT", "BOTTOM"):
                    if window_spoted:
                        if ecran.active_window.cursor_zone == "LEFT":
                            dx = event.pos[0]-Mouse.down_position[0]
                            ecran.active_window.resize(dx, "LEFT")
                            Mouse.down_position = event.pos
                        elif ecran.active_window.cursor_zone == "RIGHT":
                            dx = event.pos[0]-Mouse.down_position[0]
                            ecran.active_window.resize(dx, "RIGHT")
                            Mouse.down_position = event.pos
                        elif ecran.active_window.cursor_zone == "BOTTOM":
                            dy = event.pos[1]-Mouse.down_position[1]
                            ecran.active_window.resize(dy, "BOTTOM")
                            Mouse.down_position = event.pos

                else:
                    window_spoted = ecran.check_win_buttons(Position(*event.pos))
                    ecran.check_mouse_over_icones(Position(*event.pos))
                    ecran.check_mouse_over_raccourcis(Position(*event.pos), window_spoted)

            elif event.type == pygame.VIDEORESIZE:
                ecran.set_zone(event.size)
            elif event.type in (pygame.WINDOWRESIZED, pygame.WINDOWSIZECHANGED, 
             pygame.WINDOWRESTORED, pygame.WINDOWMOVED, pygame.WINDOWMAXIMIZED):
                pass
            elif event.type == pygame.ACTIVEEVENT:
                pass
            elif event.type == pygame.TEXTEDITING:
                pass
            elif event.type in [pygame.AUDIODEVICEADDED, pygame.AUDIO_S8, pygame.AUDIO_S16]:
                pass
            elif event.type == pygame.JOYDEVICEADDED:
                pass
            elif event.type == pygame.WINDOWSHOWN:
                pass
            elif event.type == pygame.WINDOWENTER:
                pass
            elif event.type == pygame.WINDOWFOCUSGAINED:
                pass
            elif event.type == pygame.VIDEOEXPOSE:
                pass

            else:
                print(get_pygame_const_name(event.type), end=" > ")
                print(event.dict, event.type)

    ecran.shutdown()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc()
    pygame.quit()
