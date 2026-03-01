import pygame

from time import perf_counter
from typing import Optional


class Mouse:
    DBL_CLICK_DELAY = 0.3
    left_button_down = False
    right_button_down = False
    old_position = (0, 0)
    down_position = (0, 0)
    selected_object = None
    cursor_over: Optional[str] = None
    time = [perf_counter()]

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def set_cursor(cls, curseur):
        pygame.mouse.set_cursor(curseur)

    @classmethod
    def save_pos(cls):
        cls.old_position = cls.down_position

    @classmethod
    def set_pos(cls, position):
        cls.down_position = position

    @classmethod
    def get_pos(cls):
        return cls.down_position

    @classmethod
    def get_saved_pos(cls):
        return cls.old_position

    @classmethod
    def click(cls):
        cls.time.append(perf_counter())
        if len(cls.time) > 2:
            cls.time.pop(0)

    @classmethod
    def has_double_clicked(cls):
        if len(cls.time) > 1:
            res = cls.time[-1]-cls.time[-2] <= Mouse.DBL_CLICK_DELAY
            if res: 
                cls.time.clear()
            return res
        else:
            return False


if __name__ == "__main__":
    print("Compilation: OK")
