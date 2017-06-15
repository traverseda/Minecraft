import ecs
import random
import time

from collections import deque
from utilities.maths import *
from processors import *


GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))

FACES = [(0, 1, 0),
         (0, -1, 0),
         (-1, 0, 0),
         (1, 0, 0),
         (0, 0, 1),
         (0, 0, -1)]


def random_block_generator(size=160):

    size = max(20, size)    # minimum size for this randomizer
    n = size // 2           # 1/2 width and height of world
    s = 1                   # step size
    y = 0                   # initial y height

    for x in range(-n, n + 1, s):
        for z in range(-n, n + 1, s):
            # create a layer stone an grass everywhere.
            yield ((x, y - 2, z), GRASS)
            yield ((x, y - 3, z), STONE)

            if x in (-n, n) or z in (-n, n):
                # create outer walls.
                for dy in range(-2, 3):
                    yield ((x, y + dy, z), STONE)

    # generate the hills randomly
    o = n - 10
    for _ in range(120):
        a = random.randint(-o, o)       # x position of the hill
        b = random.randint(-o, o)       # z position of the hill
        c = -1                          # base of the hill
        h = random.randint(1, 6)        # height of the hill
        s = random.randint(4, 8)        # 2 * s is the side length of the hill
        d = 1                           # how quickly to taper off the hills
        t = random.choice([GRASS, SAND, BRICK])
        for y in range(c, c + h):
            for x in range(a - s, a + s + 1):
                for z in range(b - s, b + s + 1):
                    if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                        continue
                    if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                        continue
                    yield ((x, y, z), t)

            s -= d                      # decrement side lenth so hills taper off:


class Scene:
    def __init__(self, batch, texture, fps=60):
        self.fps = fps
        self.batch = batch
        self.texture = texture
        self.group = pyglet.graphics.TextureGroup(self.texture)
        self.world = ecs.World()

        self.world.add_processor(BlockExposeProcessor(batch=self.batch, group=self.group), priority=99)

        for pos, texture in random_block_generator():
            self.world.create_entity(Show(), Block(position=pos, block_type=" ", tex_coords=texture))

    def hit_test(self, position, vector, max_distance=8):
        """ Line of sight search from current position. If a block is
        intersected it is returned, along with the block previously in the line
        of sight. If no block is found, return None, None.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check visibility from.
        vector : tuple of len 3
            The line of sight vector.
        max_distance : int
            How many blocks away to search for a hit.

        """
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in range(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and key in self.all_blocks:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None

    # def exposed(self, position):
    #     """ Returns False is given `position` is surrounded on all 6 sides by
    #     blocks, True otherwise.
    #
    #     """
    #     x, y, z = position
    #     for dx, dy, dz in FACES:
    #         if (x + dx, y + dy, z + dz) not in self.all_blocks:
    #             return True
    #     return False

    # def check_neighbors(self, position):
    #     """ Check all blocks surrounding `position` and ensure their visual
    #     state is current. This means hiding blocks that are not exposed and
    #     ensuring that all exposed blocks are shown. Usually used after a block
    #     is added or removed.
    #
    #     """
    #     x, y, z = position
    #     for dx, dy, dz in FACES:
    #         key = (x + dx, y + dy, z + dz)
    #         if key not in self.all_blocks:
    #             continue
    #         if self.exposed(key):
    #             if key not in self.shown_blocks:
    #                 self.show_block(key)
    #         else:
    #             if key in self.shown_blocks:
    #                 self.hide_block(key)

    def process(self, dt):
        self.world.process(dt)
