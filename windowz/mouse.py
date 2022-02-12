import pygame
from time import perf_counter


class Mouse:
    DBL_CLCIK_DELAY = 0.3
    left_button_down = False
    down_position = (0, 0)
    selected_object = None
    time = [perf_counter()]

    @classmethod
    def __init__(self):
        print("init Mouse()")
        pass

    @classmethod
    def set_cursor(self, curseur):
        pygame.mouse.set_cursor(curseur)

    @classmethod
    def set_pos(self, position):
        self.down_position = position

    @classmethod
    def get_pos(self, position):
        return self.down_position

    @classmethod
    def click(self):
        self.time.append(perf_counter())
        if len(self.time) > 2:
            self.time.pop(0)

    @classmethod
    def has_double_clicked(self):
        if len(self.time) > 1:
            res = self.time[-1]-self.time[-2] <= Mouse.DBL_CLCIK_DELAY
            return res
        else:
            return False


if __name__ == "__main__":
    print("Compilation: OK")
