
decal = 2


class Cell:
    width = 48

    def __init__(this, x, y):
        this.x = x
        this.y = y
        this.bee = False
        this.revealed = False
        this.marked = False
        this.nb_bees = 0

    def draw_rect(this):
        return (this.x)*(decal+Cell.width), this.y*(decal+Cell.width), Cell.width, Cell.width

    def draw_square(this):
        return (this.x)*(decal+Cell.width), this.y*(decal+Cell.width), Cell.width

    def draw_circle(this):
        return Cell.width//2+(this.x)*(decal+Cell.width), Cell.width//2+this.y*(decal+Cell.width), Cell.width//2.5

    def draw_text(this):
        return 4+Cell.width//4+(this.x)*(decal+Cell.width), this.y*(decal+Cell.width), Cell.width
