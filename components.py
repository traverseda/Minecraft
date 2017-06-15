from pyglet.gl import *


class Player:
    pass


class Visible:
    pass


class Invisible:
    pass


class Block:
    def __init__(self, position, block_type, tex_coords):
        self.position = position
        self.block_type = block_type
        self.tex_coords = tex_coords
        self.vertex_list = None


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

