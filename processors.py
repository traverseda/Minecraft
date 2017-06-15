import collections
import time

from ecs import Processor
from components import *


class BlockExposeProcessor(Processor):
    def __init__(self, batch, group):
        super().__init__()
        self.batch = batch
        self.group = group
        # self.queue = collections.deque()
        # self.all_blocks = {}
        # self.shown_blocks = {}
        # self.sectors = {}

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
