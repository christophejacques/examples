
class Colors:

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    LIGHT_GREY = (192, 192, 192)
    GREY = (128, 128, 128)
    DARK_GREY = (64, 64, 64)

    LIGHT_RED = (255, 0, 0)
    RED = (192, 0, 0)
    MIDDLE_RED = (128, 0, 0)
    DARK_RED = (64, 0, 0)

    LIGHT_ORANGE = (255, 127, 0)
    ORANGE = (192, 96, 0)
    MIDDLE_ORANGE = (128, 64, 0)
    DARK_ORANGE = (64, 32, 0)

    LIGHT_GREEN = (0, 255, 0)
    GREEN = (0, 192, 0)
    MIDDLE_GREEN = (0, 128, 0)
    DARK_GREEN = (0, 64, 0)

    LIGHT_BLUE = (0, 0, 255)
    BLUE = (0, 0, 192)
    MIDDLE_BLUE = (0, 0, 128)
    DARK_BLUE = (0, 0, 64)
    
    CYAN = (50, 130, 255)


def lighter(color: tuple, coef: float=1.2) -> tuple:
    return tuple(max(255, int(c*coef)) for c in color)


def darker(color: tuple, coef: float=0.8) -> tuple:
    return tuple(int(c*coef) for c in color)
