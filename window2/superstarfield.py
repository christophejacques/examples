import numpy as np

from classes import Application
from colors import Colors


class SuperStarfield(Application):
    MIN_SIZE = (300, 200)
    VEL_MAX = 0

    DEFAULT_CONFIG = ("Super Starfield", Colors.ORANGE)
    WINDOW_PROPERTIES = ["RESIZABLE"]

    def __init__(self, screen, args):
        # set up a random batch of stars for the background
        self.screen = screen
        self.z_range = (50, 2000)  # range for Z coordinates of stars
        self.action = ""
        self.background_color = (0, 0, 0)

    def post_init(self):
        self.resize(self.screen)

    def resize(self, screen):
        w, h = screen.get_size()
        self.nr_stars = int(w * h / 200)
        self.screen = screen
        self.screen_size = np.array(self.screen.get_size())
        self.mid_screen = self.screen_size // 2
        self.set_title(f"{self.DEFAULT_CONFIG[0]} - {self.nr_stars} étoiles")
        self.init()

    def init(self):
        self.stars = np.random.rand(self.nr_stars, 3) * np.array([self.screen_size[0] - 2, self.screen_size[1] - 2, 1.0]) \
            + np.array([-self.mid_screen[0], -self.mid_screen[1], 0.0])

        # adjust Z coordinates as more stars needed at distance for a balanced view
        self.stars[:, 2] = (self.stars[:, 2] ** 0.5) * (self.z_range[1] - self.z_range[0]) + self.z_range[0]
        self.star_move = np.array([0.0, 0.0, -0.5])
        self.prev_time = self.tools.get_ticks()

    def get_action(self):
        return self.action

    def keyreleased(self, event):
        self.touche = self.keys.get_key()
        if self.touche == self.keys.K_ESCAPE:
            self.action = "QUIT"

    def update(self):
        # clear screen for a new frame
        self.time = self.tools.get_ticks()
        # self.screen.fill(self.background_color)
        self.move_stars(self.time, self.prev_time)

    def move_stars(self, time, prev_time):

        # move stars in X,Y depending on their Z coordinate - the closer the faster / bigger move. Hence divide star_move X & Y by star Z
        self.stars += (time - prev_time) * self.star_move / np.hstack((self.stars[:, 2:3], self.stars[:, 2:3], np.ones((self.nr_stars, 1))))
        self.stars[:, 1][self.stars[:, 1] > self.mid_screen[1] - 2] -= self.screen_size[1] - 2

        # move stars using Z coordinate and Z move
        if self.star_move[2] != 0.0:
            self.stars[:, 0:2] *= self.stars[:, 2:3] / (self.stars[:, 2:3] + (time - prev_time) * self.star_move[2])

        # if outside of screen, normally replace with a new random star at a random X, Y edge and random Z
        nr_half = self.nr_stars // 2
        # first half: vertical edge
        self.stars[0:nr_half, :][(self.stars[0:nr_half, 2] > self.z_range[1])] = np.hstack((
            np.random.randint(0, 2, (np.shape(self.stars[0:nr_half, :][(self.stars[0:nr_half, 2] > self.z_range[1])])[0], 1)) * (self.screen_size[0] - 2) - self.mid_screen[0],
            np.random.rand(np.shape(self.stars[0:nr_half, :][(self.stars[0:nr_half, 2] > self.z_range[1])])[0], 1) * (self.screen_size[1] - 2) - self.mid_screen[1],
            np.random.rand(np.shape(self.stars[0:nr_half, :][(self.stars[0:nr_half, 2] > self.z_range[1])])[0], 1) * (self.z_range[1] - self.z_range[0]) + self.z_range[0]
            ))
        # second half: horizontal edge
        self.stars[nr_half:, :][(self.stars[nr_half:, 2] > self.z_range[1])] = np.hstack((
            np.random.rand(np.shape(self.stars[nr_half:, :][(self.stars[nr_half:, 2] > self.z_range[1])])[0], 1) * (self.screen_size[0] - 2) - self.mid_screen[0],
            np.random.randint(0, 2, (np.shape(self.stars[nr_half:, :][(self.stars[nr_half:, 2] > self.z_range[1])])[0], 1)) * (self.screen_size[1] - 2) - self.mid_screen[1],
            np.random.rand(np.shape(self.stars[nr_half:, :][(self.stars[nr_half:, 2] > self.z_range[1])])[0], 1) * (self.z_range[1] - self.z_range[0]) + self.z_range[0]
            ))
        # if Z too close OR X, Y out of bounds due to Z move, replace with a new random star at maximum Z
        self.stars[(self.stars[:, 2] < self.z_range[0]) | (abs(self.stars[:, 0] + 1) > self.mid_screen[0] - 1) | (abs(self.stars[:, 1] + 1) > self.mid_screen[1] - 1)] \
            = np.random.rand(np.shape(self.stars[(self.stars[:, 2] < self.z_range[0]) | (abs(self.stars[:, 0] + 1) > self.mid_screen[0] - 1) | (abs(self.stars[:, 1] + 1) > self.mid_screen[1] - 1)])[0], 3) \
            * np.array([self.screen_size[0] - 2, self.screen_size[1] - 2, 0]) + np.array([-self.mid_screen[0], -self.mid_screen[1], self.z_range[1]])

    def draw(self):
        self.screen.fill(self.background_color)
        while self.screen.get_locked():
            self.screen.unlock()
        rgb_array = self.tools.pixels3d()
        # print(self.time)

        # define color as a function of distance
        c_shades = np.array([0.6, 0.8, 1.0])  # percentage of maximum R, G, B color used to tilt to Blue
        # c_shades = np.array([0.0, 0.6, 1.0])  # percentage of maximum R, G, B color used to tilt to Green
        
        colors = (c_shades * ((1.0 - self.stars[:, 2:3] / (self.z_range[1] - self.z_range[0])) * 200 + 55)).astype(np.uint8)
        stars_int = (self.stars[:, 0:2]).astype(np.int16)
        
        rgb_array[(stars_int[:, 0] + self.mid_screen[0]), (stars_int[:, 1] + self.mid_screen[1]), 0:3] = colors
        # add additional pixels to those which are closest (color is above a threshold)
      
        rgb_array[(stars_int[:, 0][colors[:, 2] > 130] + self.mid_screen[0] + 1),
                (stars_int[:, 1][colors[:, 2] > 130] + self.mid_screen[1]), 0:3] = colors[colors[:, 2] > 130]
        rgb_array[(stars_int[:, 0][colors[:, 2] > 180] + self.mid_screen[0]),
                (stars_int[:, 1][colors[:, 2] > 180] + self.mid_screen[1] + 1), 0:3] = colors[colors[:, 2] > 180]

        rgb_array[(stars_int[:, 0][colors[:, 2] > 220] + self.mid_screen[0] + 1),
                (stars_int[:, 1][colors[:, 2] > 220] + self.mid_screen[1] + 1), 0:3] = colors[colors[:, 2] > 220]

        self.prev_time = self.time + 0


if __name__ == '__main__':
    from exec import run
    run(SuperStarfield)
