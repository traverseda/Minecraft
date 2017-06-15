import collections
import time

from ecs import Processor
from components import *


class GravityProcessor(Processor):
    def __init__(self, gravity=20):
        super().__init__()
        self.gravity = gravity

    def process(self, dt):
        for ent, (vec, grav) in self.world.get_components(Vector, Gravity):
            pass


class CameraProcessor(Processor):
    def __init__(self):
        super().__init__()

    def process(self, dt):
        pass


class BlockExposeProcessor(Processor):
    def __init__(self, batch, group):
        super().__init__()
        self.batch = batch
        self.group = group
        # self.queue = collections.deque()
        # self.all_blocks = {}
        # self.shown_blocks = {}
        # self.sectors = {}

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
        for ent, (show, block) in self.world.get_components(Show, Block):
            block.vertex_list = self.batch.add(24, GL_QUADS, self.group,
                                               ('v3f/static', block.vertices),
                                               ('t2f/static', block.tex_coords))
            self.world.remove_component(ent, Show)

        for ent, (hide, block) in self.world.get_components(Hide, Block):
            block.vertex_list.delete()
            del block.vertex_list
            self.world.remove_component(ent, Hide)
