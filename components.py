from pyglet.gl import *
from utilities.maths import cube_vertices


class Player:
    pass


class Show:
    pass


class Hide:
    pass


class Block:
    def __init__(self, position, block_type, tex_coords):
        self.position = position
        self.block_type = block_type
        self.tex_coords = tex_coords
        self.vertices = cube_vertices(*position, 0.5)
        self.vertex_list = None


class Body:
    pass


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

