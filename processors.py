from ecs import Processor
from components import *

import collections
import time


class BlockExposeProcessor(Processor):
    def __init__(self, batch):
        super().__init__()
        self.batch = batch
        self.queue = collections.deque()

    def process(self, dt):
        pass
