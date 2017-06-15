

#####################################################################
#   Some mathematical helper functions
#####################################################################


def cube_vertices(x, y, z, n):
    """ Return the vertices of the cube at position x, y, z with size 2*n.

    """
    return [x-n, y+n, z-n,  x-n, y+n, z+n,  x+n, y+n, z+n,  x+n, y+n, z-n,  # top
            x-n, y-n, z-n,  x+n, y-n, z-n,  x+n, y-n, z+n,  x-n, y-n, z+n,  # bottom
            x-n, y-n, z-n,  x-n, y-n, z+n,  x-n, y+n, z+n,  x-n, y+n, z-n,  # left
            x+n, y-n, z+n,  x+n, y-n, z-n,  x+n, y+n, z-n,  x+n, y+n, z+n,  # right
            x-n, y-n, z+n,  x+n, y-n, z+n,  x+n, y+n, z+n,  x-n, y+n, z+n,  # front
            x+n, y-n, z-n,  x-n, y-n, z-n,  x-n, y+n, z-n,  x+n, y+n, z-n]  # back


def _tex_coord(x, y, n=4):
    """ Return the bounding vertices of the texture square.

    """
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
    """ Return a list of the texture squares for the top, bottom and side.

    """
    top = _tex_coord(*top)
    bottom = _tex_coord(*bottom)
    side = _tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result


def normalize(position):
    """ Accepts `position` of arbitrary precision and returns the block
    containing that position.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    block_position : tuple of ints of len 3

    """
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return x, y, z


def sectorize(position, sector_size=16):
    """ Returns a tuple representing the sector for the given `position`.

    Parameters
    ----------
    position : tuple of len 3
    sector_size : int

    Returns
    -------
    sector : tuple of len 3

    """
    x, y, z = normalize(position)
    x, y, z = x // sector_size, y // sector_size, z // sector_size
    return x, 0, z